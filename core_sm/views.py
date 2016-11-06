from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .models import Cost, DateMonthYear
from django.db.models import Avg, Max, Min, Sum
from .forms import data_generate_form
from django.core.urlresolvers import reverse
import datetime
from bokeh.embed import components
from django.utils.safestring import mark_safe
from bokeh.resources import CDN
from bokeh.charts import Bar, output_file, show, Histogram
from bokeh.sampledata.autompg import autompg as df
import calendar
from math import pi

def costs_list(request, datemonthyear_slug = None):
    datemonthyear = None
    datesmonthsyears = DateMonthYear.objects.all()
    costs = Cost.objects.all()
    if datemonthyear_slug:
        datemonthyear = get_object_or_404(DateMonthYear, slug=datemonthyear_slug)
        costs = costs.filter(datemonthyear=datemonthyear)
    return render(request, 'core_sm/costs/list.html', {'costs': costs,
                                                 'datemonthyear': datemonthyear,
                                                 'datesmonthsyears': datesmonthsyears},)

def costs_month_detail(request, id, slug):
    cost = get_object_or_404(Cost, id=id, slug=slug)
    return render(request, 'core_sm/costs/detail.html', {'cost': cost})

def costs_stats(request):
    if request.method == "GET":
        form = data_generate_form()
    else:
        form = data_generate_form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            return HttpResponseRedirect(reverse('core_sm:month_stats_detail', args=(cd['year'], cd['month'])))
    return render(request, 'core_sm/costs/stats.html', {'form': form})

def month_stats_detail(request, year, month):
    mr = calendar.monthrange(int(year), int(month))
    day_numbers = [x for x in range(mr[1]+1)][1:]
    day_sum = []
    day_min = []
    day_max = []
    day_avg = []
    day_data = zip(day_numbers, day_sum, day_max, day_min, day_avg)
    for day in day_numbers:
        val_1 = Cost.objects.filter(publish__year=year, publish__month=month, publish__day=day).aggregate(Sum('value'))['value__sum']
        val_2 = Cost.objects.filter(publish__year=year, publish__month=month, publish__day=day).aggregate(Min('value'))['value__min']
        val_3 = Cost.objects.filter(publish__year=year, publish__month=month, publish__day=day).aggregate(Max('value'))['value__max']
        val_4 = Cost.objects.filter(publish__year=year, publish__month=month, publish__day=day).aggregate(Avg('value'))['value__avg']
        if val_1 and val_2 and val_3 and val_4 is not None:
            val_1 = float(val_1)
            val_2 = float(val_2)
            val_3 = float(val_3)
            val_4 = float(val_4)
            day_sum.append(val_1)
            day_min.append(val_2)
            day_max.append(val_3)
            day_avg.append(val_4)
        else:
            day_sum.append(0)
            day_min.append(0)
            day_max.append(0)
            day_avg.append(0)
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
                                                               'script': mark_safe(script),
                                                               'div': mark_safe(div)})

def day_stats_detail(request, year, month, day):
    
    return render(request, 'core_sm/costs/day_stats_detail.html',
                  {'year': year,
                   'month': month,
                   'day': day})