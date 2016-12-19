from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.current_detail, name='current_detail'),
    url(r'^stats$', views.costs_stats, name='costs_stats'),
    url(r'^costs/(?P<year>\d{4})/(?P<month>\d{2})/$', views.month_stats_detail, name='month_stats_detail'),
    url(r'^costs/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', views.day_stats_detail, name='day_stats_detail'),
    url(r'^costs/(?P<year>\d+)/$', views.year_stats_detail, name='year_stats_detail'),
    url(r'^day_data_multiadd/$', views.day_data_multiadd, name='day_data_multiadd'),
    url(r'^day_data_multiadd/(?P<no_of_lines>\d+)/$', views.day_data_multiadd, name='day_data_multiadd'),
    url(r'^delete/(?P<id>\d+)/$', views.day_data_delete, name='day_data_delete'),
    url(r'^compare/$', views.stats_comp, name='stats_comp'),
    url(r'^compare/(?P<date_x>\d{4}-\d{2}-\d{2})/(?P<date_y>\d{4}-\d{2}-\d{2})/$', views.stats_comp, name='stats_comp'),
    url(r'^status_edit', views.edit_status, name='edit_status'),
    url(r'^budget_setup$', views.budget_setup, name='budget_setup'),
    url(r'^budget/(?P<id>\d+)/$', views.budget_detail, name='budget_detail'),
    url(r'^budget/(?P<id>\d+)/(?P<year>\d{4})/$', views.budget_year_stats_detail, name='budget_year_stats_detail'),
    url(r'^budget/(?P<id>\d+)/(?P<year>\d{4})/(?P<month>\d{2})/$', views.budget_month_stats_detail,
        name='budget_month_stats_detail'),
    url(r'budget/(?P<id>\d+)/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
        views.budget_day_stats_detail, name='budget_day_stats_detail'),
    url(r'^budget_edit/(?P<id>\d+)/$', views.budget_edit, name='budget_edit'),
    url(r'^budget_delete/(?P<id>\d+)/$', views.budget_delete, name='budget_delete'),
    url(r'^budget_list/$', views.budget_list, name='budget_list'),
    url(r'^budget_item_delete/(?P<id>\d+)/$', views.budget_item_delete, name='budget_item_delete'),
    url(r'^category/(?P<category_id>\d+)/$', views.category_detail, name='category_detail'),
    url(r'^category/(?P<category_id>\d+)/(?P<year>\d{4})/$', views.category_year_stats_detail,
        name='category_year_stats_detail'),
    url(r'^category/(?P<category_id>\d+)/(?P<year>\d{4})/(?P<month>\d{2})/$', views.category_month_stats_detail,
        name='category_month_stats_detail'),
    url(r'^category/(?P<category_id>\d+)/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
        views.category_day_stats_detail, name='category_day_stats_detail')
]
