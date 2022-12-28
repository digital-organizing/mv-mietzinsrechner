from django.urls import path
from rechner.views import test_view

from rechner.wizard import RentWizard

app_name = "rechner"

urlpatterns = [
    path('', test_view, name="wizard"),
]
