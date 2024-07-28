import pytest

from metaschema_python.core.schemaparse import MetaschemaParser
from metaschema_python.codegen.python.generate_classes import PackageGenerator
from pathlib import Path


@pytest.fixture(scope="module")
def parsed_metaschema():
    ms = MetaschemaParser.parse(
        metaschema_location="/workspaces/metaschema-python/OSCAL/src/metaschema/oscal_complete_metaschema.xml"
    )
    return ms


@pytest.fixture(scope="module")
def generated_package(parsed_metaschema):
    pg = PackageGenerator(
        parsed_metaschema,
        Path("/tmp/metaschema_python_ptest/"),
        package_name="oscal",
    )
    return pg
