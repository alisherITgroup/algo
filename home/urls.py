from .views import HomeView, ProfileView, UsersView
from django.contrib.auth.views import LogoutView
from authentication.views import *
from django.urls import path
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("users/user/<str:username>/", ProfileView, name="profile"),
    path("users/", UsersView.as_view(), name="users"),

    path("auth/signup/", SignupView, name="signup"),
    path("auth/login/", LoginView, name="login"),
    path("auth/logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("profile/<int:pk>/change/me/", ProfileEditView.as_view(), name="profile_edit"),
    path("profile/<int:pk>/change/password/", PasswordEditView.as_view(), name="password_edit"),
]