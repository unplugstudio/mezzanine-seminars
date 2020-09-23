from __future__ import unicode_literals

from django.core.urlresolvers import reverse

from ddf import G

from mezzanine_seminars.models import (
    Seminar,
    SeminarRegistration,
    SurveyQuestion,
    SurveyResponse,
)

from .utils import WebTestBase


class SurveyResponseCreateViewTest(WebTestBase):
    def test_access(self):
        seminar = G(Seminar)
        url = reverse("seminars:survey_response_create", args=[seminar.slug])

        # Anonymous users should be sent to the login page
        self.get_literal_url(url)
        self.assertEqual(self.last_response.request.path, reverse("login"))

        # Logged in users that haven't registered should be sent back
        self.shortcut_login(username="user", password="pass")
        self.get_literal_url(url)
        self.assertUrlsEqual(seminar.get_absolute_url())

        # Registered users should be sent back if there are no questions to answer
        G(SeminarRegistration, seminar=seminar, purchaser=self.USER)
        self.get_literal_url(url)
        self.assertUrlsEqual(seminar.get_absolute_url())

        # The page should load when at least one question is added
        G(SurveyQuestion, seminar=seminar)
        self.get_literal_url(url)
        self.assertUrlsEqual(url)

    def test_survey_response_create(self):
        # Create a seminar with two required and two optional questions
        seminar = G(Seminar, title="Seminar with survey", price=10)
        reg = G(SeminarRegistration, purchaser=self.USER, seminar=seminar)
        for t in (SurveyQuestion.RATING_FIELD, SurveyQuestion.TEXT_FIELD):
            for r in (True, False):
                G(SurveyQuestion, seminar=seminar, field_type=t, required=r)
        url = reverse("seminars:survey_response_create", args=[seminar.slug])

        # User should receive an error if they skip the 2 required fields
        self.shortcut_login(username="user", password="pass")
        self.get_literal_url(url)
        self.submit("#seminar-survey [type='submit']")
        self.assertUrlsEqual(url)
        self.assertEqual(len(self.last_response.context["form"].errors), 2)

        # Registration should be created with only the required fields
        self.fill_by_name({"question_1": 1, "question_3": "Some text"})
        self.submit("#seminar-survey [type='submit']")
        self.assertUrlsEqual(seminar.get_absolute_url())
        survery_response = SurveyResponse.objects.get()
        self.assertEqual(survery_response.registration, reg)
        self.assertListEqual(
            list(survery_response.responses.values_list("rating", "text_response")),
            [(1, ""), (None, "Some text")],
        )

        # User should be redirected to the seminar page if they try to register again
        self.get_literal_url(url)
        self.assertUrlsEqual(seminar.get_absolute_url())

        # Delete the response so the user can submit the form again
        survery_response.delete()

        # Registration should be created with all fields
        self.get_literal_url(url)
        self.fill_by_name(
            {
                "question_1": 3,
                "question_2": 4,
                "question_3": "Some text",
                "question_4": "More text",
            }
        )
        self.submit("#seminar-survey [type='submit']")
        self.assertUrlsEqual(seminar.get_absolute_url())
        survery_response = SurveyResponse.objects.get()
        self.assertEqual(survery_response.registration, reg)
        self.assertListEqual(
            list(survery_response.responses.values_list("rating", "text_response")),
            [(3, ""), (4, ""), (None, "Some text"), (None, "More text")],
        )
