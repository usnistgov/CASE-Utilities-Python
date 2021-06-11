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

top_srcdir := $(shell cd ../.. ; pwd)

tests_srcdir := $(top_srcdir)/tests

all: \
  output.ttl

check: \
  output.ttl
	source $(tests_srcdir)/venv/bin/activate \
	  && pytest \
	    --log-level=DEBUG

clean:
	@rm -rf \
	  __pycache__
	@rm -f \
	  output.ttl \
	  _*

output.ttl: \
  $(tests_srcdir)/.venv.done.log \
  input-1.sparql \
  input-2.ttl \
  input-3.json
	source $(tests_srcdir)/venv/bin/activate \
	  && case_sparql_construct \
	    _$@ \
	    input-1.sparql \
	    input-2.ttl \
	    input-3.json
	mv _$@ $@
