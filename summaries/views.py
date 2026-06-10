from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import SummaryGenerateForm
from .models import Summary
from .services import generate_summary


@login_required
def summary_list(request):
    summaries = Summary.objects.filter(user=request.user).select_related('note')
    return render(request, 'summaries/list.html', {'summaries': summaries})


@login_required
def generate_summary_view(request):
    if request.method == 'POST':
        form = SummaryGenerateForm(request.POST, user=request.user)
        if form.is_valid():
            summary = generate_summary(
                user=request.user,
                note=form.cleaned_data['note'],
                summary_type=form.cleaned_data['summary_type'],
            )
            return redirect('summaries:detail', pk=summary.pk)
    else:
        form = SummaryGenerateForm(user=request.user)

    return render(request, 'summaries/generate.html', {'form': form})


@login_required
def summary_detail(request, pk):
    summary = get_object_or_404(Summary, pk=pk, user=request.user)
    return render(request, 'summaries/detail.html', {'summary': summary})
