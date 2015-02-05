from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    accepted_requlations = models.BooleanField(
        _("Accepted contest regulations"), default=False)
    institute_name = models.CharField(_("Insititute name"), max_length=255)
    institute_name.help_text = _("The name of the school/university \
                       providing this team.")


class Team(models.Model):
    order = models.IntegerField(_("Order"))
    couch = models.ForeignKey(User, verbose_name=_("Couch"),
                              related_name='teams')

    class Meta:
        verbose_name = _("Team")
        verbose_name_plural = _("Teams")

    def __unicode__(self):
        return u'Team {} for {}'.format(self.order, self.couch)


class Participant(models.Model):

    EXTRA_SMALL = 'XS'
    SMALL = 'S'
    MEDIUM = 'M'
    LARGE = 'L'
    EXTRA_LARGE = 'XL'

    SHIRT_SIZES = (
        (EXTRA_SMALL, _("Extra small")),
        (SMALL, _("Small")),
        (MEDIUM, _("Medium")),
        (LARGE, _("Large")),
        (EXTRA_LARGE, _("Extra large"))
    )

    first_name = models.CharField(_("First name"), max_length=255)
    last_name = models.CharField(_("Last name"), max_length=255)
    team = models.ForeignKey(Team, verbose_name=_("Team"),
                             related_name='participants')
    shirt_size = models.CharField(_("Shirt size"), max_length=2,
                                  choices=SHIRT_SIZES, default=MEDIUM)

    class Meta:
        verbose_name = _("Participant")
        verbose_name_plural = _("Participants")

    def __unicode__(self):
        return u'{} {}'.format(self.firstname, self.lastname)
