from django.contrib import admin
from .models import Chat, Message

@admin.register(Chat)
class ChatModelAdmin(admin.ModelAdmin):
    list_display = ["abonent1", "abonent2", "date"]

@admin.register(Message)
class MessageModelAdmin(admin.ModelAdmin):
    list_display = ["chat", "from_user", "date"]