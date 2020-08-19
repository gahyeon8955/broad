from django.db import models
from users import models as user_models

# Create your models here.


class Bakery(models.Model):
    name = models.CharField(max_length=20)  # 빵집 이름
    sub_name = models.CharField(max_length=40)  # 빵집 소제목(설명)
    lat = models.FloatField()  # 위도
    lng = models.FloatField()  # 경도
    address = models.CharField(max_length=150, default="", null=True)  # 주소
    business_hours = models.CharField(max_length=100, default="", null=True)  # 영업시간

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
    # price = models.IntegerField()  # 메뉴 가격 =>>> Django third-party app인 Django-money를 통해 money로 변경예정
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
        "Bakery", on_delete=models.CASCADE, related_name="comments"
    )  # 해당 빵집 이름(FK)
    writer = models.ForeignKey(
        user_models.User, related_name="reviews", on_delete=models.CASCADE, null=True
    )  # 작성자

    def __str__(self):
        return f"{self.bakery} | {self.text}"
