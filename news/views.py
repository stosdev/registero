#-*- coding: utf-8 -*-
from django.views.generic import ListView
from django.views.generic.detail import DetailView

from models import News


class NewsListView(ListView):
    queryset = News.on_site.all()


class NewsDetailView(DetailView):
    model = News
