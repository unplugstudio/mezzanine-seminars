from __future__ import unicode_literals, absolute_import

import json
import mock
import pytest

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import override_settings

from ddf import G

from mezzanine_seminars.models import Seminar, SeminarRegistration

from .utils import WebTestBase

pytest.importorskip("stripe", reason="Missing Stripe SDK")


@override_settings(
    STRIPE_SK="test",
    SEMINARS_REGISTRATION_FORM="mezzanine_seminars.forms.stripe.StripeRegistrationForm",
)
class TestStripe(WebTestBase):
    def test_access(self):
        seminar = G(Seminar, title="Stripe seminar", price=10)
        url = reverse("seminars:registration_create", args=[seminar.slug])
        self.shortcut_login(username="user", password="pass")

        # Registration should fail on form render (not on submit)
        # if the Stripe key is not set
        del settings.STRIPE_SK
        with self.assertRaises(AttributeError):
            self.get_literal_url(url)

        # Form should render correctly once the key is set
        settings.STRIPE_SK = "test"
        self.get_literal_url(url)
        self.assertTextPresent(seminar.title)

        # User should receive an error if the form is submitted empty
        self.submit("#seminar-registration [type='submit']")
        self.assertUrlsEqual(url)
        self.assertTextPresent("Missing payment information")
        self.assertEqual(SeminarRegistration.objects.count(), 0)

    def test_free_registration(self):
        seminar = G(Seminar, title="Stripe seminar", price=0)
        url = reverse("seminars:registration_create", args=[seminar.slug])
        self.shortcut_login(username="user", password="pass")

        # User should be able to register for free without filling out the form
        self.get_literal_url(url)
        self.submit("#seminar-registration [type='submit']")
        self.assertUrlsEqual(seminar.get_absolute_url())
        reg = SeminarRegistration.objects.get()
        self.assertEqual(reg.purchaser, self.USER)
        self.assertEqual(reg.seminar, seminar)
        self.assertEqual(reg.price, seminar.price)
        self.assertEqual(reg.payment_method, "Complimentary")
        self.assertEqual(reg.transaction_id, "")
        self.assertEqual(reg.transaction_notes, "")

    @mock.patch("mezzanine_seminars.forms.stripe.stripe.PaymentIntent.create")
    def test_successful_registration(self, create_mock):
        seminar = G(Seminar, title="Stripe seminar", price=10)
        url = reverse("seminars:registration_create", args=[seminar.slug])
        self.shortcut_login(username="user", password="pass")

        # Configure mock with successful values
        create_mock.return_value.status = "succeeded"
        create_mock.return_value.__getitem__.return_value = {
            "data": [{"id": "mock id", "mock_key": "mock_value"}]
        }

        # A registration should be created if a payment method is sent in the form
        self.get_literal_url(url)
        self.fill({"#id_stripe_method": "test"})
        self.submit("#seminar-registration [type='submit']")
        self.assertUrlsEqual(seminar.get_absolute_url())
        reg = SeminarRegistration.objects.get()
        self.assertEqual(reg.purchaser, self.USER)
        self.assertEqual(reg.seminar, seminar)
        self.assertEqual(reg.price, seminar.price)
        self.assertEqual(reg.payment_method, "Stripe")
        self.assertEqual(reg.transaction_id, "mock id")
        self.assertDictEqual(
            json.loads(reg.transaction_notes),
            {"id": "mock id", "mock_key": "mock_value"},
        )

        # User should be redirected to the seminar page if they try to register again
        self.get_literal_url(url)
        self.assertUrlsEqual(seminar.get_absolute_url())
        reg.delete()

    @mock.patch("mezzanine_seminars.forms.stripe.stripe.PaymentIntent.confirm")
    @mock.patch("mezzanine_seminars.forms.stripe.stripe.PaymentIntent.create")
    def test_multistep_registartion(self, create_mock, confirm_mock):
        seminar = G(Seminar, title="Stripe seminar", price=10)
        url = reverse("seminars:registration_create", args=[seminar.slug])
        self.shortcut_login(username="user", password="pass")

        # Configure mock to require multiple steps when creating the intent
        create_mock.return_value.status = "requires_action"
        create_mock.return_value.next_action.type = "use_stripe_sdk"
        create_mock.return_value.client_secret = "STRIPE CLIENT SECRET"

        # The form should be re-rendered if the Stripe API requires multiple steps
        self.get_literal_url(url)
        self.fill({"#id_stripe_method": "test"})
        self.submit("#seminar-registration [type='submit']")
        self.assertUrlsEqual(url)
        self.assertTextPresent("Please authenticate to complete the payment")
        self.assertTextPresent("STRIPE CLIENT SECRET")
        self.assertEqual(SeminarRegistration.objects.count(), 0)

        # Configure the mock to complete successfully when confirming the intent
        confirm_mock.return_value.status = "succeeded"
        confirm_mock.return_value.__getitem__.return_value = {
            "data": [{"id": "multistep mock id", "mock_key": "mock_value"}]
        }

        # The registration should be created on the second submission
        self.fill({"#id_stripe_intent": "test"})
        self.submit("#seminar-registration [type='submit']")
        self.assertUrlsEqual(seminar.get_absolute_url())
        reg = SeminarRegistration.objects.get()
        self.assertEqual(reg.purchaser, self.USER)
        self.assertEqual(reg.seminar, seminar)
        self.assertEqual(reg.price, seminar.price)
        self.assertEqual(reg.payment_method, "Stripe")
        self.assertEqual(reg.transaction_id, "multistep mock id")
        self.assertDictEqual(
            json.loads(reg.transaction_notes),
            {"id": "multistep mock id", "mock_key": "mock_value"},
        )

        # User should be redirected to the seminar page if they try to register again
        self.get_literal_url(url)
        self.assertUrlsEqual(seminar.get_absolute_url())
        reg.delete()
