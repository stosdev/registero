# -*- coding: utf-8 -*-
from django.conf.urls import url
from views import NewsListView, NewsDetailView

urlpatterns = [
    # Examples:
    # url(r'^$', 'registero.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', NewsListView.as_view()),
    url(r'^(?P<pk>\d+)/$', NewsDetailView.as_view(), name='news.views.detail'),
]
