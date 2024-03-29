#!/usr/bin/make -f

# Portions of this file contributed by NIST are governed by the following
# statement:
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

SHELL := /bin/bash

top_srcdir := $(shell cd ../../.. ; pwd)

tests_srcdir := $(top_srcdir)/tests

case_srcdir := $(top_srcdir)/dependencies/CASE

RDF_TOOLKIT_JAR := $(case_srcdir)/dependencies/UCO/lib/rdf-toolkit.jar

all: \
  kb.json \
  sample.txt.json \
  sample.txt-nocompact.json

check: \
  kb.json \
  kb_validation.ttl \
  sample.txt.json \
  sample.txt-nocompact.json
	source $(tests_srcdir)/venv/bin/activate \
	  && pytest \
	    --log-level=DEBUG

clean:
	@rm -f \
	  *.done.log \
	  *.json \
	  *.ttl \
	  sample.txt

kb.json: \
  kb.ttl \
  $(RDF_TOOLKIT_JAR) \
  $(tests_srcdir)/src/compact.py
	java -jar $(RDF_TOOLKIT_JAR) \
	  --infer-base-iri \
	  --inline-blank-nodes \
	  --source $< \
	  --source-format turtle \
	  --target __$@ \
	  --target-format json-ld
	source $(tests_srcdir)/venv/bin/activate \
	  && python3 $(tests_srcdir)/src/compact.py \
	    _$@ \
	    __$@
	rm __$@
	mv _$@ $@

kb.ttl: \
  sample.txt.ttl \
  sample.txt-disable_hashes.ttl \
  sample.txt-nocompact.json
	source $(tests_srcdir)/venv/bin/activate \
	  && rdfpipe \
	    --output-format turtle \
	    sample.txt.ttl \
	    sample.txt-disable_hashes.ttl \
	    > __$@
	java -jar $(RDF_TOOLKIT_JAR) \
	  --infer-base-iri \
	  --inline-blank-nodes \
	  --source __$@ \
	  --source-format turtle \
	  --target _$@ \
	  --target-format turtle
	rm __$@
	mv _$@ $@

#TODO - kb.json has a conversion error with context dictionary construction and custom datatypes.
kb_validation.ttl: \
  $(top_srcdir)/case_utils/case_validate/__init__.py \
  $(top_srcdir)/case_utils/case_validate/validate_types.py \
  $(top_srcdir)/case_utils/case_validate/validate_utils.py \
  kb.ttl
	source $(tests_srcdir)/venv/bin/activate \
	  && case_validate \
	    --format turtle \
	    kb.ttl \
	    > __$@
	java -jar $(RDF_TOOLKIT_JAR) \
	  --inline-blank-nodes \
	  --source __$@ \
	  --source-format turtle \
	  --target _$@ \
	  --target-format turtle
	rm __$@
	mv _$@ $@

sample.txt.done.log: \
  $(tests_srcdir)/.venv.done.log \
  sample_txt.py
	source $(tests_srcdir)/venv/bin/activate \
	  && python3 sample_txt.py \
	    sample.txt
	touch $@

# Display difference between rdflib default output and compacted output.
sample.txt.json: \
  $(tests_srcdir)/src/compact.py \
  $(tests_srcdir)/src/isomorphic_diff.py \
  $(top_srcdir)/case_utils/case_file/__init__.py \
  $(top_srcdir)/case_utils/inherent_uuid.py \
  $(top_srcdir)/case_utils/namespace.py \
  sample.txt-nocompact.json
	rm -f $@ _$@ __$@
	export CDO_DEMO_NONRANDOM_UUID_BASE="$(top_srcdir)" \
	  && source $(tests_srcdir)/venv/bin/activate \
	    && case_file \
	      --debug \
	      --use-deterministic-uuids \
	      __$@ \
	      sample.txt
	source $(tests_srcdir)/venv/bin/activate \
	  && python3 $(tests_srcdir)/src/compact.py \
	    _$@ \
	    __$@
	rm __$@
	# To avoid making noisy, uninformative updates from blank node identifiers, only move the new file into place if it is not isomorphic with the Git-tracked version of the target.
	git checkout -- $@ \
	  || true
	if [ -r $@ ]; then \
	  if ( source $(tests_srcdir)/venv/bin/activate && python3 $(tests_srcdir)/src/isomorphic_diff.py $@ _$@ ) ; then \
	    rm _$@ ; \
	  fi ; \
	fi
	if [ -r _$@ ]; then \
	  mv _$@ $@ ; \
	fi
	test ! -r _$@
	touch $@

sample.txt.ttl: \
  $(RDF_TOOLKIT_JAR) \
  $(tests_srcdir)/.venv.done.log \
  $(top_srcdir)/case_utils/case_file/__init__.py \
  $(top_srcdir)/case_utils/inherent_uuid.py \
  $(top_srcdir)/case_utils/namespace.py \
  sample.txt.done.log
	rm -f _$@ __$@
	export CDO_DEMO_NONRANDOM_UUID_BASE="$(top_srcdir)" \
	  && source $(tests_srcdir)/venv/bin/activate \
	    && case_file \
	      --debug \
	      --use-deterministic-uuids \
	      __$@ \
	      sample.txt
	java -jar $(RDF_TOOLKIT_JAR) \
	  --infer-base-iri \
	  --inline-blank-nodes \
	  --source __$@ \
	  --source-format turtle \
	  --target _$@ \
	  --target-format turtle
	rm __$@
	mv _$@ $@

sample.txt-disable_hashes.ttl: \
  $(RDF_TOOLKIT_JAR) \
  $(tests_srcdir)/.venv.done.log \
  $(top_srcdir)/case_utils/case_file/__init__.py \
  $(top_srcdir)/case_utils/inherent_uuid.py \
  $(top_srcdir)/case_utils/namespace.py \
  sample.txt.done.log
	rm -f _$@ __$@
	export CDO_DEMO_NONRANDOM_UUID_BASE="$(top_srcdir)" \
	  && source $(tests_srcdir)/venv/bin/activate \
	    && case_file \
	      --debug \
	      --disable-hashes \
	      --use-deterministic-uuids \
	      __$@ \
	      sample.txt
	java -jar $(RDF_TOOLKIT_JAR) \
	  --infer-base-iri \
	  --inline-blank-nodes \
	  --source __$@ \
	  --source-format turtle \
	  --target _$@ \
	  --target-format turtle
	rm __$@
	mv _$@ $@

# Confirm format guesser will generate a JSON-LD file.
sample.txt-nocompact.json: \
  $(tests_srcdir)/.venv.done.log \
  $(tests_srcdir)/src/isomorphic_diff.py \
  $(top_srcdir)/case_utils/case_file/__init__.py \
  $(top_srcdir)/case_utils/inherent_uuid.py \
  $(top_srcdir)/case_utils/namespace.py \
  sample.txt.done.log
	rm -f _$@
	export CDO_DEMO_NONRANDOM_UUID_BASE="$(top_srcdir)" \
	  && source $(tests_srcdir)/venv/bin/activate \
	    && case_file \
	      --debug \
	      --use-deterministic-uuids \
	      _$@ \
	      sample.txt
	# To avoid making noisy, uninformative updates from blank node identifiers, only move the new file into place if it is not isomorphic with the Git-tracked version of the target.
	git checkout -- $@ \
	  || true
	if [ -r $@ ]; then \
	  if ( source $(tests_srcdir)/venv/bin/activate && python3 $(tests_srcdir)/src/isomorphic_diff.py $@ _$@ ) ; then \
	    rm _$@ ; \
	  fi ; \
	fi
	if [ -r _$@ ]; then \
	  mv _$@ $@ ; \
	fi
	test ! -r _$@
	touch $@
