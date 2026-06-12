from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from rag_engine.document_reader import extract_document_pages
from rag_engine.image_reader import OCRUnavailable
from rag_engine.text_splitter import split_pages_into_chunks
from rag_engine.vector_store import index_note_chunks

from .forms import NoteUploadForm, SubjectForm
from .models import Note, NoteChunk, Subject


@login_required
def note_list(request):
    notes = Note.objects.filter(user=request.user).select_related('subject')
    subjects = Subject.objects.filter(user=request.user)
    selected_subject = request.GET.get('subject', '')
    if selected_subject.isdigit():
        notes = notes.filter(subject_id=selected_subject, subject__user=request.user)
    elif selected_subject == 'none':
        notes = notes.filter(subject__isnull=True)
    return render(
        request,
        'notes/list.html',
        {
            'notes': notes,
            'subjects': subjects,
            'selected_subject': selected_subject,
        },
    )


@login_required
def upload_note(request):
    if request.method == 'POST':
        form = NoteUploadForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()

            try:
                pages = extract_document_pages(note.file.path)
            except Exception as exc:
                note.file.delete(save=False)
                note.delete()
                if isinstance(exc, (OCRUnavailable, ValueError)):
                    message = str(exc)
                else:
                    message = 'This file could not be read. Check that it is a valid, unencrypted document.'
                form.add_error('file', message)
                return render(request, 'notes/upload.html', {'form': form})

            if not pages or not any(page.get('text', '').strip() for page in pages):
                note.file.delete(save=False)
                note.delete()
                form.add_error('file', 'No readable text was found in this file.')
                return render(request, 'notes/upload.html', {'form': form})

            note.extracted_text = '\n\n'.join(page['text'] for page in pages)
            note.save(update_fields=['extracted_text'])

            chunks = split_pages_into_chunks(pages)
            if not chunks:
                note.file.delete(save=False)
                note.delete()
                form.add_error('file', 'No searchable text chunks could be created from this file.')
                return render(request, 'notes/upload.html', {'form': form})
            NoteChunk.objects.bulk_create([
                NoteChunk(
                    note=note,
                    user=request.user,
                    text=chunk['text'],
                    page_number=chunk['page_number'],
                    chunk_index=chunk['chunk_index'],
                )
                for chunk in chunks
            ])
            try:
                index_note_chunks(note)
            except Exception:
                # Database chunks remain available for keyword retrieval when Ollama is offline.
                pass
            return redirect('notes:detail', pk=note.pk)
    else:
        form = NoteUploadForm(user=request.user)

    return render(request, 'notes/upload.html', {'form': form})


@login_required
def create_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST, user=request.user)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.user = request.user
            subject.save()
            return redirect('notes:list')
    else:
        form = SubjectForm(user=request.user)
    return render(request, 'notes/subject_form.html', {'form': form})


@login_required
def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    chunks = note.chunks.all()
    return render(request, 'notes/detail.html', {'note': note, 'chunks': chunks})

# Create your views here.
