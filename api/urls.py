from .views import *
from rest_framework.routers import DefaultRouter
from django.urls import path
router = DefaultRouter()
router.register("profiles", UserViewSet)
router.register("attempts", AttemptViewSet)
router.register("problems", ArchiveProblemViewSet)
urlpatterns = [
    path("login/", login, name="api_login"),
    path("signup/", sign_up, name="api_signup"),
]
urlpatterns += router.urls