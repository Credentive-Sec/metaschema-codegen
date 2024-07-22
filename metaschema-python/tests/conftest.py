import pytest

from metaschema_python.core.schemaparse import MetaschemaParser, MetaSchemaSet
from metaschema_python.codegen.generate_classes import PackageGenerator
from pathlib import Path


def build_metaschema_set() -> MetaSchemaSet:
    return MetaschemaParser.parse(
        metaschema_location="/workspaces/metaschema-python/OSCAL/src/metaschema/oscal_complete_metaschema.xml"
    )


def package_generator(metaschema_set: MetaSchemaSet) -> PackageGenerator:
    return PackageGenerator(
        metaschema_set, Path("/tmp/metaschema_python_ptest/"), package_name="oscal"
    )


@pytest.fixture(scope="module")
def parsed_metaschema():
    return build_metaschema_set()


@pytest.fixture(scope="module")
def generated_package(parsed_metaschema):
    return package_generator(parsed_metaschema)
