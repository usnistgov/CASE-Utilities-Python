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

top_srcdir := $(shell cd ../../.. ; pwd)

tests_srcdir := $(top_srcdir)/tests

all: \
  subclass-explicit-none.md \
  subclass-implicit-any.md \
  w3-output.html \
  w3-output.md

.PHONY: \
  check-subclass \
  check-subclass-explicit-none \
  check-subclass-implicit-any \
  check-w3-html \
  check-w3-markdown

.PRECIOUS: \
  subclass-% \
  w3-output.%

check: \
  check-w3-html \
  check-w3-markdown \
  check-subclass

check-subclass: \
  check-subclass-explicit-none \
  check-subclass-implicit-any

check-subclass-explicit-none: \
  .check-subclass-explicit-none.md \
  subclass-explicit-none.md
	diff $^

check-subclass-implicit-any: \
  .check-subclass-implicit-any.md \
  subclass-implicit-any.md
	diff $^

check-w3-html: \
  .check-w3-output.html \
  w3-output.html
	diff $^

check-w3-markdown: \
  .check-w3-output.md \
  w3-output.md
	diff $^

clean:
	@rm -rf \
	  __pycache__
	@rm -f \
	  *.html \
	  *.md \
	  _*

subclass-explicit-none.md: \
  $(tests_srcdir)/.venv.done.log \
  $(top_srcdir)/case_utils/case_sparql_select/__init__.py \
  $(top_srcdir)/case_utils/ontology/__init__.py \
  $(top_srcdir)/case_utils/ontology/version_info.py \
  subclass.json \
  subclass.sparql
	source $(tests_srcdir)/venv/bin/activate \
	  && case_sparql_select \
	    --built-version none \
	    _$@ \
	    subclass.sparql \
	    subclass.json
	mv _$@ $@

subclass-implicit-any.md: \
  $(tests_srcdir)/.venv.done.log \
  $(top_srcdir)/case_utils/case_sparql_select/__init__.py \
  $(top_srcdir)/case_utils/ontology/__init__.py \
  $(top_srcdir)/case_utils/ontology/version_info.py \
  subclass.json \
  subclass.sparql
	source $(tests_srcdir)/venv/bin/activate \
	  && case_sparql_select \
	    _$@ \
	    subclass.sparql \
	    subclass.json
	mv _$@ $@

w3-output.%: \
  $(tests_srcdir)/.venv.done.log \
  $(top_srcdir)/case_utils/case_sparql_select/__init__.py \
  $(top_srcdir)/case_utils/ontology/__init__.py \
  $(top_srcdir)/case_utils/ontology/version_info.py \
  w3-input-1.sparql \
  w3-input-2.ttl \
  w3-input-3.json
	source $(tests_srcdir)/venv/bin/activate \
	  && case_sparql_select \
	    _$@ \
	    w3-input-1.sparql \
	    w3-input-2.ttl \
	    w3-input-3.json
	mv _$@ $@
