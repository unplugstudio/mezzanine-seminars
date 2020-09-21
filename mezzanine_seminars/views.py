from __future__ import unicode_literals, absolute_import

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import generic
from django.shortcuts import get_object_or_404, redirect
from django.utils.functional import cached_property

from mezzanine.conf import settings
from mezzanine.utils.views import paginate
from mezzanine.utils.importing import import_dotted_path

from mezzy.utils.decorators import method_decorator

from .models import Seminar, SeminarRegistration, SurveyResponse


class SeminarDetailMixin(object):
    """
    Base class for any view related to a single seminar
    """

    @cached_property
    def seminar(self):
        return get_object_or_404(
            Seminar.objects.published(),
            slug=self.kwargs.get("slug"),
        )

    @cached_property
    def registration(self):
        try:
            return SeminarRegistration.objects.get(
                seminar=self.seminar, purchaser=self.request.user
            )
        except (SeminarRegistration.DoesNotExist, TypeError):
            # User not registered or not logged in
            return None

    @cached_property
    def survey_response(self):
        if self.registration is None:
            return None
        try:
            return SurveyResponse.objects.get(registration=self.registration)
        except SurveyResponse.DoesNotExist:
            return None

    def get_context_data(self, **kwargs):
        kwargs.update(
            {
                "seminar": self.seminar,
                "registration": self.registration,
                "survey_response": self.survey_response,
            }
        )
        return super(SeminarDetailMixin, self).get_context_data(**kwargs)


class SeminarDetailView(SeminarDetailMixin, generic.TemplateView):
    """
    Shows seminar details to registered and non-registered users
    """

    template_name = "seminars/seminar_detail.html"


@method_decorator(login_required, "dispatch")
class SeminarRegistrationCreate(SeminarDetailMixin, generic.CreateView):
    """
    Let's users pay and register for a seminar.
    """

    template_name = "seminars/registration_create.html"

    def dispatch(self, request, *args, **kwargs):
        if self.registration:
            messages.info(
                request,
                "You are already registered for this seminar",
                fail_silently=True,
            )
            return redirect(self.seminar)
        return super(SeminarRegistrationCreate, self).dispatch(request, *args, **kwargs)

    def get_form_class(self):
        """
        Import the registration form from settings.
        Allows swapping out payment processors by swapping the form.
        """
        if self.form_class:  # Respect the class attribute override
            return self.form_class
        return import_dotted_path(settings.SEMINARS_REGISTRATION_FORM)

    def get_form_kwargs(self):
        kwargs = super(SeminarRegistrationCreate, self).get_form_kwargs()
        kwargs.update({"seminar": self.seminar, "purchaser": self.request.user})
        return kwargs

    def get_success_url(self):
        """
        Redirect back to the seminar with full access now granted
        """
        messages.success(
            self.request,
            "You are now registered for this seminar",
            fail_silently=True,
        )
        if self.success_url:  # Respect the class attribute override
            return super(SeminarRegistrationCreate, self).get_success_url()
        return self.seminar.get_absolute_url()


@method_decorator(login_required, "dispatch")
class SurveyResponseCreate(SeminarDetailMixin, generic.CreateView):
    """
    Let's users answer the survey for seminars they are registered in
    """

    template_name = "seminars/survey_response_create.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.registration:
            messages.info(
                request,
                "Please register for this seminar before answering the survey",
                fail_silently=True,
            )
            return redirect(self.seminar)
        if self.survey_response:
            messages.info(
                request,
                "You already completed the survey for this seminar",
                fail_silently=True,
            )
            return redirect(self.seminar)
        return super(SurveyResponseCreate, self).dispatch(request, *args, **kwargs)

    def get_form_class(self):
        """
        Import the survey form from settings for easy swapping.
        """
        if self.form_class:  # Respect the class attribute override
            return self.form_class
        return import_dotted_path(settings.SEMINARS_SURVEY_FORM)

    def get_form_kwargs(self):
        kwargs = super(SurveyResponseCreate, self).get_form_kwargs()
        kwargs.update({"registration": self.registration})
        return kwargs

    def get_success_url(self):
        messages.success(
            self.request,
            "Your survey response has been submitted.",
            fail_silently=True,
        )
        if self.success_url:  # Respect the class attribute override
            return super(SurveyResponseCreate, self).get_success_url()
        return self.seminar.get_absolute_url()


class SeminarListView(generic.TemplateView):
    template_name = "seminars/seminar_list.html"
    template_name_ajax = "seminars/includes/seminar_list_ajax.html"

    def get_queryset(self):
        qs = Seminar.objects.published()
        if self.request.GET.get("q"):
            qs = qs.search(self.request.GET["q"])
        return qs

    def get_template_names(self):
        """
        Load a different template for AJAX requests
        """
        templates = super(SeminarListView, self).get_template_names()
        if self.request.is_ajax():
            templates.insert(0, self.template_name_ajax)
        return templates

    def get_context_data(self, **kwargs):
        kwargs.update(
            {
                "seminars": paginate(
                    objects=self.get_queryset(),
                    page_num=self.request.GET.get("page", 1),
                    per_page=settings.SEMINARS_PER_PAGE,
                    max_paging_links=settings.MAX_PAGING_LINKS,
                )
            }
        )
        return super(SeminarListView, self).get_context_data(**kwargs)
