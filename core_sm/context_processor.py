from .forms import DataAddForm, DataGenerateForm
from django.shortcuts import HttpResponseRedirect, render
from django.core.urlresolvers import reverse

def add_data(request):
    sent = False
    if request.method == 'POST':
        add_form = DataAddForm(request.POST)
        if add_form.is_valid():
            add_form.save()
            sent = True
    else:
        add_form = DataAddForm()
    return {'add_form': add_form,
            'sent': sent}
