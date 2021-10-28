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
  all-case_test_examples \
  all-uco_test_examples

.PHONY: \
  all-case_test_examples \
  all-uco_test_examples \
  check-case_test_examples \
  check-uco_test_examples

all-case_test_examples:
	$(MAKE) \
	  --directory case_test_examples

all-uco_test_examples:
	$(MAKE) \
	  --directory uco_test_examples

check: \
  check-case_test_examples \
  check-uco_test_examples

check-case_test_examples:
	$(MAKE) \
	  --directory case_test_examples \
	  check

check-uco_test_examples:
	$(MAKE) \
	  --directory uco_test_examples \
	  check

clean:
	@$(MAKE) \
	  --directory case_test_examples \
	  clean
	@$(MAKE) \
	  --directory uco_test_examples \
	  clean
