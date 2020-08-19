from django.shortcuts import render

# Create your views here.


def bakery_list(request):
    return render(request, "bakeries/bakery_list.html")


def bakery_detail(request):
    return render(request, "bakeries/bakery_detail.html")


def bakery_rank(request):
    return render(request, "bakeries/bakery_rank.html")


def bakery_like_list(request):
    return render(request, "bakeries/bakery_like_list.html")


def bakery_review_list(request):
    return render(request, "bakeries/bakery_review_list.html")


def user_review_list(request):
    return render(request, "bakeries/user_review_list.html")
