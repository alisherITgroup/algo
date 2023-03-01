from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectModelAdmin(admin.ModelAdmin):
    list_display = ["author", "language"]
