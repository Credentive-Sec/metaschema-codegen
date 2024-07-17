from __future__ import annotations

import collections
import collections.abc
from urllib import request, parse
import xmlschema
from lxml import etree
from pathlib import Path
from typing import cast, Iterator, TypedDict
import logging
import re
import dataclasses

logging.basicConfig(level=logging.DEBUG)


# Simple utility classes to simplify data passing


@dataclasses.dataclass
class DataType:
    name: str
    base_type: str
    description: list[str]
    pattern: re.Pattern | None


@dataclasses.dataclass
class MetaSchemaSet:
    base_path: Path
    datatypes: list[DataType] = dataclasses.field(default_factory=list)
    metaschemas: list[MetaSchema] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class SchemaPath:
    base: Path
    name: str


@dataclasses.dataclass
class GlobalElement:
    schema: str
    element: str


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
        # The following optionals are used for recursive calls
        metaschema_set: MetaSchemaSet | None = None,
    ) -> MetaSchemaSet:
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

        # First time we're called, metaschema_set isn't defined yet.
        # TODO - clean up this logic, it's a mess
        if metaschema_set is None:
            metaschema_path = MetaschemaParser._process_input_path(
                str(metaschema_location)
            )
            metaschema_set = MetaSchemaSet(base_path=metaschema_path.base)
            # Parse datatypes
            metaschema_set.datatypes = MetaschemaParser._parse_data_types(ms_schema)
        else:
            metaschema_path = SchemaPath(
                base=metaschema_set.base_path, name=str(metaschema_location)
            )

        metaschema = MetaSchema(
            file=metaschema_path.name,
            basepath=Path(metaschema_path.base),
            schema_xsd=ms_schema,
        )
        metaschema_set.metaschemas.append(metaschema)

        for sub_schema in MetaschemaParser._get_imports(metaschema):
            if sub_schema not in [
                metaschema.file for metaschema in metaschema_set.metaschemas
            ]:
                MetaschemaParser.parse(
                    metaschema_location=sub_schema,
                    base_url=base_url,
                    base_path=metaschema_path.base,
                    chase_imports=chase_imports,
                    schema_location=schema_location,
                    schema_base_url=schema_base_url,
                    metaschema_set=metaschema_set,
                )

        return metaschema_set

    @staticmethod
    def _parse_data_types(schema: xmlschema.XMLSchema) -> list[DataType]:
        datatypes: list[DataType] = []

        for datatype in schema.simple_types:

            if datatype.local_name is not None:
                dt_name = datatype.local_name
            else:
                # This will never fire because metaschema always defines a base class
                dt_name = ""

            if (
                datatype.base_type is not None
                and datatype.base_type.local_name is not None
            ):
                dt_base = datatype.base_type.local_name
            else:
                # This will never fire because metaschema always defines a base class
                dt_base = ""

            dt_descriptions = []
            for annotation in datatype.annotations:
                # Strip out newlines and tabs
                dt_descriptions.append(
                    str(annotation).replace("\n", "").replace("\t", "")
                )

            if datatype.patterns is not None:
                # Hack here - we know that metaschema only has a single pattern per datatype
                dt_pattern = datatype.patterns.patterns[0]
            else:
                dt_pattern = None

            datatypes.append(
                DataType(
                    name=dt_name,
                    base_type=dt_base,
                    description=dt_descriptions,
                    pattern=dt_pattern,
                )
            )

        return datatypes

    @staticmethod
    def _get_imports(schema: MetaSchema) -> list[str]:
        schema_list = []
        if "import" in schema.keys() and isinstance(schema["import"], list):
            for item in schema["import"]:
                if isinstance(item, dict) and "@href" in item.keys():
                    schema_list.append(item.get("@href"))

        return schema_list

    @staticmethod
    def _process_input_path(input_path: str) -> SchemaPath:
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

        if base_url_parts.scheme == "":
            # This is a file path
            path = Path(input_path)
            base_path = path.parent
            if not base_path.is_absolute():
                base_path.resolve()
            file = path.name
        else:
            # This is URL
            pass

        return SchemaPath(base=base_path, name=file)


class MetaSchema(collections.abc.Mapping):
    """
    This class represents a parsed metaschema. It presents a dict like interface by implementing the Mapping abstract class methods.
    """

    def __init__(
        self,
        file: str | Path,
        schema_xsd: xmlschema.XMLSchema,
        baseurl: str | None = None,
        basepath: Path | None = None,
    ):
        """
        Initializer for a MetaSchema instance

        Args:
            file (str | Path): A string representing a file or url, or a Path representing a local file.
            schema_xsd (xmlschema.XMLSchema): A parsed xml schema which can be passed in to prevent the same xsd from being parsed multiple times
            baseurl (str | None, optional): A base URL which will be used to import additional referenced metaschema files if obtained from a remote location. Defaults to None.
            basepath (pathlib.Path | None, optional): A base URL which will be used to import additional referenced metaschema files if obtained from a local re. Defaults to None.
        """
        # TODO: process URLs or local paths - consider reading the bytes and passing them to etree instead of a file location
        self.file = file

        # If we were passed a basepath, try to construct a location from it
        if basepath is not None:
            location = basepath.joinpath(file)
        else:
            location = Path(file)

        # Parse the file
        parser = etree.XMLParser(resolve_entities=True)
        metaschema_etree = etree.parse(location, parser=parser)

        # Extract the relevant data from the etree
        self.schema_dict = cast(
            dict, schema_xsd.to_dict(cast(xmlschema.XMLResource, metaschema_etree))
        )  # cast doesn't do anything, just shuts up the type checker
        self.short_name = cast(str, self.schema_dict["short-name"])
        self.globals = self.get_globals()

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

    def get_globals(self) -> list[str]:
        """
        Returns the global symbols defined in this metaschema, for "import" in metaschemas that reference this schema
        """
        globals = []

        # return empty list if key does not exist
        for assembly in self.schema_dict.get("define-assembly", []):
            if assembly.get("@scope") != "local":
                globals.append(assembly["formal-name"])
        # return empty list if key does not exist
        for field in self.schema_dict.get("define-field", []):
            if field.get("@scope") != "local":
                globals.append(field["formal-name"])
        # return empty list if key does not exist
        for flag in self.schema_dict.get("define-flag", []):
            if flag.get("@scope") != "local":
                globals.append(flag["formal-name"])

        return globals

    def _get_imports(self) -> list[str]:
        import_list = []
        if "import" in self.schema_dict.keys() and isinstance(
            self.schema_dict["import"], list
        ):
            for item in self.schema_dict["import"]:
                if isinstance(item, dict) and "@href" in item.keys():
                    import_list.append(item.get("@href"))

        return import_list

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.schema_dict})"

    ## implementing abstract classes to turn this into a dict-like object
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
