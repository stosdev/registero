from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from models import UserProfile, Team
from forms import UserProfileModelForm, ParticipantModelForm


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
        team = Team(couch=user, order=order)
        team.save()
        return super(TeamCreateView, self).get(*args, **kwargs)


class TeamManagementView(TemplateView):
    template_name = 'team_registration/team_management.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TeamManagementView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(TeamManagementView,
                        self).get_context_data(*args, **kwargs)

        user = self.request.user
        try:
            context['userprofile_form'] = UserProfileModelForm(
                instance=user.userprofile
            )
        except ObjectDoesNotExist:
            context['userprofile_form'] = UserProfileModelForm()

        context['team_list'] = self.request.user.teams.all()
        return context

    def post(self, request, *args, **kwargs):
        form = UserProfileModelForm(self.request.POST)
        user = self.request.user

        if form.is_valid():
            userprofile = form.save(commit=False)
            try:
                user.userprofile.institute_name = userprofile.institute_name
                user.userprofile.save()
            except ObjectDoesNotExist:
               userprofile.user = user
               userprofile.save()
            return HttpResponseRedirect('.')
        else:
            return self.render_to_response({'userprofile_form': form})
