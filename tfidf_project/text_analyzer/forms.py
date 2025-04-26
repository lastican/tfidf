from django import forms
from .models import TextDocument

class TextDocumentForm(forms.ModelForm):
    class Meta:
        model = TextDocument
        fields = ['file']
        
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if file.content_type != 'text/plain':
                raise forms.ValidationError('Only text files (.txt) are allowed.')
            if file.size > 5 * 1024 * 1024:  # 5MB
                raise forms.ValidationError('File size cannot exceed 5MB.')
        return file