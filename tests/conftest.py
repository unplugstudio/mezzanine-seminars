import os
import shutil
import sys
import tempfile

import django

from pathlib2 import Path

# Path to the temp mezzanine project folder
TMP_PATH = Path(tempfile.mkdtemp()) / "project_template"

# Injected at the bottom of local_settings.py
TEST_SETTINGS = """
# START INJECTED SETTINGS
INSTALLED_APPS = list(INSTALLED_APPS)
if "mezzanine.accounts" not in INSTALLED_APPS:
    INSTALLED_APPS.append("mezzanine.accounts")
INSTALLED_APPS.append("mezzanine_seminars")

# Use the MD5 password hasher by default for quicker test runs.
PASSWORD_HASHERS = ('django.contrib.auth.hashers.MD5PasswordHasher',)
# END INJECTED SETTINGS
"""

# Injected at the bottom of urls.py
TEST_URLS = """
# START INJECTED URLCONFIG
urlpatterns = list(urlpatterns)
urlpatterns.insert(
    0, url("^seminars/", include("mezzanine_seminars.urls", namespace="seminars"))
)
# END INJECTED URLCONFIG
"""


def after_django_setup():
    """
    Runs once per testing session AFTER Django has been set up.
    """
    from ddf import teach
    from mezzanine_seminars.models import Seminar

    # When creating Seminars we don't want to create extra sites
    teach(Seminar, site=None)


def pytest_report_header(config):
    """
    Have pytest report the path of the project folder
    """
    return "mezzanine proj (tmp): {}".format(TMP_PATH)


def pytest_configure():
    """
    Hack the `project_template` dir into an actual project to test against.
    """
    from mezzanine.utils.importing import path_for_import

    template_path = Path(path_for_import("mezzanine")) / "project_template"
    shutil.copytree(str(template_path), str(TMP_PATH))
    proj_path = TMP_PATH / "project_name"

    # Settings
    local_settings = (proj_path / "local_settings.py.template").read_text()
    (proj_path / "local_settings.py").write_text(local_settings + TEST_SETTINGS)

    # URLs
    urls = (proj_path / "urls.py").read_text()
    (proj_path / "urls.py").write_text(urls + TEST_URLS)

    # Setup the environment for Django
    sys.path.insert(0, str(TMP_PATH))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_name.settings")
    django.setup()
    after_django_setup()


def pytest_unconfigure():
    """
    Remove the temporary folder
    """
    try:
        shutil.rmtree(str(TMP_PATH))
    except OSError:
        pass
