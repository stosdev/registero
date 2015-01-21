from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from django.db import models


class Team(models.Model):
    order = models.IntegerField(_("Order"))
    name = models.CharField(_("Insititute name"), max_length=255) # TODO: Move to couch user profile
    name.help_text = _("The name of the school/university \
                       providing this team.")
    couch = models.ForeignKey(User, verbose_name=_("Couch"),
                              related_name='teams')

    class Meta:
        verbose_name = _("Team")
        verbose_name_plural = _("Teams")

    def __unicode__(self):
        return u'{}'.format(self.name)


class Participant(models.Model):
    first_name = models.CharField(_("First name"), max_length=255)
    last_name = models.CharField(_("Last name"), max_length=255)
    team = models.ForeignKey(Team, verbose_name=_("Team"),
                             related_name='participants')

    class Meta:
        verbose_name = _("Participant")
        verbose_name_plural = _("Participants")

    def __unicode__(self):
        return u'{} {}'.format(self.firstname, self.lastname)
