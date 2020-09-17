from __future__ import unicode_literals, absolute_import

from copy import deepcopy

from django.contrib import admin

from mezzanine.core.admin import DisplayableAdmin, StackedDynamicInlineAdmin

from .models import Seminar, SeminarSubject, SeminarContentArea

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


@admin.register(Seminar)
class SeminarAdmin(DisplayableAdmin):
    inlines = [SeminarContentAreaInlineAdmin]
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
