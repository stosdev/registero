from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone


class News(models.Model):
    title = models.CharField(_("Title"), max_length=255)
    content = models.TextField(_("Content"))
    timestamp = models.DateTimeField(_("Timestamp"), default=timezone.now)

    class Meta:
        verbose_name = _("News")
        verbose_name_plural = _("News")
        ordering = ('-timestamp', )

    def get_absolute_url(self):
        return reverse('news.views.detail', args=[str(self.id), ])

    def __unicode__(self):
        return "{} {} {}".format(self.id, self.title, self.timestamp)
