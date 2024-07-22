from __future__ import annotations

import jinja2
from typing import NamedTuple, cast, Literal
from pathlib import Path

from ..core.schemaparse import MetaSchemaSet, MetaSchema, DataType


# Module functions and variables


def _pythonize_name(name: str) -> str:
    """
    Returns the name of the class or variable for a defined assembly, field or flag in a module.
    Makes the name python safe by stripping spaces and converts dashes to underscores.
    This is provided to ensure consistent names when translating from fields to anything else.
    """
    # Strip spaces, convert dashes to underscores
    return f'{name.replace(" ", "").replace("-","_")}'


# Intialize the jinja environment
jinja_env = jinja2.Environment(
    loader=jinja2.PackageLoader(package_name="metaschema_python.codegen")
)


class GlobalRef(NamedTuple):
    """
    A NamedTuple to represent an element exported from a metaschema by being tagged "global". This is used to simplify
    generation of import statements and references in one module to classes defined in another module.

    Elements:
        NamedTuple (_type_): _description_
        schema_source: (str):  the metaschema defining the global
        module_name: (str): the name of the module where this ref will be located
        ref_name: (str): the name of the property that will be the "@ref"
        class_name: (str): the name of the class that will represent the element referenced
    """

    schema_source: str
    module_name: str
    ref_name: str
    class_name: str


class Document(NamedTuple):
    """
    A Class to represent a document that containts a Metaschema compliant structure, used to collect all the metaschema
    assemblies with a 'root-name' attribute. This class is not referenced directly in metascheama, but must exist for a
    root assembly to be JSON serialized by python.
    """

    root_elements: list[str]


class PackageGenerator:
    """
    This class is initialized with a MetaSchemaSet and generates a package with Python source code for each of the metaschemas.
    """

    def __init__(
        self,
        parsed_metaschemas: MetaSchemaSet,
        destination_directory: Path,
        package_name: str,
    ) -> None:
        # initialize the package
        self.destination = destination_directory
        self.package_name = package_name
        self.module_generators: list[ModuleGenerator] = []

        # Get the global symbols from all the metaschemas in the MetaschemaSet
        self.global_refs: list[GlobalRef] = []
        for metaschema in parsed_metaschemas.metaschemas:
            schema_source = str(metaschema.file)
            module_name = _pythonize_name(metaschema.short_name)
            for global_ref_key in metaschema.globals:
                self.global_refs.append(
                    GlobalRef(
                        schema_source=schema_source,
                        module_name=module_name,
                        ref_name=global_ref_key,
                        class_name=metaschema.globals[global_ref_key],
                    )
                )

        # add references for metaschema datatypes, they look a little strange because they're in the metaschema xsd,
        # not a specific metaschema
        for datatype in parsed_metaschemas.datatypes:
            self.global_refs.append(
                GlobalRef(
                    schema_source="datatype",
                    module_name="datatypes",
                    ref_name=datatype.name,
                    class_name=datatype.name,
                )
            )

        for metaschema in parsed_metaschemas.metaschemas:
            self.module_generators.append(
                ModuleGenerator(
                    metaschema=metaschema,
                    global_refs=self.global_refs,
                )
            )

    # TODO: create a directory corresponding the the metaschema namespace (top level assembly "root-name") (makes a python package)
    def write_package(self) -> None:
        """
        Writes all the files in the package to files at a location provided
        """
        pass

    def _pythonized_export_names(self, metaschema: MetaSchema) -> list[str]:
        """
        given a list of global symbols from a metaschema, convert it to a python safe string of the form "method.Class" for reference in other python strings

        Args:
            metaschema (MetaSchema): the Metaschema to be processed

        Returns:
            list[str]: a list of exported functions from the module in python safe format
        """
        # convert short name to a python module name
        module_name = _pythonize_name(metaschema.short_name)

        # convert all element names to python safe names, and prepend the module name
        class_names = [
            f"{module_name}.{_pythonize_name(_class)}" for _class in metaschema.globals
        ]
        return class_names


class ModuleGenerator:
    """
    A class to generate python source code from a parsed metaschema.
    It converts a data object representing a generic metaschema to a python oriented dictionary to pass to a template.
    """

    def __init__(self, metaschema: MetaSchema, global_refs: list[GlobalRef]) -> None:
        self.metaschema = metaschema
        self.version = cast(str, self.metaschema["schema-version"])
        self.module_name = _pythonize_name(cast(str, self.metaschema["short-name"]))
        self.module_imports = []
        self.class_generators: list[ClassGenerator] = []

        #
        # The first pass is to generate the list of elements imported by or defined in the metaschema so that we can
        # identify the appropriate class for a "@ref"
        #

        # get a list of elements from imports that could be referenced with a "@ref" in this module
        imported_schemas = [
            _import["@href"] for _import in self.metaschema.get("import", [])
        ]

        module_refs: dict[str, str] = {}
        for schema in imported_schemas:
            module_refs.update(
                {
                    g_ref.ref_name: g_ref.class_name
                    for g_ref in global_refs
                    if g_ref.schema_source == schema
                }
            )

        module_refs.update(self._get_local_refs())

        #
        # With our ref dictionary in place, we can parse through the underlying elements.
        #

        # TODO: parse out definitions of fields, flags and assemblies
        for assembly in self.metaschema.get("define-assembly", []):
            self.class_generators.append(
                ClassGenerator(
                    class_dict=assembly,
                    type="assembly",
                    refs=list(module_refs.keys()),
                )
            )

        for field in self.metaschema.get("define-field", []):
            self.class_generators.append(
                ClassGenerator(
                    class_dict=field,
                    type="field",
                )
            )

        for flag in self.metaschema.get("define-flag", []):
            self.class_generators.append(
                ClassGenerator(
                    class_dict=flag,
                    type=flag,
                )
            )

        # TODO: iterate through definitions and pass them to the appropriate jinja templates. for "@ref", include an import and reference. check global imports.

    def _get_local_refs(self) -> dict[str, str]:
        """
        Returns the local symbols defined in this metaschema, so that we can dereference "@refs".  This is the first pass.
        """
        local_refs = {}

        for assembly in self.metaschema.get("define-assembly", []):
            local_refs[f'{_pythonize_name(assembly["@name"])}'] = (
                f'{_pythonize_name(assembly["formal-name"])}'
            )

        for field in self.metaschema.get("define-field", []):
            local_refs[f'{_pythonize_name(field["@name"])}'] = (
                f'{_pythonize_name(field["formal-name"])}'
            )

        for flag in self.metaschema.get("define-flag", []):
            local_refs[f'{_pythonize_name(assembly["@name"])}'] = (
                f'{_pythonize_name(assembly["formal-name"])}'
            )

        return local_refs


class ClassGenerator:
    """
    A class to convert an Assembly, Field or Flag into a dictionary that can be passed to a template.
    """

    def __init__(
        self,
        class_dict: dict,
        type: Literal["assembly", "field", "flag"],
        refs: list[str] = [],
    ):
        # Call the appropriate function for the type, which will load and populate the template
        if type == "assembly":
            self._generate_assembly(assembly_dict=class_dict)
        elif type == "field":
            self._generate_field(field_dict=class_dict)
        else:
            self._generate_flag(flag_dict=class_dict)

    def _generate_assembly(self, assembly_dict: dict[str, str]) -> dict[str, str]:
        assembly_class = {}
        assembly_class["name"] = _pythonize_name(assembly_dict["formal-name"])
        assembly_class["root-name"] = assembly_dict.get("root-name", None)
        assembly_class["flags"] = []

        for flag in assembly_dict.get("define-flag", []):
            assembly_class["flags"].append(self._generate_flag(flag))

        return assembly_class

    def _generate_flag(self, flag_dict) -> str:
        flag_class = ""
        # Parse flag data, pass to jinja template and return generated string
        template_context = {}
        template_context["base_class"] = "Flag"
        template_context["class_name"] = flag_dict["@name"]
        return flag_class

    def _generate_field(self, field_dict) -> str:
        field_class = ""
        # Parse flag data, pass to jinja template and return generated string
        # Fields should reference datatypes which will be generated from MetaschemaSet.datatypes
        template = jinja_env.get_template("field_class.py.jinja2")
        # Parse field data, pass to jinja template and return generated string
        template_context = {}
        template_context["class_name"] = _pythonize_name(field_dict["formal-name"])
        template_context["datatype"] = field_dict["@as-type"]
        return field_class

    def _generate_constraint(self, constraint_dict) -> str:
        constraint_class = ""
        # Parse constraint data, pass to jinja template and return generated string
        return constraint_class


class DatatypesGenerator:
    """
    A class to convert the Metaschema Datatypes into classes
    """

    def __init__(self, datatypes: list[DataType]):
        # process the datatypes to make the template context to pass to the template
        template_context = {}

        # Metaschema datatypes can inherit from each other, or from an xml datatype.
        # We only count the "parent" datatype for purposes of inheritance if a datatype inherits from a
        # metaschema datatype.
        metaschema_parents = [datatype.name for datatype in datatypes]

        datatype_list = []
        for datatype in datatypes:

            # make the description a single line
            if len(datatype.description) > 0:
                description = "".join(datatype.description)
            else:
                description = None

            # check to see if the parent is another metaschema type
            if datatype.base_type in metaschema_parents:
                parent = datatype.base_type
                pattern = None
            else:
                parent = None
                pattern = datatype.pattern

            datatype_list.append(
                {
                    "name": datatype.name,
                    "pattern": pattern,
                    "description": description,
                    "parent": parent,
                }
            )
        template_context["datatypes"] = datatype_list

        template = jinja_env.get_template("datatypes.py.jinja2")

        self.datatype_module = template.render(template_context)
