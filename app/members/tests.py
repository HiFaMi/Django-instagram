
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase, TransactionTestCase

from members.exceptions import DuplicateRelationException

User = get_user_model()


class RelationTestCase(TransactionTestCase):

    def create_dummy_user(self, num):
        return [User.objects.create_user(username='test{}'.format(i+1)) for i in range(num)]

    def test_follow(self):
        u1 = User.objects.create_user(username='u1')
        u2 = User.objects.create_user(username='u2')

        u1.follow(u2)
        # u1.relations_by_from_user.create(to_user=u2, relation_type='f')

        self.assertIn(u2, u1.following)

        self.assertTrue(u1.following_relation.filter(to_user=u2).exists())

    def test_follow_only_once(self):
        u1 = User.objects.create_user(username='u1')
        u2 = User.objects.create_user(username='u2')

        u1.follow(u2)
        u1.follow(u2)

        # with self.assertRaises(DuplicateRelationException):
        #     u1.follow(u2)
        #
        # self.assertEqual(u1.following.count(), 1)

    def test_unfollow_if_follow_exit(self):
        u1, u2 = self.create_dummy_user(2)

        u1.follow(u2)
        u1.unfollow(u2)

        self.assertNotIn(u2, u1.following)

    def test_unfollow_fail_if_follow_not_exit(self):
        u1, u2 = self.create_dummy_user(2)

        u1.follow(u2)
        u1.unfollow(u2)


