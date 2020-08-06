from django.urls import path
from . import views

app_name = "map"

urlpatterns = [
    path("", views.main_map_view, name="main_map"),
]

