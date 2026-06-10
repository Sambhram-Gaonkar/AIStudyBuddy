from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from rag_engine.document_reader import extract_document_pages
from rag_engine.text_splitter import split_pages_into_chunks
from rag_engine.vector_store import index_note_chunks

from .forms import NoteUploadForm
from .models import Note, NoteChunk


@login_required
def note_list(request):
    notes = Note.objects.filter(user=request.user)
    return render(request, 'notes/list.html', {'notes': notes})


@login_required
def upload_note(request):
    if request.method == 'POST':
        form = NoteUploadForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()

            pages = extract_document_pages(note.file.path)
            note.extracted_text = '\n\n'.join(page['text'] for page in pages)
            note.save(update_fields=['extracted_text'])

            chunks = split_pages_into_chunks(pages)
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
                pass
            return redirect('notes:detail', pk=note.pk)
    else:
        form = NoteUploadForm()

    return render(request, 'notes/upload.html', {'form': form})


@login_required
def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    chunks = note.chunks.all()
    return render(request, 'notes/detail.html', {'note': note, 'chunks': chunks})

# Create your views here.
