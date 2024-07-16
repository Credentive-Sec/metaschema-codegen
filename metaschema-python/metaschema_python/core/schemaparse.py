from __future__ import annotations

import collections
import collections.abc
from urllib import request, parse
import xmlschema
from lxml import etree
from pathlib import Path
from typing import cast, Iterator
import logging

from ..shared_types import SchemaID, SchemaPath

logging.basicConfig(level=logging.DEBUG)

# Module variable for tracking files we've imported -
_import_tracker: list[str] = []
_metaschema_list: list[MetaSchema] = []


class MetaschemaParser:
    """
    This class provides a parser that will return one a dictionary containing one or more parsed Metaschema schemas.
    """

    @staticmethod
    def parse(
        metaschema_location: str | Path,
        base_url: str | None = None,
        base_path: Path | None = None,
        chase_imports: bool = True,
        schema_location: str = "https://raw.githubusercontent.com/usnistgov/metaschema/main/schema/xml/metaschema.xsd",
        schema_base_url: (
            str | None
        ) = "https://raw.githubusercontent.com/usnistgov/metaschema/main/schema/xml/",
    ) -> list[MetaSchema]:
        """
        This static method accepts a str or Path object representing a URL or file path.
        It parses the contents of the file or URL and returns a dictionary representing
        the parsed schema. If the file does not exist or the schema cannot be parsed, it
        raises an error. It accepts an optional base url or base path, but will attempt
        to automatically discover the base URL or Path if it is not provided.

        Args:
            metaschema (str | Path): the location of the metaschema to parse.
            base_url (str | None, optional): An optional base URL to use if following "import" references. Defaults to None.
            base_path (Path | None, optional): An optional base URL to use if following "import" references. Defaults to None.
            chase_imports (bool): If set to False, the parser will not try to follow imports. Defaults to True.
            schema_location (str): The location of the metaschema schema file (url or file path). Defaults to "https://raw.githubusercontent.com/usnistgov/metaschema/main/schema/xml/metaschema.xsd"
            schema_base_url (str | None, optional): An optional base_url for the schema parser to find imported schemas. Defaults to "https://raw.githubusercontent.com/usnistgov/metaschema/main/schema/xml/"

        Returns:
            list[MetaSchema]: a list of Metaschema objects
        """
        logging.debug(
            "Entering MetaschemaParser.parse() to parse " + str(metaschema_location)
        )

        xsd_contents = request.urlopen(schema_location).read()
        ms_schema = xmlschema.XMLSchema(source=xsd_contents, base_url=schema_base_url)

        metaschema_path = MetaschemaParser._normalize_input_path(
            str(metaschema_location)
        )
        metaschema = MetaSchema(metaschema=metaschema_location, schema_xsd=ms_schema)

        # Keep a list of the files we've processed so we don't parse something twice. References module variable so that it's readable by all instances
        _import_tracker.append(Path(metaschema_location).name)

        for sub_schema in MetaschemaParser._get_imports(metaschema):
            if sub_schema not in _import_tracker:
                MetaschemaParser.parse(
                    metaschema_location=Path(metaschema_path["base"], sub_schema),
                    base_url=base_url,
                    base_path=base_path,
                    chase_imports=chase_imports,
                    schema_location=schema_location,
                    schema_base_url=schema_base_url,
                )

        _metaschema_list.append(metaschema)

        return _metaschema_dict

    @staticmethod
    def _get_imports(schema: MetaSchema) -> list[str]:
        schema_list = []
        if "import" in schema.keys() and isinstance(schema["import"], list):
            for item in schema["import"]:
                if isinstance(item, dict) and "@href" in item.keys():
                    schema_list.append(item.get("@href"))

        return schema_list

    @staticmethod
    def _normalize_input_path(input_path: str) -> SchemaPath:
        """
        This function takes the file path string or URL provided to the initializer, validates it and returns the base path or base url and the file name.
        It raises an error if it cannot process the path. Called by the initializer.

        Args:
            input_path (str): the path provided to the function.
        """
        # TODO: handle http urls

        try:
            base_url_parts = parse.urlparse(input_path)
        except ValueError as e:
            print("Error parsing provided baseurl")
            raise e

        path = Path(base_url_parts.path)

        base_path = str(path.parent)
        file = path.name

        return SchemaPath(base=base_path, name=file)


class MetaSchema(collections.abc.Mapping):
    """
    This class represents a parsed metaschema. It presents a dict like interface by implementing the Mapping abstract class methods.
    """

    def __init__(
        self,
        metaschema: str | Path,
        schema_xsd: xmlschema.XMLSchema,
        baseurl: str | None = None,
        basepath: Path | None = None,
    ):
        """
        Initializer for a MetaSchema instance

        Args:
            metaschema (str | Path): A string representing a file or url, or a Path representing a local file.
            baseurl (str | None, optional): A base URL which will be used to import additional referenced metaschema files if obtained from a remote location. Defaults to None.
            basepath (pathlib.Path | None, optional): A base URL which will be used to import additional referenced metaschema files if obtained from a local re. Defaults to None.
        """
        # TODO: process URLs or local paths - consider reading the bytes and passing them to etree instead of a file location
        metaschema_file = metaschema
        parser = etree.XMLParser(resolve_entities=True)
        metaschema_etree = etree.parse(metaschema_file, parser=parser)
        self.schema_dict = cast(
            dict, schema_xsd.to_dict(cast(xmlschema.XMLResource, metaschema_etree))
        )
        self.module_name = cast(str, self.schema_dict["short-name"]).replace("-", "_")

    def _read_local_schema(
        self, metaschema: str | Path, basepath: Path | None = None
    ) -> str:
        if basepath is not None:
            schema_file = Path(basepath, metaschema)
        else:
            schema_file = Path(metaschema)

        return open(schema_file).read()

    def _read_remote_schema(self, baseurl: str, metaschema: str) -> str:
        return ""

    def get_globals(self) -> dict[str, str]:
        """
        Returns the global symbols defined in this metaschema, for "import" in metaschemas that reference this
        """
        globals = {}

        # return empty list if key does not exist
        for assembly in self.schema_dict.get("define-assembly", []):
            if assembly.get("@scope") != "local":
                globals[assembly["@name"]] = self._get_class_name(
                    assembly["formal-name"]
                )
        # return empty list if key does not exist
        for field in self.schema_dict.get("define-field", []):
            if field.get("@scope") != "local":
                globals[field["@name"]] = self._get_class_name(field["formal-name"])
        # return empty list if key does not exist
        for flag in self.schema_dict.get("define-flag", []):
            if flag.get("@scope") != "local":
                globals[flag["@name"]] = self._get_class_name(flag["formal-name"])

        return globals

    def _get_class_name(self, instance: str) -> str:
        """
        Returns the name of the Class that will instantiate a defined assembly, field or flag in a module.
        This is provided to ensure consistent names whether the class is being passed to a template, or
        the whether it is being used to support returning the global symbol for import into another module
        """
        # Strip strings, preserve case
        return f'{self.module_name}.{instance.replace(" ", "")}'

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.schema_dict})"

    ## Mapping ABC classes - turns this into a dict-like object
    def __getitem__(self, key: str) -> str | dict[str, str]:
        if isinstance(self.schema_dict, dict):
            return self.schema_dict.__getitem__(key)
        else:
            raise Exception("schema_dict is not a dict.")

    def __iter__(self) -> Iterator:
        if isinstance(self.schema_dict, dict):
            return self.schema_dict.__iter__()
        else:
            raise Exception("schema_dict is not a dict.")

    def __len__(self) -> int:
        if isinstance(self.schema_dict, dict):
            return self.schema_dict.__len__()
        else:
            raise Exception("schema_dict is not a dict.")
