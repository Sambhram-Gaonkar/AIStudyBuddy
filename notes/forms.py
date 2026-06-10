from django import forms

from .models import Note

ALLOWED_CONTENT_TYPES = {
    'application/pdf',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'image/png',
    'image/jpeg',
    'image/tiff',
    'image/bmp',
}

ALLOWED_EXTENSIONS = ('.pdf', '.docx', '.pptx', '.png', '.jpg', '.jpeg', '.tif', '.tiff', '.bmp')


class NoteUploadForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'file']

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        filename = uploaded_file.name.lower()
        if not filename.endswith(ALLOWED_EXTENSIONS):
            raise forms.ValidationError('Only PDF, DOCX, PPTX, and image files are supported.')
        if uploaded_file.content_type and uploaded_file.content_type not in ALLOWED_CONTENT_TYPES:
            raise forms.ValidationError('The uploaded file must be a PDF, DOCX, PPTX, PNG, JPG, TIFF, or BMP file.')
        return uploaded_file
