from django.db import models
from django.contrib.auth.models import User


class Chat(models.Model):
    abonent1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_abonent1")
    abonent2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_abonent2")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.abonent1)

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.chat)
