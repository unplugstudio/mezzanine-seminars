from __future__ import unicode_literals, absolute_import

from copy import deepcopy

from django.contrib import admin

from mezzanine.core.admin import (
    DisplayableAdmin,
    StackedDynamicInlineAdmin,
    TabularDynamicInlineAdmin,
)

from ..models import (
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


class SeminarContentAreaInlineAdmin(StackedDynamicInlineAdmin):
    model = SeminarContentArea
    fields = ["title", "video_link", "content"]


class SurveyQuestionInlineAdmin(TabularDynamicInlineAdmin):
    model = SurveyQuestion
    fields = ["prompt", "field_type", "required"]
    radio_fields = {"field_type": admin.HORIZONTAL}


@admin.register(Seminar)
class SeminarAdmin(DisplayableAdmin):
    inlines = [SeminarContentAreaInlineAdmin, SurveyQuestionInlineAdmin]
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
