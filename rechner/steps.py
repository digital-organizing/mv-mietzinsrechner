from django import forms
from django.utils.translation import gettext_lazy as _


class HasContractForm(forms.Form):
    has_contract = forms.BooleanField(required=False)


class HasRentChangedForm(forms.Form):
    has_rent_changed = forms.BooleanField(required=False)


class KindOfChangeForm(forms.Form):
    kind = forms.ChoiceField(choices=(('senkung', _('Senkung')), ('erhöhung', _('Erhöhung'))))
    has_document = forms.BooleanField(required=False)


class RentInfoForm(forms.Form):
    rent = forms.FloatField()
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    zip_code = forms.IntegerField()


class KostensteigerungForm(forms.Form):
    allg_kostensteigerung = forms.ChoiceField(choices=(
        ('0.5', _('nicht exkludiert: Hauswart, Heizung, TV')),
        ('0.25', _('alles exkludiert')),
        ('0', _('alles exkludiert, Neubau')),
    ))


class CouncelForm(forms.Form):
    mv_number = forms.CharField()
    no_membership = forms.BooleanField(required=False)
