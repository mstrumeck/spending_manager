from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^stats$', views.costs_stats, name='costs_stats'),
    url(r'^(?P<year>\d{4})/(?P<month>\d+)/$', views.month_stats_detail, name='month_stats_detail'),
    url(r'^(?P<year>\d{4})/(?P<month>\d+)/(?P<day>\d+)/$', views.day_stats_detail, name='day_stats_detail'),
    url(r'^(?P<year>\d{4})/$', views.year_stats_detail, name='year_stats_detail'),
    url(r'^delete/(?P<id>\d+)/$', views.day_data_delete, name='day_data_delete'),
    url(r'^add$', views.data_add, name='data_add'),
    url(r'^$', views.current_detail, name='current_detail')
]