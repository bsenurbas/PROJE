from django import forms
from .models import BlogPost

class UploadFileForm(forms.Form):
    file = forms.FileField()

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content']

class FileUploadForm(forms.Form):
    file = forms.FileField()