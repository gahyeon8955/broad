from django.shortcuts import render
from .models import User
from .forms import UpdateProfileForm

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
    user = User.objects.get(id=request.user.id)
    if request.method == "POST":
        form = UpdateProfileForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            return redirect('users:profile_update')
    else:
        form = UpdateProfileForm(instance=user)
    return render(request, "users/profile_update.html")