from django import forms
from .models import BlogPost
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UploadFileForm(forms.Form):
    file = forms.FileField()

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content']

class FileUploadForm(forms.Form):
    file = forms.FileField()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Lütfen geçerli bir email adresi girin.')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
