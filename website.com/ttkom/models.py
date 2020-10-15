from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

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


class Comment(models.Model):
    fk_author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    fk_post = models.ForeignKey(Post, on_delete=models.DO_NOTHING)
    content = models.TextField()
    date_comment = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="blog_comment")
