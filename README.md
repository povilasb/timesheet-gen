# About

This is my time sheet generator for MaidSafe.
It's a small tool written in Python 3 that reads JSON encoded work time info
and generates nice PDF time sheets.

Optionally it can generate time sheets from
[timeflow](https://github.com/trimailov/timeflow) log file.

## Dependencies

```bash
apt install texlive-latex-extra
```

## Usage

1. `cp data/personal_info.sample.json data/personal_info.json`
2. edit `data/personal_info.json` accordingly
3. `make` - this will generate time sheet in `out/timesheet.pdf`

## Known Issues

* Underscore is not allowed in task description. For some reasons latex fails
  to build document in such case.
* '&' symbol is special in latex and it is not escaped. So don't use it.
