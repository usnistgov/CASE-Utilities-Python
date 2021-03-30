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
  all-case_file

.PHONY: \
  all-case_file \
  check-case_file \
  check-isomorphic_diff \
  download

.venv.done.log: \
  $(top_srcdir)/.git_submodule_init.done.log \
  $(top_srcdir)/case_utils/__init__.py \
  $(top_srcdir)/case_utils/case_file/__init__.py \
  $(top_srcdir)/case_utils/local_uuid.py \
  $(top_srcdir)/setup.cfg \
  $(top_srcdir)/setup.py \
  requirements.txt
	rm -rf venv
	$(PYTHON3) -m virtualenv \
	  --python=$(PYTHON3) \
	  venv
	source venv/bin/activate \
	  && pip install \
	    --upgrade \
	    pip \
	    setuptools
	source venv/bin/activate \
	  && pip install \
	    --requirement requirements.txt
	source venv/bin/activate \
	  && cd $(top_srcdir) \
	    && python3 setup.py install
	touch $@

all-case_file: \
  .venv.done.log
	$(MAKE) \
	  --directory case_file

# These check calls are provided in preferred run-order.
check: \
  check-isomorphic_diff \
  check-case_file
	source venv/bin/activate \
	  && pytest \
	    --ignore case_file \
	    --log-level=DEBUG

check-case_file: \
  .venv.done.log
	$(MAKE) \
	  --directory case_file \
	  check

check-isomorphic_diff: \
  .venv.done.log
	$(MAKE) \
	  --directory isomorphic_diff \
	  check

clean:
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
