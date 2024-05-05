from django import forms


class DecryptForm(forms.Form):
    decryptFile = forms.FileField(label='Select an encrypted file')
    decryptPassword = forms.CharField(label='Decryption Password', widget=forms.PasswordInput)


class FileUploadForm(forms.Form):
    file = forms.FileField()
    encryption_key = forms.CharField(max_length=255)
