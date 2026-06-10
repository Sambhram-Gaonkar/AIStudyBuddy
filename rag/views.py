from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from rag_engine.answer_generator import answer_question

from .forms import ChatForm


@login_required
def chat(request):
    result = None
    if request.method == 'POST':
        form = ChatForm(request.POST, user=request.user)
        if form.is_valid():
            note = form.cleaned_data['note']
            question = form.cleaned_data['question']
            result = answer_question(request.user, note, question)
    else:
        form = ChatForm(user=request.user)

    return render(request, 'rag/chat.html', {'form': form, 'result': result})
