# CASE Python Utilities

This project provides various specialized utilities for producing data in the [CASE](https://caseontology.org/) format.


## Disclaimer

Participation by NIST in the creation of the documentation of mentioned software is not intended to imply a recommendation or endorsement by the National Institute of Standards and Technology, nor is it intended to imply that any specific software is necessarily the best available for the purpose.


## Installation

1. Clone this repository.
2. (Optional) Create and activate a virtual environment.
3. Run `python setup.py`.

Installation is demonstrated in the `.venv.done.log` target of the [`tests/`](tests/) directory.


## Usage


### `case_validate`

This repository provides `case_validate` as an adaptation of the `pyshacl` command from [RDFLib's pySHACL](https://github.com/RDFLib/pySHACL).  The command-line interface is adapted to run as though `pyshacl` were provided the full CASE ontology (and adopted full UCO ontology) as both a shapes and ontology graph.  "Compiled" (or, "aggregated") CASE ontologies are in the [`case_utils/ontology/`](case_utils/ontology/) directory, and are installed with `pip`, so data validation can occur without requiring networking after this repository is installed.

To see a human-readable validation report of an instance-data file:

```bash
case_validate input.json [input-2.json ...]
```

If `input.json` is not conformant, a report will be emitted, and `case_validate` will exit with status `1`.  (This is a `pyshacl` behavior, where `0` and `1` report validation success.  Status of >`1` is for other errors.)

To produce the validation report as a machine-readable graph output, the `--format` flag can be used to modify the output format:

```bash
case_validate --format turtle input.json > result.ttl
```

To use one or more supplementary ontology files, the `--ontology-graph` flag can be used, more than once if desired, to supplement the selected CASE version:

```bash
case_validate --ontology-graph internal_ontology.ttl --ontology-graph experimental_shapes.ttl input.json
```

Other flags are reviewable with `case_validate --help`.


### `case_file`

To characterize a file, including hashes:

```bash
case_file sample.txt.json sample.txt
```

To characterize a file, but skip hashing it:

```bash
case_file --disable-hashes sample.txt.json sample.txt
```


### SPARQL executors

Two commands are provided to generate output from a SPARQL query and one or more input graphs.  Input graphs can be any graph, such as instance data or supplementary ontology files that supply custom class definitions or other external ontologies.


#### `case_sparql_construct`

To use a SPARQL `CONSTRUCT` query to make a supplementary graph file from one or more input graphs:

```bash
case_sparql_construct output.json input.sparql input.json [input-2.json ...]
```


#### `case_sparql_select`

To use a SPARQL `SELECT` query to make a table from one or more input graphs:

```bash
# HTML output with Bootstrap classes
# (e.g. for Jekyll-backed websites)
case_sparql_select output.html input.sparql input.json [input-2.json ...]

# Markdown, Github-flavored
case_sparql_select output.md input.sparql input.json [input-2.json ...]
```

Note that `case_sparql_select` is not guaranteed to function with Pythons below version 3.7.


### `local_uuid`

This [module](case_utils/local_uuid.py) provides a wrapper UUID generator, `local_uuid()`.  Its main purpose is making example data generate consistent identifiers, and intentionally includes mechanisms to make it difficult to activate this mode without awareness of the caller.


## Development status

This repository follows [CASE community guidance on describing development status](https://caseontology.org/resources/software.html#development_status), by adherence to noted support requirements.

The status of this repository is:

4 - Beta


## Versioning

This project follows [SEMVER 2.0.0](https://semver.org/) where versions are declared.


## Ontology versions supported

This repository supports the CASE ontology version that is linked as a submodule [here](dependencies/CASE).  The CASE version is encoded as a variable (and checked in unit tests) in [`case_utils/ontology/version_info.py`](case_utils/ontology/version_info.py), and used throughout this code base, as `CURRENT_CASE_VERSION`.

For instructions on how to update the CASE version for an ontology release, see [`CONTRIBUTE.md`](CONTRIBUTE.md).


## Repository locations

This repository is available at the following locations:
* [https://github.com/casework/CASE-Utilities-Python](https://github.com/casework/CASE-Utilities-Python)
* [https://github.com/usnistgov/CASE-Utilities-Python](https://github.com/usnistgov/CASE-Utilities-Python) (a mirror)

Releases and issue tracking will be handled at the [casework location](https://github.com/casework/CASE-Utilities-Python).


## Make targets

Some `make` targets are defined for this repository:
* `check` - Run unit tests.
* `clean` - Remove test build files, but not downloaded files.
* `download` - Download files sufficiently to run the unit tests offline.  This will *not* include the ontology repositories tracked as submodules.  Note if you do need to work offline, be aware touching the `setup.cfg` file in the project root directory, or `tests/requirements.txt`, will trigger a virtual environment rebuild.
