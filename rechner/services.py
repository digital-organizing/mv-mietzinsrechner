import datetime
from dataclasses import dataclass
from typing import Optional, Tuple
from django.core.exceptions import ObjectDoesNotExist

from numba import float32, float64, jit

from rechner.models import KOSTENSTEIGERUNG, Address, ArbitrationBoard, Month

PAUSCHALE = 'pauschal'
KOSTENSTEIGERUNG = 'kosten'


def find_board(address: Address) -> ArbitrationBoard:
    raise NotImplementedError("This needs to be implemented")


def find_month(date: datetime.date) -> Month:
    month = Month.objects.filter(month__month=date.month, month__year=date.year).first()

    if month is not None:
        return month

    oldest = Month.objects.all().order_by('month').first()
    newest = Month.objects.all().order_by('-month').first()

    assert oldest is not None
    assert newest is not None

    if date < oldest.month:
        return oldest
    if date > newest.month:
        return newest

    raise ObjectDoesNotExist(f"Couldn't find month for date {date}")


def calc_inflation(index_0, index_1) -> float:
    """Calculate the inflation between two price indexes, in percent"""
    return (index_1 - index_0) / index_0 * 100


def cost_increase(value: float, start_date: datetime.date,
                  end_date: datetime.date) -> Tuple[float, float]:
    """Calculate the cost increase between two dates"""
    months_between = (end_date.year - start_date.year) * 12 + end_date.month - start_date.month
    return months_between, months_between / 12 * value


@jit(float32(float32, float32), nopython=True, cache=True)
def hypo_change_steps(hypo_old: float, hypo_new: float):
    change = 0
    start, goal = (hypo_old, hypo_new) if hypo_new > hypo_old else (hypo_new, hypo_old)

    if start < 5:
        if goal > 6:
            change += 3 * (5 - start)
            change += 2.5 * (6 - 5)
            change += 2.0 * (goal - 6)
        elif goal > 5:
            change += 3 * (5 - start)
            change += 2.5 * (goal - 5)
        else:
            change += 3 * (goal - start)
    elif start < 6:
        if goal > 6:
            change += 2.5 * (6 - start)
            change += 2.0 * (goal - 6)
        else:
            change += 2.5 * (goal - start)
    else:
        change += 2.0 * (goal - start)

    change *= 4
    # Rent increase
    if hypo_old < hypo_new:
        return change

    # Rent decrease
    return (100 / (100 + change) - 1) * 100


@dataclass
class Change:
    rent_initial: float
    cost_kind: str
    cost_value: float
    cost_increase_percent: float
    months: float
    inflation: float

    hypo_old: float
    hypo_new: float
    hypo_change: float

    total_percent: float

    base_old: float
    base_new: float

    @property
    def inflation_absolute(self):
        return self.rent_initial * self.inflation / 100 * 0.4

    @property
    def cost_increase_absolute(self):
        return self.cost_increase_percent / 100 * self.rent_initial

    @property
    def hypo_change_absolute(self):
        return self.hypo_change / 100 * self.rent_initial

    @property
    def total_change_absolute(self):
        return self.total_percent / 100 * self.rent_initial


def total_reference_change(
    index_old: float,
    index_new: float,
    start_date: datetime.date,
    end_date: datetime.date,
    cost_kind: str,
    value: float,
    hypo_old: float,
    hypo_new: float,
    rent_initial: float,
) -> Change:
    if cost_kind == PAUSCHALE:
        cost = 0.1 * calc_inflation(index_old, index_new)
        months = None
    else:
        months, cost = cost_increase(value, start_date, end_date)
    inflation = calc_inflation(index_old, index_new)
    hypo_change = hypo_change_steps(hypo_old, hypo_new)

    return Change(
        cost_kind=cost_kind,
        cost_increase_percent=cost,
        cost_value=value,
        inflation=inflation,
        hypo_old=hypo_old,
        hypo_new=hypo_new,
        hypo_change=hypo_change,
        total_percent=hypo_change + cost + 0.4 * inflation,
        rent_initial=rent_initial,
        base_old=index_old,
        base_new=index_new,
        months=months or 0,
    )


def delta(last: Month,
          now: Month,
          rent_initial: float,
          board: Optional[ArbitrationBoard] = None,
          cost_type: Optional[str] = None,
          cost_kind: Optional[float] = None):
    return total_reference_change(
        last.base_index,
        now.base_index,
        last.month,
        now.month,
        board.allg_kostensteigerung_type if board else cost_type or PAUSCHALE,
        board.allg_kostensteigerung_value if board else cost_kind or 0,
        last.hypo,
        now.hypo,
        rent_initial,
    )


def calculate_rent_history(
    address: Address,
    initial_rent: float,
    initial_month: Month,
    end_date: datetime.date,
):
    board = find_board(address)
    values = [
        {
            'rent': initial_rent,
            'index': initial_month.base_index,
            'hypo': initial_month.hypo,
            'date': initial_month.month,
        },
    ]

    for month in Month.objects.filter(month__gt=initial_month.month, month__lte=end_date):
        info = delta(initial_month, month, initial_rent, board)
        values.append({
            'rent': initial_rent + info.total_percent * initial_rent,
            'info': info,
        })

    return values
