from django.db import models
from django.contrib.auth.models import User
from problems.models import ArchiveProblem
from problemsets.models import Problem
from contests.models import Contest, ContestProblem

STATUS = (
    ("accepted", "accepted"),
    ("wronganswer", "wronganswer"),
    ("runtimeerror", "runtimeerror"),
    ("presentationerror", "presentationerror"),
    ("timelimit", "timelimit"),
    ("memorylimit", "memorylimit"),
    ("compilationerror", "compilationerror"),
    ("outputlimit", "outputlimit"),
    ("notavailable", "notavailable")
)


class Attempt(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE) # Urinish muallifi.
    problem = models.ForeignKey(ArchiveProblem, on_delete=models.CASCADE) # Urinish masalasi.
    date = models.DateTimeField(auto_now_add=True) # Urinish sanasi.
    status = models.CharField(max_length=20) # Urinish holati
    time = models.IntegerField() # Urinish vaqti.
    memory = models.IntegerField() # Urinish xotirasi.
    code = models.TextField()
    language = models.CharField(max_length=20)
    lengthcode = models.IntegerField() # Urinish kod uzunligi.
    cases = models.TextField() # Urinish holatlari.
    output = models.TextField()

    def __str__(self):
        return self.status

    def count(self):
        return self.count()

class Attempt2(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE) # Urinish muallifi.
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE) # Urinish masalasi.
    date = models.DateTimeField(auto_now_add=True) # Urinish sanasi.
    status = models.CharField(max_length=20) # Urinish holati
    time = models.IntegerField() # Urinish vaqti.
    memory = models.IntegerField() # Urinish xotirasi.
    code = models.TextField()
    language = models.CharField(max_length=20)
    lengthcode = models.IntegerField() # Urinish kod uzunligi.
    cases = models.TextField() # Urinish holatlari.
    output = models.TextField()

    def __str__(self):
        return self.status

class ContestAttempt(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE) # Urinish muallifi.
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE) 
    problem = models.ForeignKey(ContestProblem, on_delete=models.CASCADE) # Urinish masalasi.
    date = models.DateTimeField(auto_now_add=True) # Urinish sanasi.
    status = models.CharField(max_length=20) # Urinish holati
    time = models.IntegerField() # Urinish vaqti.
    memory = models.IntegerField() # Urinish xotirasi.
    code = models.TextField()
    language = models.CharField(max_length=20)
    lengthcode = models.IntegerField() # Urinish kod uzunligi.
    cases = models.TextField() # Urinish holatlari.
    output = models.TextField()

    def __str__(self):
        return self.status