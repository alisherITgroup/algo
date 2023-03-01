from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm

choice = (
    ("erkak", "Male"),
    ("ayol", "Female")
)

country = (
    ("Uzbekiston", "O'zbekistan"),
)

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "name": "username",}),
            "email": forms.EmailInput(attrs={"class": "form-control", "name": "email", "pattern": "^([a-zA-Z0-9_.-])+@(([a-zA-Z0-9-])+.)+([a-zA-Z0-9]{2,4})+$", "required": "required", "id": "bootstrap-wizard-wizard-email", "data-wizard-validate-email": "true"}),
            "password1": forms.TextInput(attrs={"class": "form-control"}),
            "password2": forms.PasswordInput(attrs={"class": "form-control"}),
        }
    def __init__(self, *args, **kwargs) -> None:
        super(UserForm, self).__init__(*args, **kwargs)
        for field in ["username", "email", "password1", "password2"]:
            self.fields[field].help_text = None

        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["username"].widget.attrs["id"] = "username"
        self.fields["email"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs["type"] = "password"
        self.fields["password2"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["type"] = "password"
    
class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "gender", "last_name", "country", "city", "town", "bio", "image", "edu", "telegramlink", "instagramlink", "image", "isTeacher", "isExpert")

        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "name": "username",}),
            "email": forms.EmailInput(attrs={"class": "form-control", "name": "email"}),
            "password1": forms.TextInput(attrs={"class": "form-control"}),
            "password2": forms.PasswordInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "gender": forms.Select(attrs={"class": "form-control"}, choices=choice),
            "country": forms.Select(attrs={"class": "form-control"}, choices=country),
            "city": forms.Select(attrs={"class": "form-control", "id": "city"}),
            "town": forms.Select(attrs={"class": "form-control", "id": "town"}),
            "bio": forms.Textarea(attrs={"id": "area", "name": "content"}),
            "edu": forms.TextInput(attrs={"class": "form-control", "id": "edu"}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "telegramlink": forms.TextInput(attrs={"class": "form-control"}),
            "instagramlink": forms.TextInput(attrs={"class": "form-control"}),
            "isTeacher": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "isExpert": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
    def __init__(self, *args, **kwargs) -> None:
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        for field in ["username", "email", "password"]:
            self.fields[field].help_text = None

        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["username"].widget.attrs["id"] = "username"
        self.fields["email"].widget.attrs["class"] = "form-control"
        self.fields["password"].widget.attrs["class"] = "form-control"
        self.fields["password"].widget.attrs["type"] = "password"

class PasswordEditForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs) -> None:
        super().__init__(user, *args, **kwargs)
        self.fields["old_password"].widget.attrs["class"] = "form-control"
        self.fields["new_password1"].widget.attrs["class"] = "form-control"
        self.fields["new_password2"].widget.attrs["class"] = "form-control"
