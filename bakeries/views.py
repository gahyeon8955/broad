from django.shortcuts import render
from . import models as bakery_models

# Create your views here.


def bakery_list(request):
    return render(request, "bakeries/bakery_list.html")


def bakery_detail(request):
    bakery = bakery_models.Bakery.objects.get(name="가좌빵집")
    return render(request, "bakeries/bakery_detail.html", {"bakery": bakery})


def bakery_rank(request):
    return render(request, "bakeries/bakery_rank.html")


def bakery_like_list(request):
    return render(request, "bakeries/bakery_like_list.html")


def bakery_review_list(request):
    return render(request, "bakeries/bakery_review_list.html")


def user_review_list(request):
    return render(request, "bakeries/user_review_list.html")
