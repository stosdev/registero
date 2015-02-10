from django.conf.urls import patterns, include, url
from django.contrib import admin
from views import TeamManagementView, TeamCreateView


urlpatterns = patterns('',
    url(r'^$', TeamManagementView.as_view(),
        name='team.views.management'),
    url(r'^new/$', TeamCreateView.as_view(),
        name='team.views.create'),

)
