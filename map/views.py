import json
from django.shortcuts import render
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
