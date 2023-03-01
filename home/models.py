from django.db import models
from django.contrib.auth.models import User

STATUS = (
    ("success", "success"),
    ("danger", "danger"),
    ("warning", "warning"),
    ("info", "info")
)

ICONS = (
    ("check", "check"),
    ("times", "times"),
    ("info", "info"),
    ("thumbtack", "thumbtack")
)

class TimeLine(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS, default="success")
    icon = models.CharField(max_length=20, choices=ICONS, default="check")


    def __str__(self):
        return self.title
