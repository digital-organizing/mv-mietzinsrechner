from django.shortcuts import render
from formtools.wizard.views import SessionWizardView

from rechner.steps import (
    CouncelForm,
    HasContractForm,
    HasRentChangedForm,
    KindOfChangeForm,
    KostensteigerungForm,
    RentInfoForm,
)


def show_rent_changed_form(wizard):
    return True


def show_rent_info_form(wizard):

    has_contract = wizard.get_cleaned_data_for_step(RentWizard.HAS_CONTRACT_FORM) or {}
    has_contract = has_contract.get('has_contract', False)

    has_rent_changed = wizard.get_cleaned_data_for_step(RentWizard.HAS_RENT_CHANGED_FORM) or {}
    has_rent_changed = has_rent_changed.get('has_rent_changed', False)

    if (not has_contract) and (not has_rent_changed):
        return False

    kind_of_change = wizard.get_cleaned_data_for_step(RentWizard.KIND_OF_CHANGE_FORM) or {}

    if kind_of_change.get('kind') == 'erhöhung' and not kind_of_change.get('has_document'):
        return False
    return True


def show_kostensteigerung_form(wizard):
    return show_rent_info_form(wizard)


def show_kind_of_change_form(wizard):
    return show_rent_changed_form(wizard)


def show_member_form(wizard):
    kind_of_change = wizard.get_cleaned_data_for_step(RentWizard.KIND_OF_CHANGE_FORM) or {}

    if kind_of_change.get('kind') == 'erhöhung' and not kind_of_change.get('has_document'):
        return True

    return False


class RentWizard(SessionWizardView):
    form_list = [
        HasContractForm,
        HasRentChangedForm,
        KindOfChangeForm,
        RentInfoForm,
        KostensteigerungForm,
        CouncelForm,
    ]

    HAS_CONTRACT_FORM = '0'
    HAS_RENT_CHANGED_FORM = '1'
    KIND_OF_CHANGE_FORM = '2'
    RENT_INFO_FORM = '3'
    KOSTEN_FORM = '4'
    COUNCEL_FORM = '5'

    template_name: str = 'rechner/wizard.html'
    condition_dict = {
        HAS_CONTRACT_FORM: True,
        HAS_RENT_CHANGED_FORM: show_rent_changed_form,
        RENT_INFO_FORM: show_rent_info_form,
        KIND_OF_CHANGE_FORM: show_kind_of_change_form,
        KOSTEN_FORM: show_kostensteigerung_form,
        COUNCEL_FORM: show_member_form,
    }

    def done(self, form_list, **kwargs):

        return render(self.request, 'rechner/result.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })
