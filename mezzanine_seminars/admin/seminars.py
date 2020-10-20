from __future__ import unicode_literals, absolute_import

import unicodecsv as csv

from copy import deepcopy

from django.conf.urls import url
from django.contrib import admin
from django.shortcuts import get_object_or_404, HttpResponse
from django.utils.module_loading import import_string

from mezzanine.conf import settings
from mezzanine.core.admin import (
    DisplayableAdmin,
    StackedDynamicInlineAdmin,
    TabularDynamicInlineAdmin,
)

from ..models import (
    RegistrationCode,
    Seminar,
    SeminarSubject,
    SeminarContentArea,
    SeminarRegistration,
    SurveyQuestion,
)

###########
# Subject #
###########


@admin.register(SeminarSubject)
class SeminarSubjectAdmin(admin.ModelAdmin):
    pass


###########
# Seminar #
###########


class RegistrationCodeInlineAdmin(TabularDynamicInlineAdmin):
    model = RegistrationCode


class SeminarContentAreaInlineAdmin(StackedDynamicInlineAdmin):
    model = SeminarContentArea
    fields = ["title", "video_link", "content"]


class SurveyQuestionInlineAdmin(TabularDynamicInlineAdmin):
    model = SurveyQuestion
    fields = ["prompt", "field_type", "required"]
    radio_fields = {"field_type": admin.HORIZONTAL}


@admin.register(Seminar)
class SeminarAdmin(DisplayableAdmin):
    inlines = [
        RegistrationCodeInlineAdmin,
        SeminarContentAreaInlineAdmin,
        SurveyQuestionInlineAdmin,
    ]
    list_display = ["title", "publish_date", "status", "featured", "admin_link"]
    list_filter = ["status", "featured"]
    list_editable = ["status", "featured"]
    filter_horizontal = ["subjects"]
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "title",
                    "status",
                    ("publish_date", "expiry_date"),
                    "featured_image",
                    "featured",
                    "length",
                    "price",
                    "subjects",
                ]
            },
        ),
        (
            "Public Content",
            {
                "fields": ["preview_video_link", "content"],
            },
        ),
        # Copy the meta panel from PageAdmin
        deepcopy(DisplayableAdmin.fieldsets[1]),
    ]

    def get_urls(self, *args, **kwargs):
        return [
            url(
                r"^(?P<pk>[\d]+)/export/$",
                self.admin_site.admin_view(self.export_registrations),
                name="mezzanine_seminars_registration_export",
            )
        ] + super(SeminarAdmin, self).get_urls(*args, **kwargs)

    def export_registrations(self, request, pk):
        """
        Admin view that generates a CSV export of all registrations on a Seminar.
        """
        col_names = settings.SEMINARS_REGISTRATION_EXPORT_CSV_COLUMN_NAMES
        get_row_data = import_string(settings.SEMINARS_REGISTRATION_EXPORT_CSV_ROW_DATA)
        seminar = get_object_or_404(Seminar, pk=pk)
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename={}.csv".format(
            seminar.slug
        )
        # https://stackoverflow.com/a/44898198/1330003
        response.write("\ufeff".encode("utf8"))

        writer = csv.writer(response)
        writer.writerow(col_names)
        for registration in seminar.registrations.all():
            writer.writerow(get_row_data(registration))
        return response


#################
# Registrations #
#################


@admin.register(SeminarRegistration)
class SeminarRegistrationAdmin(admin.ModelAdmin):
    date_hierarchy = "created"
    readonly_fields = ["created", "updated", "seminar", "purchaser"]
    list_filter = ["purchaser", "seminar"]
    list_display = [
        "__str__",
        "seminar",
        "created",
        "payment_method",
        "transaction_id",
    ]
    search_fields = [
        "purchaser__first_name",
        "purchaser__last_name",
        "purchaser__email",
        "transaction_id",
        "payment_method",
    ]
    fieldsets = [
        (
            None,
            {
                "fields": [
                    ("created", "updated"),
                    ("purchaser", "seminar"),
                    "price",
                    "payment_method",
                    "transaction_id",
                ]
            },
        ),
        (
            "Notes",
            {
                "classes": ["collapse-closed"],
                "fields": ["transaction_notes"],
            },
        ),
    ]

    def has_add_permission(self, *args, **kwargs):
        return False  # Don't allow creating registrations
