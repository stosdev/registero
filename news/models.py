from django.utils.translation import ugettext as _, pgettext_lazy
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone


class News(models.Model):
    """The news model consisting of a title and content."""

    title = models.CharField(_("Title"), max_length=255)
    content = models.TextField(_("Content"))
    timestamp = models.DateTimeField(_("Timestamp"), default=timezone.now)
    site = models.ForeignKey(Site, verbose_name=_("Site"))
    on_site = CurrentSiteManager()

    class Meta:
        verbose_name = _("News")
        verbose_name_plural = pgettext_lazy("Plural", "News")
        ordering = ('-timestamp', )

    def get_absolute_url(self):
        return reverse('news.views.detail', args=[str(self.id), ])

    def __unicode__(self):
        return "{} {} {}".format(self.id, self.title, self.timestamp)
