from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from rag_engine.answer_generator import answer_question

from .forms import ChatForm
from .models import ChatHistory


@login_required
def chat(request):
    result = None
    if request.method == 'POST':
        form = ChatForm(request.POST, user=request.user)
        if form.is_valid():
            note = form.cleaned_data['note']
            question = form.cleaned_data['question']
            result = answer_question(request.user, note, question)
            ChatHistory.objects.create(
                user=request.user,
                note=note,
                question=question,
                answer=result['answer'],
                source_chunks=result['sources'],
                retrieval_mode=result['retrieval_mode'],
                used_llm=result['used_llm'],
            )
    else:
        form = ChatForm(user=request.user)

    recent_history = ChatHistory.objects.filter(user=request.user).select_related('note')[:10]
    return render(request, 'rag/chat.html', {
        'form': form,
        'result': result,
        'recent_history': recent_history,
    })
