import requests
import random
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.conf import settings
from .models import User
from .forms import UpdateProfileForm, UpdateProfileImageForm, LoginForm, SignUpForm


# Create your views here.


def index(request):
    return render(request, "index.html")


def login(request):
    if request.user.is_authenticated:
        return redirect("map:main_map")
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            auth_user = authenticate(request, username=username, password=password)
            if auth_user is not None:
                auth_login(request, auth_user)
                return redirect("map:main_map")
    else:
        form = LoginForm()
    return render(request, "users/login.html", {"form": form})


def logout(request):
    auth_logout(request)
    return redirect("users:login")


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            username = email
            nickname = form.cleaned_data.get("nickname")
            if nickname is None:
                nickname = email.split("@")[0]
            password = form.cleaned_data.get("password")
            user = User.objects.create_user(
                username=username, nickname=nickname, email=email, password=password
            )
            auth_user = authenticate(request, username=username, password=password)
            if auth_user is not None:
                auth_login(request, auth_user)
                return redirect("map:main_map")
    else:
        form = SignUpForm()
    return render(request, "users/signup.html", {"form": form})


def profile_view(request):
    if request.user.is_anonymous:
        return redirect("users:login")
    return render(request, "users/my_profile.html")


def profile_update(request):
    user = User.objects.get(id=request.user.id)
    if request.method == "POST":
        form = UpdateProfileForm(request.POST, instance=user)
        if user.is_social_login:
            if request.POST.get("nickname") == "":
                pass
            else:
                user.nickname = request.POST.get("nickname")
                user.save()
            return redirect(reverse("users:profile"))
        if form.is_valid():
            username = request.user.username
            user = form.save(commit=False)
            user.nickname = form.cleaned_data.get("nickname")
            if form.cleaned_data.get("nickname") is None:
                user.nickname = request.user.email.split("@")[0]
            user.set_password(form.cleaned_data.get("password"))
            user.save()
            auth_login(request, user)
            return redirect(reverse("users:profile"))
    else:
        form = UpdateProfileForm(instance=user)
    return render(request, "users/profile_update.html", {"form": form})


# 카카오 소셜로그인
def kakao_login(request):
    client_id = settings.KAKAO_ID
    redirect_uri = "http://127.0.0.1:8000/user/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )


class KakaoException(Exception):
    pass


def kakao_callback(request):
    try:
        code = request.GET.get("code")
        client_id = settings.KAKAO_ID
        redirect_uri = "http://127.0.0.1:8000/user/login/kakao/callback"
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
        )
        token_json = token_request.json()
        error = token_json.get("error", None)
        if error is not None:
            raise KakaoException("접근할 수 없습니다.")
        access_token = token_json.get("access_token")
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()
        kakao_account = profile_json.get("kakao_account")
        properties = profile_json.get("properties")
        nickname = properties.get("nickname")
        email = f"{nickname}@KakaoLogin.com"
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
        username = "".join((random.choice(chars)) for x in range(8)) + "@kakaologin.com"
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create(
                email=email, username=username, nickname=nickname, is_social_login=True
            )
            user.set_unusable_password()
            user.save()
        # messages.success(request, f"환영합니다, {user.nickname}님!")
        auth_login(request, user)
        return redirect(reverse("map:main_map"))
    except KakaoException as e:
        # messages.error(request, e)
        return redirect(reverse("users:login"))


def profileimage_update(request):
    user = User.objects.get(id=request.user.id)
    if request.method == "POST":
        form = UpdateProfileImageForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save()
            return redirect("users:profile_update")
    else:
        form = UpdateProfileImageForm(instance=user)
        return render(request, "users/profileimage_form.html", {"form": form})
