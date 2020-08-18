from django.db import models

# Create your models here.

class Bakery_post(models.Model):
    title = models.CharField(max_length=20)
    nick_name = models.CharField(max_length=10)
    time = models.DateTimeField(auto_now_add=True)
    hits = models.IntegerField()
    comment_number = models.IntegerField()
    body = models.CharField(max_length=500)
    # image =

    def __str__(self):
        return self.title

    