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
    fields = ["title", "content"]


@admin.register(Seminar)
class SeminarAdmin(DisplayableAdmin):
    inlines = [SeminarContentAreaInlineAdmin]
    filter_horizontal = ["subjects"]
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "title",
                    "status",
                    ("publish_date", "expiry_date"),
                    "length",
                    "price",
                    "subjects",
                ]
            },
        ),
        (
            "Public Content",
            {
                "classes": ["collapse-closed"],
                "fields": ["public_video_link", "content"],
            },
        ),
        (
            "Private Content",
            {
                "classes": ["collapse-closed"],
                "fields": ["private_video_link", "private_content"],
            },
        ),
        # Copy the meta panel from PageAdmin
        deepcopy(DisplayableAdmin.fieldsets[1]),
    ]
