from __future__ import unicode_literals, absolute_import

import unicodecsv as csv

from copy import deepcopy

from django.conf.urls import url
from django.contrib import admin
from django.utils.module_loading import import_string
from django.shortcuts import get_list_or_404, HttpResponse

from mezzanine.core.admin import TabularDynamicInlineAdmin
from mezzanine.conf import settings

from ..models import SurveyResponse, QuestionResponse


class QuestionResponseInlineAdmin(TabularDynamicInlineAdmin):
    model = QuestionResponse
    fields = ["question_prompt", "rating", "text_response"]
    readonly_fields = fields
    extra = 0

    def question_prompt(self, response):
        return response.question.prompt


@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = ["__str__", "seminar_title", "created"]
    list_filter = ["registration__purchaser", "registration__seminar"]
    search_fields = [
        "registration__purchaser__first_name",
        "registration__purchaser__last_name",
        "registration__purchaser__email",
        "registration__seminar__title",
    ]
    date_hierarchy = "created"

    inlines = [QuestionResponseInlineAdmin]
    fields = ["__str__", "seminar_title", "created"]
    readonly_fields = fields

    def seminar_title(self, response):
        return response.registration.seminar.title

    seminar_title.short_description = "Seminar"
    seminar_title.admin_order_field = "seminar__title"

    def has_add_permission(self, *args, **kwargs):
        return False  # Don't allow adding through the admin

    def get_urls(self, *args, **kwargs):
        return [
            url(
                r"export/",
                self.admin_site.admin_view(self.export_surveys),
                name="mezzanine_seminars_surveys_export",
            )
        ] + super(SurveyResponseAdmin, self).get_urls(*args, **kwargs)

    def export_surveys(self, request):
        """
        Admin view that generates a CSV export of all surveys response
        """
        col_name = settings.SURVEYS_EXPORT_CSV_COLUMN_NAMES
        get_row_data = import_string(settings.SURVEYS_EXPORT_CSV_ROW_DATA)
        surveys = QuestionResponse.objects.all()
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename={}.csv".format(
            "SurveyResponses"
        )
        response.write("\ufeff".encode("utf8"))
        writer = csv.writer(response)
        writer.writerow(col_name)
        for survey in surveys:
            writer.writerow(get_row_data(survey))
        return response
