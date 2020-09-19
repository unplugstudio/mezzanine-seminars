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

from .models import Seminar


class SeminarDetailView(generic.DetailView):
    template_name = "seminars/seminar_detail.html"
    context_object_name = "seminar"

    def get_queryset(self):
        return Seminar.objects.published()


@method_decorator(login_required, "dispatch")
class SeminarRegistrationCreate(generic.CreateView):
    """
    Let's users pay and register for a seminar.
    """

    template_name = "seminars/registration_create.html"

    @cached_property
    def seminar(self):
        return get_object_or_404(
            Seminar.objects.published(),
            slug=self.kwargs.get("slug"),
        )

    def dispatch(self, request, *args, **kwargs):
        if self.seminar.registrations.filter(purchaser=request.user).exists():
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
        return import_dotted_path(settings.SEMINARS_REGISTRATION_FORM)

    def get_form_kwargs(self):
        kwargs = super(SeminarRegistrationCreate, self).get_form_kwargs()
        kwargs.update({"seminar": self.seminar, "purchaser": self.request.user})
        return kwargs

    def get_context_data(self, **kwargs):
        kwargs.update({"seminar": self.seminar})
        return super(SeminarRegistrationCreate, self).get_context_data(**kwargs)

    def get_success_url(self):
        """
        Redirect back to the seminar with full access now granted
        """
        messages.success(
            self.request,
            "You are now registered for this seminar",
            fail_silently=True,
        )
        if self.success_url:  # Proceed as usual if a URL has been set
            return super(SeminarRegistrationCreate, self).get_success_url()
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
                    per_page=settings.BLOG_POST_PER_PAGE,
                    max_paging_links=settings.MAX_PAGING_LINKS,
                )
            }
        )
        return super(SeminarListView, self).get_context_data(**kwargs)
