# secure_files/forms.py

from django import forms


class FileUploadForm(forms.Form):
    file = forms.FileField()
    encryption_key = forms.CharField(max_length=255)
