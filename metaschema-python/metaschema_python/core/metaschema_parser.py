from __future__ import annotations
from typing import Optional, Union, Any, TypeAlias, TypeGuard, cast
import urllib.parse
from pathlib import Path

from lxml import etree
from xml.etree import ElementTree
import xmlschema


from . import metaschema_models

# Type Aliases
ParsedMetaschemaDictType: TypeAlias = dict[
    str, Union["ParsedMetaschemaValueType", "ParsedMetaschemaListType"]
]
ParsedMetaschemaValueType: TypeAlias = Union[str, int, ParsedMetaschemaDictType]
ParsedMetaschemaListType: TypeAlias = list[ParsedMetaschemaValueType]


class MetaschemaParser:
    VALUE_ERROR = ValueError("Parsed Metadata has unexpected contents")

    def __init__(
        self,
        location: str,
        base_url: Optional[str] = None,
        schema_file: Optional[str] = None,
    ):
        # If Base URL is not passed in, derive it from the location
        if base_url is not None:
            try:
                base_url_parts = urllib.parse.urlparse(base_url)
            except ValueError as e:
                print("Error parsing provided baseurl")
                raise e

            self.base_path = Path(base_url_parts.path)
        else:
            try:
                base_url_parts = urllib.parse.urlparse(location)
            except ValueError as e:
                print("Error parsing provided baseurl")
                raise e

            self.base_path = Path(Path(base_url_parts.path).parent)

        # If we parse a file path as a URL, the schema will be empty.
        # Alternatively, the user can pass a "file:" url
        # In both cases, make sure the path exists
        if Path(location).exists():
            self.metaschema_file = location
        elif Path(self.base_path, location).exists():
            self.metaschema_file = str(Path(self.base_path, location))
        else:
            raise FileNotFoundError(
                f"No file at {location} or {str(Path(self.base_path, location))}"
            )

        if schema_file is not None:
            self.schema_file = schema_file
        else:
            raise NotImplementedError("We haven't implemented schema discovery yet")

        self.parsed_metaschema = self.parse()

    def parse(self) -> dict[str, ParsedMetaschemaDictType]:
        metaschema_schema = xmlschema.XMLSchema(source=self.schema_file)
        metaschema_parser = etree.XMLParser(load_dtd=True, resolve_entities=True)
        metaschema_tree = etree.parse(self.metaschema_file, parser=metaschema_parser)
        parsed_metaschema = metaschema_schema.to_dict(
            # Cast doesn't do anything, just shuts up the type checker
            cast(xmlschema.XMLResource, metaschema_tree)
        )
        if self.type_guard(parsed_metaschema):
            schema_name = str(
                parsed_metaschema.get("short-name", Path(self.base_path).name)
            )  # shortname is always a str, so we just convert it.
            self.parsed_metaschema = parsed_metaschema
            return {schema_name: self.parsed_metaschema}
        else:
            raise self.VALUE_ERROR

    def get_imports(self) -> list[str]:
        # Import is always a list if it exists
        import_refs = cast(
            list, self.parsed_metaschema["oscal-catalog"].get("import", [])
        )
        return [item["@href"] for item in import_refs]

    # This function ensures that the parsed document has the correct underlying types
    def type_guard(self, input: Any) -> TypeGuard[ParsedMetaschemaDictType]:
        bool_array: list[bool] = []
        if isinstance(input, dict):
            bool_array.extend(self.parsed_metaschema_dict_typeguard(input))
        elif isinstance(input, list):
            bool_array.extend(self.parsed_metaschema_list_typeguard(input))
        else:
            bool_array.append(False)

        return all(bool_array)

    # Called by typeguard for dicts
    def parsed_metaschema_dict_typeguard(self, input: dict[str, Any]) -> list[bool]:
        bool_array: list[bool] = []
        bool_array.extend([isinstance(key, str) for key in input.keys()])
        for value in input.values():
            if isinstance(value, str) or isinstance(value, int):
                bool_array.append(True)
            elif isinstance(value, list):
                bool_array.extend(self.parsed_metaschema_list_typeguard(value))
            elif isinstance(value, dict):
                bool_array.extend(self.parsed_metaschema_dict_typeguard(value))
            else:
                bool_array.append(False)

        return bool_array

    # Called by typeguard for lists
    def parsed_metaschema_list_typeguard(self, input: list[Any]) -> list[bool]:
        bool_array: list[bool] = []
        for item in input:
            if isinstance(item, str) or isinstance(item, int):
                bool_array.append(True)
            elif isinstance(item, dict):
                bool_array.extend(self.parsed_metaschema_dict_typeguard(item))
            elif isinstance(item, list):
                bool_array.extend(self.parsed_metaschema_list_typeguard(item))

        return bool_array
