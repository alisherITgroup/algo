from django import forms
from .models import Course, Lesson

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ("author", "name", "price", "description", "cover", "isPublic")
        widgets = {
            "author": forms.Select(attrs={"class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "cover": forms.FileInput(attrs={"class": "form-control"}),
            "isPublic": forms.CheckboxInput(attrs={"class": "form-check-input"})
        }