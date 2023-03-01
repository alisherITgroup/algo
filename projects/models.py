from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from random import randint



class Project(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    subname = models.CharField(max_length=10)
    password = models.CharField(max_length=20)
    language = models.CharField(max_length=20)
    code = models.TextField(null=True, blank=True)
    cdate = models.DateTimeField(auto_now_add=True)
    udate = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("project", args=[str(self.subname)])

