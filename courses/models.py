from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4
from django.urls import reverse_lazy, reverse

def content_file_name(instance, filename):
    return '/'.join(['courses', f"course{instance.id}", filename])

class Course(models.Model):
    nanoid = models.SlugField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Muallif")
    name = models.CharField(max_length=1000, verbose_name="Nomi")
    price = models.FloatField(default=0, verbose_name="Narxi")
    description = models.TextField(verbose_name="Izox")
    cover = models.ImageField(upload_to="course/images/", verbose_name="Rasm")
    isPublic = models.BooleanField(default=True, verbose_name="Ommaviy/Yashirin")
    users = models.ManyToManyField(User, related_name="course_users", verbose_name="Foydalanuvchilar")
    likes = models.ManyToManyField(User, related_name="course_likes", verbose_name="Likelar")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs) -> None:
        self.nanoid = uuid4()
        return super().save()

    def get_absolute_url(self):
        return reverse("course", args=[str(self.pk)])

    def count_likes(self):
        return self.likes.count()
    
    def count_users(self):
        return self.users.count()
    
    def count(self):
        return self.count()

class Lesson(models.Model):
    nanoid = models.SlugField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=2000)
    body = models.TextField()
    video = models.URLField(null=True, blank=True)
    likes = models.ManyToManyField(User, related_name="lesson_likes")
    enders = models.ManyToManyField(User, related_name="lesson_enders")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs) -> None:
        self.nanoid = uuid4()
        return super().save()

    def get_absolute_url(self):
        return reverse_lazy("home")

    def count_likes(self):
        return self.likes.count()

    def count(self):
        return self.count

class LessonComment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    reply = models.IntegerField(default=0)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.lesson

class CourseRating(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.rating


