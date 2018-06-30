from django.contrib.auth.models import AbstractUser
from django.db import models

from members.exceptions import FollowRelationNotExist, DuplicateRelationException


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
        q=self.relations_by_from_user.filter(
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




    @property
    def following(self):
        return User.objects.filter(
            relations_by_to_user__from_user=self,
            relations_by_to_user__relation_type=Relation.RELATION_TYPE_FOLLOW,
        )

    @property
    def followers(self):
        return User.objects.filter(
            relations_by_to_from__to_user=self,
            relations_by_to_from__relation_type=Relation.RELATION_TYPE_FOLLOW,
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
