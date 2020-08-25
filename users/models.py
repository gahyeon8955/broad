from django.db import models
from django.contrib.auth.models import AbstractUser
import os
import random

# Create your models here.


# User모델의 avatar(프로필사진)의 경로설정 함수
def photo_path(instance, filename):
    basefilename, file_extension = os.path.splitext(filename)
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
    randomstr = "".join((random.choice(chars)) for x in range(10))
    return "user/avatar/{userid}/{randomstring}{ext}".format(
        userid=instance.id,
        basename=basefilename,
        randomstring=randomstr,
        ext=file_extension,
    )


class User(AbstractUser):
    nickname = models.CharField(max_length=10, default="", null=True, blank=True)
    avatar = models.ImageField(
        upload_to=photo_path, default="user/avatar/avatar_default.png"
    )
    is_social_login = models.BooleanField(default=False, blank=True, null=True)

