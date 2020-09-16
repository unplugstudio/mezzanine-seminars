from __future__ import unicode_literals, absolute_import

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^(?P<slug>[\w-]+)/$", views.SeminarDetailView.as_view(), name="detail")
]
