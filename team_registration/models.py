from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from django.db import models


class CoachProfile(models.Model):
    """The team coaches profile which has details about the teams origin."""

    user = models.OneToOneField(User)
    institute_name = models.CharField(_("Insititute name"), max_length=255)
    institute_name.help_text = _(
        "The name of the school/university providing teams for this coach.")

    class Meta:
        verbose_name = _("Coach Profile")
        verbose_name_plural = _("Coach Profiles")

    def get_absolute_url(self):
        return reverse('team.views.management', args=())

    def __unicode__(self):
        return u'{} {}'.format(self.user, self.institute_name)


class Team(models.Model):
    """Team model consisting of the importance of this team for the given
    coach (order), and a foreign key to the coach model."""

    order = models.IntegerField(_("Order"))
    coach = models.ForeignKey(User, verbose_name=_("Coach"),
                              related_name='teams')

    class Meta:
        verbose_name = _("Team")
        verbose_name_plural = _("Teams")

    def __unicode__(self):
        return u'Team {} for {}'.format(self.order, self.coach)


class Participant(models.Model):
    """The participant model, each participant has a name and a
    shirt size and belongs to a given team."""

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
        return u'{} {}'.format(self.first_name, self.last_name)