import os

from django.http.response import HttpResponse
from django.shortcuts import render

from rechner.forms import BasicRentCalculator
from rechner.services import delta, find_month

# Create your views here.


def test_view(request):

    if not request.GET:
        return render(request, 'rechner/test_view.html', {
            'form': BasicRentCalculator(),
            'result': None
        })

    form = BasicRentCalculator(request.GET)

    result = None

    if form.is_valid():
        data = form.cleaned_data
        # TODO: Calculate stuff ro return
        start_month = find_month(data['start_date'])
        new_month = find_month(data['new_date'])

        result = delta(start_month,
                       new_month,
                       data['start_rent'],
                       cost_type=data['cost_type'],
                       cost_kind=data['cost_value'])

    return render(request, 'rechner/test_view.html', {'form': form, 'result': result})
