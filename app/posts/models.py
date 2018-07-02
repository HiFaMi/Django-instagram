from django.conf import settings
from django.db import models

from members.models import User


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    photo = models.ImageField(upload_to='post', blank=True)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='like_posts',
    )


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

# class AnotherComment(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     parent_comment = models.ForeignKey(
#         'self',
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#     )
#     author = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#     )
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     modeified_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return 'Comment (post: {}, author: {})'.format(self.post.pk, self.author.username)



