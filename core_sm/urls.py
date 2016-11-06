from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.costs_list, name='cost_list'),
    url(r'^(?P<datemonthyear_slug>[-\w]+)/$', views.costs_list, name='cost_list_by_datemonthyear'),
    url(r'^stats$', views.costs_stats, name='costs_stats'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', views.month_stats_detail, name='month_stats_detail'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', views.day_stats_detail, name='day_stats_detail')
]