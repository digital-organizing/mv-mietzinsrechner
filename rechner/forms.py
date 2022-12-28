from django import forms

from rechner.models import KOSTENSTEIGERUNG


class BasicRentCalculator(forms.Form):
    start_rent = forms.FloatField()
    start_date = forms.DateField(widget=forms.DateInput(format=('%Y-%m-%d'), ))

    new_date = forms.DateField(widget=forms.DateInput(format=('%Y-%m-%d'), ))

    cost_value = forms.FloatField()
    cost_type = forms.ChoiceField(choices=KOSTENSTEIGERUNG)
