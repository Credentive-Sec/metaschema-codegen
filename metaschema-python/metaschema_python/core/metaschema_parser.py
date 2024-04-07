from __future__ import annotations
from typing import Optional
import urllib.parse
from pathlib import Path

from lxml import etree, objectify


from . import metaschema_models


class MetaschemaParser:
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

    def parse(self) -> dict[str, etree._Element]:
        parsed_metaschema: dict[str, etree._Element] = {}
        metaschema_schema = etree.XMLSchema(file=self.schema_file)
        metaschema_parser = etree.XMLParser(load_dtd=True, resolve_entities=True)
        metaschema_tree = etree.parse(self.metaschema_file, parser=metaschema_parser)
        if metaschema_schema.validate(metaschema_tree):
            self.root = metaschema_tree.getroot()
        else:
            raise IOError("XML did not conform to schema in ", self.metaschema_file)

        if self.root.nsmap and None in self.root.nsmap.keys():
            namespace = "{" + self.root.nsmap[None] + "}"
            print(namespace)
        else:
            namespace = ""

        short_names = [name.text for name in self.root.iter(f"{namespace}short-name")]

        short_name = short_names[0]

        if short_name is not None:
            parsed_metaschema[short_name] = metaschema_tree.getroot()
        else:
            raise Exception("short-name is None in " + self.metaschema_file)

        # Chase imports
        for sub_schema in self.root.iter(f"{namespace}import"):
            sub_schema_href = sub_schema.get("href")
            if sub_schema_href:
                print(f"Attempting to import {sub_schema_href}")
                try:
                    sub_schema_parser = MetaschemaParser(
                        location=sub_schema_href,
                        base_url=str(self.base_path),
                        schema_file=self.schema_file,
                    )
                    parsed_metaschema.update(sub_schema_parser.parse())
                except Exception as e:
                    print(f"error loading {sub_schema_href}: {e}")

        return parsed_metaschema
