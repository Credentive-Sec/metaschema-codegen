from __future__ import annotations

from urllib import request, parse
import xmlschema
from lxml import etree
from pathlib import Path
from typing import cast
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


#  utility classes to simplify data passing


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
class RootElement:
    metaschema_file: str
    element_name: str


@dataclasses.dataclass
class GlobalElement:
    metaschema_file: str
    effective_name: str
    formal_name: str


@dataclasses.dataclass
class MetaSchemaSet:
    simple_datatypes: list[SimpleDataType] = dataclasses.field(default_factory=list)
    complex_datatypes: list[ComplexDataType] = dataclasses.field(default_factory=list)
    metaschemas: list[MetaSchema] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class SchemaPath:
    base: Path
    file: str


class SchemaParseException(Exception):
    pass


class MetaschemaParser:
    """
    This class provides a parser that will return a MetaschemaSet containing datatypes and or more parsed Metaschema schemas.
    """

    def __init__(
        self,
        metaschema_location: str | Path,
        chase_imports: bool = True,
        schema_location: str = "https://raw.githubusercontent.com/usnistgov/metaschema/main/schema/xml/metaschema.xsd",
        schema_base_url: (
            str | None
        ) = "https://raw.githubusercontent.com/usnistgov/metaschema/main/schema/xml/",
    ):

        # Parse the XML Schema
        xsd_contents = request.urlopen(schema_location).read()
        ms_schema = xmlschema.XMLSchema(source=xsd_contents, base_url=schema_base_url)

        # Initialize a metaschema set for the parser
        self.metaschema_set = MetaSchemaSet()

        # Parse the datatypes from the XSD
        self.metaschema_set.simple_datatypes = self._parse_simple_datatypes(ms_schema)
        self.metaschema_set.complex_datatypes = self._parse_complex_datatypes(ms_schema)

        # Start parsing the metaschema itself
        start_path = self._process_input_path(metaschema_location)
        base = start_path.base

        # Create a list to track the metaschemas we have to evaluate
        schemas_to_parse: set[str] = set()
        schemas_to_parse.add(start_path.file)

        # Create a list of metaschemas we've already processed
        parsed_schemas = set()

        # Parse all of the schemas
        while len(schemas_to_parse) > 0:
            next_schema = (
                schemas_to_parse.pop()
            )  # removes the schema from the list and returns it
            metaschema = MetaSchema(schema_xsd=ms_schema, file=Path(base, next_schema))
            self.metaschema_set.metaschemas.append(metaschema)

            # Add the schema we just parsed to the list of schemas we've already parsed
            parsed_schemas.add(next_schema)

            # Get the set of imported schemas from the metaschema that are not in the "parsed_schema" set
            new_schemas = set(metaschema.imports).difference(parsed_schemas)

            # add the new_schemas to the schemas_to_parse
            schemas_to_parse.update(new_schemas)

    def _parse_simple_datatypes(
        self, xml_schema: xmlschema.XMLSchema
    ) -> list[SimpleDataType]:
        simple_datatypes: list[SimpleDataType] = []

        for simple_datatype in xml_schema.simple_types:

            if simple_datatype.local_name is not None:
                datatype_name = simple_datatype.local_name
            else:
                # This will never fire because metaschema always defines a name for datatypes
                datatype_name = ""

            if (
                simple_datatype.base_type is not None
                and simple_datatype.base_type.local_name is not None
            ):
                dt_base = simple_datatype.base_type.local_name
            else:
                # we should never get here because metaschema always defines a base class for datatypes
                dt_base = ""

            dt_descriptions = []
            for annotation in simple_datatype.annotations:
                # Strip out newlines and tabs
                dt_descriptions.append(
                    str(annotation).replace("\n", "").replace("\t", "")
                )

            if simple_datatype.patterns is not None:
                if len(simple_datatype.patterns) > 1:
                    logging.debug(
                        f"More than one pattern for datatype {datatype_name}!"
                    )
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

        return simple_datatypes

    def _parse_complex_datatypes(
        self, xml_schema: xmlschema.XMLSchema
    ) -> list[ComplexDataType]:
        complex_datatypes: list[ComplexDataType] = []

        for complex_datatype in xml_schema.complex_types:
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

        return complex_datatypes

    def _process_input_path(self, input_path: str | Path) -> SchemaPath:
        """
        This function takes the file path string or URL provided to the initializer, validates it and returns the base path or base url and the file name.
        It raises an error if it cannot process the path. Called by the initializer.

        Args:
            input_path (str): the path provided to the function.
        """

        if isinstance(input_path, Path):
            # process as path
            if input_path.exists and input_path.is_file:
                base_path = input_path.parent
                file = input_path.name

        elif isinstance(input_path, str):
            try:
                base_url_parts = parse.urlparse(input_path)
            except ValueError as e:
                print("Error parsing provided baseurl")
                raise e

            if base_url_parts.scheme in ["", "file"]:
                # This is a file path
                path = Path(input_path)
                base_path = path.parent
                if not base_path.is_absolute():
                    base_path.resolve()
                file = path.name
            elif base_url_parts.scheme == "http":
                # TODO: handle http urls
                pass
            else:
                pass
        else:
            raise SchemaParseException(
                f"Base must be a str or a Path. You provided a {type(input_path)}."
            )

        return SchemaPath(base=base_path, file=file)


class MetaSchema:
    """
    This class represents a parsed metaschema.

    Attributes
    __________
    file: Path
        the filename of the original location
    short_name: str
        the short-name of the metaschema definition
    imports: list[str]
        a list of metaschema files to import
    roots: list[str]
        a list of schema elements that can be the root of a document
    globals: list[str]
        a list of importable elements (by formal-name)
    schema_dict: dict
        a dictionary containing the full, parsed metaschema
    """

    def __init__(self, schema_xsd: xmlschema.XMLSchema, file: Path):
        """
        Initializer for a MetaSchema instance

        Args:
            file (Path): A Path representing a local file.
            schema_xsd (xmlschema.XMLSchema): A parsed xml schema which can be passed in to prevent the same xsd from being parsed multiple times
        """
        # Parse the file
        parser = etree.XMLParser(resolve_entities=True)

        # TODO: process URLs or local paths - consider reading the bytes and passing them to etree instead of a file location
        metaschema_etree = etree.parse(file, parser=parser)

        # Extract the relevant data from the etree
        self.schema_dict = (
            cast(  # cast doesn't do anything, just shuts up the type checker
                dict,
                schema_xsd.to_dict(cast(xmlschema.XMLResource, metaschema_etree)),
            )
        )

        self.file = file.name
        self.short_name = cast(str, self.schema_dict["short-name"])
        self.imports = self._get_imports()
        self.globals = self._get_globals()
        self.roots = self._get_root_elements()

    def _read_local_metaschema(
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

    def _read_remote_metaschema(self, metaschema: str, baseurl: str) -> str:
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
            if "@href" in item.keys():
                import_list.append(item.get("@href"))

        return import_list

    def __repr__(self) -> str:
        return f"{self.__dict__}"
