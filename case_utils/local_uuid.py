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
This library was a wrapper for uuid, provided to generate repeatable UUIDs if requested.  It is now a temporary re-export of functionality migrated to cdo_local_uuid.
"""

__version__ = "0.4.1"

__all__ = ["configure", "local_uuid"]

import warnings

from cdo_local_uuid import configure, local_uuid

warnings.warn(
    "case_utils.local_uuid has exported its functionality to cdo_local_uuid.  Imports should be changed to use cdo_local_uuid.  case_utils currently re-exports that functionality, but this will cease in a future release.",
    DeprecationWarning,
)
