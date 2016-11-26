from .forms import data_add_form, data_generate_form
from django.shortcuts import HttpResponseRedirect, render
from django.core.urlresolvers import reverse

def add_data(request):
    if request.method == 'POST':
        add_form = data_add_form(request.POST)
        if add_form.is_valid():
            add_form.save()
    else:
        add_form = data_add_form()
    return {'add_form': add_form}

def day_find(request):
    if request.method == 'POST':
        find_form = data_generate_form(request.POST)
        if find_form.is_valid():
            cd = find_form.cleaned_data
            year = cd['year']
            month = cd['month']
            return HttpResponseRedirect(reverse('core_sm:month_stats_detail', args=(year, month)))
    else:
        find_form = data_generate_form()
    return {'find_form': find_form}