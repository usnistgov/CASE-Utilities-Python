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

import typing

import rdflib.plugins.sparql  # type: ignore

import case_utils

def _test_w3_templates_with_blank_nodes_result(
  filename : str
) -> None:
    ground_truth_positive = {
      ("Alice", "Hacker"),
      ("Bob", "Hacker")
    }
    ground_truth_negative : typing.Set[str] = set()

    graph = rdflib.Graph()
    graph.parse(filename)

    computed = set()
    query_string = """\
PREFIX vcard:   <http://www.w3.org/2001/vcard-rdf/3.0#>

SELECT ?lGivenName ?lFamilyName
WHERE {
  ?nNode
    vcard:givenName ?lGivenName ;
    vcard:familyName ?lFamilyName ;
    .
}
"""
    for result in graph.query(query_string):
        (
          l_given_name,
          l_family_name
        ) = result
        computed.add((
          l_given_name.toPython(),
          l_family_name.toPython()
        ))
    assert computed == ground_truth_positive

def test_w3_templates_with_blank_nodes_result_json() -> None:
    _test_w3_templates_with_blank_nodes_result("w3-output.json")

def test_w3_templates_with_blank_nodes_result_turtle() -> None:
    _test_w3_templates_with_blank_nodes_result("w3-output.ttl")
