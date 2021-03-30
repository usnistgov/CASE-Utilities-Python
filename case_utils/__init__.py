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

import rdflib.util

from . import local_uuid

def guess_format(fpath, fmap=None):
    """
    This function is a wrapper around rdflib.util.guess_format(), adding that the .json extension should be recognized as JSON-LD.

    :param fpath: File path.
    :type fpath: string

    :param fmap: Mapper dictionary; see rdflib.util.guess_format() for further description.  Note that as in rdflib 5.0.0, supplying this argument overwrites, not augments, the suffix format map used by rdflib.
    :type fmap: dict

    :returns: RDF file format, fit for rdflib.Graph.parse() or .serialize(); or, None if file extension not mapped.
    :rtype: string
    """

    assert fmap is None or isinstance(fmap, dict), "Type check failed"

    if fmap is None:
        updated_fmap = {key:rdflib.util.SUFFIX_FORMAT_MAP[key] for key in rdflib.util.SUFFIX_FORMAT_MAP}
        if not "json" in updated_fmap:
            updated_fmap["json"] = "json-ld"
    else:
        updated_fmap = {k:fmap[k] for k in fmap}

    return rdflib.util.guess_format(fpath, updated_fmap)
