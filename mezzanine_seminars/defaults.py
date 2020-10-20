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
    name="SEMINARS_REGISTRATION_EXPORT_CSV_COLUMN_NAMES",
    editable=False,
    default=(
        "Registration",
        "Email",
        "Seminar",
        "Date created",
        "Price",
        "Payment method",
        "Transcation ID",
    ),
)

register_setting(
    name="SEMINARS_REGISTRATION_EXPORT_CSV_ROW_DATA",
    editable=False,
    default="mezzanine_seminars.models.seminars.registration_row_data",
)

register_setting(
    name="SEMINARS_PER_PAGE",
    editable=False,
    default=10,
)
