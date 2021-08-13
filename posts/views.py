import json
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from . import models as post_models
from .models import Comment
from .forms import PostForm
from .forms import CommentForm

# Create your views here.


def post_list(request):
    all_posts = post_models.Post.objects.all().order_by("-created_date")
    sorted_posts = post_models.Post.objects.all().order_by("-views")
    top3_posts = sorted_posts[:3]
    return render(
        request,
        "posts/post_list.html",
        {"all_posts": all_posts, "top3_posts": top3_posts},
    )


def post_my(request):
    return render(request, "posts/my_post_list.html")


def post_detail(request, post_id):
    post_detail = get_object_or_404(post_models.Post, pk=post_id)
    try:
        is_scraped = request.user.scraped.filter(pk=post_id).exists()
    except:
        is_scraped = ""

    if request.method == "POST":
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post_detail
            comment.user = request.user
            comment.save()
            return redirect("/post/" + str(post_id))
    else:
        form = CommentForm()
    return render(
        request,
        "posts/post_detail.html",
        {"post_detail": post_detail, "form": form, "is_scraped": is_scraped},
    )


def post_write(request):

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect("/post/")

    else:
        form = PostForm()
    return render(request, "posts/post_write.html", {"form": form})


def post_update(request, post_id):
    post = get_object_or_404(post_models.Post, pk=post_id)
    form = PostForm(request.POST, request.FILES, instance=post, auto_id=True)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("/post/" + str(post_id))
    else:
        form = PostForm(instance=post)
        return render(request, "posts/post_update.html", {"form": form})


def post_delete(request, post_id):
    post = post_models.Post.objects.get(pk=post_id)
    post.delete()
    return redirect("/post/")


def add_comment_to_post(request, post_id):
    post = get_object_or_404(post_models.Post, pk=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect("/post/" + str(post_id))
    else:
        form = CommentForm()
    return render(request, "posts/post_add_comment.html", {"form": form})


def comment_delete(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.author = request.user

    if (
        comment.author != request.user
        and not request.is_staff
        and request.user != document.author
    ):
        return redirect("/post/" + str(post_id))
    else:
        comment.delete()
        return redirect("/post/" + str(post_id))


@login_required
@require_POST
def ajax_scrap(request):
    if request.method == "POST":
        user = request.user
        pk = request.POST.get("pk", None)
        post = post_models.Post.objects.get(pk=pk)
        if user.scraped.filter(pk=pk).exists():
            post.scraped.remove(user)
        else:
            post.scraped.add(user)
    context = {}
    return HttpResponse(json.dumps(context), content_type="application/json")


def scrap_post_list(request):
    return render(request, "posts/scrap_post_list.html")

