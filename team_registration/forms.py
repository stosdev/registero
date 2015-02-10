from django.forms import ModelForm

from models import Participant, UserProfile


class UserProfileModelForm(ModelForm):

    class Meta:
        model = UserProfile
        fields = ('institute_name', )


class ParticipantModelForm(ModelForm):

    class Meta:
        model = Participant
        fields = ('first_name', 'last_name', 'shirt_size',)
