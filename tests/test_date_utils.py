from hamcrest import assert_that, is_, contains
import pytest

from timesheet_gen.date_utils import Date, Week, Month


def describe_Date():
    def describe_next_week():
        @pytest.mark.parametrize('curr_day,next_week', [
            ('2018-03-01', '2018-03-05'),
            ('2018-03-05', '2018-03-12'),
            ('2018-03-11', '2018-03-12'),
            ('2018-03-26', '2018-04-02'),
        ])
        def it_returns_first_day_of_the_next_week(curr_day: str, next_week: str):
            curr_day = Date.from_str(curr_day)

            coming_monday = curr_day.next_week()

            assert_that(str(coming_monday), is_(next_week))
            assert_that(coming_monday.weekday, is_(1))


def describe_Week():
    def describe_workdays():
        @pytest.mark.parametrize('week_start,expected_days', [
            ('2018-03-01', ['2018-03-01', '2018-03-02']),
            ('2018-03-05', ['2018-03-05', '2018-03-06', '2018-03-07',
                            '2018-03-08', '2018-03-09']),
            ('2018-09-01', []),
            ('2018-07-30', ['2018-07-30', '2018-07-31']),
        ])
        def it_returns_first_day_of_the_next_week(week_start, expected_days):
            week = Week.from_str(week_start)

            workdays = [str(day) for day in week.workdays()]

            assert_that(workdays, is_(expected_days))

def describe_Month():
    def describe_weeks():
        def describe_weeks_starting_on_weekend_are_emitted():
            month = Month('2018-04')

            weeks = [str(w.start) for w in month.weeks()]

            assert_that(
                weeks,
                contains('2018-04-02', '2018-04-09', '2018-04-16',
                         '2018-04-23', '2018-04-30')
            )
