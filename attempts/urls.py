from django.urls import path
from .views import (
    AttemptsView, 
    AttemptView,
    AttemptsView2,
    AttemptView2,
)

urlpatterns = [
    path("", AttemptsView.as_view(), name="attempts"),
    path("attempt/<int:pk>/", AttemptView.as_view(), name="attempt"),
    path("problemset/", AttemptsView2.as_view(), name="attempts2"),
    path("problemset/attempt/<int:pk>/", AttemptView2.as_view(), name="attempt2"),
]