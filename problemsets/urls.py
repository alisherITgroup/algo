from django.urls import path
from .views import (
    ProblemCreateView, 
    ProblemUpdateView,
    ProblemView,
    ProblemSetView,
    archive,
    send2
)

urlpatterns = [
    path('create/', ProblemCreateView.as_view(), name="problemset_create"),
    path('problem/<int:pk>/edit/', ProblemUpdateView.as_view(), name="problemset_update"),
    path('<str:author>/', ProblemSetView, name="problemsets"),
    path('problem/<str:string>/', ProblemView, name="problemset"),
    path('problem/<int:pk>/<str:username>/', archive, name="archive"),
    path('problem/send/<int:pk>/', send2, name="problemset_send"),
]