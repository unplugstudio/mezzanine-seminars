from __future__ import unicode_literals, absolute_import

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible

from mezzanine.conf import settings
from mezzanine.core.fields import FileField
from mezzanine.core.models import Displayable, Slugged, RichText, TimeStamped

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

    class Meta:
        ordering = ["-featured", "-publish_date"]

    def get_absolute_url(self):
        return reverse("seminars:detail", args=[self.slug])

    def get_price_display(self):
        if self.price == 0:
            return "Free"
        return "${:,.2f}".format(self.price)

    def get_length_display(self):
        if self.length is None:
            return "N/A"
        return "{} min.".format(self.length)

    def get_subjects_display(self):
        string = ", ".join(self.subjects.values_list("title", flat=True))
        return string or "Uncategorized"


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


@python_2_unicode_compatible
class SeminarRegistration(TimeStamped):
    """
    A record of a user paying and registering for a Seminar
    """

    purchaser = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="seminar_registrations",
    )
    seminar = models.ForeignKey(
        Seminar, on_delete=models.CASCADE, related_name="registrations"
    )

    price = models.DecimalField("Price", max_digits=8, decimal_places=2, default=0)
    payment_method = models.CharField("Payment method", max_length=100)
    transaction_id = models.CharField("Transaction ID", max_length=100, blank=True)
    transaction_notes = models.TextField("Transaction notes", blank=True)

    class Meta:
        unique_together = ("purchaser", "seminar")

    def __str__(self):
        return self.purchaser.get_full_name() or self.purchaser.username
