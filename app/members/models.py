from django.contrib.auth.models import AbstractUser
from django.db import models


from members.exceptions import FollowRelationNotExist, DuplicateRelationException, DoesNotExist
from posts.exceptions import FollowRelationNotExistPost, DuplicateRelationExceptionPost
# from posts.models import Post


class User(AbstractUser):
    CHOICES_GENDER = (
        ('m', '남성'),
        ('f', '여성'),
        ('x', '선택안함'),
    )
    img_profile = models.ImageField(upload_to='user', blank=True)
    site = models.URLField(blank=True)
    introduce = models.TextField(blank=True)
    gender = models.CharField(max_length=1, choices=CHOICES_GENDER)
    to_relation_user = models.ManyToManyField(
        'self',
        through='Relation',
        symmetrical=False,
        blank=True,
        related_name='from_relation_users',
        related_query_name='form_relation_user',
    )

    def __str__(self):
        return self.username

    def follow(self, another_user):
        if not self.relations_by_from_user.filter(
                to_user=another_user).exists():
            return self.relations_by_from_user.create(
                to_user=another_user,
                relation_type=Relation.RELATION_TYPE_FOLLOW,
            )
        elif self.relations_by_from_user.filter(
                to_user=another_user,
                relation_type=Relation.RELATION_TYPE_BLOCK
        ).exists():
            re = self.relations_by_from_user.get(to_user=another_user)
            re.relation_type = Relation.RELATION_TYPE_FOLLOW
            re.save()
            return re

        else:
            raise DuplicateRelationException(
                from_user=self,
                to_user=another_user,
                relation_type=Relation.RELATION_TYPE_FOLLOW,
            )

    def unfollow(self, another_user):
        q = self.relations_by_from_user.filter(
            to_user=another_user,
            relation_type=Relation.RELATION_TYPE_FOLLOW,
        )
        if q:
            q.delete()
        else:
            raise FollowRelationNotExist(
                from_user=self,
                to_user=another_user,
                relation_type=Relation.RELATION_TYPE_FOLLOW
            )

    def following_block(self, another_user):
        if self.relations_by_from_user.filter(
                to_user=another_user,
                relation_type=Relation.RELATION_TYPE_FOLLOW,
        ).exists():
            re = self.relations_by_from_user.get(to_user=another_user)
            re.relation_type = Relation.RELATION_TYPE_BLOCK
            re.save()

        else:
            raise DoesNotExist(
                from_user=self,
                to_user=another_user,
                relation_type=Relation.RELATION_TYPE_FOLLOW
            )

    def follower_block(self, another_user):
        if self.relations_by_to_user.filter(
                from_user=another_user,
                relation_type=Relation.RELATION_TYPE_FOLLOW,
        ).exists():
            re = self.relations_by_to_user.get(from_user=another_user)
            re.relation_type = Relation.RELATION_TYPE_BLOCK
            re.save()

        else:
            raise DoesNotExist(
                from_user=self,
                to_user=another_user,
                relation_type=Relation.RELATION_TYPE_FOLLOW
            )


    @property
    def following(self):
        return User.objects.filter(
            relations_by_to_user__from_user=self,
            relations_by_to_user__relation_type=Relation.RELATION_TYPE_FOLLOW,
        )

    @property
    def followers(self):
        return User.objects.filter(
            relations_by_from_user__to_user=self,
            relations_by_from_user__relation_type=Relation.RELATION_TYPE_FOLLOW,
        )


    @property
    def block_user(self):
        return User.objects.filter(
            relations_by_to_user__from_user=self,
            relations_by_to_user__relation_type=Relation.RELATION_TYPE_BLOCK,
        )

    @property
    def following_relation(self):
        return self.relations_by_from_user.filter(relation_type=Relation.RELATION_TYPE_FOLLOW)

    @property
    def follower_relation(self):
        return self.relations_by_to_user.filter(relation_type=Relation.RELATION_TYPE_FOLLOW)

    @property
    def block_relation(self):
        return self.relations_by_from_user.filter(relation_type=Relation.RELATION_TYPE_BLOCK)

    # def likes(self, post):
    #     if not self.likes_by_from_user.filter(
    #             post=post,
    #     ).exists():
    #         return self.likes_by_from_user.create(
    #             post=post,
    #             user=self,
    #             post_like=PostLike.CHOICES_POST_LIKE,
    #         )
    #     elif self.likes_by_from_user.filter(
    #             post=post,
    #             post_like=PostLike.CHOICES_POST_UNLIKE,
    #     ).exists():
    #         re = self.likes_by_from_user.get(post=post)
    #         re.post_like = PostLike.CHOICES_POST_LIKE
    #         re.save()
    #         return re
    #
    #     else:
    #         raise DuplicateRelationExceptionPost(
    #             post=post,
    #             user=self,
    #             likes_type=PostLike.CHOICES_POST_LIKE,
    #         )
    #
    # def unlikes(self, post):
    #     q = self.likes_by_from_user.filter(
    #         post=post,
    #         post_like=PostLike.CHOICES_POST_LIKE,
    #     )
    #     if q:
    #         q.delete()
    #
    #     else:
    #         raise FollowRelationNotExistPost(
    #             post=post,
    #             user=self,
    #             likes_type=PostLike.CHOICES_POST_LIKE,
    #         )
    #
    # @property
    # def like_post(self):
    #     return User.objects.filter(
    #         likes_by_from_user__user=self,
    #         likes_by_from_user__post_like=PostLike.CHOICES_POST_LIKE,
    #     )


class Relation(models.Model):
    RELATION_TYPE_BLOCK = 'b'
    RELATION_TYPE_FOLLOW = 'f'

    CHOICE_RELATION_TYPE = (
        (RELATION_TYPE_FOLLOW, 'Follow'),
        (RELATION_TYPE_BLOCK, 'Block'),
    )

    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='relations_by_from_user'
    )

    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='relations_by_to_user'
    )

    relation_type = models.CharField(max_length=1, choices=CHOICE_RELATION_TYPE)

    class Meta:
        unique_together = (
            ('from_user', 'to_user'),
        )

    def __str__(self):
        return 'From {from_user} to {to_user} ({type})'.format(
            from_user=self.from_user.username,
            to_user=self.to_user.username,
            type=self.get_relation_type_display(),
        )


# class PostLike(models.Model):
#     CHOICES_POST_LIKE = 'L'
#     CHOICES_POST_UNLIKE = 'U'
#
#     CHOICES_LIKE = (
#         (CHOICES_POST_LIKE, 'Like'),
#         (CHOICES_POST_UNLIKE, 'Unlike')
#     )
#     post = models.ForeignKey(
#         Post,
#         on_delete=models.CASCADE,
#         related_name='likes_by_from_post',
#
#     )
#
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='likes_by_from_user',
#     )
#
#     post_like = models.CharField(max_length=1, choices=CHOICES_LIKE)
#
#     created_at = models.DateTimeField(auto_now_add=True)
