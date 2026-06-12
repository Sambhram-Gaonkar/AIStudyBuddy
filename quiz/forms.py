from django import forms

from notes.models import Note
from .models import Quiz


class QuizGenerateForm(forms.Form):
    note = forms.ModelChoiceField(queryset=Note.objects.none())
    question_type = forms.ChoiceField(choices=Quiz.QUESTION_TYPES)
    difficulty = forms.ChoiceField(choices=Quiz.DIFFICULTIES)
    number_of_questions = forms.IntegerField(min_value=1, max_value=10, initial=5)

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['note'].queryset = Note.objects.filter(user=user).exclude(extracted_text='')
