from django import forms
from .models import Cost, Budget, Category
import datetime
from django.utils.translation import ugettext_lazy as _


YEARS_CHOICES = [(datetime.date.today() - datetime.timedelta(days=x*365)).year for x in range(10)]
YEAR_CHOICES = zip(YEARS_CHOICES, YEARS_CHOICES)

MONTHS_CHOICES = [str(x).zfill(2) for x in range(13)[1:]]
MONTH_CHOICES = zip(MONTHS_CHOICES, MONTHS_CHOICES)


class DataGenerateForm(forms.Form):
    month = forms.ChoiceField(choices=MONTH_CHOICES)
    year = forms.ChoiceField(choices=YEAR_CHOICES)


class DataAddForm(forms.ModelForm):
    class Meta:
        model = Cost
        fields = ['title', 'value', 'publish', 'category', 'budget']
        labels = {
            'title': _('Tytuł'),
            'value': _('Wartość'),
            'publish': _('Data'),
            'category': _('Kategoria'),
            'budget': _('Budżet')
        }




class MultiaddGenerateForm(forms.Form):
    formy = forms.IntegerField(max_value=20, min_value=1, label='Ilość zakupów')


class comp_form(forms.Form):
    date_x = forms.DateField(label='Od', initial=datetime.date.today())
    date_y = forms.DateField(label='Do', initial=datetime.date.today())


class StatusFormEdit(forms.Form):
    status = forms.CharField(max_length=20)


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['title', 'value']
        labels = {
            'title': _('Tytuł'),
            'value': _('Wartość')
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title']
        labels = {
            'title': _('Tytuł')
        }


class BudgetDelete(forms.Form):
    delete = forms.BooleanField()
