from django.urls import path
from .views import (
    quiz, 
    Quizzes, 
    check, 
    quiz_ratings, 
    QuizCreateView, 
    question_create, 
    EditQuestionView,
    publish,
    QuizEditView,
    follow_quiz
)


urlpatterns = [
    path("", Quizzes.as_view(), name="quizzes"),
    path("quiz/<int:pk>/", quiz, name="quiz"),
    path("quiz/<int:pk>/follow/", follow_quiz, name="follow_quiz"),
    path("quiz/<int:pk>/edit/", QuizEditView.as_view(), name="quiz_edit"),
    path("quiz/<int:pk>/publish", publish, name="publish"),
    path("quiz/<int:pk>/result/<str:username>/", check, name="check"),
    path("quiz/<int:pk>/results/", quiz_ratings, name="quiz_ratings"),
    path("create/", QuizCreateView.as_view(), name="create_quiz"),
    path("quiz/<int:pk>/create/", question_create, name="create_question"),
    path("quiz/question/<int:pk>/edit/", EditQuestionView.as_view(), name="edit_question"),
]