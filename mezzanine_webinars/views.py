from __future__ import unicode_literals, absolute_import

from django.views.generic import DetailView

from .models import Seminar


class SeminarDetailView(DetailView):
    template_name = "seminars/seminar_detail.html"
    context_object_name = "seminar"

    def get_queryset(self):
        return Seminar.objects.published(for_user=self.request.user)
