# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_str
from django.contrib import admin
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response

from models import TeamRegistrationConfiguration, CoachProfile, Team,\
    Participant

from solo.admin import SingletonModelAdmin

import csv


def export_teams_cvs(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=teams.csv'
    writer = csv.writer(response)
    writer.writerow([
        smart_str(unicode(_("Institute name"))),
        smart_str(unicode(_("Institute type"))),
        smart_str(unicode(_("Accomodation required"))),
        smart_str(unicode(_("Coach"))),
        smart_str(unicode(_("Team order"))),
        smart_str(unicode(_("First name"))),
        smart_str(unicode(_("Last name"))),
        smart_str(unicode(_("Shirt size"))),
    ])
    for team in queryset.all():
        for participant in team.participants.all():

            try:
                coach_profile = team.coach.coach_profile
            except ObjectDoesNotExist:
                continue

            if coach_profile.accomodation_required:
                accomodation_required = unicode(_("Yes"))
            else:
                accomodation_required = unicode(_("No"))

            writer.writerow([
                smart_str(coach_profile.institute_name),
                smart_str(coach_profile.get_institute_type_display()),
                smart_str(accomodation_required),
                smart_str(coach_profile.user),
                smart_str(team.order),
                smart_str(participant.first_name),
                smart_str(participant.last_name),
                smart_str(participant.shirt_size)
            ])
    return response
export_teams_cvs.short_description = _("Export teams to csv")


def get_coach_profiles_for_teams(queryset):
    coach_profiles = []
    for team in queryset.all():
        try:
            coach_profile = team.coach.coach_profile
        except ObjectDoesNotExist:
            continue
        if coach_profile not in coach_profiles:
            coach_profiles.append(coach_profile)
    return coach_profiles


def export_teams_html(modeladmin, request, queryset):
    coach_profiles = get_coach_profiles_for_teams(queryset)
    response = render_to_response('team_registration/coach_profiles.html',
                                  {'coach_profiles': coach_profiles},
                                  content_type='text/html')
    response['Content-Disposition'] = 'attachment; filename=teams.html'
    return response
export_teams_html.short_description = _("Export teams to html")


def export_institutes(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=institutes.csv'
    writer = csv.writer(response)
    writer.writerow([
        smart_str(unicode(_("Institute name"))),
        smart_str(unicode(_("Institute type"))),
        smart_str(unicode(_("Number of valid teams"))),
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
            smart_str(profile.valid_team_count),
            smart_str(profile.participant_count),
            smart_str(accomodation_required),
            smart_str(profile.institute_address.replace('\r\n', ' ')),
            smart_str(profile.institute_nip),
            smart_str(profile.comment.replace('\r\n', ' '))
        ])
    return response
export_institutes.short_description = _("Export institute data to csv")


@admin.register(TeamRegistrationConfiguration)
class TeamRegistrationConfigurationAdmin(SingletonModelAdmin):
    pass


@admin.register(CoachProfile)
class CoachProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('user', 'institute_name', 'institute_type',
                       'accomodation_required'),
        }),
        (_("Additional info"), {
            'classes': ('collapse',),
            'fields': ('institute_address', 'institute_nip', 'comment'),
        }),
    )
    list_display = ('user', 'institute_name', '_valid_team_count',
                    '_approved_team_count', 'accomodation_required')
    actions = [export_institutes, ]


class ParticipantInline(admin.TabularInline):
    model = Participant
    extra = 3


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('coach', 'order', 'participant_count', 'approved')
    search_fields = ('participants__first_name',
                     'participants__last_name')
    inlines = [ParticipantInline, ]
    actions = [export_teams_cvs, export_teams_html]


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (('first_name', 'last_name'), 'shirt_size'),
        }),
    )
    list_display = ('first_name', 'last_name', 'team', 'shirt_size')
    list_display_links = ('first_name', 'last_name')
    search_fields = list_display
