from django.contrib import admin
from .models import Attempt, Attempt2, ContestAttempt

@admin.register(Attempt)
class AttemptModelAdmin(admin.ModelAdmin):
    list_display = ["author", "problem", "status", "date"]
    list_filter = ["author", "problem", "status"]

@admin.register(Attempt2)
class Attempt2ModelAdmin(admin.ModelAdmin):
    list_display = ["author", "problem", "status", "date"]
    list_filter = ["author", "problem", "status"]

@admin.register(ContestAttempt)
class ContestAttemptModelAdmin(admin.ModelAdmin):
    list_display = ["contest", "problem", "author", "status"]
    list_filter = ["contest", "problem", "author", "status"]