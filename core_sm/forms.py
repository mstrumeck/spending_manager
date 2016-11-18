from django import forms
from .models import Cost


class data_generate_form(forms.Form):
    month = forms.CharField(label='Miesiąc', max_length=100)
    year = forms.CharField(label='Rok', max_length=100)


class data_add_form(forms.ModelForm):
    class Meta:
        model = Cost
        fields = ['title', 'value', 'publish', 'category']

def validate_follow(value):
    return None