from django import forms
from .models import Cost

class data_generate_form(forms.Form):
    month = forms.CharField(label='Month', max_length=100)
    year = forms.CharField(label='Year', max_length=100)