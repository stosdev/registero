from django.forms import ModelForm

from models import Participant, CoachProfile


class CoachProfileModelForm(ModelForm):

    class Meta:
        model = CoachProfile
        fields = ('institute_name', )


class ParticipantModelForm(ModelForm):

    class Meta:
        model = Participant
        fields = ('first_name', 'last_name', 'shirt_size',)
