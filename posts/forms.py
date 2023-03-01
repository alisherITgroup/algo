from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("author", "name", "cover", "body", "description", "tags")
        widgets = {
            "author": forms.TextInput(attrs={"class": "form-control", "type": "hidden", "id": "author"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "cover": forms.FileInput(attrs={"class": "form-control"}),
            "body": forms.Textarea(attrs={"id": "area", "name": "content"}),
            "tags": forms.SelectMultiple(attrs={"id": "tags"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
        }