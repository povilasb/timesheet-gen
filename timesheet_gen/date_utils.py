from typing import List

import maya
from timeflow import utils, stats


class Date:
    def __init__(self, date) -> None:
        self._inner = date

    @staticmethod
    def from_str(date: str) -> 'Date':
        return Date(maya.when(date))

    @property
    def weekday(self) -> int:
        return self._inner.weekday

    @property
    def month(self) -> int:
        return self._inner.month

    def snap(self, instruction: str) -> 'Date':
        return Date(self._inner.snap(instruction))

    def next_week(self) -> 'Date':
        """Returns Monday of the next week."""
        return Date(self._inner.subtract(days=1).add(weeks=1).snap('@w+1d'))

    def __str__(self) -> str:
        return self._inner.datetime().strftime('%Y-%m-%d')

    def __repr__(self) -> str:
        return 'Date({})'.format(self)

    @property
    def uk_format(self) -> str:
        return self._inner.datetime().strftime('%d/%m/%Y')


class Week:
    """Week starts from Monday."""

    def __init__(self, start: Date) -> None:
        self.start = start

    @staticmethod
    def from_str(date: str) -> 'Week':
        return Week(Date.from_str(date))

    def workdays(self) -> List[Date]:
        day1 = self.start.weekday
        days = []
        for i in range(day1, 6):
            day = self.start.snap('+{}d'.format(i - day1))
            if day.month != self.start.month:
                break
            days.append(day)
        return days

    def starts_on_weekend(self) -> bool:
        return len(self.workdays()) == 0


class Month:
    def __init__(self, month: str) -> None:
        """
        Args:
            month: in format '%Y-%m', e.g. '2018-03'.
        """
        days = utils.get_month_range(month)
        self.first_day = Date.from_str(days[0])
        self.last_day = Date.from_str(days[1])

    def weeks(self) -> List[Week]:
        """
        Excludes weeks that start on weekend: Saturday or Sunday.

        Returns:
            work weeks
        """
        month_weeks = []
        curr_day = self.first_day
        while curr_day.month == self.first_day.month:
            week = Week(curr_day)
            if not week.starts_on_weekend():
                month_weeks.append(week)
            curr_day = curr_day.next_week()
        return month_weeks


def month_range(month: str) -> List[Date]:
    """Returns dates of this month."""
    date_from, date_to = utils.get_month_range(month)
    year, month = [int(i) for i in month.split('-')]
    last_day = int(date_to.split('-')[2])
    return [Date(format_date(year, month, d)) for d in range(1, last_day + 1)]


def format_date(year: int, month: int, day: int) -> str:
    return '{}-{:02}-{:02}'.format(year, month, day)


def this_month() -> str:
    """Returns current month in YYYY-MM format.
    This is the expected format by utilities from timeflow package.
    """
    date = maya.when('this month')
    return date.datetime().strftime('%Y-%m')


def last_month() -> str:
    date = maya.when('last month')
    return date.datetime().strftime('%Y-%m')
