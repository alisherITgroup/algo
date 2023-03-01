from django.contrib import admin
from .models import Quiz, Question, QuizRating


@admin.register(Quiz)
class QuizModelAdmin(admin.ModelAdmin):
    list_display = ["name", "author", "isPublic", "count_solvers"]
    list_filter = ["author", "isPublic"]
    search_fields = ["name"]

@admin.register(Question)
class QuestionModelAdmin(admin.ModelAdmin):
    list_display = ["quiz", "true", "level"]

@admin.register(QuizRating)
class QuizModelAdmin(admin.ModelAdmin):
    list_display = ["author", "quiz", "rating"]