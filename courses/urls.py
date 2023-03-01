from django.urls import path
from .views import (
    CourseCreateView,
    CourseEditView,
    CourseDetailView,
    CoursesListView,
    LessonDetailView
)

urlpatterns = [
    path("", CoursesListView.as_view(), name="courses"),
    path("create/", CourseCreateView.as_view(), name="create_course"),
    path("course/<int:pk>/", CourseDetailView.as_view(), name="course"),
    path("course/<int:pk>/edit/", CourseEditView.as_view(), name="edit_course"),
    path("course/<int:pk>/lessons/lesson/<str:integer>/", LessonDetailView, name="lesson"),
]