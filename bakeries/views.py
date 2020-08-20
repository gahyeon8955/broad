from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from .forms import WriteReviewForm
from . import models as bakery_models


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


# 현재는 테스트용으로 bakery_id=4로 기본값4 줬지만, 다른것들과 연동되면 '=4'부분 제거 예정
def review_write(request, bakery_id=4):
    if request.user.is_anonymous:
        raise Http404("접근할 수 없습니다.")

    if request.method == "POST":
        form = WriteReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.bakery = bakery_models.Bakery.objects.get(id=bakery_id)
            review.user = request.user
            review.save()
            return redirect("bakeries:user_review_list")
    else:
        form = WriteReviewForm()
    return render(request, "bakeries/review_write.html", {"form": form})


def review_delete(request, review_id):
    review = get_object_or_404(bakery_models.Review, id=review_id)
    if review.user == request.user:
        review.delete()
        return redirect("map:main_map")
    else:
        raise Http404("접근할 수 없습니다.")
