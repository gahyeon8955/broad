from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    # 배포시에는 index페이지 삭제
    path("", views.index),
    path("user/profile/", views.profile_view, name="profile"),
    path("user/profile-update/", views.profile_update, name="profile_update"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("signup/", views.signup, name="signup"),
    path("user/login/kakao/", views.kakao_login, name="kakao-login"),
    path("user/login/kakao/callback/", views.kakao_callback, name="kakao-callback"),
    path("imageupdate/", views.profileimage_update, name="imageupdate"),
]
