from django import forms
from .models import ArchiveProblem

class ArchiveProblemForm(forms.ModelForm):
    class Meta:
        model = ArchiveProblem
        fields = ('author', 'name', 'problem', 'timelimit', 'memorylimit', 'difficulty', 'allowedlangs', 'category', 'comment', 'infoin', 'infoout', 'simpletests', 'tests', 'solution')
        widgets = {
            "author": forms.TextInput(attrs={"class": "form-control mb-3", "id": "ali", "type": "hidden"}),
            "name": forms.TextInput(attrs={"class": "form-control", "id": "name", "placeholder": "Hello World"}),
            "problem": forms.Textarea(attrs={"class": "tinymce d-none", "name": "content", "id": "problem"}),
            "comment": forms.Textarea(attrs={"class": "tinymce d-none", "name": "content", "placeholder": "Masala shartinni yaxshilab o'qing.", "id": "comment"}),
            "timelimit": forms.TextInput(attrs={"class": "form-control mb-3", "type": "number", "placeholder": "1000", "id": "timelimit"}),
            "memorylimit": forms.TextInput(attrs={"class": "form-control mb-3", "type": "number", "placeholder": "16", "id": "memorylimit"}),
            "difficulty": forms.TextInput(attrs={"class": "form-control mb-3", "type": "number", "placeholder": "23", "id": "difficulty"}),
            "category": forms.SelectMultiple(attrs={"class": "form-control mb-3", "id": "category"}),
            "allowedlangs": forms.SelectMultiple(attrs={"class": "form-control mb-3", "id": "langs"}),
            "infoin": forms.Textarea(attrs={"class": "tinymce d-none", "name": "content", "id": "infoin"}),
            "infoout": forms.Textarea(attrs={"class": "tinymce d-none", "name": "content", "id": "infoout"}),
            "simpletests": forms.Textarea(attrs={"class": "form-control mb-3", "id": "simpletests"}),
            "tests": forms.Textarea(attrs={"class": "form-control mb-3", "id": "tests"}),
            "solution": forms.Textarea(attrs={"class": "tinymce d-none", "id": "solution"}),
        }
