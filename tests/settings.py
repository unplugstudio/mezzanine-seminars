import tempfile

SECRET_KEY = "for testing purposes"
ALLOWED_HOSTS = ["*"]
INSTALLED_APPS = (
    "grappelli_safe",
    "filebrowser_safe",
    "tests",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
)
MIDDLEWARE = (
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
)
ROOT_URLCONF = "tests.urls"

STATIC_URL = "/static/"
MEDIA_URL = "/media/"
MEDIA_ROOT = tempfile.mkdtemp()


DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}

# List of callables that know how to import templates from various sources.
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
                "mezzanine.conf.context_processors.settings",
            ],
        },
    },
]

# Non standart settings
THUMBNAILS_DIR_NAME = "thumbnails"

# Mezzanine specific settings
GRAPPELLI_INSTALLED = False
PACKAGE_NAME_FILEBROWSER = "filebrowser_safe"
TINYMCE_SETUP_JS = STATIC_URL
JQUERY_FILENAME = STATIC_URL
JQUERY_UI_FILENAME = STATIC_URL
TEMPLATE_ACCESSIBLE_SETTINGS = (
    "JQUERY_FILENAME",
    "JQUERY_UI_FILENAME",
    "TINYMCE_SETUP_JS",
)
