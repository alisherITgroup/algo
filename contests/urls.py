from django.urls import path
from .views import (
    CreateContestView,
    ContestView,
    ContestProblemView,
    AddProblemToContest,
    ContestProblemCreateView,
    ContestsView,
    EditContestView,
    send_p,
    contest_attempt,
    results,
    follow,
    EditContestProblemView,
    follow_hide_contest
)

urlpatterns = [
    path("", ContestsView.as_view(), name="contests"),
    path("create/", CreateContestView.as_view(), name="create_contest"),
    path("contest/<int:pk>/edit/", EditContestView.as_view(), name="edit_contest"),
    path("contest/problem/edit/<int:pk>/", EditContestProblemView.as_view(), name="edit_contest_problem"),
    path("contest/<int:pk>/", ContestView.as_view(), name="contest"),
    path("contest/<int:pk>/follow/", follow_hide_contest, name="follow_hide_contest"),
    path("contest/<int:pk>/join/", follow, name="join"),
    path("contest/<int:pk>/results/", results, name="results"),
    path("contest/<int:pk>/problem/<str:problem>/", ContestProblemView, name="contest_problem"),
    path("contest/<int:pk>/problem/<str:problem>/<str:letter>/send/", send_p, name="contest_problem_send"),
    path("contest/<int:pk>/problem/<str:letter>/attempt/<str:integer>/", contest_attempt, name="contest_problem_attempt"),
    path("contest/<int:pk>/add/problem/", AddProblemToContest, name="add_problem_to_contest"),
    path("contest/<int:pk>/create/problem/", ContestProblemCreateView.as_view(), name="create_contest_problem")
]