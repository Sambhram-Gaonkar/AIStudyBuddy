from django import forms

from notes.models import Note
from .models import Summary


class SummaryGenerateForm(forms.Form):
    note = forms.ModelChoiceField(queryset=Note.objects.none())
    summary_type = forms.ChoiceField(choices=Summary.SUMMARY_TYPES)

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['note'].queryset = Note.objects.filter(user=user)
