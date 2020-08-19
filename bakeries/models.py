from django.db import models
from django.utils import timezone
from users import models as user_models
from phonenumber_field.modelfields import PhoneNumberField
import datetime

# Create your models here.


class Bakery(models.Model):
    name = models.CharField(max_length=20, default="")  # 빵집 이름
    sub_name = models.CharField(max_length=40, default="")  # 빵집 소제목(설명)
    lat = models.FloatField(default=0)  # 위도
    lng = models.FloatField(default=0)  # 경도
    address = models.CharField(max_length=150, default="", null=True, blank=True)  # 주소
    open_time = models.TimeField(default="00:00:00.000000", blank=True)
    close_time = models.TimeField(default="00:00:00.000000", blank=True)
    phone_number = PhoneNumberField(default="", region="KR")  # 전화번호
    # like

    def business_hour(self):
        return f"{self.open_time.hour}:{self.open_time.minute} ~ {self.close_time.hour}:{self.close_time.minute}"

    def total_rating(self):
        pass

    def __str__(self):
        return self.name


# Photo 모델의 사진경로 설정 함수
def photo_path(instance, filename):
    basefilename, file_extension = os.path.splitext(filename)
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
    randomstr = "".join((random.choice(chars)) for x in range(10))
    return "bakery/image/{bakeryid}/{randomstring}{ext}".format(
        bakeryid=instance.bakery.id,
        basename=basefilename,
        randomstring=randomstr,
        ext=file_extension,
    )


class Photo(models.Model):
    bakery = models.ForeignKey(
        "Bakery", related_name="photos", on_delete=models.CASCADE
    )
    file = models.ImageField(upload_to=photo_path)


class Menu(models.Model):
    name = models.CharField(max_length=80)  # 메뉴 이름
    price = models.IntegerField(default=0)
    bakery = models.ForeignKey(
        "Bakery", related_name="menus", on_delete=models.CASCADE, null=True
    )  # 해당 빵집 이름(FK)

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

    body = models.CharField(max_length=300)  # 리뷰 내용
    rating = models.IntegerField(choices=RATING, default=5)  # 평점
    created_date = models.DateTimeField(auto_now=True)  # 작성 시간
    bakery = models.ForeignKey(
        "Bakery", on_delete=models.CASCADE, related_name="reviews"
    )  # 해당 빵집 이름(FK)
    writer = models.ForeignKey(
        user_models.User, related_name="reviews", on_delete=models.CASCADE, null=True
    )  # 작성자

    def __str__(self):
        return f"{self.bakery} | {self.text}"
