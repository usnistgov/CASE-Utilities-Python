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

__version__ = "0.2.1"

import warnings

import rdflib.util

from . import local_uuid

def guess_format(fpath, fmap=None):
    warnings.warn("The functionality in case_utils.guess_format is now upstream.  Please revise your code to use rdflib.util.guess_format.  The function arguments remain the same.  case_utils.guess_format will be removed in case_utils 0.4.0.", DeprecationWarning)

    return rdflib.util.guess_format(fpath, fmap)
