from __future__ import unicode_literals, absolute_import

from django.views import generic

from mezzanine.conf import settings
from mezzanine.utils.views import paginate

from .models import Seminar


class SeminarDetailView(generic.DetailView):
    template_name = "seminars/seminar_detail.html"
    context_object_name = "seminar"

    def get_queryset(self):
        return Seminar.objects.published(for_user=self.request.user)


class SeminarListView(generic.TemplateView):
    template_name = "seminars/seminar_list.html"

    def get_queryset(self):
        qs = Seminar.objects.published(for_user=self.request.user)
        if self.request.GET.get("q"):
            qs = qs.search(self.request.GET["q"])
        return qs

    def get_context_data(self, **kwargs):
        kwargs.update(
            {
                "seminars": paginate(
                    objects=self.get_queryset(),
                    page_num=self.request.GET.get("page", 1),
                    per_page=settings.BLOG_POST_PER_PAGE,
                    max_paging_links=10,
                )
            }
        )
        return super(SeminarListView, self).get_context_data(**kwargs)
