from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import CharField

# Create your models here.
class user(AbstractUser):
    tutorGroup = CharField(max_length=4, default="0000")
    pass




class sessiondates(models.Model):
    date = models.DateField()
    
    class Meta:
        ordering = ['date']
class sessionTimes(models.Model):
    time = models.TimeField()
    
    class Meta:
        ordering = ['time']  
