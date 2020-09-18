from mezzanine.conf import register_setting


register_setting(
    name="SEMINARS_REGISTRATION_FORM",
    editable=False,
    default="mezzanine_seminars.forms.SeminarRegistrationForm",
)
