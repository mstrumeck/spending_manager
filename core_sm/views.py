from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .models import Cost
from django.db.models import Avg, Max, Min, Sum
from .forms import data_generate_form
from django.core.urlresolvers import reverse
import datetime
from bokeh.embed import components
from django.utils.safestring import mark_safe
from bokeh.resources import CDN
from bokeh.plotting import figure
from bokeh.charts import Bar, output_file, show, Histogram
from bokeh.sampledata.autompg import autompg as df
from collections import OrderedDict
import calendar
from math import pi
from bokeh.models import DatetimeTickFormatter
from core_sm.functions import month_day_calculations, month_category_calculation, \
    day_day_calculation, day_category_calculation, year_month_calculation, year_data_calculation


def costs_stats(request):
    if request.method == "GET":
        form = data_generate_form()
    else:
        form = data_generate_form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            return HttpResponseRedirect(reverse('core_sm:month_stats_detail', args=(cd['year'], cd['month'])))
    return render(request, 'core_sm/costs/stats.html', {'form': form})


def year_stats_detail(request, year):
    Months = []
    Months_data = []
    year_data_calculation(Months_data, year)
    year_month_calculation(Months, year)
    all_data = zip(Months, Months_data)
    data = {
        'Miesiące': Months,
        'ZŁ': Months_data
    }
    p = Bar(all_data)
    script, div = components(p, CDN)

    return render(request, 'core_sm/costs/year_stats_detail.html', {'year': year,
                                                                    'Months': Months,
                                                                    'Months_data': Months_data,
                                                                    'script': mark_safe(script),
                                                                    'div': mark_safe(div),
                                                                    'all_data': all_data})


def month_stats_detail(request, year, month):
    mr = calendar.monthrange(int(year), int(month))
    day_numbers = [str(x).zfill(2) for x in range(mr[1]+1)][1:]
    day_sum = []
    day_min = []
    day_max = []
    day_avg = []
    day_data = zip(day_numbers, day_sum, day_max, day_min, day_avg)
    month_day_calculations(day_numbers, year, month, day_sum, day_min, day_max, day_avg)
    data = {
        'Dni': day_numbers,
        'ZŁ': day_sum
    }
    p = Bar(data, plot_width=1250, values='ZŁ', legend=False)
    script, div = components(p, CDN)
    max_month_value = (max(day_max))
    max_month_day = day_numbers[day_max.index(max(day_max))]
    min_month_value = (min(day_min))
    min_month_day = day_numbers[day_min.index(min(day_min))]
    jedzenie = []
    domowe = []
    kosmetyki_i_chemia = []
    rozrywka = []
    okazyjne = []
    inne = []
    month_category_calculation(jedzenie, domowe, kosmetyki_i_chemia, rozrywka, okazyjne, inne)
    data1 = {
        'money': [sum(jedzenie), sum(domowe), sum(kosmetyki_i_chemia), sum(rozrywka), sum(okazyjne), sum(inne)],
        'labels': ['Jedzenie', 'Domowe', 'Kosmetyki i Chemia', 'Rozrywka', 'Okazyjne', 'Inne']
    }
    p1 = Bar(data1, values='money', label='labels')
    script1, div1 = components(p1, CDN)
    sum_cost = Cost.objects.filter(publish__year=year, publish__month=month).aggregate(Sum('value'))
    min_cost = Cost.objects.filter(publish__year=year, publish__month=month).aggregate(Min('value'))
    max_cost = Cost.objects.filter(publish__year=year, publish__month=month).aggregate(Max('value'))
    avg_cost = Cost.objects.filter(publish__year=year, publish__month=month).aggregate(Avg('value'))
    return render(request, 'core_sm/costs/month_stats_detail.html', {'year': year,
                                                                     'month': month,
                                                                     'sum_cost': sum_cost['value__sum'],
                                                                     'min_cost': min_cost['value__min'],
                                                                     'max_cost': max_cost['value__max'],
                                                                     'avg_cost': avg_cost['value__avg'],
                                                                     'day_numbers': day_numbers,
                                                                     'day_data': day_data,
                                                                     'max_month_value': max_month_value,
                                                                     'max_month_day': max_month_day,
                                                                     'min_month_value': min_month_value,
                                                                     'min_month_day': min_month_day,
                                                                     'jedzenie': sum(jedzenie),
                                                                     'domowe': sum(domowe),
                                                                     'kosmetyki_i_chemia': sum(kosmetyki_i_chemia),
                                                                     'rozrywka': sum(rozrywka),
                                                                     'okazyjne': sum(okazyjne),
                                                                     'inne': sum(inne),
                                                                     'script': mark_safe(script),
                                                                     'div': mark_safe(div),
                                                                     'script1': mark_safe(script1),
                                                                     'div1': mark_safe(div1)})

def day_stats_detail(request, year, month, day):
    day_data = Cost.objects.filter(publish__year=year, publish__month=month, publish__day=day)
    title = []
    value = []
    category = []
    id = []
    day_day_calculation(day_data, title, value, category, id)
    all_data = zip(title, value, category, id)
    day_max = [title[value.index(max(value))], max(value), category[value.index(max(value))]]
    day_min = [title[value.index(min(value))], min(value), category[value.index(min(value))]]
    day_sum = day_data.aggregate(Sum('value'))
    day_avg = day_data.aggregate(Avg('value'))
    jedzenie = []
    domowe = []
    kosmetyki_i_chemia = []
    rozrywka = []
    okazyjne = []
    inne = []
    day_category_calculation(day_data, jedzenie, domowe, kosmetyki_i_chemia, rozrywka, okazyjne, inne)
    data = {
        'money': [sum(jedzenie), sum(domowe), sum(kosmetyki_i_chemia), sum(rozrywka), sum(okazyjne), sum(inne)],
        'labels': ['Jedzenie', 'Domowe', 'Kosmetyki i Chemia', 'Rozrywka', 'Okazyjne', 'Inne']
    }
    p = Bar(data, values='money', label='labels')
    script, div = components(p, CDN)
    return render(request, 'core_sm/costs/day_stats_detail.html',
                  {'year': year,
                   'month': month,
                   'day': day,
                   'day_data': day_data,
                   'all_data': all_data,
                   'day_sum': day_sum['value__sum'],
                   'day_avg': day_avg['value__avg'],
                   'day_max': day_max,
                   'day_min': day_min,
                   'script': mark_safe(script),
                   'div': mark_safe(div)})