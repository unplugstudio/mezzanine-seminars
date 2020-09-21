from mezzanine.conf import register_setting


register_setting(
    name="SEMINARS_REGISTRATION_FORM",
    editable=False,
    default="mezzanine_seminars.forms.SeminarRegistrationForm",
)

register_setting(
    name="SEMINARS_SURVEY_FORM",
    editable=False,
    default="mezzanine_seminars.forms.surveys.SurveyResponseForm",
)

register_setting(
    name="SEMINARS_PER_PAGE",
    editable=False,
    default=10,
)
