from pathlib import Path

from metaschema_python.core.schemaparse import MetaSchemaSet


class TestSchemaParser:
    def test_metaschema_parse_type(self, parsed_metaschema):
        assert isinstance(
            parsed_metaschema,
            MetaSchemaSet,
        )

    def test_metaschama_set_contents(self, parsed_metaschema):
        assert (
            parsed_metaschema.base_path is not None
            and parsed_metaschema.datatypes is not None
            and parsed_metaschema.metaschemas is not None
        )

    def test_base_path(self, parsed_metaschema):
        assert isinstance(parsed_metaschema.base_path, Path)

    def test_datatypes(self, parsed_metaschema):
        assert isinstance(parsed_metaschema.datatypes, list)

    def test_metaschemas(self, parsed_metaschema):
        assert isinstance(parsed_metaschema.metaschemas, list)
