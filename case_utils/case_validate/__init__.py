#!/usr/bin/env python3

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

"""
This script provides a wrapper to the pySHACL command line tool,
available here:
https://github.com/RDFLib/pySHACL

Portions of the pySHACL command line interface are preserved and passed
through to the underlying pySHACL validation functionality.

Other portions of the pySHACL command line interface are adapted to
CASE, specifically to support CASE and UCO as ontologies that store
subclass hierarchy and node shapes together (rather than as separate
ontology and shape graphs).  More specifically to CASE, if no particular
ontology or shapes graph is requested, the most recent version of CASE
will be used.  (That most recent version is shipped with this package as
a monolithic file; see case_utils.ontology if interested in further
details.)
"""

__version__ = "0.3.0"

import argparse
import importlib.resources
import logging
import os
import sys
import warnings
from typing import Dict, Set, Tuple, Union

import pyshacl  # type: ignore
import rdflib

import case_utils.ontology
from case_utils.ontology.version_info import (
    CURRENT_CASE_VERSION,
    built_version_choices_list,
)

NS_OWL = rdflib.OWL
NS_RDF = rdflib.RDF
NS_RDFS = rdflib.RDFS
NS_SH = rdflib.SH

_logger = logging.getLogger(os.path.basename(__file__))


class NonExistentCDOConceptWarning(UserWarning):
    """
    This class is used when a concept is encountered in the data graph that is not part of CDO ontologies, according to the --built-version flags and --ontology-graph flags.
    """

    pass


def concept_is_cdo_concept(n_concept: rdflib.URIRef) -> bool:
    concept_iri = str(n_concept)
    return concept_iri.startswith(
        "https://ontology.unifiedcyberontology.org/"
    ) or concept_iri.startswith("https://ontology.caseontology.org/")


def get_invalid_cdo_concepts(
    data_graph: rdflib.Graph, ontology_graph: rdflib.Graph
) -> Set[rdflib.URIRef]:
    """
    Get the set of concepts in the data graph that are not part of the CDO ontologies as specified with the ontology_graph argument.

    :param data_graph: The data graph to validate.
    :param ontology_graph: The ontology graph to use for validation.
    :return: The list of concepts in the data graph that are not part of the CDO ontology.

    >>> from case_utils.namespace import NS_RDF, NS_OWL, NS_UCO_CORE
    >>> from rdflib import Graph, Literal, Namespace, URIRef
    >>> # Define a namespace for a knowledge base, and a namespace for custom extensions.
    >>> ns_kb = Namespace("http://example.org/kb/")
    >>> ns_ex = Namespace("http://example.org/ontology/")
    >>> dg = Graph()
    >>> og = Graph()
    >>> # Use an ontology graph in review that includes only a single class and a single property excerpted from UCO, but also a single custom property.
    >>> _ = og.add((NS_UCO_CORE.UcoObject, NS_RDF.type, NS_OWL.Class))
    >>> _ = og.add((NS_UCO_CORE.name, NS_RDF.type, NS_OWL.DatatypeProperty))
    >>> _ = og.add((ns_ex.ourCustomProperty, NS_RDF.type, NS_OWL.DatatypeProperty))
    >>> # Define an individual.
    >>> n_uco_object = ns_kb["UcoObject-f494d239-d9fd-48da-bc07-461ba86d8c6c"]
    >>> n_uco_object
    rdflib.term.URIRef('http://example.org/kb/UcoObject-f494d239-d9fd-48da-bc07-461ba86d8c6c')
    >>> # Review a data graph that includes only the single individual, class typo'd (capitalized incorrectly), but property OK.
    >>> _ = dg.add((n_uco_object, NS_RDF.type, NS_UCO_CORE.UCOObject))
    >>> _ = dg.add((n_uco_object, NS_UCO_CORE.name, Literal("Test")))
    >>> _ = dg.add((n_uco_object, ns_ex.customProperty, Literal("Custom Value")))
    >>> invalid_cdo_concepts = get_invalid_cdo_concepts(dg, og)
    >>> invalid_cdo_concepts
    {rdflib.term.URIRef('https://ontology.unifiedcyberontology.org/uco/core/UCOObject')}
    >>> # Note that the property "ourCustomProperty" was typo'd in the data graph, but this was not reported.
    >>> assert ns_ex.ourCustomProperty not in invalid_cdo_concepts
    """
    # Construct set of CDO concepts for data graph concept-existence review.
    cdo_concepts: Set[rdflib.URIRef] = set()

    for n_structural_class in [
        NS_OWL.Class,
        NS_OWL.AnnotationProperty,
        NS_OWL.DatatypeProperty,
        NS_OWL.ObjectProperty,
        NS_RDFS.Datatype,
        NS_SH.NodeShape,
        NS_SH.PropertyShape,
        NS_SH.Shape,
    ]:
        for ontology_triple in ontology_graph.triples(
            (None, NS_RDF.type, n_structural_class)
        ):
            if not isinstance(ontology_triple[0], rdflib.URIRef):
                continue
            if concept_is_cdo_concept(ontology_triple[0]):
                cdo_concepts.add(ontology_triple[0])
    for n_ontology_predicate in [
        NS_OWL.backwardCompatibleWith,
        NS_OWL.imports,
        NS_OWL.incompatibleWith,
        NS_OWL.priorVersion,
        NS_OWL.versionIRI,
    ]:
        for ontology_triple in ontology_graph.triples(
            (None, n_ontology_predicate, None)
        ):
            assert isinstance(ontology_triple[0], rdflib.URIRef)
            assert isinstance(ontology_triple[2], rdflib.URIRef)
            cdo_concepts.add(ontology_triple[0])
            cdo_concepts.add(ontology_triple[2])
    for ontology_triple in ontology_graph.triples((None, NS_RDF.type, NS_OWL.Ontology)):
        if not isinstance(ontology_triple[0], rdflib.URIRef):
            continue
        cdo_concepts.add(ontology_triple[0])

    # Also load historical ontology and version IRIs.
    ontology_and_version_iris_data = importlib.resources.read_text(
        case_utils.ontology, "ontology_and_version_iris.txt"
    )
    for line in ontology_and_version_iris_data.split("\n"):
        cleaned_line = line.strip()
        if cleaned_line == "":
            continue
        cdo_concepts.add(rdflib.URIRef(cleaned_line))

    data_cdo_concepts: Set[rdflib.URIRef] = set()
    for data_triple in data_graph.triples((None, None, None)):
        for data_triple_member in data_triple:
            if isinstance(data_triple_member, rdflib.URIRef):
                if concept_is_cdo_concept(data_triple_member):
                    data_cdo_concepts.add(data_triple_member)
            elif isinstance(data_triple_member, rdflib.Literal):
                if isinstance(data_triple_member.datatype, rdflib.URIRef):
                    if concept_is_cdo_concept(data_triple_member.datatype):
                        data_cdo_concepts.add(data_triple_member.datatype)

    return data_cdo_concepts - cdo_concepts


def main() -> None:
    parser = argparse.ArgumentParser(
        description="CASE wrapper to pySHACL command line tool."
    )

    # Configure debug logging before running parse_args, because there
    # could be an error raised before the construction of the argument
    # parser.
    logging.basicConfig(
        level=logging.DEBUG
        if ("--debug" in sys.argv or "-d" in sys.argv)
        else logging.INFO
    )

    # Add arguments specific to case_validate.
    parser.add_argument(
        "-d", "--debug", action="store_true", help="Output additional runtime messages."
    )
    parser.add_argument(
        "--built-version",
        choices=tuple(built_version_choices_list),
        default="case-" + CURRENT_CASE_VERSION,
        help="Monolithic aggregation of CASE ontology files at certain versions.  Does not require networking to use.  Default is most recent CASE release.  Passing 'none' will mean no pre-built CASE ontology versions accompanying this tool will be included in the analysis.",
    )
    parser.add_argument(
        "--ontology-graph",
        action="append",
        help="Combined ontology (i.e. subclass hierarchy) and shapes (SHACL) file, in any format accepted by rdflib recognized by file extension (e.g. .ttl).  Will supplement ontology selected by --built-version.  Can be given multiple times.",
    )

    # Inherit arguments from pyshacl.
    parser.add_argument(
        "--abort",
        action="store_true",
        help="(As with pyshacl CLI) Abort on first invalid data.",
    )
    parser.add_argument(
        "--allow-info",
        "--allow-infos",
        dest="allow_infos",
        action="store_true",
        default=False,
        help="(As with pyshacl CLI) Shapes marked with severity of Info will not cause result to be invalid.",
    )
    parser.add_argument(
        "-w",
        "--allow-warning",
        "--allow-warnings",
        action="store_true",
        dest="allow_warnings",
        help="(As with pyshacl CLI) Shapes marked with severity of Warning or Info will not cause result to be invalid.",
    )
    parser.add_argument(
        "-f",
        "--format",
        choices=("human", "turtle", "xml", "json-ld", "nt", "n3"),
        default="human",
        help="(ALMOST as with pyshacl CLI) Choose an output format. Default is \"human\".  Difference: 'table' not provided.",
    )
    parser.add_argument(
        "-im",
        "--imports",
        action="store_true",
        help="(As with pyshacl CLI) Allow import of sub-graphs defined in statements with owl:imports.",
    )
    # NOTE: The "ontology graph" in the --inference help is the mix of the SHACL shapes graph and OWL ontology (or RDFS schema) graph.
    parser.add_argument(
        "-i",
        "--inference",
        choices=("none", "rdfs", "owlrl", "both"),
        help='(As with pyshacl CLI) Choose a type of inferencing to run against the Data Graph before validating. The default behavior if this flag is not provided is to behave as "none", if not using the --metashacl flag.  The default behavior when using the --metashacl flag will apply "rdfs" inferencing to the ontology graph, but the data graph will still have no inferencing applied.  If the --inference flag is provided, it will apply to both the ontology graph, and the data graph.',
    )
    parser.add_argument(
        "-m",
        "--metashacl",
        dest="metashacl",
        action="store_true",
        default=False,
        help="(As with pyshacl CLI) Validate the SHACL Shapes graph against the shacl-shacl Shapes Graph before validating the Data Graph.",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output",
        nargs="?",
        type=argparse.FileType("x"),
        help='(ALMOST as with pyshacl CLI) Send output to a file.  If absent, output will be written to stdout.  Difference: If specified, file is expected not to exist.  Clarification: Does NOT influence --format flag\'s default value of "human".  (I.e., any machine-readable serialization format must be specified with --format.)',
        default=sys.stdout,
    )

    parser.add_argument("in_graph", nargs="+")

    args = parser.parse_args()

    data_graph = rdflib.Graph()
    for in_graph in args.in_graph:
        _logger.debug("in_graph = %r.", in_graph)
        data_graph.parse(in_graph)

    ontology_graph = rdflib.Graph()
    if args.built_version != "none":
        ttl_filename = args.built_version + ".ttl"
        _logger.debug("ttl_filename = %r.", ttl_filename)
        ttl_data = importlib.resources.read_text(case_utils.ontology, ttl_filename)
        ontology_graph.parse(data=ttl_data, format="turtle")
    if args.ontology_graph:
        for arg_ontology_graph in args.ontology_graph:
            _logger.debug("arg_ontology_graph = %r.", arg_ontology_graph)
            ontology_graph.parse(arg_ontology_graph)

    # Get the list of undefined CDO concepts in the graph
    undefined_cdo_concepts = get_invalid_cdo_concepts(data_graph, ontology_graph)

    for undefined_cdo_concept in sorted(undefined_cdo_concepts):
        warnings.warn(undefined_cdo_concept, NonExistentCDOConceptWarning)
    undefined_cdo_concepts_message = (
        "There were %d concepts with CDO IRIs in the data graph that are not in the ontology graph."
        % len(undefined_cdo_concepts)
    )

    # Determine output format.
    # pySHACL's determination of output formatting is handled solely
    # through the -f flag.  Other CASE CLI tools handle format
    # determination by output file extension.  case_validate will defer
    # to pySHACL behavior, as other CASE tools don't (at the time of
    # this writing) have the value "human" as an output format.
    validator_kwargs: Dict[str, str] = dict()
    if args.format != "human":
        validator_kwargs["serialize_report_graph"] = args.format

    validate_result: Tuple[bool, Union[Exception, bytes, str, rdflib.Graph], str]
    validate_result = pyshacl.validate(
        data_graph,
        shacl_graph=ontology_graph,
        ont_graph=ontology_graph,
        inference=args.inference,
        meta_shacl=args.metashacl,
        abort_on_first=args.abort,
        allow_infos=True if args.allow_infos else False,
        allow_warnings=True if args.allow_warnings else False,
        debug=True if args.debug else False,
        do_owl_imports=True if args.imports else False,
        **validator_kwargs
    )

    # Relieve RAM of the data graph after validation has run.
    del data_graph

    conforms = validate_result[0]
    validation_graph = validate_result[1]
    validation_text = validate_result[2]

    # NOTE: The output logistics code is adapted from pySHACL's file
    # pyshacl/cli.py.  This section should be monitored for code drift.
    if args.format == "human":
        args.output.write(validation_text)
    else:
        if isinstance(validation_graph, rdflib.Graph):
            raise NotImplementedError(
                "rdflib.Graph expected not to be created from --format value %r."
                % args.format
            )
        elif isinstance(validation_graph, bytes):
            args.output.write(validation_graph.decode("utf-8"))
        elif isinstance(validation_graph, str):
            args.output.write(validation_graph)
        else:
            raise NotImplementedError(
                "Unexpected result type returned from validate: %r."
                % type(validation_graph)
            )

    if len(undefined_cdo_concepts) > 0:
        warnings.warn(undefined_cdo_concepts_message)
        if not args.allow_warnings:
            undefined_cdo_concepts_alleviation_message = "The data graph is SHACL-conformant with the CDO ontologies, but nonexistent-concept references raise Warnings with this tool.  Please either correct the concept names in the data graph; use the --ontology-graph flag to pass a corrected CDO ontology file, also using --built-version none; or, use the --allow-warnings flag."
            warnings.warn(undefined_cdo_concepts_alleviation_message)
            conforms = False

    sys.exit(0 if conforms else 1)


if __name__ == "__main__":
    main()
