import pytest

from metaschema_python.core.schemaparse import MetaschemaParser, MetaSchemaSet


def build_metaschema_set() -> MetaSchemaSet:
    return MetaschemaParser.parse(
        metaschema_location="/workspaces/metaschema-python/OSCAL/src/metaschema/oscal_complete_metaschema.xml"
    )


@pytest.fixture(scope="module")
def parsed_metaschema(pytestconfig):
    # NOTE: Caching doesn't work because a MetasSchemaSet is not json serializable.
    # metaschema = pytestconfig.cache.get("metaschema", None)
    # if metaschema is None:
    #     metaschema = build_metaschema_set()
    #     pytestconfig.cache.set("metaschema", metaschema)
    # return metaschema
    return build_metaschema_set()
