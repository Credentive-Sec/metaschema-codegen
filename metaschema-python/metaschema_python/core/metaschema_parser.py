from typing import Optional
import urllib.parse
from pathlib import Path

from lxml import etree, objectify


from . import metaschema_models


class MetaschemaParser:
    def __init__(self, location: str, base_url: Optional[str] = None):
        # If Base URL is not passed in, derive it from the location
        if base_url is not None:
            try:
                base_url_parts = urllib.parse.urlparse(base_url)
            except ValueError as e:
                print("Error parsing provided baseurl")
                raise e

            base_path = Path(Path(base_url_parts.path).anchor)
        else:
            try:
                base_url_parts = urllib.parse.urlparse(location)
            except ValueError as e:
                print("Error parsing provided baseurl")
                raise e

            base_path = Path(Path(base_url_parts.path).anchor)

        # If we parse a file path as a URL, the schema will be empty.
        # Alternatively, the user can pass a "file:" url
        # In both cases, make sure the path exists
        if not base_url_parts.scheme or base_url_parts.scheme == "file":
            if not base_path.exists():
                raise FileNotFoundError(
                    "A local base URL was specified or derived, but it does not exist."
                )

        METASCHEMA_SCHEMA_FILE = (
            "/workspaces/metaschema-python/metaschema/schema/xml/metaschema.xsd"
        )
        metaschema_schema = etree.XMLSchema(file=METASCHEMA_SCHEMA_FILE)

        metaschema_tree = etree.parse(location)

        print([entity for entity in metaschema_tree.iter(etree.Entity)])

        if metaschema_schema.validate(metaschema_tree):
            self.root = metaschema_tree.getroot()
        else:
            raise IOError("Unable to parse xml at ", location)

        if self.root.nsmap and None in self.root.nsmap.keys():
            ns = self.root.nsmap[None]
        else:
            ns = ""

        # Create an entry in the schema dict for the current document
        # self.schema_elements: dict[str, etree._Element] = {

        # }
        short_name = [name for name in self.root.iter("{" + ns + "}shortname")]
        print(short_name)

        # Chase imports
        for sub_schema in self.root.iter("{" + ns + "}import"):
            sub_schema_location = sub_schema.get("href")
            if sub_schema_location:
                try:
                    sub_schema_root = MetaschemaParser(
                        location=sub_schema_location, base_url=sub_schema_location
                    )
                except Exception as e:
                    print(f"error loading {sub_schema_location}")

    def get_schema_elements(self) -> dict[str, str]:
        schema_elements: dict[str, str] = {}
        return schema_elements
