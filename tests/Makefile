#!/usr/bin/make -f

# This software was developed at the National Institute of Standards
# and Technology by employees of the Federal Government in the course
# of their official duties. Pursuant to title 17 Section 105 of the
# United States Code this software is not subject to copyright
# protection and is in the public domain. NIST assumes no
# responsibility whatsoever for its use by other parties, and makes
# no guarantees, expressed or implied, about its quality,
# reliability, or any other characteristic.
#
# We would appreciate acknowledgement if the software is used.

SHELL := /bin/bash

top_srcdir := $(shell cd .. ; pwd)

srcdir := $(shell pwd)

PYTHON3 ?= $(shell which python3.9 2>/dev/null || which python3.8 2>/dev/null || which python3.7 2>/dev/null || which python3.6 2>/dev/null || which python3)

all: \
  all-case_file \
  all-case_sparql_construct \
  all-case_sparql_select

.PHONY: \
  all-case_file \
  all-case_sparql_construct \
  all-case_sparql_select \
  check-case_file \
  check-case_sparql_construct \
  check-case_sparql_select \
  check-isomorphic_diff \
  check-mypy \
  download

.venv.done.log: \
  $(top_srcdir)/.git_submodule_init.done.log \
  $(top_srcdir)/case_utils/__init__.py \
  $(top_srcdir)/setup.cfg \
  $(top_srcdir)/setup.py \
  requirements.txt
	rm -rf venv
	$(PYTHON3) -m venv \
	  venv
	source venv/bin/activate \
	  && pip install \
	    --upgrade \
	    pip \
	    setuptools \
	    wheel
	source venv/bin/activate \
	  && pip install \
	    --requirement requirements.txt
	source venv/bin/activate \
	  && cd $(top_srcdir) \
	    && pip install \
	      --editable \
	      .
	touch $@

all-case_file: \
  .venv.done.log
	$(MAKE) \
	  --directory case_file

all-case_sparql_construct: \
  .venv.done.log
	$(MAKE) \
	  --directory case_sparql_construct

all-case_sparql_select: \
  .venv.done.log
	# Only descend if python>=3.7, due to pandas dependency unsatisfiable in 3.6.x.
	# Boolean explanation: sys.exit(False) has exit status 0.
	venv/bin/python3 -c 'import sys ; sys.exit(not (sys.version_info < (3, 7)))' \
	  || $(MAKE) \
	    --directory case_sparql_select

# These check calls are provided in preferred run-order.
check: \
  check-isomorphic_diff \
  check-mypy \
  check-case_file \
  check-case_sparql_construct \
  check-case_sparql_select
	source venv/bin/activate \
	  && pytest \
	    --ignore case_file \
	    --ignore case_sparql_construct \
	    --ignore case_sparql_select \
	    --log-level=DEBUG

check-case_file: \
  .venv.done.log
	$(MAKE) \
	  --directory case_file \
	  check

check-case_sparql_construct: \
  .venv.done.log
	$(MAKE) \
	  --directory case_sparql_construct \
	  check

check-case_sparql_select: \
  .venv.done.log
	# Only descend if python>=3.7, due to pandas dependency unsatisfiable in 3.6.x.
	# Boolean explanation: sys.exit(False) has exit status 0.
	venv/bin/python3 -c 'import sys ; sys.exit(not (sys.version_info < (3, 7)))' \
	  || $(MAKE) \
	    --directory case_sparql_select \
	    check

check-isomorphic_diff: \
  .venv.done.log
	$(MAKE) \
	  --directory isomorphic_diff \
	  check

# mypy is called against specific members of the tests directory to avoid descending into the virtual environment.
check-mypy: \
  .venv.done.log
	source venv/bin/activate \
	  && mypy \
	    $(top_srcdir)/case_utils \
	    case_file \
	    case_sparql_construct \
	    case_utils \
	    hexbinary \
	    src

clean:
	@$(MAKE) \
	  --directory case_sparql_select \
	  clean
	@$(MAKE) \
	  --directory case_sparql_construct \
	  clean
	@$(MAKE) \
	  --directory case_file \
	  clean
	@rm -f \
	  .venv.done.log
	@rm -rf \
	  .pytest_cache \
	  venv

download: \
  .venv.done.log
