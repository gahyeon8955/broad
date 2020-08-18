from django.db import models

# Create your models here.

class Bakery(models.Model):
    name = models.CharField(max_length=20) #빵집 이름
    sub_name = models.CharField(max_length=40) #빵집 소제목(설명)
    lat = models.FloatField() #위도
    lng = models.FloatField() #경도
    address = models.CharField(max_length=150, default="", null=True) #주소
    business_hours = models.CharField(max_length=100, default="", null=True) #영업시간


    def __str__(self):
        return self.name

class Comment(models.Model):
    EVALUATION = (
        (1, '★'),
        (2, '★★'),
        (3, '★★★'),
        (4, '★★★★'),
        (5, '★★★★★'),
    )

    bakery_name = models.ForeignKey('Bakery', on_delete=models.CASCADE, related_name='comments') #해당 빵집 이름(FK)
    evaluation = models.IntegerField(choices=EVALUATION, default= 5) #평점
    created_date = models.DateTimeField(auto_now=True) #작성 시간
    text = models.TextField(default="") #리뷰 내용
    # author = models.ForeignKey(, on_delete=models.CASCADE, null=True) #작성자(로그인 모델 연결 필요)
    approved_comment = models.BooleanField(default=False)

    def __str__(self):
        return str(self.bakery_name)

class Menu(models.Model):
    shop_name = models.ForeignKey('Bakery', on_delete=models.CASCADE, null=True) #해당 빵집 이름(FK)
    menu_name = models.CharField(max_length=80) #메뉴 이름
    price = models.IntegerField() #메뉴 가격

    def __str__(self):
        return str(self.shop_name)