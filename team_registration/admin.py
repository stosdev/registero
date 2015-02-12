from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_str
from django.contrib import admin
from django.http import HttpResponse

from guardian.admin import GuardedModelAdmin

from models import CoachProfile, Team, Participant

import csv


def export_teams(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=teams.csv'
    writer = csv.writer(response)
    writer.writerow([
        smart_str(unicode(_("Institute name"))),
        smart_str(unicode(_("Institute type"))),
        smart_str(unicode(_("Accomodation required"))),
        smart_str(unicode(_("Team order"))),
        smart_str(unicode(_("First name"))),
        smart_str(unicode(_("Last name"))),
        smart_str(unicode(_("Shirt size"))),
    ])
    for team in queryset.all():
        for participant in team.participants.all():
            coach_profile = team.coach.coach_profile

            if coach_profile.accomodation_required:
                accomodation_required = unicode(_("Yes"))
            else:
                accomodation_required = unicode(_("No"))

            writer.writerow([
                smart_str(coach_profile.institute_name),
                smart_str(coach_profile.get_institute_type_display()),
                smart_str(accomodation_required),
                smart_str(team.order),
                smart_str(participant.first_name),
                smart_str(participant.last_name),
                smart_str(participant.shirt_size)
            ])
    return response
export_teams.short_description = _("Export teams to csv")


def export_institutes(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=institutes.csv'
    writer = csv.writer(response)
    writer.writerow([
        smart_str(unicode(_("Institute name"))),
        smart_str(unicode(_("Institute type"))),
        smart_str(unicode(_("Number of teams"))),
        smart_str(unicode(_("Number of participants"))),
        smart_str(unicode(_("Accomodation required"))),
        smart_str(unicode(_("Institute address"))),
        smart_str(unicode(_("Institutes NIP"))),
        smart_str(unicode(_("Comment"))),
    ])
    for profile in queryset.all():
        if profile.accomodation_required:
            accomodation_required = unicode(_("Yes"))
        else:
            accomodation_required = unicode(_("No"))

        writer.writerow([
            smart_str(profile.institute_name),
            smart_str(profile.get_institute_type_display()),
            smart_str(profile.user.teams.count()),
            smart_str(profile.participant_count),
            smart_str(accomodation_required),
            smart_str(profile.institute_address),
            smart_str(profile.institute_nip),
            smart_str(profile.comment)
        ])
    return response
export_institutes.short_description = _("Export institute data to csv")


@admin.register(CoachProfile)
class CoachProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('institute_name', 'institute_type',
                       'accomodation_required'),
        }),
        (_("Additional info"), {
            'classes': ('collapse',),
            'fields': ('institute_address', 'institute_nip', 'comment'),
        }),
    )
    list_display = ('user', 'institute_name', 'accomodation_required')
    actions = [export_institutes, ]


class ParticipantInline(admin.TabularInline):
    model = Participant
    extra = 3


@admin.register(Team)
class TeamAdmin(GuardedModelAdmin):
    list_display = ('coach', 'order', 'participant_count')
    search_fields = ('participants__first_name',
                     'participants__last_name')
    inlines = [ParticipantInline, ]
    actions = [export_teams, ]


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
