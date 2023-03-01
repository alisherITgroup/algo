from django.contrib import admin
from .models import (
    Contest, 
    ContestProblem, 
    ContestComment, 
    ContestRating
)


@admin.register(Contest)
class ContestsModelAdmin(admin.ModelAdmin):
    list_display = ["name", "startdate", "starttime", "enddate", "endtime"]
    list_filter = ["author"]
    search_fields = ["name"]

@admin.register(ContestProblem)
class ContestProblemModelAdmin(admin.ModelAdmin):
    list_display = ["name", "author", "difficulty", "timelimit", "memorylimit"]
    list_filter = ["author", "difficulty", "timelimit", "memorylimit"]
    search_fields = ["name"]

@admin.register(ContestComment)
class ContestCommentModelAdmin(admin.ModelAdmin):
    list_display = ["author", "contest", "date"]
    list_filter = ["contest"]

@admin.register(ContestRating)
class ContestRatingModalAdmin(admin.ModelAdmin):
    list_display = ["author", "contest", "rating", "status"]
    list_filter = ["contest"]