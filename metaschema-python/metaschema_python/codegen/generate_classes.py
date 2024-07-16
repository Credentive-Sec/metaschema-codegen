import jinja2

from ..shared_types import SchemaID
from ..core.schemaparse import MetaSchema


class PackageGenerator:
    """
    This class takes a dict[SchemaID, MetaSchema] and generates a package with Python source code for each
    metaschemas present in the dictionary.
    """

    def __init__(self, parsed_metaschemas: dict[SchemaID, MetaSchema]) -> None:
        globals: dict[str, list[str, str]] = {}
        classes: list[ClassGenerator] = []
        schema_id_list = list(parsed_metaschemas.keys())
        # We parse in two passes. First we extract all the globals, then we call ClassGenerator on each class,
        # passing the globals as an argument

        for metaschema in parsed_metaschemas.values():
            classes.append(
                ClassGenerator(
                    metaschema=metaschema,
                    schema_file2name_map=schema_id_list,
                )
            )


class Document:
    """
    A Class to represent a document that containts a Metaschema compliant structure.
    This is used to collect all the metaschema assemblies with a 'root-name' attribute.
    """

    root_elements: list[str]


class ClassGenerator:
    """
    A class to generate python source code from a parsed metaschema
    """

    def __init__(
        self, metaschema: MetaSchema, schema_file2name_map: list[SchemaID]
    ) -> None:
        self.metaschema_dict = metaschema
        self.version = metaschema["schema-version"]
        self.package_name = metaschema["short-name"]
        self.assemblies = []
        self.fields = []
        self.flags = []

        # TODO: check the "import" for items with scope "global" or no scope (global is the default) - add them to the list of assemblies that can be referenced
        for sub_schema in self.metaschema_dict.get("import", []):
            # process imports and add the globals as available to import - assume that our naming scheme will be consistent
            schema_key = sub_schema.get("@href")

        # TODO: parse out definitions of fields, flags and assemblies
        for assembly in self.metaschema_dict["define-assembly"]:
            self.assemblies.append(self._generate_assembly(assembly_dict=assembly))

        for field in self.metaschema_dict["define-field"]:
            self.fields.append(self._generate_field(field_dict=field))

        for flag in self.metaschema_dict["define-flag"]:
            self.flags.append(self._generate_flag(flag_dict=flag))

        # TODO: create a directory corresponding the the metaschema namespace (top level assembly "root-name") (makes a python package)

        # TODO: iterate through definitions and pass them to the appropriate jinja templates. for "@ref", include an import and reference. check global imports.

    def _generate_flag(self, flag_dict) -> str:
        flag_class = ""
        # Parse flag data, pass to jinja template and return generated string
        return flag_class

    def _generate_field(self, field_dict) -> str:
        field_class = ""
        # Parse flag data, pass to jinja template and return generated string
        return field_class

    def _generate_assembly(self, assembly_dict) -> str:
        assembly_class = ""
        # Parse assembly data, pass to jinja template and return generated string
        return assembly_class

    def _generate_constraint(self, constraint_dict) -> str:
        constraint_class = ""
        # Parse constraint data, pass to jinja template and return generated string
        return constraint_class

    def _process_import(self, import_dict) -> dict[str, str]:
        """
        Add importable schema elements to the namespace of the current object. This function doesn't do full parsing,
        just adds the globals from the imported schema to the internal mapping table available to the classes for @ref
        calls.

        Args:
            import_dict (dict): A dict containing the parsed, imported schema.

        Returns:
            dict[str, str]: _description_
        """
        import_functions = {}

        return import_functions
