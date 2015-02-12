from django.conf.urls import patterns, url
from views import TeamManagementView, TeamCreateView, TeamDeleteView, \
    TeamReorderView, ParticipantCreateView, ParticipantDeleteView, \
    ParticipantUpdateView


urlpatterns = patterns('',
    url(r'^$', TeamManagementView.as_view(),
        name='team.views.management'),
    url(r'^new/$', TeamCreateView.as_view(),
        name='team.views.create'),
    url(r'^(?P<pk>\d+)/delete/$', TeamDeleteView.as_view(),
        name='team.views.delete'),
    url(r'^reorder/', TeamReorderView.as_view(),
        name='team.views.reorder'),

    url(r'^(?P<team_pk>\d+)/participant/new/$',
        ParticipantCreateView.as_view(), name='participant.views.create'),
    url(r'^(?P<team_pk>\d+)/participant/(?P<pk>\d+)/delete/$',
        ParticipantDeleteView.as_view(), name='participant.views.delete'),
    url(r'^(?P<team_pk>\d+)/participant/(?P<pk>\d+)/edit/$',
        ParticipantUpdateView.as_view(), name='participant.views.edit'),


)
