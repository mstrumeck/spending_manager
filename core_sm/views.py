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
from core_sm.functions import month_day_calculations, month_category_calculation, \
    day_day_calculation, day_category_calculation, year_data_calculation, year_month_calculation, \
    year_categories_calculation

def day_data_delete(request, id):
    Message = 'Zapis {} został poprawnie usunięty'.format(Cost.objects.filter(id=id).values('title', 'value'))
    Cost.objects.filter(id=id).delete()
    return render(request, 'core_sm/cost/day_delete.html', {'Message', Message})


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
    Months_url = [str(x).zfill(2) for x in range(13)[1:]]
    year_month_calculation(Months)
    year_data_calculation(Months_data, year)
    data = {
        'Miesiące': Months,
        'ZŁ': Months_data
    }
    p = Bar(data, values='ZŁ', label='Miesiące')
    script, div = components(p, CDN)
    all_data = zip(Months, Months_data, Months_url)
    year_sum = Cost.objects.filter(publish__year=year).aggregate(Sum('value'))['value__sum']
    categories = ['Jedzenie', 'Domowe', 'Kosmetyki i Chemia', 'Rozrywka', 'Okazyjne', 'Inne']
    categories_data = []
    year_categories_calculation(year, categories, categories_data)
    data1 = {
        'money': [float(x) for x in categories_data],
        'labels': categories
    }
    p1 = Bar(data1, values='money', label='labels')
    script1, div1 = components(p1, CDN)
    categories_res = zip(categories, categories_data)
    return render(request, 'core_sm/costs/year_stats_detail.html', {'year': year,
                                                                    'Months': Months,
                                                                    'Months_data': Months_data,
                                                                    'script': mark_safe(script),
                                                                    'div': mark_safe(div),
                                                                    'all_data': all_data,
                                                                    'year_sum': year_sum,
                                                                    'script1': mark_safe(script1),
                                                                    'div1': mark_safe(div1),
                                                                    'categories_res': categories_res})


def month_stats_detail(request, year, month):
    mr = calendar.monthrange(int(year), int(month))
    day_numbers = [str(x).zfill(2) for x in range(mr[1]+1)][1:]
    day_sum = []
    day_min = []
    day_max = []
    day_avg = []
    month_day_calculations(day_numbers, year, month, day_sum, day_min, day_max, day_avg)
    day_data = zip(day_numbers, day_sum, day_max, day_min, day_avg)
    data = {
        'Dni': day_numbers,
        'ZŁ': [float(x) for x in day_sum]
    }
    p = Bar(data, plot_width=1250, values='ZŁ', legend=False)
    script, div = components(p, CDN)
    max_month_value = (max(day_max))
    max_month_day = day_numbers[day_max.index(max(day_max))]
    min_month_value = (min(day_min))
    min_month_day = day_numbers[day_min.index(min(day_min))]
    categories = ['Jedzenie', 'Domowe', 'Kosmetyki i Chemia', 'Rozrywka', 'Okazyjne', 'Inne']
    categories_data = []
    month_category_calculation(year, month, categories, categories_data)
    data1 = {
        'money': [float(x) for x in categories_data],
        'labels': categories
    }
    p1 = Bar(data1, values='money', label='labels')
    script1, div1 = components(p1, CDN)
    categories_res = zip(categories, categories_data)
    sum_cost = Cost.objects.filter(publish__year=year, publish__month=month).aggregate(Sum('value'))
    min_cost = Cost.objects.filter(publish__year=year, publish__month=month).aggregate(Min('value'))
    max_cost = Cost.objects.filter(publish__year=year, publish__month=month).aggregate(Max('value'))
    avg_cost = "%.2f" % Cost.objects.filter(publish__year=year, publish__month=month).aggregate(Avg('value'))['value__avg']
    return render(request, 'core_sm/costs/month_stats_detail.html', {'year': year,
                                                                     'month': month,
                                                                     'sum_cost': sum_cost['value__sum'],
                                                                     'min_cost': min_cost['value__min'],
                                                                     'max_cost': max_cost['value__max'],
                                                                     'avg_cost': avg_cost,
                                                                     'day_numbers': day_numbers,
                                                                     'day_data': day_data,
                                                                     'max_month_value': max_month_value,
                                                                     'max_month_day': max_month_day,
                                                                     'min_month_value': min_month_value,
                                                                     'min_month_day': min_month_day,
                                                                     'script': mark_safe(script),
                                                                     'div': mark_safe(div),
                                                                     'script1': mark_safe(script1),
                                                                     'div1': mark_safe(div1),
                                                                     'categories_res': categories_res,
                                                                     'day_sum': day_avg})

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
    categories = ['Jedzenie', 'Domowe', 'Kosmetyki i Chemia', 'Rozrywka', 'Okazyjne', 'Inne']
    categories_data = []
    day_category_calculation(year, month, day, categories, categories_data)
    data = {
        'money': [float(x) for x in categories_data],
        'labels': categories
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
                   'script': mark_safe(script),
                   'div': mark_safe(div),
                   'day_max': day_max,
                   'day_min': day_min})