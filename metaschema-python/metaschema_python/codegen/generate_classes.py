import jinja2
from typing import TypeAlias

from ..core.schemaparse import MetaSchemaSet


def _get_class_name(instance: str) -> str:
    """
    Returns the name of the Class that will instantiate a defined assembly, field or flag in a module.
    This is provided to ensure consistent names when translating from fields to anything else
    """
    # Strip spaces, convert dashes to underscores
    return f'{instance.replace(" ", "").replace("-","_")}'


class PackageGenerator:
    """
    This class takes a dict[SchemaID, MetaSchema] and generates a package with Python source code for each
    metaschemas present in the dictionary.
    """

    def __init__(self, parsed_metaschemas: MetaSchemaSet) -> None:
        self.classes: list[ModuleGenerator] = []

        # We process this in two passes. First we extract all the globals from all the items in the MetaSchemaSet,
        # then we call ClassGenerator on each class
        self.globals: dict[str, list[str]] = {}

        for metaschema in parsed_metaschemas.metaschemas:
            

        # Next, we parse the metaschemas, passing in the globals dict
        for metaschema in parsed_metaschemas.values():
            self.classes.append(
                ModuleGenerator(
                    metaschema=metaschema,
                    globals=self.globals,
                )
            )

    # TODO: create a directory corresponding the the metaschema namespace (top level assembly "root-name") (makes a python package)
    def write_package(self) -> None:
        """
        Writes all the files in the package to files at a location provided
        """
        pass


class Document:
    """
    A Class to represent a document that containts a Metaschema compliant structure.
    This is used to collect all the metaschema assemblies with a 'root-name' attribute.
    """

    root_elements: list[str]


class ModuleGenerator:
    """
    A class to generate python source code from a parsed metaschema
    """

    def __init__(self, metaschema: MetaSchemaSet) -> None:
        self.metaschema_dict = metaschema
        self.version = metaschema["schema-version"]
        self.module_name = metaschema["short-name"]
        self.assemblies = []
        self.fields = []
        self.flags = []
        self.imported_globals: GlobalsDictType = {}
        self.local_methods: dict[str, str] = {}

        # TODO: check the "import" for items with scope "global" or no scope (global is the default) - add them to the list of assemblies that can be referenced
        for sub_schema in self.metaschema_dict.get("import", []):
            # Create subset of globals that are relevant to our scope
            import_filename = sub_schema.get("@href")
            self.imported_globals[import_filename] = globals[import_filename]

        # TODO: parse out definitions of fields, flags and assemblies
        for assembly in self.metaschema_dict.get("define-assembly", []):
            self.assemblies.append(self._generate_assembly(assembly_dict=assembly))

        for field in self.metaschema_dict.get("define-field", []):
            self.fields.append(self._generate_field(field_dict=field))

        for flag in self.metaschema_dict.get("define-flag", []):
            self.flags.append(self._generate_flag(flag_dict=flag))

        # TODO: iterate through definitions and pass them to the appropriate jinja templates. for "@ref", include an import and reference. check global imports.

    def _get_local_methods(self) -> None:
        """
        Returns the local symbols defined in this metaschema, so that we can dereference "@refs"
        """

        # return empty list if key does not exist
        for assembly in self.metaschema_dict.get("define-assembly", []):
            self.local_methods[assembly["@name"]] = (
                f'{self.metaschema_dict._get_class_name(assembly["formal-name"])}'
            )
        # return empty list if key does not exist
        for field in self.metaschema_dict.get("define-field", []):
            self.local_methods[field["@name"]] = (
                f'{self.metaschema_dict._get_class_name(field["formal-name"])}'
            )
        # return empty list if key does not exist
        for flag in self.metaschema_dict.get("define-flag", []):
            self.local_methods[flag["@name"]] = (
                f'{self.metaschema_dict._get_class_name(flag["formal-name"])}'
            )

    def _generate_assembly(self, assembly_dict) -> dict[str, str]:
        assembly_class = {}
        assembly_class["name"] = self.metaschema_dict._get_class_name(
            assembly_dict["formal-name"]
        )
        assembly_class["root-name"] = assembly_dict.get("root-name", None)
        if "define-flag" in assembly_dict.keys():
            pass

        return assembly_class

    def _generate_flag(self, flag_dict) -> str:
        flag_class = ""
        # Parse flag data, pass to jinja template and return generated string
        return flag_class

    def _generate_field(self, field_dict) -> str:
        field_class = ""
        # Parse flag data, pass to jinja template and return generated string
        return field_class

    def _generate_constraint(self, constraint_dict) -> str:
        constraint_class = ""
        # Parse constraint data, pass to jinja template and return generated string
        return constraint_class
