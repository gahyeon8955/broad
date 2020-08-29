from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    # 배포시에는 index페이지 삭제
    path("index/", views.index),
    # 나중에 데이터 갖고 작업할시에, <int:pk> 붙여서 유저별 프로필 구분해주자(프로필,프로필수정 둘다)
    path("user/profile/", views.profile_view, name="profile"),
    path("user/profile-update/", views.profile_update, name="profile_update"),
    # 현재는 "login/"이지만, 나중에 배포할때는 ""로 해서 가장 첫화면을 로그인화면으로 사용할것임
    path("", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("signup/", views.signup, name="signup"),
    path("imageupdate/", views.profileimage_update, name="imageupdate"),
]
