#!/usr/bin/make -f

# Portions of this file contributed by NIST are governed by the
# following statement:
#
# This software was developed at the National Institute of Standards
# and Technology by employees of the Federal Government in the course
# of their official duties. Pursuant to Title 17 Section 105 of the
# United States Code, this software is not subject to copyright
# protection within the United States. NIST assumes no responsibility
# whatsoever for its use by other parties, and makes no guarantees,
# expressed or implied, about its quality, reliability, or any other
# characteristic.
#
# We would appreciate acknowledgement if the software is used.

# This Makefile is incorporated to support versions of case-utils since
# 0.5.0 that had not yet incorporated rdf-toolkit-1.11.0.jar into their
# testing process.  The Makefile is adapted from the `/lib` directory of
# UCO at version 1.2.0.

SHELL := /bin/bash

all: \
  rdf-toolkit.jar

rdf-toolkit.jar:
	test -r rdf-toolkit.jar.sha512
	rm -f $@_
	# Try retrieval from files.caseontology.org.
	wget \
	  --output-document $@_ \
	  https://files.caseontology.org/rdf-toolkit-1.11.0.jar
	test \
	  "x$$(openssl dgst -sha512 $@_ | awk '{print($$NF)}')" \
	  == \
	  "x$$(head -n1 rdf-toolkit.jar.sha512)"
	mv $@_ $@
