from datetime import datetime

from django.test import TestCase

from rechner.services import cost_increase, hypo_change_steps, calc_inflation

# Create your tests here.


class CalculationTests(TestCase):

    def test_hypo_change(self):
        # Hypo incrases
        self.assertAlmostEqual(3.00, hypo_change_steps(1.25, 1.5))
        self.assertAlmostEqual(33.00, hypo_change_steps(2.25, 5.0))
        self.assertAlmostEqual(5.00, hypo_change_steps(5.5, 6.0))
        self.assertAlmostEqual(19.5, hypo_change_steps(4.0, 5.75))
        self.assertAlmostEqual(19.5, hypo_change_steps(4.0, 5.75))
        self.assertAlmostEqual(19.5, hypo_change_steps(4.0, 5.75))
        self.assertAlmostEqual(61.0, hypo_change_steps(1.25, 6.75))
        self.assertAlmostEqual(2.0, hypo_change_steps(6.5, 6.75))
        self.assertAlmostEqual(5, hypo_change_steps(5, 5.5))
        # Hypo decreases
        self.assertAlmostEqual(-4.76, hypo_change_steps(5.5, 5), places=2)
        self.assertAlmostEqual(-19.03, hypo_change_steps(5.25, 3.25), places=2)
        self.assertAlmostEqual(-5.66, hypo_change_steps(2, 1.50), places=2)
        self.assertAlmostEqual(-1.96, hypo_change_steps(6.75, 6.5), places=2)
        self.assertAlmostEqual(-13.04, hypo_change_steps(4.5, 3.25), places=2)
        self.assertAlmostEqual(-37.89, hypo_change_steps(6.75, 1.25), places=2)
        self.assertAlmostEqual(-2.91, hypo_change_steps(1.5, 1.25), places=2)

    def test_inflation(self):
        self.assertAlmostEqual(0.0, calc_inflation(100.0, 100.0))
        self.assertAlmostEqual(2.0, calc_inflation(100.0, 102.0))
        self.assertAlmostEqual(1.610, 0.4 * calc_inflation(159.0, 165.4), places=2)
        self.assertAlmostEqual(1.553, 0.4 * calc_inflation(128.8, 133.8), places=2)
        self.assertAlmostEqual(12.15, calc_inflation(100.4, 112.6), places=2)

    def test_cost_change(self):
        self.assertAlmostEqual(0.0, cost_increase(0, datetime(2022, 12, 1), datetime(2022, 12, 1)))
        self.assertAlmostEqual(
            0.25,
            cost_increase(0.25, datetime(2021, 12, 1), datetime(2022, 12, 1)),
        )
        self.assertAlmostEqual(
            0.5,
            cost_increase(0.25, datetime(2020, 12, 1), datetime(2022, 12, 1)),
        )
        self.assertAlmostEqual(
            0.75,
            cost_increase(0.5, datetime(2021, 6, 1), datetime(2022, 12, 1)),
        )
