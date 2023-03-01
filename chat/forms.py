from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ("author", "to", "message")
        widgets = {
            "author": forms.Select(attrs={"class": "form-control"}),
            "to": forms.Select(attrs={"class": "form-control"}),
            "message": forms.Textarea(attrs={}),
        }