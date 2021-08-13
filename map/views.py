import json
from django.shortcuts import render, get_object_or_404
from django.core import serializers
from django.http import HttpResponse
from bakeries import models as bakery_models

# Create your views here.


def main_map_view(request):
    return render(request, "map/main_map.html")


def get_region_api(request):
    if request.method == "GET":
        region = request.GET.get("region")
        all_datas = {}
        photos = bakery_models.Photo.objects.filter(bakery__city=region)
        bakeries = bakery_models.Bakery.objects.filter(city=region)
        for bakery in bakeries:
            bkr = json.loads(serializers.serialize("json", [bakery,]))
            pts = json.loads(
                serializers.serialize("json", photos.filter(bakery=bakery))
            )
            result = {"bakery": bkr, "photos": pts}
            all_datas[bakery.name] = result
        result_data = json.dumps(all_datas)
        return HttpResponse(result_data, content_type="application/json")


def get_bakery_list_api(request):
    region = request.GET.get("region")
    a_bakery_list = bakery_models.Bakery.objects.filter(city=region)
    bakery_list = sorted(a_bakery_list, key=lambda x: x.total_rating(), reverse=True)
    counts = {"review": [], "rating": []}
    for index, bakery in enumerate(bakery_list):
        counts["review"].append(bakery.review_count())
        counts["rating"].append(bakery.total_rating())
    if a_bakery_list.exists():
        obj_json = json.loads(serializers.serialize("json", bakery_list))

        return HttpResponse(
            json.dumps({"obj": obj_json, "counts": counts}),
            content_type="application/json",
        )
    else:
        return HttpResponse(
            json.dumps({"result": "none"}), content_type="application/json"
        )


def get_bakery_detail_api(request):
    pk = request.GET.get("pk")
    try:
        is_liked = request.user.like.filter(pk=pk).exists()
    except:
        is_liked = ""
    bakery = bakery_models.Bakery.objects.get(pk=pk)
    photos = bakery.photos.all()
    menus = bakery.menus.all()
    reviews = bakery.reviews.all().order_by("-created_date")[:2]
    reviews_list = []
    for review in reviews:
        created_d = review.created_date.strftime("%y.%m.%d")
        reviews_list.append(
            {
                "user_img": review.user.avatar.url,
                "user_nickname": review.user.nickname,
                "created_date": created_d,
                "user_rating": review.rating,
                "body": review.body,
            }
        )
    bakery_dict = json.loads(serializers.serialize("json", [bakery,]))
    photos_dict = json.loads(serializers.serialize("json", photos))
    menus_dict = json.loads(serializers.serialize("json", menus))
    result = {}
    result["bakery"] = bakery_dict[0]
    result["photos"] = photos_dict
    result["menus"] = menus_dict
    result["reviews"] = reviews_list
    result["is_liked"] = is_liked
    result["total_rating"] = bakery.total_rating()
    result["review_count"] = bakery.review_count()
    data = json.dumps(result)
    return HttpResponse(data, content_type="application/json")


def get_bakery_detail_reviews_api(request):
    pk = request.GET.get("pk")
    reviews = (
        bakery_models.Bakery.objects.get(pk=pk).reviews.all().order_by("-created_date")
    )
    reviews_dict = json.loads(serializers.serialize("json", reviews))
    created_date_list = []
    photos_list = []
    nicknames_list = []
    is_equal_writer_and_login_list = []
    for review in reviews:
        created_date_list.append(review.created_date.strftime("%y.%m.%d"))
        photos_list.append(review.user.avatar.url)
        nicknames_list.append(review.user.nickname)
        is_equal_writer_and_login_list.append(review.user == request.user)
    result = {}

    result["reviews"] = reviews_dict
    result["created_date"] = created_date_list
    result["photos"] = photos_list
    result["nicknames"] = nicknames_list
    result["is_equal_writer_and_login"] = is_equal_writer_and_login_list
    data = json.dumps(result)
    return HttpResponse(data, content_type="application/json")


def ajax_delete_review(request):
    pk = request.POST.get("pk")
    review = get_object_or_404(bakery_models.Review, pk=pk)
    if review.user == request.user:
        review.delete()
        return HttpResponse({"success": "success"}, content_type="application/json")
    else:
        raise Http404("접근할 수 없습니다.")
