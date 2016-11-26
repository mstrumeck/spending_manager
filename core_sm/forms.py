from django import forms
from .models import Cost
import datetime
from django.forms.formsets import BaseFormSet


YEARS_CHOICES = [(datetime.date.today() - datetime.timedelta(days=x*365)).year for x in range(10)]
YEAR_CHOICES = zip(YEARS_CHOICES, YEARS_CHOICES)

MONTHS_CHOICES = [str(x).zfill(2) for x in range(13)[1:]]
MONTH_CHOICES = zip(MONTHS_CHOICES, MONTHS_CHOICES)


class data_generate_form(forms.Form):
    month = forms.ChoiceField(choices=MONTH_CHOICES)
    year = forms.ChoiceField(choices=YEAR_CHOICES)


class data_add_form(forms.ModelForm):
    class Meta:
        model = Cost
        fields = ['title', 'value', 'publish', 'category']

class multiadd_generate_form(forms.Form):
    formy = forms.IntegerField(max_value=30, min_value=1)

class BaseLineFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super(BaseLineFormSet, self).__init__(*args, **kwargs)
        no_of_forms = len(self)
        for i in range(0, no_of_forms):
            self[i].fields['title', 'value', 'publish', 'category'].label += "-%d" % (i + 1)


