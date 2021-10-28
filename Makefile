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

PYTHON3 ?= $(shell which python3.9 2>/dev/null || which python3.8 2>/dev/null || which python3.7 2>/dev/null || which python3.6 2>/dev/null || which python3)

all:

.PHONY: \
  download

.git_submodule_init.done.log: \
  .gitmodules
	# Log current submodule pointers.
	cd dependencies \
	  && git diff . \
	    | cat
	git submodule init dependencies/CASE-Examples-QC
	git submodule update dependencies/CASE-Examples-QC
	# Build an ontology terms list, which has a side effect of initiating further submodules.
	$(MAKE) \
	  --directory dependencies/CASE-Examples-QC \
	  download
	$(MAKE) \
	  --directory dependencies/CASE-Examples-QC/tests \
	  ontology_vocabulary.txt
	test -r dependencies/CASE/ontology/master/case.ttl \
	  || (git submodule init dependencies/CASE && git submodule update dependencies/CASE)
	test -r dependencies/CASE/ontology/master/case.ttl
	touch $@

check: \
  .git_submodule_init.done.log
	$(MAKE) \
	  PYTHON3=$(PYTHON3) \
	  --directory tests \
	  check

clean:
	@$(MAKE) \
	  --directory tests \
	  clean
	@rm -f \
	  .git_submodule_init.done.log
	@test ! -r dependencies/CASE/README.md \
	  || @$(MAKE) \
	    --directory dependencies/CASE \
	    clean
	@# Restore CASE validation output files that do not affect CASE build process.
	@test ! -r dependencies/CASE/README.md \
	  || ( \
	    cd dependencies/CASE \
	      && git checkout \
	        -- \
	        tests/examples \
	        || true \
	  )
	@#Remove flag files that are normally set after deeper submodules and rdf-toolkit are downloaded.
	@rm -f \
	  dependencies/CASE-Examples-QC/.git_submodule_init.done.log \
	  dependencies/CASE-Examples-QC/.lib.done.log

distclean: \
  clean
	@rm -rf \
	  build \
	  *.egg-info \
	  dist

download: \
  .git_submodule_init.done.log
	$(MAKE) \
	  --directory tests \
	  download
