from django.shortcuts import render

# Create your views here.


def main_map_view(request):
    return render(request, "map/main_map.html")
