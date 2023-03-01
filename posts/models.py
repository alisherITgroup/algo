from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

def content_file_name(instance, filename):
    return '/'.join(['posts', f"post{instance.id}", filename])

class Tag(models.Model):
    tag = models.CharField(max_length=200)

    def __str__(self):
        return self.tag

class Post(models.Model):
    nanoid = models.SlugField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    description = models.TextField()
    cover = models.ImageField(upload_to=content_file_name)
    body = models.TextField(default="Bu yerga maqola matnini yozing.") 
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="post_likes")
    tags = models.ManyToManyField(Tag, related_name="post_tags")

    def __str__(self):
        return self.name

    def count_likes(self):
        return self.likes.count()
    
    def get_absolute_url(self):
        return reverse("post", args=[str(self.pk)])

class PostComment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reply = models.IntegerField(default=0)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.post)