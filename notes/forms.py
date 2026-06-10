from django import forms

from .models import Note

ALLOWED_CONTENT_TYPES = {
    'application/pdf',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
}


class NoteUploadForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'file']

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        filename = uploaded_file.name.lower()
        if not (filename.endswith('.pdf') or filename.endswith('.docx')):
            raise forms.ValidationError('Only PDF and DOCX files are supported.')
        if uploaded_file.content_type and uploaded_file.content_type not in ALLOWED_CONTENT_TYPES:
            raise forms.ValidationError('The uploaded file must be a PDF or DOCX document.')
        return uploaded_file
