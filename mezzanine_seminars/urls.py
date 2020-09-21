from __future__ import unicode_literals, absolute_import

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^$", views.SeminarListView.as_view(), name="list"),
    url(
        r"^(?P<slug>[\w-]+)/register/$",
        views.SeminarRegistrationCreate.as_view(),
        name="registration_create",
    ),
    url(
        r"^(?P<slug>[\w-]+)/survey/$",
        views.SurveyResponseCreate.as_view(),
        name="survey_response_create",
    ),
    url(r"^(?P<slug>[\w-]+)/$", views.SeminarDetailView.as_view(), name="detail"),
]
