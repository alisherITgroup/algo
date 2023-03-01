from django.contrib import admin
from .models import ArchiveProblem, ArchiveProblemComment

@admin.register(ArchiveProblem)
class ProblemModelAdmin(admin.ModelAdmin):
    list_display = ["name", "author", "difficulty", "timelimit", "memorylimit", "count_solvers"]
    list_filter = ["author", "difficulty", "timelimit", "memorylimit"]
    search_fields = ["name"]
    sortable_by = ["name", "difficulty"]


@admin.register(ArchiveProblemComment)
class ArchiveProblemCommentModelAdmin(admin.ModelAdmin):
    list_display = ["author", "problem", "date"]
    list_filter = ["author", "problem"]
    search_fields = ["body"]
    sortable_by = ["author", "problem"]