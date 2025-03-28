from django import forms

class FileUploadForm(forms.Form):
    file = forms.FileField(label="Upload a file")

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

class FileFieldForm(forms.Form):
    file_field = UploadFileForm()
