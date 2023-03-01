from django.urls import path
from .views import (
    PostCreateView, 
    PostUpdateView,
    PostDetailView,
    PostsView,
    comment, 
    like
)

urlpatterns =[
    path("", PostsView.as_view(), name="posts"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post"),
    path("create/", PostCreateView.as_view(), name="create_post"),
    path("post/<int:pk>/edit/", PostUpdateView.as_view(), name="edit_post"),
    path("post/<int:pk>/comment/", comment, name="post_comment"),
    path("post/<int:pk>/like/", like, name="like"),
]