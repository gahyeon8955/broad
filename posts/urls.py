from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path("", views.post_list, name="list"),
    # 프론트앤드 작업할때는 "1/"로 해놨지만, 나중에는 "<int:pk>/"로 변경예정"
    path("my/", views.post_my, name="my"),
    path("<int:post_id>/", views.post_detail, name="detail"),
    path("write/", views.post_write, name="write"),
    path("<int:post_id>/update/", views.post_update, name="update"),
    path("<int:post_id>/delete/", views.post_delete, name="delete"),
    path(
        "<int:post_id>/addcomment/",
        views.add_comment_to_post,
        name="add_comment_to_post",
    ),
    path(
        "<int:post_id>/comment/<int:comment_id>/delete",
        views.comment_delete,
        name="comment_delete",
    ),
    path("ajax_scrap/", views.ajax_scrap, name="ajax_scrap"),
    path("scrap/", views.scrap_post_list, name="scrap"),
]
