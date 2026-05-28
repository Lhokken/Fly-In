# Makefile

.PHONY: all install run test lint clean

UV      = uv
PYTHON  = .venv/bin/python

export UV_CACHE_DIR=/sgoinfre/gcerrete/.cache/uv

all: install

install:
	$(UV) sync
	$(UV) pip install transformers outlines torch

run:
	$(UV) run python main.py --definition src/functions_definition.json --calling src/function_calling_tests.json

run2:
	$(UV) run python main.py --definition src/f2unctions_definition.json --calling src/f2unction_calling_tests.json

pub_grade:
	cd moulinette && python3 -m moulinette grade_student_answers --set public ../src/results.json

priv_grade:
	cd moulinette && python3 -m moulinette grade_student_answers --set private ../src/results.json

debug:
	$(UV) run python -m pdb main.py config.txt

# Run pdb in a shell
# 	Command		Short	What it does
# 	next		n		Execute next line (don't step into calls)
# 	step		s		Step into a function call
# 	continue	c		Run until next breakpoint
# 	quit		q		Exit debugger
# 	list		l		Show surrounding source code
# 	where		w		Print call stack
# 	up / down	u / d	Move up/down the call stack
# 	return		r		Run until current function returns
	
clean:
	rm -rf .venv

re: clean install

lint:
	$(UV) run flake8 main.py
	$(UV) run mypy main.py \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	$(UV) run flake8 *.py
	$(UV) run mypy . --strict

build:
	$(UV) build
