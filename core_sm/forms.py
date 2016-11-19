from django import forms
from .models import Cost


class data_generate_form(forms.Form):
    month = forms.IntegerField(label='Miesiąc')
    year = forms.IntegerField(label='Rok')


class data_add_form(forms.ModelForm):
    class Meta:
        model = Cost
        fields = ['title', 'value', 'publish', 'category']

def validate_follow(value):
    return None