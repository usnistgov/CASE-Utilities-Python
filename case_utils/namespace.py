#!/usr/bin/env python3

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

"""
This module provides importable constants for namespaces.

To use, add "from case_utils.namespace import *".  Namespace variables starting with "NS_" are imported.  As needs are demonstrated in CASE tooling (both in case_utils and from downstream requests), namespaces will also be imported from rdflib for a consistent "NS_*" spelling.
"""

__version__ = "0.2.2"

import rdflib

NS_OWL = rdflib.OWL
NS_RDF = rdflib.RDF
NS_RDFS = rdflib.RDFS
NS_SH = rdflib.SH
NS_XSD = rdflib.XSD

NS_CASE_INVESTIGATION = rdflib.Namespace(
    "https://ontology.caseontology.org/case/investigation/"
)
NS_CASE_VOCABULARY = rdflib.Namespace(
    "https://ontology.caseontology.org/case/vocabulary/"
)
NS_CO = rdflib.Namespace("http://purl.org/co/")
NS_UCO_ACTION = rdflib.Namespace(
    "https://ontology.unifiedcyberontology.org/uco/action/"
)
NS_UCO_ANALYSIS = rdflib.Namespace(
    "https://ontology.unifiedcyberontology.org/uco/analysis/"
)
NS_UCO_CONFIGURATION = rdflib.Namespace(
    "https://ontology.unifiedcyberontology.org/uco/configuration/"
)
NS_UCO_CORE = rdflib.Namespace("https://ontology.unifiedcyberontology.org/uco/core/")
NS_UCO_IDENTITY = rdflib.Namespace(
    "https://ontology.unifiedcyberontology.org/uco/identity/"
)
NS_UCO_LOCATION = rdflib.Namespace(
    "https://ontology.unifiedcyberontology.org/uco/location/"
)
NS_UCO_MARKING = rdflib.Namespace(
    "https://ontology.unifiedcyberontology.org/uco/marking/"
)
NS_UCO_OBSERVABLE = rdflib.Namespace(
    "https://ontology.unifiedcyberontology.org/uco/observable/"
)
NS_UCO_PATTERN = rdflib.Namespace(
    "https://ontology.unifiedcyberontology.org/uco/pattern/"
)
NS_UCO_ROLE = rdflib.Namespace("https://ontology.unifiedcyberontology.org/uco/role/")
NS_UCO_TIME = rdflib.Namespace("https://ontology.unifiedcyberontology.org/uco/time/")
NS_UCO_TOOL = rdflib.Namespace("https://ontology.unifiedcyberontology.org/uco/tool/")
NS_UCO_TYPES = rdflib.Namespace("https://ontology.unifiedcyberontology.org/uco/types/")
NS_UCO_VICTIM = rdflib.Namespace(
    "https://ontology.unifiedcyberontology.org/uco/victim/"
)
NS_UCO_VOCABULARY = rdflib.Namespace(
    "https://ontology.unifiedcyberontology.org/uco/vocabulary/"
)
