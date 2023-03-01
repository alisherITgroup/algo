from django.db import models
from django.contrib.auth.models import User
from problemsets.models import Category, ProgrammingLanguage
from django.urls import reverse_lazy, reverse

class ArchiveProblem(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="archive_problem_author") # Masala muallifi.
    name = models.CharField(max_length=1000, verbose_name="Masala nomi") # Masala nomi.
    problem = models.TextField(verbose_name="Masala matni") # Masala matni.
    timelimit = models.IntegerField(verbose_name="TimeLimit") # Masala vaqt cheklovi.
    memorylimit = models.IntegerField(verbose_name="MemoryLimit") # Masala xotira cheklovi.
    difficulty = models.IntegerField(verbose_name="Masala qiyinchiligi") # Masala qiyinchilik darajasi.
    category = models.ManyToManyField(Category, related_name="archive_problem_category")
    allowedlangs = models.ManyToManyField(ProgrammingLanguage, related_name="archive_problem_langs")
    comment = models.TextField(null=True, blank=True, verbose_name="Masala uchun izoh.") # Masala uchun izox.
    infoin = models.TextField(default="Kirish ma'lumotlari mavjud emas.", null=True, blank=True, verbose_name="Kirish ma'lumotlari") # Kirish ma'lumotlari.
    infoout = models.TextField(default="Masala javobi.", null=True, blank=True, verbose_name="Chiqish ma'lumotlari") # Chiqish ma'lumotlari
    simpletests = models.TextField(default="{}", null=True, blank=True, verbose_name="Simple testlar") # Simple testlar
    tests = models.TextField(verbose_name="Testlar") # Testlar
    solution = models.TextField(verbose_name="Masalar yechimi.", null=True, blank=True, default="Muallif bu masala yechimini taqdim qilmagan.")
    solvers = models.ManyToManyField(User, related_name="problem_solvers")
    errors = models.ManyToManyField(User, related_name="problem_errors")
    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        # return reverse_lazy("problems")
        return reverse("problem", args=[str(self.pk)])
    
    def count(self):
        return self.count()

    def count_solvers(self):
        return self.solvers.count()
    
    def username(self):
        return self.author.username

class ArchiveProblemComment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(ArchiveProblem, on_delete=models.CASCADE)
    reply = models.IntegerField(default=0)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author