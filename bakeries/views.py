import json
from django.shortcuts import render, redirect, get_object_or_404
from django.core import serializers
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import WriteReviewForm
from . import models as bakery_models
from .crawling import add_data

try:
    from django.utils import simplejson as json
except ImportError:
    import json
# Create your views here.


def bakery_list(request):
    all_bakeries = bakery_models.Bakery.objects.all()
    return render(request, "bakeries/bakery_list.html", {"all_bakeries": all_bakeries})


def bakery_detail(request, bakery_id):
    bakery_detail = bakery_models.Bakery.objects.get(pk=bakery_id)
    reviews = bakery_detail.reviews.all().order_by("-created_date")[:2]
    try:
        is_liked = request.user.like.filter(pk=bakery_id).exists()
    except:
        is_liked = ""
    return render(
        request,
        "bakeries/bakery_detail.html",
        {"bakery_detail": bakery_detail, "reviews": reviews, "is_liked": is_liked},
    )


@login_required
@require_POST
def ajax_like(request):
    if request.method == "POST":
        user = request.user
        pk = request.POST.get("pk", None)
        bakery = bakery_models.Bakery.objects.get(pk=pk)
        if user.like.filter(pk=pk).exists():
            bakery.like.remove(user)
        else:
            bakery.like.add(user)
    context = {}
    return HttpResponse(json.dumps(context), content_type="application/json")


def get_sorted_data(bread):
    soboro_object = bakery_models.Menu.objects.filter(name=bread)
    # soboro_bakery = list(
    #     map(lambda x: (x.bakery, x.bakery.total_rating()), soboro_object)
    # )
    soboro_bakery = []
    for x in soboro_object:
        x.bakery.temp_review_count = x.bakery.review_count()
        x.bakery.temp_total_rating = x.bakery.total_rating()
        x.bakery.save()
        soboro_bakery.append((x.bakery, x.bakery.total_rating()))
    soboro_bakery = sorted(soboro_bakery, key=lambda x: x[1], reverse=True)
    return [i[0] for i in soboro_bakery]


def soboro_sort_data(request):
    data = serializers.serialize("json", get_sorted_data("소보로빵"))
    response = HttpResponse(content=data)
    return response


def rollcake_sort_data(request):
    data = serializers.serialize("json", get_sorted_data("롤케이크"))
    response = HttpResponse(content=data)
    return response


def makarong_sort_data(request):
    data = serializers.serialize("json", get_sorted_data("마카롱"))
    response = HttpResponse(content=data)
    return response


def cookie_sort_data(request):
    data = serializers.serialize("json", get_sorted_data("쿠키"))
    response = HttpResponse(content=data)
    return response


def bakery_rank(request):
    return render(request, "bakeries/bakery_rank.html")


def bakery_like_list(request):
    return render(request, "bakeries/bakery_like_list.html")


def bakery_review_list(request, bakery_id):
    one_bakery = get_object_or_404(bakery_models.Bakery, pk=bakery_id)
    reviews = one_bakery.reviews.all().order_by("-created_date")
    return render(
        request,
        "bakeries/bakery_review_list.html",
        {"bakery": one_bakery, "reviews": reviews},
    )


def user_review_list(request):
    return render(request, "bakeries/user_review_list.html")


def review_write(request, bakery_id):
    if request.user.is_anonymous:
        raise Http404("접근할 수 없습니다.")

    if request.method == "POST":
        form = WriteReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.bakery = bakery_models.Bakery.objects.get(id=bakery_id)
            review.user = request.user
            review.save()
            return redirect(f"/bakery/{bakery_id}/reviews/")
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
