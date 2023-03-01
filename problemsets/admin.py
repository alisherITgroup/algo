from django.contrib import admin
from .models import Problem, Category, ProgrammingLanguage

@admin.register(Problem)
class ProblemsetModelAdmin(admin.ModelAdmin):
    list_display = ["name", "author", "timelimit", "memorylimit", "isArchive", "count_solvers"]
    list_filter = ["timelimit", "memorylimit", "difficulty", "category"]
    search_fields = ["name"]

@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ["name"]

@admin.register(ProgrammingLanguage)
class ProgrammingLanguageModelAdmin(admin.ModelAdmin):
    list_display = ["name", "version"]
