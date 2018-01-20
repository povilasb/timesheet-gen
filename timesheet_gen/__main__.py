from jinja2 import Template
import json

from .timeflow_parser import time_info_for_month
from .date_utils import this_month, last_month


def main():
    personal_info = read_json('data/personal_info.json')
    time_info = time_info_for_month(this_month())
    personal_info.update(time_info)

    template = load_template('templates/timesheet.jinja2.tex')
    page = template.render(personal_info)
    print(page)


def read_json(fname: str) -> dict:
    return json.loads(read_file(fname))


def load_template(fname: str) -> Template:
    content = read_file(fname)
    return Template(content)


def read_file(fname: str) -> str:
    with open(fname, 'r') as f:
        return f.read()


main()
