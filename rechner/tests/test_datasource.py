from datetime import date, datetime

from django.test import TestCase

from rechner.datasource import (
    fetch_base_index,
    fetch_hypo,
    get_hypo_for_date,
    update_price_db,
)
from rechner.models import Month
from rechner.services import find_month


class CalculationTests(TestCase):

    def test_fetch_hypo(self):
        df = fetch_hypo()
        self.assertGreater(len(df), 5)
        self.assertEqual(2, len(df.columns))

    def test_fetch_base_index(self):
        df = fetch_base_index()
        self.assertGreater(len(df), 5)

    def test_hypo_search(self):
        df = fetch_hypo()
        self.assertAlmostEqual(2.5, get_hypo_for_date(df, datetime(2011, 12, 13)))
        self.assertAlmostEqual(3.5, get_hypo_for_date(df, datetime(2008, 9, 11)))
        self.assertAlmostEqual(1.25, get_hypo_for_date(df, datetime(2022, 12, 13)))
        self.assertAlmostEqual(3, get_hypo_for_date(df, datetime(2010, 3, 2)))

    def test_update_price_db(self):
        self.assertEqual(0, Month.objects.all().count())
        update_price_db()
        self.assertGreater(Month.objects.all().count(), 2)

        self.assertEqual(Month.objects.get(month=datetime(2022, 9, 1)).base_index, 165.3)
        self.assertEqual(Month.objects.get(month=datetime(2018, 8, 1)).base_index, 159.6)
        self.assertEqual(Month.objects.get(month=datetime(2018, 8, 1)).hypo, 1.5)

    def test_find_correct_month_in_bounds(self):
        update_price_db()
        self.assertEqual(find_month(date(2022, 9, 12)).month, date(2022, 9, 1))
        self.assertEqual(find_month(date(2012, 4, 1)).month, date(2012, 4, 1))
        self.assertEqual(find_month(date(2000, 9, 12)).month, date(2000, 9, 1))

    def test_find_correct_month_old(self):
        update_price_db()
        self.assertEqual(find_month(date(1980, 9, 12)).month, date(1982, 12, 1))
        self.assertEqual(find_month(date(1971, 1, 1)).month, date(1982, 12, 1))

    def test_find_correct_month_future(self):
        update_price_db()
        self.assertEqual(find_month(date(2023, 9, 12)).month, date(2022, 11, 1))
        self.assertEqual(find_month(date(2022, 12, 12)).month, date(2022, 11, 1))
        self.assertEqual(find_month(date(2032, 12, 12)).month, date(2022, 11, 1))
