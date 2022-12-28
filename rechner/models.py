# models.py
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.query import QuerySet
from django.utils.translation import gettext as _

# Create your models here.


class Section(models.Model):
    users = models.ManyToManyField(get_user_model())
    name = models.CharField(max_length=120)
    website = models.URLField(blank=True)
    contact = models.EmailField(blank=True)

    min_amount_for_dispute_raise = models.FloatField()
    min_amount_for_dispute_reduction = models.FloatField()

    commune_set: QuerySet["Commune"]


class Address(models.Model):
    street = models.CharField(max_length=120)
    zip_code = models.CharField(max_length=5)
    city = models.CharField(max_length=120)


class Month(models.Model):
    month = models.DateField()
    base_index = models.FloatField()
    hypo = models.FloatField()

    class Meta:
        ordering = ["month"]

    def __str__(self) -> str:
        return f"{self.month}: Hypo: {self.hypo}, Basis-Index: {self.base_index}"


KOSTENSTEIGERUNG = (
    ('rechner', _("Gemäss Rechner")),
    ('vorgabe', _("Vorgabe")),
    ('pauschal', _("Pauschal")),
)


class ArbitrationBoard(models.Model):
    name = models.CharField(max_length=120)
    section = models.ForeignKey(Section, models.CASCADE)
    address = models.ForeignKey(Address, models.CASCADE)

    allg_kostensteigerung_type = models.CharField(max_length=120, choices=KOSTENSTEIGERUNG)
    allg_kostensteigerung_value = models.FloatField()

    is_landloard_required = models.BooleanField(default=False)


class Commune(models.Model):
    section = models.ForeignKey(Section, models.CASCADE)
    zip_code = models.IntegerField()
    name = models.CharField(max_length=120)
