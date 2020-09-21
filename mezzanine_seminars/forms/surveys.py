from __future__ import unicode_literals, absolute_import

from django import forms

from ..models import SurveyResponse, SurveyQuestion, QuestionResponse


class SurveyResponseForm(forms.ModelForm):
    """
    Allows users to answer survey questions.
    """

    class Meta:
        model = SurveyResponse
        fields = []  # No model fields are user-editable

    def __init__(self, registration, *args, **kwargs):
        """
        Create dynamic fields for each question in the Seminar.
        """
        self.registration = registration
        self.questions = registration.seminar.survey_questions.order_by("field_type")
        super(SurveyResponseForm, self).__init__(*args, **kwargs)

        rating_choices = [(i, i) for i in range(1, 6)]  # 1 to 5
        for question in self.questions:
            field_key = "question_%s" % question.pk

            if question.field_type == SurveyQuestion.RATING_FIELD:
                field = forms.ChoiceField(
                    label=question.prompt,
                    widget=forms.RadioSelect,
                    required=question.required,
                    choices=rating_choices,
                )
                field.type = "choicefield"  # Required to apply the right CSS rules
            elif question.field_type == SurveyQuestion.TEXT_FIELD:
                field = forms.CharField(
                    label=question.prompt,
                    widget=forms.Textarea,
                    required=question.required,
                )

            # Use the HTML5 required attribute
            if question.required:
                field.widget.attrs["required"] = ""

            self.fields[field_key] = field

    def save(self, *args, **kwargs):
        """
        Create a QuestionResponse for each Question.
        """
        self.instance.registration = self.registration
        survey_response = super(SurveyResponseForm, self).save(*args, **kwargs)

        if survey_response.pk is None:
            return survey_response  # Bail if the SurveyResponse wasn't saved to the DB

        question_responses = []
        for question in self.questions:
            value = self.cleaned_data.get("question_{}".format(question.pk))
            if not value:
                continue  # Leave out empty (optional) fields
            response = QuestionResponse(
                response=survey_response,
                question=question,
                rating=value
                if question.field_type == SurveyQuestion.RATING_FIELD
                else None,
                text_response=value
                if question.field_type == SurveyQuestion.TEXT_FIELD
                else "",
            )
            question_responses.append(response)
        QuestionResponse.objects.bulk_create(question_responses)

        return survey_response
