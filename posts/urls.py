from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path("", views.post_list, name="list"),
    # 프론트앤드 작업할때는 "1/"로 해놨지만, 나중에는 "<int:pk>/"로 변경예정"
    path("1/", views.post_detail, name="detail"),
]
