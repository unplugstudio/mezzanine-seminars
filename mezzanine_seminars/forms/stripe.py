from __future__ import unicode_literals, absolute_import

import json
import stripe

from django import forms
from mezzanine.conf import settings

from . import BaseSeminarRegistrationForm


class StripeRegistrationForm(BaseSeminarRegistrationForm):
    stripe_method = forms.CharField(required=False, widget=forms.HiddenInput())
    stripe_intent = forms.CharField(required=False, widget=forms.HiddenInput())
    stripe_client_secret = forms.CharField(required=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(StripeRegistrationForm, self).__init__(*args, **kwargs)
        self.api_key = settings.STRIPE_SK  # Catch missing keys early

    def execute_transaction(self):
        """
        Connect to Stripe to execute the transaction
        https://stripe.com/docs/payments/accept-a-payment-synchronously
        """
        payment_method_id = self.cleaned_data.get("stripe_method")
        payment_intent_id = self.cleaned_data.get("stripe_intent")
        try:
            if payment_method_id:
                # Single step payment
                intent = stripe.PaymentIntent.create(
                    api_key=self.api_key,
                    payment_method=payment_method_id,
                    amount=int(self.seminar.price * 100),
                    currency="usd",
                    confirmation_method="manual",
                    confirm=True,
                )
            elif payment_intent_id:
                # Multi step payment
                intent = stripe.PaymentIntent.confirm(
                    payment_intent_id, api_key=self.api_key
                )
            else:
                raise forms.ValidationError("Missing payment information")
        except stripe.error.CardError as error:
            raise forms.ValidationError(error.user_message)

        if (
            intent.status == "requires_action"
            and intent.next_action.type == "use_stripe_sdk"
        ):
            # Further action required, raise error to re-render the form
            # Attach the client secret to be read by frontend code
            data = self.data.copy()  # self.data is immutable, work on a copy
            data["stripe_method"] = ""
            data["stripe_client_secret"] = intent.client_secret
            self.data = data
            raise forms.ValidationError("Please authenticate to complete the payment")
        elif intent.status == "succeeded":
            # The payment didn't need any additional actions and completed!
            # Prepare transaction details for storage
            charge = intent["charges"]["data"][0]
            return {
                "payment_method": "Stripe",
                "transaction_id": charge["id"],
                "transaction_notes": json.dumps(charge, indent=2),
            }
        raise forms.ValidationError("Stripe communication error")
