from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    email = models.EmailField()
    password = models.CharField(max_length=30)
    nickname = models.CharField(max_length=20, blank = True)
    
    def __str__(self):
            return self.name