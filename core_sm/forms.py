from django import forms
from .models import Cost
from django.forms import ModelForm


class data_generate_form(forms.Form):
    month = forms.CharField(label='Miesiąc', max_length=100)
    year = forms.CharField(label='Rok', max_length=100)


class data_add_form(ModelForm):
    class Meta:
        model = Cost
        fields = ['title', 'value', 'publish', 'category']
