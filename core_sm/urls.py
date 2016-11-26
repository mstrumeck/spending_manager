from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.current_detail, name='current_detail'),
    url(r'^stats$', views.costs_stats, name='costs_stats'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', views.month_stats_detail, name='month_stats_detail'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', views.day_stats_detail, name='day_stats_detail'),
    url(r'^(?P<year>\d{4})/$', views.year_stats_detail, name='year_stats_detail'),
    url(r'^day_data_multiadd/$', views.day_data_multiadd, name='day_data_multiadd'),
    url(r'^day_data_multiadd/(?P<no_of_lines>\d+)/$', views.day_data_multiadd, name='day_data_multiadd'),
    url(r'^delete/(?P<id>\d+)/$', views.day_data_delete, name='day_data_delete'),
    url(r'^add$', views.data_add, name='data_add'),
    url(r'^compare/$', views.stats_comp, name='stats_comp'),
    url(r'^compare/(?P<year_x>\d{4})/(?P<month_x>\d{2})/(?P<day_x>\d{2})/'
        r'(?P<year_y>\d{4})/(?P<month_y>\d{2})/(?P<day_y>\d{2})/$', views.stats_comp, name='stats_comp')
]
