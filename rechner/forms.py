from django import forms

from rechner.models import KOSTENSTEIGERUNG


class BasicRentCalculator(forms.Form):
    start_rent = forms.FloatField()
    start_date = forms.DateField(input_formats=['%d.%m.%Y'])
    new_date = forms.DateField(input_formats=['%d.%m.%Y'])

    cost_value = forms.FloatField()
    cost_type = forms.ChoiceField(choices=KOSTENSTEIGERUNG)
