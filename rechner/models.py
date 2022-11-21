from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet

# Create your models here.


class Section(models.Model):
    users = models.ManyToManyField(get_user_model())
    name = models.CharField(max_length=120)
    website = models.URLField(blank=True)
    contact = models.EmailField(blank=True)

    min_amount_for_dispute_raise = models.FloatField()
    min_amount_for_dispute_reduction = models.FloatField()

    commune_set: QuerySet["Commune"]


class Commune(models.Model):
    section = models.ForeignKey(Section, models.CASCADE)
    zip_code = models.IntegerField()
    name = models.CharField(max_length=120)
