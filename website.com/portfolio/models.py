from django.db import models

# Create your models here.

class Skill(models.Model):
    name = models.CharField("Nom", max_length=50)
    wording = models.TextField()
    picture = models.ImageField(str(name)+"_skill", upload_to="skill/")

class Projet(models.Model):
    name = models.CharField("Nom", max_length=50)
    wording = models.TextField()
    picture = models.ImageField(str(name)+"_picture", upload_to="projet/")
    skills = models.ManyToManyField(Skill)
