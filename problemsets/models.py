from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.db import models
from uuid import uuid4

class ProgrammingLanguage(models.Model):
    name = models.CharField(max_length=20)
    version = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Katgoriya nomi")
    
    def __str__(self):
        return self.name


class Problem(models.Model):
    nanoid = models.SlugField() # Masalaning nanoidsi.
    author = models.ForeignKey(User, on_delete=models.CASCADE) # Masala muallifi.
    name = models.CharField(max_length=1000, verbose_name="Masala nomi") # Masala nomi.
    problem = models.TextField(verbose_name="Masala matni") # Masala matni.
    timelimit = models.IntegerField(verbose_name="TimeLimit") # Masala vaqt cheklovi.
    memorylimit = models.IntegerField(verbose_name="MemoryLimit") # Masala xotira cheklovi.
    difficulty = models.IntegerField(verbose_name="Masala qiyinchiligi") # Masala qiyinchilik darajasi.
    category = models.ManyToManyField(Category)
    allowedlangs = models.ManyToManyField(ProgrammingLanguage)
    comment = models.TextField(null=True, blank=True, verbose_name="Masala uchun izoh.") # Masala uchun izox.
    infoin = models.TextField(default="Kirish ma'lumotlari mavjud emas.", null=True, blank=True, verbose_name="Kirish ma'lumotlari") # Kirish ma'lumotlari.
    infoout = models.TextField(default="Masala javobi.", null=True, blank=True, verbose_name="Chiqish ma'lumotlari") # Chiqish ma'lumotlari
    simpletests = models.TextField(default="{}", null=True, blank=True, verbose_name="Simple testlar") # Simple testlar
    tests = models.TextField(verbose_name="Testlar") # Testlar
    solution = models.TextField(verbose_name="Masalar yechimi.", null=True, blank=True, default="Muallif bu masala yechimini taqdim qilmagan.")
    isArchive = models.BooleanField(default=False, verbose_name="Arxivga qo'shish") # Masalalar arxiviga qoshish
    isContest = models.BooleanField(default=False)
    solvers = models.ManyToManyField(User, related_name="problemset_solvers")
    errors = models.ManyToManyField(User, related_name="problemset_errors")
    
    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs) -> None:
        self.nanoid = uuid4()
        return super().save()
    
    def get_absolute_url(self):
        return reverse_lazy("home")
        # return reverse("problemsets", [(self.author)])
    
    def count(self):
        return self.count()
    
    def count_solvers(self):
        return self.solvers.count()