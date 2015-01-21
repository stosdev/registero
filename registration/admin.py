from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from models import Team, Participant


@admin.register(Team)
class TeamAdmin(GuardedModelAdmin):
    list_display = ('name', )
    search_fields = ('name', 'participants__first_name',
                     'participants__last_name')


@admin.register(Participant)
class ParticipantAdmin(GuardedModelAdmin):
    list_display = ('first_name', 'last_name')
    list_display_links = list_display
    search_fields = list_display
