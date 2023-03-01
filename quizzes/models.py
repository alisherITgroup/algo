from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Quiz(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=20, null=True, blank=True)
    # settings
    isPublic = models.BooleanField(default=True)
    users = models.ManyToManyField(User, related_name="quiz_users")
    solvers = models.ManyToManyField(User, related_name="quiz_solvers")
    isPublished = models.BooleanField(default=False)
    duration = models.FloatField(default=2)
    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse("quiz", args=[str(self.pk)])

    def count_solvers(self):
        return self.solvers.count()

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.TextField()
    answer1 = models.TextField()
    answer2 = models.TextField()
    answer3 = models.TextField()
    answer4 = models.TextField()
    true = models.TextField()
    level = models.FloatField(default=3.1)

    def get_absolute_url(self):
        return reverse("quizzes")

class QuizRating(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    rating = models.FloatField(default=0)
    status = models.TextField(default="")