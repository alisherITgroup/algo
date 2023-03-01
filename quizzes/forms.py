from django import forms 
from .models import Quiz, Question


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ("author", "name", "password", "isPublic", "duration")

        widgets = {
            "author": forms.TextInput(attrs={"class": "form-control", "type": "hidden", "id": "author"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "password": forms.TextInput(attrs={"class": "form-control"}),
            "duration": forms.NumberInput(attrs={"class": "form-control"}),
            "isPublic": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
    
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ("quiz", "question", "answer1", "answer2", "answer3", "answer4", "true", "level")

        widgets = {
            "quiz": forms.TextInput(attrs={"class": "form-control", "id": "quiz", "type": "hidden"}),
            "question": forms.Textarea(attrs={"class": "tinymce d-none", "name": "content"}),
            "answer1": forms.Textarea(attrs={"class": "tinymce d-none", "name": "content"}),
            "answer2": forms.Textarea(attrs={"class": "tinymce d-none", "name": "content"}),
            "answer3": forms.Textarea(attrs={"class": "tinymce d-none", "name": "content"}),
            "answer4": forms.Textarea(attrs={"class": "tinymce d-none", "name": "content"}),
            "true": forms.Textarea(attrs={"class": "tinymce d-none", "name": "content"}),
            "level": forms.NumberInput(attrs={"class": "form-control"})
        }