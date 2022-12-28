from django.core.management.base import BaseCommand, CommandError

from rechner.datasource import update_price_db
from rechner.models import Month


class Command(BaseCommand):
    help = 'Fetch new data about cost incrases and stuff'

    def handle(self, *args, **options):
        update_price_db()

        print("Updated data, newest record: ", Month.objects.order_by('-month').first())
