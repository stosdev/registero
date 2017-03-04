# -*- coding: utf-8 -*-
from django.forms import ModelForm, Textarea, ValidationError
from localflavor.pl.forms import PLNIPField
from .models import Team, Participant, CoachProfile
from django.shortcuts import get_object_or_404

from django.utils.translation import ugettext as _


class CoachProfileModelForm(ModelForm):
    institute_nip = PLNIPField(label=_("Institutes NIP"), required=False)
    institute_nip.help_text = _(
        "The institutes NIP number used for the accomodation invoice.")

    class Meta:
        model = CoachProfile
        fields = ('institute_name', 'institute_type', 'accomodation_required',
                  'institute_address', 'institute_nip', 'comment')
        widgets = {
            'institute_address': Textarea(attrs={'cols': 30, 'rows': 3}),
            'comment': Textarea(attrs={'cols': 30, 'rows': 2}),
        }


class ParticipantModelForm(ModelForm):

    def __init__(self, *args, **kwargs):
        self.team_pk = kwargs.pop('team_pk')
        super(ParticipantModelForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Participant
        fields = ('first_name', 'last_name', 'shirt_size',)

    def clean(self):
        team = get_object_or_404(Team, pk=self.team_pk)
        if team.participant_count > 2:
            raise ValidationError(_("Too many participants on this team."))
        return super(ParticipantModelForm, self).clean()
