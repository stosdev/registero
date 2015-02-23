#-*- coding: utf-8 -*-
from django.views.generic.edit import FormView, CreateView, DeleteView, \
    UpdateView
from django.views.generic.base import RedirectView
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from models import Team, Participant
from forms import CoachProfileModelForm, ParticipantModelForm
import json


class ParticipantCreateView(CreateView):
    form_class = ParticipantModelForm
    template_name = 'team_registration/participant_form.html'
    success_url = reverse_lazy('team.views.management')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ParticipantCreateView, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(ParticipantCreateView, self).get_form_kwargs()
        kwargs.update({'team_pk': self.kwargs.get('team_pk')})
        return kwargs

    def form_valid(self, form):
        team = get_object_or_404(Team, pk=self.kwargs.get('team_pk'))

        if team.coach != self.request.user:
            raise PermissionDenied()

        form.instance.team = team

        return super(ParticipantCreateView, self).form_valid(form)


class ParticipantDeleteView(DeleteView):
    model = Participant
    success_url = reverse_lazy('team.views.management')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ParticipantDeleteView, self).dispatch(*args, **kwargs)

    def get_object(self):
        participant = super(ParticipantDeleteView, self).get_object()

        if participant.team.coach != self.request.user:
            raise PermissionDenied()

        return participant


class ParticipantUpdateView(UpdateView):
    model = Participant
    template_name = 'team_registration/participant_update_form.html'
    fields = ('first_name', 'last_name', 'shirt_size')
    success_url = reverse_lazy('team.views.management')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ParticipantUpdateView, self).dispatch(*args, **kwargs)

    def get_object(self):
        participant = super(ParticipantUpdateView, self).get_object()

        if participant.team.coach != self.request.user:
            raise PermissionDenied()

        return participant


class TeamCreateView(RedirectView):
    pattern_name = 'team.views.management'
    permanent = False

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TeamCreateView, self).dispatch(*args, **kwargs)

    def get(self, *args, **kwargs):
        user = self.request.user
        teams = user.teams.order_by('-order')
        if len(teams) > 0:
            order = teams[0].order + 1
        else:
            order = 1
        team = Team(coach=user, order=order)
        team.save()
        return super(TeamCreateView, self).get(*args, **kwargs)


class TeamManagementView(FormView):
    template_name = 'team_registration/team_management.html'
    form_class = CoachProfileModelForm
    success_url = reverse_lazy('team.views.management')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TeamManagementView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(TeamManagementView,
                        self).get_context_data(*args, **kwargs)
        context['team_list'] = self.request.user.teams.all()
        return context

    def get_initial(self, *args, **kwargs):
        initial = super(TeamManagementView, self).get_initial(*args, **kwargs)
        try:
            coach_profile = self.request.user.coach_profile
            initial.update({
                'institute_name': coach_profile.institute_name,
                'institute_type': coach_profile.institute_type,
                'institute_address': coach_profile.institute_address,
                'accomodation_required': coach_profile.accomodation_required,
                'institute_nip': coach_profile.institute_nip,
                'comment': coach_profile.comment,
            })
        except ObjectDoesNotExist:
            pass
        return initial

    def form_valid(self, form):
        user = self.request.user
        res = form.save(commit=False)
        try:
            user.coach_profile.institute_name = res.institute_name
            user.coach_profile.institute_type = res.institute_type
            user.coach_profile.comment = res.comment
            user.coach_profile.accomodation_required = \
                res.accomodation_required
            if res.accomodation_required:
                user.coach_profile.institute_address = res.institute_address
                user.coach_profile.institute_nip = res.institute_nip
            else:
                user.coach_profile.institute_address = ''
                user.coach_profile.institute_nip = ''
        except ObjectDoesNotExist:
            user.coach_profile = res
        user.coach_profile.save()
        return super(TeamManagementView, self).form_valid(form)


class TeamDeleteView(DeleteView):
    model = Team
    success_url = reverse_lazy('team.views.management')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TeamDeleteView, self).dispatch(*args, **kwargs)

    def get_object(self):
        team = super(TeamDeleteView, self).get_object()

        if team.coach != self.request.user:
            raise PermissionDenied()

        return team

    def delete(self, request, *args, **kwargs):
        response = super(TeamDeleteView, self).delete(request, *args, **kwargs)

        teams = Team.objects.filter(coach=request.user).order_by('order')
        for team, order in zip(teams, xrange(1, len(teams) + 1)):
            team.order = order
            team.save()

        return response


class TeamReorderView(View):

    def post(self, request):
        try:
            data = json.loads(request.POST['data'])
        except:
            return HttpResponse(status=400)

        teams = Team.objects.filter(coach=request.user)

        for ordering in data:
            try:
                team = teams.get(pk=int(ordering['id']))
                team.order = int(ordering['order'])
                team.save()
            except:
                raise PermissionDenied()

        return HttpResponse()
