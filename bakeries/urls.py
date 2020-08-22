from django.urls import path
from . import views

app_name = "bakeries"

urlpatterns = [
    # 현재는 1-3)빵집리스트를 url로 나눠놨지만, html,css 작업이 끝나면 map에서 자바스크립트를 통해 페이지 새로고침 없이 보이게 할것임
    path("list/", views.bakery_list, name="list"),
    # 프론트앤드 작업할때는 "1/"로 해놨지만, 나중에는 "<int:pk>/"로 변경예정"
    path("<int:bakery_id>/", views.bakery_detail, name="detail"),
    path("rank/", views.bakery_rank, name="rank"),
    # 나중에 데이터 갖고 작업할시에, <int:pk> 붙여서 유저별 좋아요리스트 구분해주자
    path("like/", views.bakery_like_list, name="like_list"),
    # 프론트앤드 작업할때는 "1/reviews/"로 해놨지만, 나중에는 "<int:pk>/reviews/"로 변경예정"
    path("<int:bakery_id>/reviews/", views.bakery_review_list, name="review_list"),
    path("my/reviews/", views.user_review_list, name="user_review_list"),
]
