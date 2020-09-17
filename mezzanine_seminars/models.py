from __future__ import unicode_literals, absolute_import

from django.db import models
from django.core.urlresolvers import reverse

from mezzanine.core.fields import FileField
from mezzanine.core.models import Displayable, Slugged, RichText

from mezzy.utils.models import TitledInline


class SeminarSubject(Slugged):
    """
    A subject to group seminars
    """


class Seminar(Displayable, RichText):
    """
    Main content model that holds all the information about a seminar
    """

    featured_image = FileField(
        "Featured image", format="Image", blank=True, upload_to="seminars"
    )
    featured = models.BooleanField(
        "Featured", default=False, help_text="Highlight this item above others"
    )
    subjects = models.ManyToManyField(
        SeminarSubject, related_name="seminars", blank=True
    )
    length = models.PositiveIntegerField(
        "Length", blank=True, null=True, help_text="Seminar duration in minutes"
    )
    price = models.DecimalField("Price", max_digits=8, decimal_places=2, default=0)
    preview_video_link = models.URLField(
        "Preview Video Link",
        max_length=200,
        blank=True,
        help_text="Publicly-accessible teaser or preview",
    )

    def get_absolute_url(self):
        return reverse("seminars:detail", args=[self.slug])

    def format_price(self):
        if self.price == 0:
            return "Free"
        return "${:,.2f}".format(self.price)

    class Meta:
        ordering = ["-featured", "-publish_date"]


class SeminarContentArea(TitledInline, RichText):
    """
    An additional content area for a seminar
    """

    seminar = models.ForeignKey(
        Seminar, on_delete=models.CASCADE, related_name="content_areas"
    )
    video_link = models.URLField(
        "Video Link",
        max_length=200,
        blank=True,
    )

    class Meta:
        verbose_name = "content area"
        verbose_name_plural = "content areas"
