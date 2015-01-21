from django.views.generic import ListView
from django.views.generic.detail import DetailView

from models import News


class NewsListView(ListView):
    model = News


class NewsDetailView(DetailView):
    model = News
