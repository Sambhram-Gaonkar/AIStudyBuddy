from django import forms

from .models import Note, Subject

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
        fields = ['title', 'subject', 'file']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].required = False
        self.fields['subject'].empty_label = 'No subject'
        if user is not None:
            self.fields['subject'].queryset = Subject.objects.filter(user=user)
        else:
            self.fields['subject'].queryset = Subject.objects.none()

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        filename = uploaded_file.name.lower()
        if not filename.endswith(ALLOWED_EXTENSIONS):
            raise forms.ValidationError('Only PDF, DOCX, PPTX, and image files are supported.')
        if uploaded_file.content_type and uploaded_file.content_type not in ALLOWED_CONTENT_TYPES:
            raise forms.ValidationError('The uploaded file must be a PDF, DOCX, PPTX, PNG, JPG, TIFF, or BMP file.')
        return uploaded_file


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_name(self):
        name = ' '.join(self.cleaned_data['name'].split())
        if self.user and Subject.objects.filter(user=self.user, name__iexact=name).exists():
            raise forms.ValidationError('You already have a subject with this name.')
        return name
