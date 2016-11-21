from django import forms
from .models import Cost
import datetime
from django.forms import BaseModelFormSet


YEARS_CHOICES = [(datetime.date.today() - datetime.timedelta(days=x*365)).year for x in range(10)]
YEAR_CHOICES = zip(YEARS_CHOICES, YEARS_CHOICES)

MONTHS_CHOICES = [str(x).zfill(2) for x in range(13)[1:]]
MONTH_CHOICES = zip(MONTHS_CHOICES, MONTHS_CHOICES)


class data_generate_form(forms.Form):
    miesiąc = forms.ChoiceField(choices=MONTH_CHOICES)
    rok = forms.ChoiceField(choices=YEAR_CHOICES)


class data_add_form(forms.ModelForm):
    class Meta:
        model = Cost
        fields = ['title', 'value', 'publish', 'category']



