from datetime import datetime
from pathlib import Path
from typing import Any

import pytest

from metaschema_codegen.codegen.python.package_generator import PackageGenerator
from metaschema_codegen.core.schemaparse import MetaSchemaSet, MetaschemaSetParser


@pytest.fixture(scope="module")
def output_path() -> Path:
    return Path("test-output-" + datetime.now().isoformat())


@pytest.fixture(scope="module")
def parsed_metaschema():
    """Fixture to parse the metaschema and return a MetaSchemaSet object."""
    metaschema_path = (
        Path(__file__).parent.parent.parent
        / "OSCAL"
        / "src"
        / "metaschema"
        / "oscal_complete_metaschema.xml"
    )
    ms = MetaschemaSetParser(metaschema_location=metaschema_path).metaschema_set
    return ms


def find_constraint_targets(data: list[Any] | dict[str, Any]) -> list[str]:
    target_list: list[str] = []
    if isinstance(data, dict):
        for key, value in data.items():
            if key == "@target" and isinstance(value, str):
                target_list.append(value)
            else:
                target_list.extend(find_constraint_targets(data=value))

    elif isinstance(data, list):
        for item in data:
            target_list.extend(find_constraint_targets(data=item))

    return target_list


@pytest.fixture(scope="module")
def metapaths(parsed_metaschema: MetaSchemaSet):
    """Fixture to return a list of metapath strings from a MetaSchemaSet"""
    targets: set[str] = set()
    for metaschema in parsed_metaschema.metaschemas:
        targets.update(find_constraint_targets(metaschema.schema_dict))

    return targets


@pytest.fixture(scope="module")
def generated_package(parsed_metaschema: MetaSchemaSet, output_path: Path):
    if not output_path.exists():
        output_path.mkdir()
    pg = PackageGenerator(
        parsed_metaschema,
        output_path,
        package_name="oscal",
        ignore_existing_files=True,
    )
    return pg
