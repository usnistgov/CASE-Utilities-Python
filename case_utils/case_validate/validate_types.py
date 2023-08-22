from typing import Set, Union

import rdflib


class ValidationResult:
    def __init__(
        self,
        conforms: bool,
        graph: Union[Exception, bytes, str, rdflib.Graph],
        text: str,
        undefined_concepts: Set[rdflib.URIRef],
    ) -> None:
        self.conforms = conforms
        self.graph = graph
        self.text = text
        self.undefined_concepts = undefined_concepts


class NonExistentCDOConceptWarning(UserWarning):
    """
    This class is used when a concept is encountered in the data graph that is not part of CDO ontologies, according to the --built-version flags and --ontology-graph flags.
    """

    pass


class NonExistentCASEVersionError(Exception):
    """
    This class is used when an invalid CASE version is requested that is not supported by the library.
    """

    pass
