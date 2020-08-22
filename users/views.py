from django.shortcuts import render, redirect
from .models import User
from .forms import UpdateProfileForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .forms import LoginForm
from .forms import SignUpForm

# Create your views here.


def index(request):
    return render(request, "index.html")


def login(request):
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


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            auth_user = authenticate(request, username=username, password=password)
            if auth_user is not None:
                auth_login(request, auth_user)
                return redirect("map:main_map")
    else:
        form = SignUpForm()
    return render(request, "users/signup.html", {"form": form})


def profile_view(request):
    return render(request, "users/my_profile.html")


def profile_update(request):
    user = User.objects.get(id=request.user.id)
    if request.method == "POST":
        form = UpdateProfileForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            return redirect("users:profile")
    else:
        form = UpdateProfileForm(instance=user)
    return render(request, "users/profile_update.html", {"form": form})
