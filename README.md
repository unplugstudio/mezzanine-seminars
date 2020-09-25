# Mezzanine Seminars

![Workflow status](https://github.com/unplugstudio/mezzanine-seminars/workflows/Test%20and%20release/badge.svg)
[![PyPI version](https://badge.fury.io/py/mezzanine-seminars.svg)](https://pypi.org/project/mezzanine-seminars/)
[![Python versions](https://img.shields.io/pypi/pyversions/mezzanine-seminars)](https://pypi.org/project/mezzanine-seminars/)
[![Code style: Black](https://img.shields.io/badge/follows-semver-blue.svg)](https://github.com/psf/black)
[![Code style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Seminar platform for [Mezzanine](http://mezzanine.jupo.org/) sites.

## Features

- Create seminars with public and private content
- Accept payments to grant users access to seminars
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

