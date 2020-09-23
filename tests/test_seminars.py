from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.test import override_settings

from ddf import G

from mezzanine.core.models import CONTENT_STATUS_DRAFT, CONTENT_STATUS_PUBLISHED

from mezzanine_seminars.models import Seminar, SeminarRegistration

from .utils import WebTestBase


class SeminarListViewTest(WebTestBase):
    def test_access(self):
        seminar1 = G(Seminar, title="First Seminar")
        seminar2 = G(Seminar, title="Second Seminar")
        url = reverse("seminars:list")

        # Both seminars should be available in the list view
        self.get_literal_url(url)
        self.assertTextPresent(seminar1.title)
        self.assertTextPresent(seminar2.title)

        # The search form should return relevant results
        self.fill({"#seminar-search [name='q']": "second"})
        self.submit("#seminar-search [type='submit']")
        self.assertTextAbsent(seminar1.title)
        self.assertTextPresent(seminar2.title)

        # Non-published seminar should not be listed
        seminar1.status = CONTENT_STATUS_DRAFT
        seminar1.save()
        self.get_literal_url(url)
        self.assertTextAbsent(seminar1.title)
        self.assertTextPresent(seminar2.title)
        seminar1.status = CONTENT_STATUS_PUBLISHED
        seminar1.save()

        # Pagination should be respected
        with override_settings(SEMINARS_PER_PAGE=1):
            # Page 1, newest seminar
            self.get_literal_url(url)
            self.assertTextAbsent(seminar1.title)
            self.assertTextPresent(seminar2.title)

            # Page 2, oldest seminar
            self.get_literal_url(url + "?page=2")
            self.assertTextPresent(seminar1.title)
            self.assertTextAbsent(seminar2.title)


class SeminarDetailViewTest(WebTestBase):
    def test_access(self):
        seminar = G(Seminar, title="Example Seminar")
        url = seminar.get_absolute_url()

        # Non-published pages cannot be accessed
        seminar.status = CONTENT_STATUS_DRAFT
        seminar.save()
        response = self.get_literal_url(url, expect_errors=True)
        self.assertEqual(response.status_code, 404)

        # Published seminars can be accessed
        seminar.status = CONTENT_STATUS_PUBLISHED
        seminar.save()
        self.get_literal_url(url)
        self.assertTextPresent(seminar.title)


class SeminarRegistrationCreateViewTest(WebTestBase):
    def test_registration(self):
        seminar = G(Seminar, title="Seminar with registration", price=10)
        url = reverse("seminars:registration_create", args=[seminar.slug])

        # Anonymous users should be sent to the login page
        response = self.get_literal_url(url)
        self.assertEqual(response.request.path, reverse("login"))

        # Logged in users should have access
        self.shortcut_login(username="user", password="pass")
        self.get_literal_url(url)
        self.assertTextPresent(seminar.title)

        # User should be able to register by submitting the form
        self.submit("#seminar-registration [type='submit']")
        self.assertUrlsEqual(seminar.get_absolute_url())
        reg = SeminarRegistration.objects.get()
        self.assertEqual(reg.purchaser, self.USER)
        self.assertEqual(reg.seminar, seminar)
        self.assertEqual(reg.price, seminar.price)
        self.assertEqual(reg.payment_method, "Default")
        self.assertEqual(reg.transaction_id, "")
        self.assertEqual(reg.transaction_notes, "")

        # User should be redirected to the seminar page if they try to register again
        self.get_literal_url(url)
        self.assertUrlsEqual(seminar.get_absolute_url())
