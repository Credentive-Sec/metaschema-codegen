import pytest

from metaschema_python.core.schemaparse import MetaschemaParser
from metaschema_python.codegen.python.generate_classes import PackageGenerator
from pathlib import Path


@pytest.fixture(scope="module")
def parsed_metaschema():
    ms = MetaschemaParser(
        metaschema_location="OSCAL/src/metaschema/oscal_complete_metaschema.xml"
    ).metaschema_set
    return ms


@pytest.fixture(scope="module")
def generated_package(parsed_metaschema):
    pg = PackageGenerator(
        parsed_metaschema,
        Path("test-output"),
        package_name="oscal",
        ignore_existing_files=True,
    )
    return pg
