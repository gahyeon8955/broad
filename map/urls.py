from django.urls import path
from . import views

app_name = "map"

urlpatterns = [
    path("", views.main_map_view, name="main_map"),
    path("region-api/", views.get_region_api, name="get_region_api"),
    path("bakery-list-api/", views.get_bakery_list_api, name="get_bakery_list_api"),
    path(
        "bakery-detail-api/", views.get_bakery_detail_api, name="get_bakery_detail_api"
    ),
    path(
        "bakery-detail-reviews-api/",
        views.get_bakery_detail_reviews_api,
        name="get_bakery_detail_reviews_api",
    ),
    path("bakery-delete-review/", views.ajax_delete_review, name="ajax_delete_review"),
]

