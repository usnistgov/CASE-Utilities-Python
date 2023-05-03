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
This library provides supporting constants and functions for generating deterministic UUIDs (version 5) for UCO Hash and Facet nodes.
"""

import binascii
import re
import uuid
from typing import Dict, Optional, Tuple

from rdflib import Literal, URIRef

from case_utils.namespace import NS_UCO_VOCABULARY, NS_XSD

L_MD5 = Literal("MD5", datatype=NS_UCO_VOCABULARY.HashNameVocab)
L_SHA1 = Literal("SHA1", datatype=NS_UCO_VOCABULARY.HashNameVocab)
L_SHA256 = Literal("SHA256", datatype=NS_UCO_VOCABULARY.HashNameVocab)
L_SHA3_256 = Literal("SHA3-256", datatype=NS_UCO_VOCABULARY.HashNameVocab)
L_SHA3_512 = Literal("SHA3-512", datatype=NS_UCO_VOCABULARY.HashNameVocab)
L_SHA384 = Literal("SHA384", datatype=NS_UCO_VOCABULARY.HashNameVocab)
L_SHA512 = Literal("SHA512", datatype=NS_UCO_VOCABULARY.HashNameVocab)
L_SSDEEP = Literal("SSDEEP", datatype=NS_UCO_VOCABULARY.HashNameVocab)

# Key: hashMethod literal.
# Value: Tuple.
#   * Lowercase spelling
HASH_METHOD_CASTINGS: Dict[Literal, Tuple[str, Optional[int]]] = {
    L_MD5: ("md5", 32),
    L_SHA1: ("sha1", 40),
    L_SHA256: ("sha256", 64),
    L_SHA3_256: ("sha3-256", 64),
    L_SHA3_512: ("sha3-512", 128),
    L_SHA384: ("sha384", 96),
    L_SHA512: ("sha512", 128),
    L_SSDEEP: ("ssdeep", None),
}

RX_UUID = re.compile(
    "[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[0-9a-f]{4}-[0-9a-f]{12}$", re.IGNORECASE
)


def inherence_uuid(n_node: URIRef) -> uuid.UUID:
    node_iri = str(n_node)
    if len(node_iri) < 40 or RX_UUID.search(node_iri) is None:
        # <40 -> Too short to have a UUID and scheme.
        return uuid.uuid5(uuid.NAMESPACE_URL, node_iri)
    else:
        return uuid.uuid5(uuid.NAMESPACE_OID, node_iri[-36:])


def predicated_inherence_uuid(
    node_inherence_uuid: uuid.UUID, n_predicate: URIRef
) -> uuid.UUID:
    return uuid.uuid5(node_inherence_uuid, str(n_predicate))


def facet_inherence_uuid(
    predicated_inherence_uuid: uuid.UUID, n_facet_class: URIRef
) -> uuid.UUID:
    return uuid.uuid5(predicated_inherence_uuid, str(n_facet_class))


def hash_method_value_uuid(l_hash_method: Literal, l_hash_value: Literal) -> uuid.UUID:
    """
    The UUIDv5 seed data for Hash nodes is a URN following the scheme in this draft IETF memo:

    https://datatracker.ietf.org/doc/html/draft-thiemann-hash-urn-01

    Note that at the time of this writing, that memo was expired (expiration date 2004-03-04) and did not have a linked superseding document.
    """

    if l_hash_value.datatype != NS_XSD.hexBinary:
        raise ValueError("Expected hexBinary datatype for l_hash_value.")
    hash_value_str: str = binascii.hexlify(l_hash_value.toPython()).decode().lower()

    hash_method_str = HASH_METHOD_CASTINGS[l_hash_method][0]

    urn_template = "urn:hash::%s:%s"
    urn_populated = urn_template % (hash_method_str, hash_value_str)

    return uuid.uuid5(uuid.NAMESPACE_URL, urn_populated)
