from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from django.db import models


class Team(models.Model):
    name = models.CharField(_("Insititute name"), max_length=255)
    name.help_text = _("The name of the school/university \
                       providing this team.")
    couch = models.ForeignKey(User, verbose_name=_("Couch"))

    class Meta:
        verbose_name = _("Team")
        verbose_name_plural = _("Teams")


class Participant(models.Model):
    firstname = models.CharField(_("First name"), max_length=255)
    lastname = models.CharField(_("Last name"), max_length=255)
    team = models.ForeignKey(Team, verbose_name=_("Team"))

    class Meta:
        verbose_name = _("Participant")
        verbose_name_plural = _("Participants")
