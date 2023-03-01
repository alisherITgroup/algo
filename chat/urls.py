from django.urls import path
from .views import follow, chat

urlpatterns = [
    path("start/<int:pk>/with/<str:integer>/", follow, name="start"),
    path("chat/<int:pk>/with/<str:integer>/", chat, name="chat"),
]