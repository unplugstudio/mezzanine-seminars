from __future__ import unicode_literals, absolute_import

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from mezzanine.core.models import Orderable, TimeStamped


@python_2_unicode_compatible
class SurveyQuestion(Orderable):
    """
    An admin-editable survey question on a Seminar
    """

    RATING_FIELD = 1
    TEXT_FIELD = 2
    QUESTION_TYPES = (
        (RATING_FIELD, "Rating"),
        (TEXT_FIELD, "Text"),
    )

    seminar = models.ForeignKey(
        "mezzanine_seminars.Seminar",
        on_delete=models.CASCADE,
        related_name="survey_questions",
    )
    field_type = models.IntegerField("Question type", choices=QUESTION_TYPES)
    prompt = models.CharField("Prompt", max_length=300)
    required = models.BooleanField("Required", default=True)

    def __str__(self):
        return self.prompt


@python_2_unicode_compatible
class SurveyResponse(TimeStamped):
    """
    Collection of all responses related to a Registration.
    """

    registration = models.OneToOneField(
        "mezzanine_seminars.SeminarRegistration",
        related_name="survey_response",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.registration)


@python_2_unicode_compatible
class QuestionResponse(models.Model):
    """
    Response to a single Question.
    """

    response = models.ForeignKey(
        SurveyResponse, related_name="responses", on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        SurveyQuestion, related_name="responses", on_delete=models.CASCADE
    )
    rating = models.PositiveSmallIntegerField("Rating", blank=True, null=True)
    text_response = models.TextField("Text response", blank=True)

    def __str__(self):
        if self.rating is not None:
            return str(self.rating)
        return self.text_response
