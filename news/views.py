from django.views.generic import ListView

from models import News


class NewsListView(ListView):
    model = News
