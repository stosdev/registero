from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from models import CoachProfile, Team, Participant


@admin.register(CoachProfile)
class CoachProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Team)
class TeamAdmin(GuardedModelAdmin):
    search_fields = ('participants__first_name',
                     'participants__last_name')


@admin.register(Participant)
class ParticipantAdmin(GuardedModelAdmin):
    list_display = ('first_name', 'last_name')
    list_display_links = list_display
    search_fields = list_display
