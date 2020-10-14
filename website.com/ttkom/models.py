from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    name = models.CharField(max_length=150)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_post = models.DateTimeField()
    likes = models.ManyToManyField(User, blank=True, related_name="blog_post")

    @property
    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.name
