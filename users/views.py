from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, "index.html")


def login(request):
    return render(request, "users/login.html")


def signup(request):
    return render(request, "users/signup.html")


def profile_view(request):
    return render(request, "users/my_profile.html")


def profile_update(request):
    return render(request, "users/profile_update.html")
