from django.urls import path

from rechner.wizard import RentWizard

app_name = "rechner"

urlpatterns = [
    path('', RentWizard.as_view(), name="wizard"),
]
