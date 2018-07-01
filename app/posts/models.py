from django.conf import settings
from django.db import models

from members.models import User, PostLike


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    photo = models.ImageField(upload_to='post', blank=True)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    user_comment = models.CharField(
        max_length=200,
        verbose_name='댓글')
    create_at = models.DateTimeField(auto_now_add=True)






