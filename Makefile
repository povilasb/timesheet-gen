src_dir := timesheet_gen

python ?= python3
virtualenv_dir ?= pyenv
pip := $(virtualenv_dir)/bin/pip
linter := $(virtualenv_dir)/bin/flake8
pytest := $(virtualenv_dir)/bin/py.test
py_requirements ?= requirements/prod.txt requirements/dev.txt

build_dir := $(CURDIR)/out

.PHONY: all
all: $(virtualenv_dir)
	mkdir -p $(build_dir)
	$(virtualenv_dir)/bin/python3 -m timesheet_gen > $(build_dir)/timesheet.tex
	pdflatex -output-directory $(build_dir) timesheet.tex

.PHONY: test
test: $(virtualenv_dir)
	PYTHONPATH=$(PYTHONPATH):. $(pytest) --cov=$(src_dir) tests

.PHONY: lint
lint: $(virtualenv_dir)
	$(linter) $(src_dir)

$(virtualenv_dir): $(py_requirements)
	$(python) -m venv $@
	for r in $^ ; do \
		$(pip) install -r $$r ; \
	done

.PHONY: clean
clean:
	rm -rf $(build_dir)
