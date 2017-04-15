from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^$', views.current_detail, name='current_detail'),
    url(r'^stats$', views.costs_stats, name='costs_stats'),
    url(r'^costs/(?P<year>\d{4})/(?P<month>\d{2})/$', views.month_stats_detail, name='month_stats_detail'),
    url(r'^costs/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', views.day_stats_detail, name='day_stats_detail'),    url(r'^costs/(?P<year>\d+)/$', views.year_stats_detail, name='year_stats_detail'),
    url(r'^day_data_multiadd/$', views.day_data_multiadd, name='day_data_multiadd'),
    url(r'^day_data_multiadd/(?P<no_of_lines>\d+)/$', views.day_data_multiadd, name='day_data_multiadd'),
    url(r'^delete/(?P<id>\d+)/$', views.day_data_delete, name='day_data_delete'),
    url(r'^compare/$', views.stats_comp, name='stats_comp'),
    url(r'^compare/(?P<date_x>\d{4}-\d{2}-\d{2})/(?P<date_y>\d{4}-\d{2}-\d{2})/$', views.stats_comp, name='stats_comp'),
    url(r'^budget_setup$', views.budget_setup, name='budget_setup'),
    url(r'^budget/(?P<budget_id>\d+)/$', views.budget_detail, name='budget_detail'),
    url(r'^budget/(?P<id>\d+)/(?P<year>\d{4})/$', views.budget_year_stats_detail, name='budget_year_stats_detail'),
    url(r'^budget/(?P<id>\d+)/(?P<year>\d{4})/(?P<month>\d{2})/$', views.budget_month_stats_detail,
        name='budget_month_stats_detail'),
    url(r'budget/(?P<id>\d+)/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
        views.budget_day_stats_detail, name='budget_day_stats_detail'),
    url(r'^budget_edit/(?P<id>\d+)/$', views.budget_edit, name='budget_edit'),
    url(r'^budget_delete/(?P<budget_id>\d+)/$', views.budget_delete, name='budget_delete'),
    url(r'^budget_item_delete/(?P<id>\d+)/$', views.budget_item_delete, name='budget_item_delete'),
    url(r'^category/(?P<category_id>\d+)/$', views.category_detail, name='category_detail'),
    url(r'^category/(?P<category_id>\d+)/(?P<year>\d{4})/$', views.category_year_stats_detail,
        name='category_year_stats_detail'),
    url(r'^category/(?P<category_id>\d+)/(?P<year>\d{4})/(?P<month>\d+)/$', views.category_month_stats_detail,
        name='category_month_stats_detail'),
    url(r'^category/(?P<category_id>\d+)/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
        views.category_day_stats_detail, name='category_day_stats_detail'),
    url(r'^category_setup/$', views.category_setup, name='category_setup'),
    url(r'^category_edit/(?P<category_id>\d+)/$', views.category_edit, name='category_edit'),
    url(r'^category_delete/(?P<category_id>\d+)/$', views.category_delete, name='category_delete'),
    #Bajery związane z logowaniem
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^logout-then-login/$', auth_views.logout_then_login, name='logout_then_login'),
    url(r'^password-change/$', auth_views.password_change, name='password_change'),
    url(r'^password_change/done/$', auth_views.password_change_done, name='password_change_done'),
    url(r'^password-reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password-reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',
        auth_views.password_reset_confirm,
        name='password_reset_confirm'),
    url(r'^password-reset/complete/$', auth_views.password_reset_complete,
        name='password_reset_complete'),
    url(r'test_view/(?P<budget_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', views.test_view, name='test_view'),
]