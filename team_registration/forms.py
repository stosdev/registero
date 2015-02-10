from django.forms import ModelForm, Textarea
from localflavor.pl.forms import PLNIPField
from models import Participant, CoachProfile

from django.utils.translation import ugettext as _


class CoachProfileModelForm(ModelForm):
    institute_nip = PLNIPField(label=_("Institutes NIP"), required=False)
    institute_nip.help_text = _("The institutes NIP number.")

    class Meta:
        model = CoachProfile
        fields = ('institute_name', 'accomodation_required',
                  'institute_address', 'institute_nip', 'comment')
        widgets = {
            'institute_address': Textarea(attrs={'cols': 30, 'rows': 3}),
        }

class ParticipantModelForm(ModelForm):

    class Meta:
        model = Participant
        fields = ('first_name', 'last_name', 'shirt_size',)
