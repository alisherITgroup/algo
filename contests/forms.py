from django import forms
from .models import Contest, ContestProblem


class ContestForm(forms.ModelForm):
    class Meta:
        model = Contest
        fields = ["author", "name", "authors", 'isPublic', 'isIndividual', 'langs', "description", "startdate", "starttime", "enddate", "endtime", "users", "password"]

        widgets = {
            "author": forms.TextInput(attrs={"class": "form-control", "type": "hidden", "id": "author"}),
            "authors": forms.SelectMultiple(attrs={"class": "form-control", "id": "authors"}),
            "users": forms.SelectMultiple(attrs={"class": "form-control", "id": "users"}),
            "category": forms.SelectMultiple(attrs={"class": "form-control", "id": "category"}),
            "langs": forms.SelectMultiple(attrs={"class": "form-control", "id": "langs"}),
            "isPublic": forms.CheckboxInput(attrs={"class": "form-check-input", "id": "isPublic"}),
            "isIndividual": forms.CheckboxInput(attrs={"class": "form-check-input", "id": "isIndividual"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "password": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "tinymce d-none", "name": "content"}),
            "startdate": forms.TextInput(attrs={"class": "form-control datetimepicker flatpickr-input", "type": "date", "data-options": "{\"disableMobile\":true,\"allowInput\":true}"}),
            "starttime": forms.TextInput(attrs={"class": "form-control datetimepicker flatpickr-input", "type": "time", "data-options": "{\"enableTime\":true,\"noCalendar\":true,\"dateFormat\":\"H:i\",\"disableMobile\":true}"}),
            "enddate": forms.TextInput(attrs={"class": "form-control datetimepicker flatpickr-input", "type": "date", "data-options": "{\"disableMobile\":true,\"allowInput\":true}"}),
            "endtime": forms.TextInput(attrs={"class": "form-control datetimepicker flatpickr-input", "type": "time", "data-options": "{\"enableTime\":true,\"noCalendar\":true,\"dateFormat\":\"H:i\",\"disableMobile\":true}"}),
        }

class ContestProblemForm(forms.ModelForm):
    class Meta:
        model = ContestProblem
        fields = ('author', 'contest', 'name', 'problem', 'timelimit', 'memorylimit', 'difficulty', 'comment', 'infoin', 'infoout', 'simpletests', 'tests', 'solution', "category")
        widgets = {
            "author": forms.TextInput(attrs={"class": "form-control mb-3", "id": "author", "type": "hidden"}),
            "contest": forms.TextInput(attrs={"class": "form-control mb-3", "id": "contest", "type": "hidden"}),
            "category": forms.SelectMultiple(attrs={"class": "form-control mb-3", "id": "category"}),
            "name": forms.TextInput(attrs={"class": "form-control", "id": "name", "placeholder": "Hello World"}),
            "problem": forms.Textarea(attrs={"class": "tinymce d-none", "name": "content", "id": "problem"}),
            "comment": forms.Textarea(attrs={"class": "tinymce d-none", "name": "content", "placeholder": "Masala shartinni yaxshilab o'qing.", "id": "comment"}),
            "timelimit": forms.TextInput(attrs={"class": "form-control mb-3", "type": "number", "placeholder": "1000", "id": "timelimit"}),
            "memorylimit": forms.TextInput(attrs={"class": "form-control mb-3", "type": "number", "placeholder": "16", "id": "memorylimit"}),
            "difficulty": forms.TextInput(attrs={"class": "form-control mb-3", "type": "number", "placeholder": "23", "id": "difficulty"}),
            "infoin": forms.Textarea(attrs={"class": "tinymce d-none", "name": "content", "id": "infoin"}),
            "infoout": forms.Textarea(attrs={"class": "tinymce d-none", "name": "content", "id": "infoout"}),
            "simpletests": forms.Textarea(attrs={"class": "form-control mb-3", "id": "simpletests"}),
            "tests": forms.Textarea(attrs={"class": "form-control mb-3", "id": "tests"}),
            "solution": forms.Textarea(attrs={"class": "tinymce d-none", "id": "solution"}),
            # "isArchive": forms.CheckboxInput(attrs={"class": "form-check-input", "name": "content", "id": "isArchive"}),
        }