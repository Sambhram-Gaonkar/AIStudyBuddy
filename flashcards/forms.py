from django import forms

from notes.models import Note


class FlashcardGenerateForm(forms.Form):
    note = forms.ModelChoiceField(queryset=Note.objects.none())
    number_of_cards = forms.IntegerField(min_value=1, max_value=20, initial=10)

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['note'].queryset = Note.objects.filter(user=user)
