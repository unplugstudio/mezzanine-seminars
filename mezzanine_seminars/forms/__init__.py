from __future__ import unicode_literals, absolute_import

import json

from django import forms
from django.db.models import F

from ..models import SeminarRegistration, RegistrationCode

TRANSACTION_KEYS = ["payment_method", "transaction_id", "transaction_notes"]
MISSING_KEY = "Key `{}` is missing from return value of `{}.execute_transaction()`"


class BaseSeminarRegistrationForm(forms.ModelForm):
    """
    Base class for all registrations.
    Subclasses must override the `execute_transaction` method
    """

    class Meta:
        model = SeminarRegistration
        fields = []  # No fields are editable

    def __init__(self, seminar, purchaser, *args, **kwargs):
        """
        Receive arguments from the view for later use
        """
        self.purchaser = purchaser
        self.seminar = seminar
        super(BaseSeminarRegistrationForm, self).__init__(*args, **kwargs)

    def execute_transaction(self):
        """
        Override this method to interact with payment gateways.
        Raise `ValidationError` if the transaction is rejected.
        Return a transaction details dictionary if successful.
        """
        raise NotImplementedError

    def clean(self):
        """
        Execute the transaction when cleaning the form.
        This way payment gateway errors are treated as validation errors.
        """
        cleaned_data = super(BaseSeminarRegistrationForm, self).clean()
        if self.errors:  # Standard validation failed already, don't continue
            return cleaned_data
        details = self.execute_transaction()
        for k in TRANSACTION_KEYS:
            if k not in details:
                raise ValueError(MISSING_KEY.format(k, self.__class__))
        cleaned_data.update(details)
        return cleaned_data

    def save(self, *args, **kwargs):
        """
        Attach extra information to the instance before saving
        """
        for k in TRANSACTION_KEYS:
            setattr(self.instance, k, self.cleaned_data[k])

        self.instance.purchaser = self.purchaser
        self.instance.seminar = self.seminar
        self.instance.price = self.seminar.price
        return super(BaseSeminarRegistrationForm, self).save(*args, **kwargs)


class SeminarRegistrationForm(BaseSeminarRegistrationForm):
    def execute_transaction(self):
        """
        Provides placeholder transaction details
        """
        return {
            "payment_method": "Default",
            "transaction_id": "",
            "transaction_notes": "",
        }


class BaseRegistrationCodeForm(BaseSeminarRegistrationForm):
    """
    Form with support for registration codes
    Combine with another form that supports a different registration method
    """

    code = forms.CharField(label="Register with Code", max_length=50, required=False)

    def clean_code(self):
        code = self.cleaned_data.get("code", "")
        return RegistrationCode.normalize_code(code)

    def execute_transaction(self):
        """
        Create a registration using the code (if provided)
        """
        code = self.cleaned_data.get("code")
        if not code:
            # No code was provided, proceed as usual
            return super(BaseRegistrationCodeForm, self).execute_transaction()

        try:
            registration_code = RegistrationCode.objects.get(
                code=code, seminar=self.seminar, available__gt=0
            )
        except RegistrationCode.DoesNotExist:
            raise forms.ValidationError("The registration code is not valid")

        registration_code.available = F("available") - 1
        registration_code.save()
        registration_code.refresh_from_db()  # Get the new available number
        return {
            "payment_method": "Registration code",
            "transaction_id": code,
            "transaction_notes": json.dumps({"available": registration_code.available}),
        }
