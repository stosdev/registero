from django.conf.urls import patterns, url
from views import NewsListView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'registero.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', NewsListView.as_view()),
)
