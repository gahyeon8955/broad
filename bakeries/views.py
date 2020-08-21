from django.shortcuts import render, get_object_or_404
from . import models as bakery
from . import models as review

# Create your views here.


def bakery_list(request):
    all_bakeries = bakery.Bakery.objects.all()
    print(all_bakeries)
    return render(request, "bakeries/bakery_list.html", {"all_bakeries":all_bakeries})


def bakery_detail(request, bakery_id):
    bakery_detail = bakery.Bakery.objects.get(pk=bakery_id)
    return render(request, "bakeries/bakery_detail.html", {"bakery_detail":bakery_detail})


def bakery_rank(request):
    return render(request, "bakeries/bakery_rank.html")


def bakery_like_list(request):
    return render(request, "bakeries/bakery_like_list.html")


def bakery_review_list(request,bakery_id=1):
    one_bakery = get_object_or_404(bakery.Bakery,pk=bakery_id)
    return render(request, "bakeries/bakery_review_list.html", {"bakery":one_bakery})


def user_review_list(request):
    return render(request, "bakeries/user_review_list.html")
