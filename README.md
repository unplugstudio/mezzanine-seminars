# Mezzanine Seminars

[![Workflow status](https://github.com/unplugstudio/mezzanine-seminars/workflows/Test%20and%20release/badge.svg)](https://github.com/unplugstudio/mezzanine-seminars/actions)
[![PyPI version](https://badge.fury.io/py/mezzanine-seminars.svg)](https://pypi.org/project/mezzanine-seminars/)
[![Python versions](https://img.shields.io/pypi/pyversions/mezzanine-seminars)](https://pypi.org/project/mezzanine-seminars/)
[![Follows: Semantic Versioning](https://img.shields.io/badge/follows-SemVer-blue.svg)](https://semver.org/)
[![Code style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Seminar platform for [Mezzanine](http://mezzanine.jupo.org/) sites.

## Features

- Create seminars with public and private content
- Accept payments to grant users access to seminars
- Use registration codes to give access to select user groups without paying
- "Subject" (category) system to group seminars by topic
- Allows attendees to fill out "post-seminar surveys" to provide feedback
- CSV exports of seminar registrations

## Changelog / History / Release Notes

Check out [GitHub Releases](https://github.com/unplugstudio/mezzanine-seminars/releases).

## Installation

1. Install via pip: `pip install mezzanine-seminars`.
2. Add `"mezzanine_seminars"` to `INSTALLED_APPS`. Make sure `"mezzanine.accounts"` is also added.
3. Add to your root `urls.py`:

```python
url("^seminars/", include("mezzanine_seminars.urls", namespace="seminars"))
```

4. A new Seminars section will appear in the admin. Create your first Seminar!
5. Point your visitors to `/seminars/` to see the list of available seminars.

## Accepting payments

By default registering for a Seminar is completely free even if the seminar has a set price. You can enforce a payment requirement by using a custom form in `settings.SEMINARS_REGISTRATION_FORM` . Different payment processors require different forms:

### Stripe

First, make sure you install the additional requirements with `pip install mezzanine-seminars[stripe]`. Then make sure you define your secret API key in `settings.STRIPE_SK`. In development this should be a test key.

Finally set the Stripe form to be used when users register for a seminar:

```python
# settings.py
SEMINARS_REGISTRATION_FORM = "mezzanine_seminars.forms.stripe.StripeRegistrationForm"
```

This will handle the backend configuration, but you will need to override `seminars/seminar_registration_create.html` to configure Stripe's browser bindings `stripe.js`. This is explained in [Stripe's official docs](https://stripe.com/docs/payments/accept-a-payment-synchronously), but it boils down to sending a PaymentMethod ID in the hidden field named `stripe_method`. With that the server will be able to complete the purchase.

## Registration Codes

Some users might pay for seminar access without using the website, or you (the site owner) might have a special agreement with them to give them access to seminar content without paying. Registration Codes let you do this. Here's an example:

> ACME Inc. has reached an agreement with you for 20 seats for Seminar XYZ. Site admins create the Purchase Code "acme" with the capacity limited to 20. Employees of ACME Inc. will now create their own accounts on the site and enter code "acme" during the registration step for Seminar XYZ instead of paying for their registration. Once the code has been used on 20 registrations it is no longer valid. Site admins will be able to see which code was used in the Seminar Registration admin to identify the 20 attendees from ACME. Multiple Purchase Codes can be active at the same time to allow enrolling multiple user groups, each with a set number of seats.

Generally you will want to combine Registration Codes with an alternative payment method to give users a choice of which to use. For this reason the form `mezzanine_seminars.forms.BaseRegistrationCodeForm` is provided to be mixed in with other forms.

For example, to allow users to register with Stripe OR Registration Codes:

```python
# your_app/forms.py
from mezzanine_seminars.forms import BaseRegistrationCodeForm
from mezzanine_seminars.forms.stripe import StripeRegistrationForm

class CombinedRegistrationForm(BaseRegistrationCodeForm, StripeRegistrationForm):
    """
    Seminar Registration form that supports both Stripe and Registration Codes
    """

# settings.py
SEMINARS_REGISTRATION_FORM = "your_app.forms.CombinedRegistrationForm"
```

## Contributing

Before you contribute a bugfix or add a new feature, please check the issue tracker and open a new issue to discuss the work to be done. Once you're clear you want to work on the codebase:

```bash
git clone git@github.com:unplugstudio/mezzanine-seminars
cd mezzanine-seminars

# Test suite
pip install -e .[testing]
pytest tests

# Code style
pip install flake8 black
flake8 .
black .

# ALTERNATIVE: have Tox run everything (tests and code style)
pip install tox
tox
```

Once you're done with your changes and ensured all tests pass, create a pull request and verify the continuos integration tests also pass.

