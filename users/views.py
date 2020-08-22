from django.shortcuts import render, redirect, reverse
from .models import User
from .forms import UpdateProfileForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .forms import LoginForm
from .forms import SignUpForm

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
        if form.is_valid():
            username = request.user.username
            user = form.save(commit=False)
            user.nickname = form.cleaned_data.get("nickname")
            if form.cleaned_data.get("nickname") is None:
                user.nickname = request.user.email.split("@")[0]
            user.set_password(form.cleaned_data.get("password"))
            user.save()
            auth_user = authenticate(
                request, username=username, password=form.cleaned_data.get("password")
            )
            auth_login(request, auth_user)
            return redirect(reverse("users:profile"))
    else:
        form = UpdateProfileForm(instance=user)
    return render(request, "users/profile_update.html", {"form": form})
