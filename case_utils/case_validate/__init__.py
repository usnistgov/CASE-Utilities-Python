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
import logging
import os
import sys
import warnings
from typing import Any, Dict, List, Optional, Tuple, Union

import pyshacl  # type: ignore
import rdflib
from rdflib import Graph

from case_utils.case_validate.validate_types import (
    NonExistentCDOConceptWarning,
    ValidationResult,
)
from case_utils.case_validate.validate_utils import (
    get_invalid_cdo_concepts,
    get_ontology_graph,
)
from case_utils.ontology.version_info import (
    CURRENT_CASE_VERSION,
    built_version_choices_list,
)

_logger = logging.getLogger(os.path.basename(__file__))


def validate(
    input_file: str,
    *args: Any,
    case_version: Optional[str] = None,
    supplemental_graphs: Optional[List[str]] = None,
    abort_on_first: bool = False,
    inference: Optional[str] = "none",
    **kwargs: Any,
) -> ValidationResult:
    """
    Validate the given data graph against the given CASE ontology version and supplemental graphs.
    :param *args: The positional arguments to pass to the underlying pyshacl.validate function.
    :param input_file: The path to the file containing the data graph to validate.
    :param case_version: The version of the CASE ontology to use (e.g. 1.2.0).  If None, the most recent version will
        be used.
    :param supplemental_graphs: The supplemental graphs to use.  If None, no supplemental graphs will be used.
    :param abort_on_first: Whether to abort on the first validation error.
    :param inference: The type of inference to use.  If "none", no inference will be used.
    :param **kwargs: The keyword arguments to pass to the underlying pyshacl.validate function.
    :return: The validation result object containing the defined properties.
    """
    # Convert the data graph string to a rdflib.Graph object.
    data_graph = rdflib.Graph()
    data_graph.parse(input_file)

    # Get the ontology graph from the case_version and supplemental_graphs arguments
    ontology_graph: Graph = get_ontology_graph(case_version, supplemental_graphs)

    # Get the undefined CDO concepts
    undefined_cdo_concepts = get_invalid_cdo_concepts(data_graph, ontology_graph)

    # Validate data graph against ontology graph.
    validate_result: Tuple[
        bool, Union[Exception, bytes, str, rdflib.Graph], str
    ] = pyshacl.validate(
        data_graph,
        *args,
        shacl_graph=ontology_graph,
        ont_graph=ontology_graph,
        inference=inference,
        meta_shacl=False,
        abort_on_first=abort_on_first,
        allow_infos=False,
        allow_warnings=False,
        debug=False,
        do_owl_imports=False,
        **kwargs,
    )

    # Relieve RAM of the data graph after validation has run.
    del data_graph

    return ValidationResult(
        validate_result[0],
        validate_result[1],
        validate_result[2],
        undefined_cdo_concepts,
    )


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

    # Get the ontology graph based on the CASE version and supplemental graphs specified by the CLI
    ontology_graph = get_ontology_graph(
        case_version=args.built_version, supplemental_graphs=args.ontology_graph
    )

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

    validate_result: Tuple[
        bool, Union[Exception, bytes, str, rdflib.Graph], str
    ] = pyshacl.validate(
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
        **validator_kwargs,
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
