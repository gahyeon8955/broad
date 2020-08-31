from django.db import models
from django.utils import timezone
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.html import mark_safe
from users import models as user_models
from phonenumber_field.modelfields import PhoneNumberField
import datetime
import os
import random

# Create your models here.


# Photo 모델의 사진경로 설정 함수
def logo_photo_path(instance, filename):
    basefilename, file_extension = os.path.splitext(filename)
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
    randomstr = "".join((random.choice(chars)) for x in range(10))
    return "bakery/image/{bakeryid}/{randomstring}{ext}".format(
        bakeryid=instance.id,
        basename=basefilename,
        randomstring=randomstr,
        ext=file_extension,
    )


class Bakery(models.Model):
    name = models.CharField(max_length=100)  # 빵집 이름
    sub_name = models.CharField(max_length=100, default="", blank=True)  # 빵집 소제목(설명)
    lat = models.FloatField(default=0, blank=True)  # 위도
    lng = models.FloatField(default=0, blank=True)  # 경도
    address = models.CharField(max_length=150, default="", blank=True)  # 주소
    phone_number = models.CharField(max_length=30, default="", blank=True)  # 전화번호
    business_hour = models.CharField(max_length=100, default="", blank=True)
    temp_review_count = models.IntegerField(default=0, blank=True, null=True)
    temp_total_rating = models.IntegerField(default=0, blank=True, null=True)
    logo = models.ImageField(
        upload_to="logo_photo_path", default="bakery/image/logo_default.png"
    )
    like = models.ManyToManyField(user_models.User, blank=True, related_name="like")
    city = models.CharField(
        max_length=20, default="", blank=True, null=True
    )  # 도시(진주/울산/전주/의정부 등)

    def short_sub_name(self):
        return self.sub_name[:30] + "..." if self.sub_name != "" else ""

    def review_count(self):
        return self.reviews.all().count()

    def total_rating(self):
        all_reviews_rating_list = list(map(lambda x: x.rating, self.reviews.all()))
        rating_sum = sum(all_reviews_rating_list)
        try:
            return round(rating_sum / len(all_reviews_rating_list), 1)
        except:
            return 0

    def __str__(self):
        return self.name


# Bakery 객체 삭제시, logo필드의 사진파일도 같이 삭제됨
@receiver(post_delete, sender=Bakery)
def submission_delete(sender, instance, **kwargs):
    instance.logo.delete(False)


class Photo(models.Model):
    bakery = models.ForeignKey(
        "Bakery", related_name="photos", on_delete=models.CASCADE
    )
    photo = models.ImageField(upload_to="bakery/bread_imgs")

    def __str__(self):
        return f"{self.bakery} | 사진"


# Photo 객체 삭제시, 사진파일도 같이 삭제됨
@receiver(post_delete, sender=Photo)
def submission_delete(sender, instance, **kwargs):
    instance.photo.delete(False)


class Menu(models.Model):
    name = models.CharField(max_length=80)  # 메뉴 이름
    row_price = models.IntegerField(default=0)
    bakery = models.ForeignKey(
        "Bakery", related_name="menus", on_delete=models.CASCADE, null=True
    )  # 해당 빵집 이름(FK)

    def price(self):
        string = str(self.row_price)
        if self.row_price >= 1000000:
            return f"{string[0]},{string[1:4]},{string[4:7]}"
        elif self.row_price >= 100000:
            return f"{string[0:3]},{string[3:6]}"
        elif self.row_price >= 10000:
            return f"{string[0:2]},{string[2:5]}"
        elif self.row_price >= 1000:
            return f"{string[0:1]},{string[1:4]}"
        else:
            return string

    def __str__(self):
        return f"{self.bakery}의 메뉴 | {self.name}"


class Review(models.Model):
    RATING = (
        (1, "★"),
        (2, "★★"),
        (3, "★★★"),
        (4, "★★★★"),
        (5, "★★★★★"),
    )

    body = models.TextField()  # 리뷰 내용
    rating = models.FloatField(choices=RATING, default=5)  # 평점
    created_date = models.DateTimeField(auto_now=True)  # 작성 시간
    bakery = models.ForeignKey(
        "Bakery", on_delete=models.CASCADE, related_name="reviews"
    )  # 해당 빵집 이름(FK)
    user = models.ForeignKey(
        user_models.User, related_name="reviews", on_delete=models.CASCADE, null=True
    )  # 작성자

    def __str__(self):
        return f"{self.bakery} 리뷰 | {self.body}"
