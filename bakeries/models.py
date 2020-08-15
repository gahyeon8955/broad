from django.db import models

# Create your models here.

class Bakery(models.Model):
    name = models.CharField(max_length=20)
    sub_name = models.CharField(max_length=40)
    lat = models.FloatField()
    lng = models.FloatField()
    # img = models.ImageField()
    # 이미지 필드 pillow 설치 필요
    

    def __str__(self):
        return self.name

