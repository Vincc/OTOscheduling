from django.db import models
from django import forms
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Permission
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField


class UserManager(BaseUserManager): #customizing built in user manager
    def create_user(self, username, password=None): #create and save user with a given password and studentcode
        if not username:
            raise ValueError("User must have a valid username")
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        if not username:
            raise ValueError("User must have a valid username")
        user = self.create_user(username,password=password)
        user.is_admin = True
        user.is_teacher = True
        user.save(using=self._db)
        return user

class user(AbstractBaseUser, PermissionsMixin): #custom user model based on base user framework
    email = None
    is_teacher = models.BooleanField(default=False) 
    is_admin = models.BooleanField(default=False) 

    tutorGroup = CharField(max_length=4, default="0000") 
    username = models.CharField(max_length=30, unique=True, default="appUser")
    meetingtimes = models.ManyToManyField("sessionTimes", related_name="students")

    #username and password field is built in, and dosen't need to be redefined
    objects = UserManager() #define the usermanager for customuser
    list_display = ("username", "is_admin")#backend configuration for django
    list_filter = ("is_admin")#backend configuration for django
    USERNAME_FIELD = "username" #point to username field as django's identifier for username
    REQUIRED_FIELDS = [] #make username required, password field is requierd by default

    @property
    def is_staff(self):
        return self.is_teacher

    @property
    def is_superuser(self):
        return self.is_admin

    def __str__(self):
        return self.username



class sessiondates(models.Model):#define a sessiondates table
    date = models.DateField(unique = True) #create field of dates
    class Meta: #define metadata
        ordering = ["date"] #order table by value of date

class sessionTimes(models.Model):#define a sessiontimes table
    """
    Line 71 creates a one to many relationship between sessionTimes 
    and sessiondates(the timeslots are constant across different dates)
    """
    sessiontimedate = models.ForeignKey(sessiondates, on_delete=CASCADE)
    time = models.TimeField() #create field of sessiontimes
    class Meta: #define metadata
        ordering = ["time"] #order table by value of time



