from django.contrib import admin
from .models import Course, Lesson, LessonComment

@admin.register(Course)
class CourseModelAdmi(admin.ModelAdmin):
    list_display = ["name", "author", "price", "count_likes", "count_users", "isPublic"]
    list_filter = ["price"]
    search_fields = ["name"]

@admin.register(Lesson)
class LessonModelAdmin(admin.ModelAdmin):
    list_display = ["name", "course", "author", "count_likes"]
    list_filter = ["course"]

@admin.register(LessonComment)
class LessonCommentModelAdmin(admin.ModelAdmin):
    list_display = ["author", "lesson", "date"]
