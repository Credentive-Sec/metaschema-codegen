from __future__ import annotations

import collections
import collections.abc
from urllib import request, parse
import xmlschema
from lxml import etree
from pathlib import Path
from typing import cast, Iterator
import logging
import re
import dataclasses

logging.basicConfig(level=logging.DEBUG)

# FIXME: This dict is necessary because of a bug in the metaschema xsd. This should be something we can calculate.
simple_type_map = {
    "Base64Datatype": "base64",
    "BooleanDatatype": "boolean",
    "DateDatatype": "date",
    "DateTimeDatatype": "date-time",
    "DateTimeWithTimezoneDatatype": "date-time-with-timezone",
    "DateWithTimezoneDatatype": "date-with-timezone",
    "DayTimeDurationDatatype": "day-time-duration",
    "DecimalDatatype": "decimal",
    "EmailAddressDatatype": "email-address",
    "HostnameDatatype": "hostname",
    "IntegerDatatype": "integer",
    "IPV4AddressDatatype": "ip-v4-address",
    "IPV6AddressDatatype": "ip-v6-address",
    "NonNegativeIntegerDatatype": "non-negative-integer",
    "PositiveIntegerDatatype": "positive-integer",
    "StringDatatype": "string",
    "TokenDatatype": "token",
    "URIDatatype": "uri",
    "URIReferenceDatatype": "uri-reference",
    "UUIDDatatype": "uuid",
    "MarkupLineDatatype": "markup-line",
    "MarkupMultilineDatatype": "markup-multiline",
}


# Simple utility classes to simplify data passing


@dataclasses.dataclass
class SimpleDataType:
    ref_name: str | None
    class_name: str
    base_type: str
    description: list[str]
    pattern: re.Pattern | None


@dataclasses.dataclass
class ComplexDataType:
    ref_name: str
    class_name: str
    elements: list[str]
    description: str | None = None


@dataclasses.dataclass
class MetaSchemaSet:
    base_path: Path
    simple_datatypes: list[SimpleDataType] = dataclasses.field(default_factory=list)
    complex_datatypes: list[ComplexDataType] = dataclasses.field(default_factory=list)
    metaschemas: list[MetaSchema] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class SchemaPath:
    base: Path
    name: str


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
            metaschema_set.simple_datatypes, metaschema_set.complex_datatypes = (
                MetaschemaParser._parse_data_types(ms_schema)
            )
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
    def _parse_data_types(
        schema: xmlschema.XMLSchema,
    ) -> tuple[list[SimpleDataType], list[ComplexDataType]]:
        simple_datatypes: list[SimpleDataType] = []
        complex_datatypes: list[ComplexDataType] = []

        for simple_datatype in schema.simple_types:

            if simple_datatype.local_name is not None:
                datatype_name = simple_datatype.local_name
            else:
                # This will never fire because metaschema always defines a base class
                datatype_name = ""

            if (
                simple_datatype.base_type is not None
                and simple_datatype.base_type.local_name is not None
            ):
                dt_base = simple_datatype.base_type.local_name
            else:
                # we should never get here because metaschema always defines a base class
                dt_base = ""

            dt_descriptions = []
            for annotation in simple_datatype.annotations:
                # Strip out newlines and tabs
                dt_descriptions.append(
                    str(annotation).replace("\n", "").replace("\t", "")
                )

            if simple_datatype.patterns is not None:
                # Hack here - we know that metaschema only has a single pattern per datatype
                dt_pattern = simple_datatype.patterns.patterns[0]
            else:
                dt_pattern = None

            simple_datatypes.append(
                SimpleDataType(
                    ref_name=simple_type_map.get(datatype_name),
                    class_name=datatype_name,
                    base_type=dt_base,
                    description=dt_descriptions,
                    pattern=dt_pattern,
                )
            )

        for complex_datatype in schema.complex_types:
            name = complex_datatype.local_name
            if name is not None and name in simple_type_map.keys():
                elements = []
                if type(complex_datatype.content) is xmlschema.validators.XsdGroup:
                    for element in complex_datatype.content.iter_elements():
                        elements.append(element.local_name)

                complex_datatypes.append(
                    ComplexDataType(
                        ref_name=simple_type_map[name],
                        class_name=name,
                        elements=elements,
                    )
                )

        return simple_datatypes, complex_datatypes

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
            # This is a URL
            pass

        return SchemaPath(base=base_path, name=file)


class MetaSchema(collections.abc.Mapping):
    """
    This class represents a parsed metaschema. It presents a dict like interface by implementing the Mapping abstract class methods.

    Attributes
    __________
    file: Path
        the filename of the original location
    short_name: str
        the short-name of the metaschema definition
    roots: list[str]
        a list of schema elements that can be the root of a document
    globals: list[str]
        a list of importable elements (by formal-name)
    schema_dicts: dict
        a dictionary containing the full, parsed metaschema
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
        self.globals = self._get_globals()
        self.roots = self._get_root_elements()

    def _read_local_schema(
        self, metaschema: str | Path, basepath: Path | None = None
    ) -> str:
        """
        Reads a schema on a local filesystem.

        Args:
            metaschema (str | Path): The file to read
            basepath (Path | None, optional): A optional base path to locate the directory containing the file. Defaults to None.

        Returns:
            str: The contents of the file.
        """
        if basepath is not None:
            schema_file = Path(basepath, metaschema)
        else:
            schema_file = Path(metaschema)

        return open(schema_file).read()

    def _read_remote_schema(self, metaschema: str, baseurl: str) -> str:
        """
        NOT YET IMPLEMENTED: Gets a schema if it is not stored locally, e.g. on a web site.

        Args:
            baseurl (str): The base URL where the schema can be found
            metaschema (str): The filename of the schema

        Returns:
            str: The contents of the file.
        """
        # TODO: implement
        return ""

    def _get_globals(self) -> dict[str, str]:
        """
        Returns the global symbols defined in this metaschema, for "import" in metaschemas that reference this schema.
        Use the .globals property to fetch this for performance, since it is pre-calcuated by the initializer.
        """
        globals = {}

        # return empty list if key does not exist
        for assembly in self.schema_dict.get("define-assembly", []):
            if assembly.get("@scope") != "local":
                globals.update(self._ref_name(instance=assembly))
        # return empty list if key does not exist
        for field in self.schema_dict.get("define-field", []):
            if field.get("@scope") != "local":
                globals.update(self._ref_name(instance=field))
        # return empty list if key does not exist
        for flag in self.schema_dict.get("define-flag", []):
            if flag.get("@scope") != "local":
                globals.update(self._ref_name(instance=flag))

        return globals

    def _ref_name(self, instance: dict) -> dict[str, str]:
        """
        calculates the names of the references

        Args:
            instance (dict): dictionary representing a flag, field or assembly

        Returns:
            dict[str, str]: a dictionary with a key of the reference name and a value of the formal name
        """
        use_name = instance.get("use-name")
        if use_name is not None:
            return {use_name: instance["formal-name"]}
        else:
            return {instance["@name"]: instance["formal-name"]}

    def _get_root_elements(self) -> list[str]:
        """
        Get a list of assemblies in this metaschema that have the "root-name" attribute, and can be a top level element of a document.

        Returns:
            list[str]: list of elements with "root-name"
        """
        root_elements = [
            assembly["formal-name"]
            for assembly in self.schema_dict.get("define-assembly", [])
            if assembly.get("root-name") is not None
        ]

        return root_elements

    def _get_imports(self) -> list[str]:
        """
        Function to get the other metaschemas that are imported by this one.

        Returns:
            list[str]: A list of strings representing filenames containing other metaschemas to import
        """
        import_list = []

        for item in self.schema_dict.get("import", []):
            if isinstance(item, dict) and "@href" in item.keys():
                import_list.append(item.get("@href"))

        return import_list

    def __repr__(self) -> str:
        return f"{self.__dict__}"

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
