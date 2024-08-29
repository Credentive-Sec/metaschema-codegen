# Setting up your development environment

This project uses [poetry](https://python-poetry.org/) for development and packaging. This installation should be handled automatically via installation of the development container.

## Development Container

The project team uses a [develoment container](https://containers.dev/) to simplify development, which works well in Visual Studio Code. If you clone the repository in VS Code, you should be prompted to reopen the project in a dev container.

## Use `Dev` Branch

Immediately after cloning the repository, switch to the 'dev' branch. This is where development is occuring, and it differs significantly from the main branch.

## Install Submodules

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

## Setup virtual env

Poetry has been configured to install a virtual env inside the project directory, since VS Code prefers that configuration.

Change to the directory containing the pyproject.toml

```sh
cd metaschema-python
```

Generate the virtual environment 

```sh
poetry shell
```

This command will read the poetry configuration, generate a virtual environment, and activate it in the current terminal. It may be necessary to reload the VS Code window for VS Code to pick up and activate the new virtual environment.