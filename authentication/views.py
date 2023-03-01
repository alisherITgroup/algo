from .forms import UserForm, UserUpdateForm, PasswordEditForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import login, authenticate
from django.contrib.messages import constants
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import generic

def SignupView(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = UserForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            messages.add_message(request, constants.SUCCESS, "Ro'yxatdan o'tish mufaqqiyatli amalga oshirildi! End kirishingi mumkin!")
            return redirect("login")
        else:
            try:
                a = dict(eval(form.errors.as_json()))["username"]
                messages.add_message(request, constants.ERROR, "Bu foydalanuvchi nomi oldin olingan!")
            except:
                pass
            try:
                a = dict(eval(form.errors.as_json()))["password2"]
                messages.add_message(request, constants.ERROR, "Kalit so'zlar bir xil emas, yoki xafsiz emas!(Belgilardan fodalaning!)")
            except:
                pass
    return render(request, "auth/signup.html", {"form": form})

def LoginView(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.add_message(request, constants.SUCCESS, "Tizimga kirish muvaqqiyatli amalga oshirildi!")
            messages.add_message(request, constants.SUCCESS, "AlgorithmsHub ga xush kelibsiz!")
            return redirect("home")
        else:
            messages.add_message(request, constants.ERROR, "Foydalanuvchi nomi yoki kalit so'z xato!(Iltimos qayta urinib ko'ring) :(")
    return render(request, "auth/login.html")

class ProfileEditView(LoginRequiredMixin, generic.UpdateView):
    form_class = UserUpdateForm
    model = User
    template_name = "auth/edit.html"
    success_url = reverse_lazy("home")
    login_url = reverse_lazy("login")
    context_object_name = "profile"
    
    def form_invalid(self, form, *args, **kwargs):
        context = super(ProfileEditView, self).form_invalid(form)
        context["error"] = form.errors.as_json()
        try:
            user_error = dict(eval(context["error"]))["username"]
            user_error = "Bu foydalanuvchi nomi olingan"
        except:
            user_error = ""
        context["user_error"] = user_error
        messages.error(self.request, context["user_error"])
        return context
    def form_valid(self, form):
        messages.add_message(self.request, constants.SUCCESS, "Profile mufaqqiyatli tahrirlandi!")
        return super().form_valid(form)


class PasswordEditView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordEditForm
    template_name = "auth/password.html"
    success_url = reverse_lazy("home")
    login_url = reverse_lazy("login")

    def form_invalid(self, form, *args, **kwargs):
        context = super(PasswordChangeView, self).form_invalid(form)
        context["error"] = eval(form.errors.as_json())
        try:
            error = dict(eval(context["error"]))["old_password"]
            messages.add_message(self.request, constants.ERROR, "Eski kalit so'zni to'gri kiriting!")
        except:
            pass
        try:
            error = dict(eval(context["error"]))["new_password1"]
            messages.add_message(self.request, constants.ERROR, "Kalit so'z xafsiz emas!")
        except:
            pass
        try:
            error = dict(eval(context["error"]))["new_password2"]
            messages.add_message(self.request, constants.ERROR, "Yangi kalit so'z xafsiz emas yoki bir xil emas!")
        except:
            pass
        return context
    def form_valid(self, form):
        messages.add_message(self.request, constants.SUCCESS, "Kalit so'zni almashtirish muvaqqiyatli amalga oshirildi!")
        return super().form_valid(form)