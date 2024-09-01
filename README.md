# Overview of Metaschema-Codegen

## Purpose

The Metaschema-codegen library and application is designed to parse a schema designed in the Metaschema lanaguage and generate a source library that implements the schema using a clear and idiomatic API. The generated library is intended to be standalone, with minimal dependencies beyond those provided by the language's standard library.

## How it works

Metaschema-codegen has a two phase approach to generating code from a metaschema.

1. First, it parses the metaschema into an internal data structure that is generic, and suitable for transformation into other programming languages.
1. Second, it uses the [jinja2](https://jinja.palletsprojects.com/en/3.0.x/) templating library to produce output files converting the schema into source code for the generated library.

Both of these steps have many sub-processes, but this design allows a developer to modify the second step to produce a library in another programming language without needing to develop a parser for metaschema. 

## What the library provides for you (the developer)

By parsing the metaschema, the library will provide the following elements:

- Simple Datatypes, including their regular expressions.
- Complex Datatypes (Markup Types, fields, flags and assemblies), including the definition of the structures and references to datatypes for primitive elements
- Information about cross-references between metaschema elements defined in different schema documents.

## What you (the developer) provides for a language specific implementation

The library provides information about the structure of defined metaschema, but a language implementation should provide the following elements:

- idiomatic representations of the structures
- functions and behaviours such as data validation
- import and export functions for documents that comply with a metaschema in one of the supported representations, such as an OSCAL catalog expressed in JSON

## Setting up your development environment

This project uses [poetry](https://python-poetry.org/) for development and packaging. This installation should be handled automatically via installation of the development container.

### Development Container

The project team uses a [develoment container](https://containers.dev/) to simplify development, which works well in Visual Studio Code. If you clone the repository in VS Code, you should be prompted to reopen the project in a dev container.

### Use 'dev' Branch

Immediately after cloning the repository, switch to the 'dev' branch. This is where development is occuring, and it differs significantly from the main branch.

```sh
git switch dev
```

### Install Submodules

Next, install all of the required submodules with the `git submodule update --init` command. Confirm that all four of the submodules listed below are cloned.

```sh
$ git submodule update --init
Submodule 'OSCAL' (https://github.com/usnistgov/OSCAL.git) registered for path 'OSCAL'
Submodule 'metaschema' (https://github.com/usnistgov/metaschema.git) registered for path 'metaschema'
Submodule 'metaschema-python/elementpath' (https://github.com/sissaschool/elementpath.git) registered for path 'metaschema-python/metaschema_python/elementpath'
Submodule 'oscal-content' (https://github.com/usnistgov/oscal-content.git) registered for path 'oscal-content'
Cloning into '/workspaces/metaschema-python/OSCAL'...
Cloning into '/workspaces/metaschema-python/metaschema'...
Cloning into '/workspaces/metaschema-python/metaschema-python/metaschema_python/elementpath'...
Cloning into '/workspaces/metaschema-python/oscal-content'...
remote: Enumerating objects: 17, done.
remote: Counting objects: 100% (17/17), done.
remote: Compressing objects: 100% (3/3), done.
remote: Total 17 (delta 14), reused 17 (delta 14), pack-reused 0 (from 0)
Unpacking objects: 100% (17/17), 49.52 KiB | 4.95 MiB/s, done.
From https://github.com/usnistgov/OSCAL
 * branch                737ce66a738ca6f2d1808ab00e04c0e4bcd70d7b -> FETCH_HEAD
Submodule path 'OSCAL': checked out '737ce66a738ca6f2d1808ab00e04c0e4bcd70d7b'
Submodule path 'metaschema': checked out 'cf5966076cce4756081a05db46a784f5fb25af27'
remote: Enumerating objects: 3, done.
remote: Counting objects: 100% (3/3), done.
remote: Compressing objects: 100% (2/2), done.
remote: Total 3 (delta 1), reused 3 (delta 1), pack-reused 0 (from 0)
Unpacking objects: 100% (3/3), 439 bytes | 439.00 KiB/s, done.
From https://github.com/sissaschool/elementpath
 * branch              e0edb2998c866aecfd106d4ce125f9ca371925b4 -> FETCH_HEAD
Submodule path 'metaschema-python/metaschema_python/elementpath': checked out 'e0edb2998c866aecfd106d4ce125f9ca371925b4'
Submodule path 'oscal-content': checked out '941c978d14c57379fbf6f7fb388f675067d5bff7'
```

### Setup virtual env

Poetry has been configured to install a virtual env inside the project directory, since VS Code prefers that configuration.

Change to the directory containing the pyproject.toml

```sh
cd metaschema-python
```

#### Generate the virtual environment. 
This command will read the poetry configuration, generate a virtual environment, and activate it in the current terminal.

```sh
poetry shell
```

#### Install poetry dependencies
This command will install the appropriate vesions of all dependencies in the project.

```sh
poetry install
```

 It may be necessary to reload the VS Code window for VS Code to pick up and activate the new virtual environment and installed dependencies ("Developer: Reload Window").


## Tests

 Tests should automatically be discovered, however the tests that are included in the imported "elementpath" module are not complete. A "pytest Discovery Error" will appear, but can be ignored. 

### Useful Tests

To generate the python package source code, run the "test_package_generator" test. The generated code will appear in the "test-output/oscal" directory under the main project directory. 
 
Breakpoints can be added added at various points to inspect the data structures used for code generation:

- metaschema-python/metaschema_python/core/schemaparse.py line 134: the "metaschema_schema" variable shows the contents of the internal representation of the metaschema xsd. See "metaschema_schema.complex_types" and "metaschema_schema.simple_types" for the items we use most.
- metaschema-python/tests/test_codegen.py line 13: the "ms" variable has a complete MetaschemaSet object
- metaschema-python/tests/conftest.py line 26: The "pg" variable contains a complete generated package.

## Other documentation

The "design-docs" folder contains some useful notes, and is a general folder for putting things that we refer to frequently during development. See "parsing-samples.md" for a dump of the metaschema-schema object.