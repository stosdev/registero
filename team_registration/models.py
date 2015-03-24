# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from django.utils import timezone

from django.contrib.auth.models import User

from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError

from django.db import models

from solo.models import SingletonModel

from datetime import timedelta


def days_from_now(n):
    def fun():
        return timezone.now() + timedelta(days=n)
    return fun


class TeamRegistrationConfiguration(SingletonModel):
    """Class for storing global registration configuration."""

    enabled = models.BooleanField(_("Team registration enabled"),
                                  default=False)
    enabled.help_text = _("If set to false the team registration is disabled,\
                          now matter the start and end settings below.")
    registration_start = models.DateTimeField(_("Team registration start"),
                                              default=timezone.now)
    registration_freeze = models.DataTimeField(_("Team registration freeze start"),
                                               default=days_from_now(25))
    registration_freeze.help_text = _("After team freeze the team participants \
                                      cannot be changed, but the teams can \
                                      still be reordered")
    registration_end = models.DateTimeField(_("Team registration end"),
                                            default=days_from_now(30))

    @property
    def registration_active(self):
        """Return true if registration is active."""
        return self.enabled and self.start <= timezone.now() \
            and timezone.now() <= self.end

    @property
    def registration_not_started(self):
        """Return true if the registration is yet to start."""
        return self.enabled and timezone.now() <= self.start

    @property
    def registration_has_ended(self):
        """Return true if the registration has ended."""
        return self.enabled and self.end <= timezone.now()

    @property
    def registration_is_freezed(self):
        return self.registration_start <= self.team_freeze \
            and timezone.now() > self.team_freeze

    def clean(self):
        if not self.registration_start <= self.registration_freeze or \
           not self.registration_freeze <= self.registration_end:
            raise ValidationError({
                'registration_freeze': _(
                    "The team registration freeze time \
                    should be between the registration start and end date.")
            })
        return super(TeamRegistrationConfiguration, self).clean()

    class Meta:
        verbose_name = _("Team registration configuration")

    def __unicode__(self):
        return u"Team Registration configuration"


class CoachProfile(models.Model):
    """The team coaches profile which has details about the teams origin."""

    UNIVERSITY = 'u'
    SCHOOL = 's'

    INSTITUTE_TYPES = (
        (UNIVERSITY, _("University")),
        (SCHOOL, _("School")),
    )

    user = models.OneToOneField(User, related_name='coach_profile')
    institute_name = models.CharField(_("Institute name"), max_length=255)
    institute_name.help_text = _(
        "The name of the school/university providing teams for this coach.")
    institute_type = models.CharField(_("Institute type"), max_length=1,
                                      choices=INSTITUTE_TYPES)
    accomodation_required = models.BooleanField(_("Accomodation required"),
                                                default=False)
    accomodation_required.help_text = _(
        "Check if teams require finding a place to sleep.")
    institute_address = models.TextField(_("Institute address"),
                                         blank=True, null=True)
    institute_address.help_text = _(
        "The address of the institute provided above.")
    institute_nip = models.CharField(_("Institutes NIP"), max_length=10,
                                     blank=True, null=True)
    institute_nip.help_text = _(
        "The institutes NIP number used for the accomodation invoice.")
    comment = models.TextField(_("Comment"), blank=True, null=True)
    comment.help_text = _("Share any additional comments on your teams.")

    class Meta:
        verbose_name = _("Coach Profile")
        verbose_name_plural = _("Coach Profiles")

    def _participant_count(self):
        q = self.user.teams.aggregate(count=models.Count('participants'))
        return q['count']
    _participant_count.short_description = _("Number of participants")
    participant_count = property(_participant_count)

    def _valid_team_count(self):
        count = 0
        for team in self.user.teams.all():
            if team.participant_count >= 2:
                count += 1
                return count
    _valid_team_count.short_description = _("Number of valid teams")
    valid_team_count = property(_valid_team_count)

    def get_absolute_url(self):
        return reverse('team.views.management', args=())

    def __unicode__(self):
        return u'{} {}'.format(self.user, self.institute_name)


class Team(models.Model):
    """A model representing the team."""

    order = models.IntegerField(_("Order"))
    coach = models.ForeignKey(User, verbose_name=_("Coach"),
                              related_name='teams')
    selected = models.BooleanField(_("Selected"), default=False)
    selected.help_text = _("Mark true if the team is selected for the contest.")

    class Meta:
        verbose_name = _("Team")
        verbose_name_plural = _("Teams")
        ordering = ('order', )

    def _participant_count(self):
        return self.participants.count()
    _participant_count.short_description = _("Number of participants")
    participant_count = property(_participant_count)

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

    def get_absolute_url(self):
        return reverse('team.views.management', args=())

    def __unicode__(self):
        return u'{} {}'.format(self.first_name, self.last_name)
