from django.urls import path
from .views import (
    send,
    ArchiveProblemView, 
    ArchiveProblemsView, 
    ArchiveProblemUpdateView,
    ArchiveProblemCreateView,
)

urlpatterns = [
    path("", ArchiveProblemsView.as_view(), name="problems"),
    path("problem/<int:pk>/send/", send, name="problem_send"),
    path("problem/<int:pk>/", ArchiveProblemView.as_view(), name="problem"),
    path("create/", ArchiveProblemCreateView.as_view(), name="problem_create"),
    path("problem/<int:pk>/edit/", ArchiveProblemUpdateView.as_view(), name="problem_update"),
]