from django.contrib import admin
from .models import TimeLine


@admin.register(TimeLine)
class TimeLine(admin.ModelAdmin):
    list_display  = ["title", "author", "date"]
