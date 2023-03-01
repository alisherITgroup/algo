from django.db import models
from django.contrib.auth.models import User
from problemsets.models import Category, ProgrammingLanguage
from uuid import uuid4
from django.urls import reverse_lazy


class Contest(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    authors = models.ManyToManyField(User, related_name="contest_authors")
    password = models.CharField(max_length=20, default="123", null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    users = models.ManyToManyField(User, related_name="contest_users")
    langs = models.ManyToManyField(ProgrammingLanguage, related_name="contest_langs")
    startdate = models.CharField(max_length=20)
    starttime = models.CharField(max_length=20)
    enddate = models.CharField(max_length=20)
    endtime = models.CharField(max_length=20)
    isPublic = models.BooleanField(default=True)
    isIndividual = models.BooleanField(default=True)
    isContinued = models.CharField(max_length=20, default="notstarted")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy("home")

    def count(self):
        return self.count()
 
class ContestProblem(models.Model):
    nanoid = models.SlugField() # Masalaning nanoidsi.
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE) # Masala muallifi.
    name = models.CharField(max_length=1000, verbose_name="Masala nomi") # Masala nomi.
    problem = models.TextField(verbose_name="Masala matni") # Masala matni.
    timelimit = models.IntegerField(verbose_name="Masala vaqt chegarasi(TimeLimit)") # Masala vaqt cheklovi.
    memorylimit = models.IntegerField(verbose_name="Masala xotira chegarasi(MemoryLimit)") # Masala xotira cheklovi.
    difficulty = models.IntegerField(verbose_name="Masala qiyinchiligi") # Masala qiyinchilik darajasi.
    comment = models.TextField(null=True, blank=True, verbose_name="Masala uchun izoh.") # Masala uchun izox.
    category = models.ManyToManyField(Category, related_name="contest_problem_category") # Masala kategoriyasi
    infoin = models.TextField(default="Kirish ma'lumotlari mavjud emas.", null=True, blank=True, verbose_name="Kirish ma'lumotlari") # Kirish ma'lumotlari.
    infoout = models.TextField(default="Masala javobi.", null=True, blank=True, verbose_name="Chiqish ma'lumotlari") # Chiqish ma'lumotlari
    simpletests = models.TextField(default="{}", null=True, blank=True, verbose_name="Simple testlar") # Simple testlar
    tests = models.TextField(verbose_name="Testlar") # Testlar
    solution = models.TextField(verbose_name="Masalar yechimi.", null=True, blank=True, default="Muallif bu masala yechimini taqdim qilmagan.")
    isArchive = models.BooleanField(default=False, verbose_name="Arxivga qo'shish") # Masalalar arxiviga qoshish
    solvers = models.ManyToManyField(User, related_name="contest_problem_solvers")
    errors = models.ManyToManyField(User, related_name="contest_problem_errors")

    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs) -> None:
        self.nanoid = uuid4()
        return super().save()
    
    def get_absolute_url(self):
        return reverse_lazy("home")
    
    def count(self):
        return self.count()

        
class ContestRating(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contest_rating_author")
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, related_name="contest_rating")
    rating = models.IntegerField(default=0)
    status = models.TextField(default="{}")

class ContestComment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    reply = models.IntegerField(default=0)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
