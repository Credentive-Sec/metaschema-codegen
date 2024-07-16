from metaschema_python.core.schemaparse import MetaschemaParser


def test_metaschema_parse():
    assert isinstance(
        MetaschemaParser.parse(
            metaschema_location="/workspaces/metaschema-python/OSCAL/src/metaschema/oscal_complete_metaschema.xml"
        ),
        dict,
    )
