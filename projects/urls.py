from django.urls import path
from .views import (
    create,
    projects,
    project,
    run
)

urlpatterns = [
    path("create/", create, name="create_project"),
    path("<str:username>/", projects, name="projects"),
    path("project/<str:subname>/", project, name="project"),
    path("project/<str:subname>/run/", run, name="run"),
]