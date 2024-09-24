from __future__ import annotations

import urllib.parse
import datetime

from . import _initialize_jinja, ImportItem

from ...core.schemaparse import SimpleRestrictionDatatype, ComplexDataType, DataType

from .. import CodeGenException


jinja_env = _initialize_jinja()


class DatatypeModuleGenerator:
    """
    A class to generate the datatypes module, including all of the datatypes classes related to the models
    """

    def __init__(self, datatypes: list[DataType]) -> None:
        generatedclasses: list[str] = []
        # Generate the simple type classes

        # Map XML datatypes to python built-in types
        # This ignores any restrictions, e.g a positiveInteger is an int
        TYPE_MAP: dict[str, type] = {
            "anyURI": urllib.parse.ParseResult,
            "base64Binary": str,
            "boolean": bool,
            "date": datetime.date,
            "dateTime": datetime.datetime,
            "decimal": float,
            "duration": datetime.timedelta,
            "integer": int,
            "nonNegativeInteger": int,
            "positiveInteger": int,
            "string": str,
            "token": str,
        }

        # Metaschema datatypes can inherit from each other, or from an xml datatype.
        # We only count the "parent" datatype for purposes of inheritance if a datatype inherits from a
        # metaschema datatype.
        metaschema_parents = [datatype.name for datatype in datatypes]

        # First pass generates the datatypes
        simple_datatype_list = []
        for datatype in datatypes:
            if isinstance(datatype, SimpleRestrictionDatatype):
                datatype_dict = {}
                if datatype.base_type in metaschema_parents:
                    datatype_dict["parent"] = datatype.base_type

                datatype_dict["documentation"] = datatype.documentation

                datatype_dict["name"] = datatype.name

                datatype_dict["pattern"] = datatype.patterns["pcre"]

                if datatype.base_type in TYPE_MAP.keys():
                    datatype_dict["python_type"] = TYPE_MAP[datatype.base_type].__name__

                simple_datatype_list.append(datatype_dict)

            elif isinstance(datatype, ComplexDataType):
                datatype_dict = {}

                datatype_dict["documentation"] = datatype.documentation

                datatype_dict["name"] = datatype.name

                datatype_dict["elements"] = datatype.elements

                generatedclasses.extend(
                    ComplexDatatypesClassGenerator(
                        datatype_dict=datatype_dict
                    ).generated_class
                )

            else:
                raise CodeGenException(
                    "Unidentified dataclass type" + datatype.__class__.__name__
                )

        # Second pass pulls out classes without a metaschema parent
        parent_types = [
            type for type in simple_datatype_list if "parent" not in type.keys()
        ]
        for type_dict in parent_types:
            generatedclasses.extend(
                SimpleDatatypeClassGenerator(datatype_dict=type_dict).generated_class
            )

        # Final pass gets the rest of the types
        child_types = [type for type in simple_datatype_list if "parent" in type.keys()]
        for type_dict in child_types:
            generatedclasses.extend(
                SimpleDatatypeClassGenerator(datatype_dict=type_dict).generated_class
            )

        template_context = {}
        template_context["imports"] = [
            ImportItem(
                module=".base_classes", classes={"SimpleDatatype", "ComplexDataType"}
            ),
            ImportItem(module="re", classes={"Pattern", "compile"}),
        ]

        # Add the imports from TYPE_MAP - we do this dynamically so we only have to update one place.
        type_imports = {}
        for value in TYPE_MAP.values():
            type_name = value.__name__
            type_module = value.__module__

            if type_module != "builtins":
                name_set = type_imports.get(type_module, set())
                name_set.add(type_name)
                type_imports[type_module] = name_set

        for type_import in type_imports:
            template_context["imports"].append(
                ImportItem(
                    module=type_import,
                    classes=type_imports[type_import],
                )
            )

        # Finally, we are ready to generate the module source
        template_context["classes"] = generatedclasses

        template = jinja_env.get_template("module.py.jinja2")

        self.module_name = "datatypes"
        self.generated_module = template.render(template_context)


class SimpleDatatypeClassGenerator:
    """
    A class to convert the Metaschema Datatypes into classes
    """

    def __init__(self, datatype_dict: dict[str, str]):
        # process the datatypes to make the template context to pass to the template
        template = jinja_env.get_template("class_datatype_simple.py.jinja2")

        self.generated_class = template.render(datatype=datatype_dict)


class ComplexDatatypesClassGenerator:
    """
    A class to convert the Metaschema Datatypes into classes
    """

    # class ComplexDataType:
    # ref_name: str
    # class_name: str
    # elements: list[SimpleDataType | ComplexDataType]
    # description: str | None = None

    def __init__(self, datatype_dict: dict[str, str | list[str]]):
        # process the datatypes to make the template context to pass to the template
        template = jinja_env.get_template("class_datatype_complex.py.jinja2")

        self.generated_class = template.render(datatype=datatype_dict)
