from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_str
from django.contrib import admin
from django.http import HttpResponse

from guardian.admin import GuardedModelAdmin

from models import CoachProfile, Team, Participant

import csv


def export(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=teams.csv'
    writer = csv.writer(response)
    writer.writerow([
        smart_str(unicode(_("Institute name"))),
        smart_str(unicode(_("Team order"))),
        smart_str(unicode(_("First name"))),
        smart_str(unicode(_("Last name"))),
        smart_str(unicode(_("Shirt size")))
    ])
    for team in queryset.all():
        for participant in team.participants.all():
            writer.writerow([
                smart_str(team.coach.coach_profile.institute_name),
                smart_str(team.order),
                smart_str(participant.first_name),
                smart_str(participant.last_name),
                smart_str(participant.shirt_size)
            ])
    return response
export.short_description = _("Export teams to csv")


@admin.register(CoachProfile)
class CoachProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('institute_name', 'accomodation_required'),
        }),
        (_("Additional info"), {
            'classes': ('collapse',),
            'fields': ('institute_address', 'institute_nip', 'comment'),
        }),
    )
    list_display = ('user', 'institute_name', 'accomodation_required')


class ParticipantInline(admin.TabularInline):
    model = Participant
    extra = 3


@admin.register(Team)
class TeamAdmin(GuardedModelAdmin):
    list_display = ('coach', 'order', 'participants_number')
    search_fields = ('participants__first_name',
                     'participants__last_name')
    inlines = [ParticipantInline, ]
    actions = [export, ]


@admin.register(Participant)
class ParticipantAdmin(GuardedModelAdmin):
    fieldsets = (
        (None, {
            'fields': (('first_name', 'last_name'), 'shirt_size'),
        }),
    )
    list_display = ('first_name', 'last_name', 'team', 'shirt_size')
    list_display_links = ('first_name', 'last_name')
    search_fields = list_display
