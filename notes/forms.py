from django import forms

from .models import Note


class NoteUploadForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'file']

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        if not uploaded_file.name.lower().endswith('.pdf'):
            raise forms.ValidationError('Only PDF files are supported for the MVP.')
        if uploaded_file.content_type and uploaded_file.content_type != 'application/pdf':
            raise forms.ValidationError('The uploaded file must be a PDF.')
        return uploaded_file
