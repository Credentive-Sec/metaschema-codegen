import pytest

from metaschema_python.core.schemaparse import MetaschemaParser, MetaSchemaSet
from metaschema_python.codegen.generate_classes import PackageGenerator, Package
from pathlib import Path


def build_metaschema_set() -> MetaSchemaSet:
    return MetaschemaParser.parse(
        metaschema_location="/workspaces/metaschema-python/OSCAL/src/metaschema/oscal_complete_metaschema.xml"
    )


def package_generator(metaschema_set: MetaSchemaSet) -> PackageGenerator:
    return PackageGenerator(metaschema_set, Path("/tmp/metaschema_python_ptest/"))


@pytest.fixture(scope="module")
def parsed_metaschema(pytestconfig):
    # NOTE: Caching doesn't work because a MetasSchemaSet is not json serializable.
    # metaschema = pytestconfig.cache.get("metaschema", None)
    # if metaschema is None:
    #     metaschema = build_metaschema_set()
    #     pytestconfig.cache.set("metaschema", metaschema)
    # return metaschema
    return build_metaschema_set()


@pytest.fixture(scope="module")
def generated_package(parsed_metaschema):
    return package_generator(parsed_metaschema)
