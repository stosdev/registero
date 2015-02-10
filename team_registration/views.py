from django.views.generic.edit import FormView
from django.views.generic.base import RedirectView
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy

from models import Team
from forms import CoachProfileModelForm


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
            coachprofile = self.request.user.coachprofile
            initial.update({'institute_name': coachprofile.institute_name, })
        except ObjectDoesNotExist:
            pass

    def form_valid(self, form):
        user = self.request.user
        coachprofile = form.save(commit=False)
        try:
            user.coachprofile.institute_name = coachprofile.institute_name
        except ObjectDoesNotExist:
            user.coachprofile = coachprofile
        user.coachprofile.save()
        return super(TeamManagementView, self).form_valid(form)
