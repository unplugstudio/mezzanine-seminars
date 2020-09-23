from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import User
from django.test import TestCase

from django_functest import FuncWebTestMixin, ShortcutLoginMixin


class WebTestBase(FuncWebTestMixin, ShortcutLoginMixin, TestCase):
    @classmethod
    def setUpTestData(cls):

        super(WebTestBase, cls).setUpTestData()
        cls.USER = User.objects.create_user(username="user", password="pass")
