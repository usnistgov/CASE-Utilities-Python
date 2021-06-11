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


### `local_uuid`

This [module](case_utils/local_uuid.py) provides a wrapper UUID generator, `local_uuid()`.  Its main purpose is making example data generate consistent identifiers, and intentionally includes mechanisms to make it difficult to activate this mode without awareness of the caller.


## Development status

This repository follows [CASE community guidance on describing development status](https://caseontology.org/resources/software.html#development_status), by adherence to noted support requirements.

The status of this repository is:

4 - Beta


## Versioning

This project follows [SEMVER 2.0.0](https://semver.org/) where versions are declared.


## Ontology versions supported

This repository supports the ontology versions that are linked as submodules in the [CASE Examples QC](https://github.com/ajnelson-nist/CASE-Examples-QC) repository.  Currently, the ontology versions are:

* CASE - 0.3.0
* UCO - 0.5.0


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
