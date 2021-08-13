from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from users import models as user_models
from bakeries import models as bakery_models
import datetime, os, random

# Post모델의 image필드(게시글에 들어갈 사진)의 경로설정 함수
def photo_path(instance, filename):
    basefilename, file_extension = os.path.splitext(filename)
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
    randomstr = "".join((random.choice(chars)) for x in range(10))
    return "post/image/{postid}/{randomstring}{ext}".format(
        postid=instance.id,
        basename=basefilename,
        randomstring=randomstr,
        ext=file_extension,
    )


class Post(models.Model):
    title = models.CharField(max_length=20)
    body = models.CharField(max_length=500)
    created_date = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(
        user_models.User, related_name="posts", on_delete=models.CASCADE
    )
    photo = models.ImageField(upload_to=photo_path, blank=True)
    scraped = models.ManyToManyField(
        user_models.User, blank=True, related_name="scraped"
    )

    def comments_count(self):
        pass

    @property
    def click(self):
        self.views += 1
        self.save()

    def __str__(self):
        return self.title


# Post 객체 삭제시, photo필드의 사진파일도 같이 삭제됨
@receiver(post_delete, sender=Post)
def submission_delete(sender, instance, **kwargs):
    instance.photo.delete(False)


class Comment(models.Model):
    body = models.CharField(max_length=300)
    created_date = models.DateTimeField(auto_now=True)
    post = models.ForeignKey("Post", related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(
        user_models.User, related_name="comments", on_delete=models.CASCADE,
    )
    target_comment = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="comments",
        default=None,
        blank=True,
        null=True,
    )  # 댓글의 답글이 달릴경우 생성되는 필드. 없으면 빈상태로 DB에 저장

    def __str__(self):
        if self.target_comment == None:
            return f"{self.post} | {self.body[:15]}..."
        else:
            return f"{self.post} | [답글]{self.body[:15]}..."
