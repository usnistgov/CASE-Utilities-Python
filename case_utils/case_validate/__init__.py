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

__version__ = "0.1.0"

import argparse
import importlib.resources
import logging
import os
import pathlib
import sys
import typing

import rdflib  # type: ignore
import pyshacl  # type: ignore

import case_utils.ontology

from case_utils.ontology.version_info import *

_logger = logging.getLogger(os.path.basename(__file__))

def main() -> None:
    parser = argparse.ArgumentParser(description="CASE wrapper to PySHACL command line tool.")

    # Configure debug logging before running parse_args, because there could be an error raised before the construction of the argument parser.
    logging.basicConfig(level=logging.DEBUG if ("--debug" in sys.argv or "-d" in sys.argv) else logging.INFO)

    case_version_choices_list = ["none", "case-" + CURRENT_CASE_VERSION]

    # Add arguments specific to case_validate.
    parser.add_argument(
      '-d',
      '--debug',
      action='store_true',
      help='Output additional runtime messages.'
    )
    parser.add_argument(
      "--built-version",
      choices=tuple(case_version_choices_list),
      default="case-"+CURRENT_CASE_VERSION,
      help="Monolithic aggregation of CASE ontology files at certain versions.  Does not require networking to use.  Default is most recent CASE release."
    )
    parser.add_argument(
      "--ontology-graph",
      action="append",
      help="Combined ontology (i.e. subclass hierarchy) and shapes (SHACL) file, in any format accepted by rdflib recognized by file extension (e.g. .ttl).  Will supplement ontology selected by --built-version.  Can be given multiple times."
    )

    # Inherit arguments from pyshacl.
    parser.add_argument(
      '--abort',
      action='store_true',
      help='(As with pyshacl CLI) Abort on first invalid data.'
    )
    parser.add_argument(
      '-w',
      '--allow-warnings',
      action='store_true',
      help='(As with pyshacl CLI) Shapes marked with severity of Warning or Info will not cause result to be invalid.',
    )
    parser.add_argument(
      "-f",
      "--format",
      choices=('human', 'turtle', 'xml', 'json-ld', 'nt', 'n3'),
      default='human',
      help="(ALMOST as with pyshacl CLI) Choose an output format. Default is \"human\".  Difference: 'table' not provided."
    )
    parser.add_argument(
      '-im',
      '--imports',
      action='store_true',
      help='(As with pyshacl CLI) Allow import of sub-graphs defined in statements with owl:imports.',
    )
    parser.add_argument(
      '-i',
      '--inference',
      choices=('none', 'rdfs', 'owlrl', 'both'),
      default='none',
      help="(As with pyshacl CLI) Choose a type of inferencing to run against the Data Graph before validating. Default is \"none\".",
    )

    parser.add_argument("in_graph")

    args = parser.parse_args()

    data_graph = rdflib.Graph()
    data_graph.parse(args.in_graph)

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

    validate_result : typing.Tuple[
      bool,
      typing.Union[Exception, bytes, str, rdflib.Graph],
      str
    ]
    validate_result = pyshacl.validate(
      data_graph,
      shacl_graph=ontology_graph,
      ont_graph=ontology_graph,
      inference=args.inference,
      abort_on_first=args.abort,
      allow_warnings=True if args.allow_warnings else False,
      debug=True if args.debug else False,
      do_owl_imports=True if args.imports else False
    )

    # Relieve RAM of the data graph after validation has run.
    del data_graph

    conforms = validate_result[0]
    validation_graph = validate_result[1]
    validation_text = validate_result[2]

    if args.format == "human":
        sys.stdout.write(validation_text)
    else:
        if isinstance(validation_graph, rdflib.Graph):
            validation_graph_str = validation_graph.serialize(format=args.format)
            sys.stdout.write(validation_graph_str)
            del validation_graph_str
        elif isinstance(validation_graph, bytes):
            sys.stdout.write(validation_graph.decode("utf-8"))
        elif isinstance(validation_graph, str):
            sys.stdout.write(validation_graph)
        else:
            raise NotImplementedError("Unexpected result type returned from validate: %r." % type(validation_graph))

    sys.exit(0 if conforms else 1)
    
if __name__ == "__main__":
    main()
