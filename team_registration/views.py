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
            coach_profile = self.request.user.coach_profile
            initial.update({
                'institute_name': coach_profile.institute_name,
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
