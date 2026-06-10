from django import forms

from notes.models import Note


class ChatForm(forms.Form):
    note = forms.ModelChoiceField(queryset=Note.objects.none())
    question = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['note'].queryset = Note.objects.filter(user=user)
