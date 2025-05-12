from pathlib import Path

import pytest

from metaschema_codegen.codegen.python.package_generator import PackageGenerator
from metaschema_codegen.core.schemaparse import MetaschemaSetParser, MetaSchemaSet


@pytest.fixture(scope="module")
def parsed_metaschema():
    """Fixture to parse the metaschema and return a MetaSchemaSet object."""
    metaschema_path = Path(__file__).parent.parent.parent / "OSCAL" / "src" / "metaschema" / "oscal_complete_metaschema.xml"
    ms = MetaschemaSetParser(metaschema_location=metaschema_path).metaschema_set
    return ms


@pytest.fixture(scope="module")
def generated_package(parsed_metaschema: MetaSchemaSet):
    output_path = Path("test-output")
    if not output_path.exists():
        output_path.mkdir()
    pg = PackageGenerator(
        parsed_metaschema,
        output_path,
        package_name="oscal",
        ignore_existing_files=True,
    )
    return pg
