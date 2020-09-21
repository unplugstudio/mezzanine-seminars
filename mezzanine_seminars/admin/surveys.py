from __future__ import unicode_literals, absolute_import


from django.contrib import admin

from mezzanine.core.admin import TabularDynamicInlineAdmin

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
