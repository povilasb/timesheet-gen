from typing import List, Tuple
import json

from timeflow import utils, stats

from timesheet_gen.date_utils import Date, month_range, Month, Week


def main():
    month = Month('2018-04')
    w = month.weeks()
    time_info = time_info_for_month('2018-04')
    print(json.dumps(time_info, indent=2))


def time_info_for_month(month: str) -> dict:
    month = Month(month)
    time_info = {
        'start_date': month.first_day.uk_format,
        'end_date': month.last_day.uk_format,
        'total_hours': 0,
        'weeks': {},
    }

    log = utils.read_log_file_lines()
    for i, week in enumerate(month.weeks(), 1):
        info, hours = week_info(week, log)
        time_info['weeks'][i] = {
            'days': info,
            'total_hours': hours,
        }
        time_info['total_hours'] += hours
    return time_info


def week_info(week: Week, log: List[str]) -> Tuple[dict, float]:
    week_name = ['mo', 'tu', 'we', 'th', 'fr']
    info = {}
    total_hours = 0
    last_day = None

    for day in week.workdays():
        work_report, _breaks = stats.calculate_report(log, str(day), str(day))
        dinfo = day_info(day, work_report)
        last_day = week_name[day.weekday - 1]
        info[last_day] = dinfo
        total_hours += dinfo['hours']

    if last_day:
        info[last_day]['last_in_workweek'] = True

    return info, total_hours


def day_info(day: Date, report: dict) -> dict:
    info = {
        'date': day.uk_format,
        'description': '',
        'hours': 0,
        'last_in_workweek': False,
    }
    if len(report) > 0:
        total_seconds = 0
        for log in report.values():
            for seconds in log.values():
                total_seconds += seconds
        description = stats.create_report(report)
        info['description'] = description.replace('\n', '\\newline ')
        info['hours'] = total_seconds / 3600
    return info


if __name__ == '__main__':
    main()
