import pytest
from django.conf import settings

from test_plus.test import TestCase

pytestmark = pytest.mark.django_db


# def test_user_get_absolute_url(user: settings.AUTH_USER_MODEL):
#     assert user.get_absolute_url() == f"/users/{user.username}/"


class TestUser(TestCase):

    def setUp(self):
        self.user = self.make_user()

    def test__str__(self):
        self.assertEqual(self.user.__str__(), 'testuser')

    def test_get_absolute_url(self):
        self.assertEqual(self.user.get_absolute_url(), '/users/testuser/')

    def test_get_profile_name(self):
        assert self.user.get_profile_name() == 'testuser'
        self.user.nickname = '昵称'
        assert self.user.get_profile_name() == '昵称'
