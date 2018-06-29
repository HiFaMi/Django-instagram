from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class RelationTestCase(TestCase):

    def test_follow(self):
        u1 = User.objects.create_user(username='u1')
        u2 = User.objects.create_user(username='u2')

        u1.follow(u2)
        # u1.relations_by_from_user.create(to_user=u2, relation_type='f')

        self.assertIn(u2, u1.following)

