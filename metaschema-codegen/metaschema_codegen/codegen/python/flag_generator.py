from . import CommonTopLevelDefinition, GeneratedClass, ImportItem, _initialize_jinja

from .constraint_generator import ConstraintsGenerator

jinja_env = _initialize_jinja


class TopLevelFlagClassGenerator:
    """
    A class to generate a flag object from parsed metaschema flag data
    """

    def __init__(self, class_dict: dict, refs: dict[str, str]) -> None:
        # Parse flag data, and produce a GeneratedClass object
        template_context = CommonTopLevelDefinition(
            class_dict=class_dict
        ).common_properties

        # look up the datatype class in the class_dict
        datatype = class_dict["@as-type"]
        datatype_class = refs[datatype]

        template_context["datatype"] = datatype_class

        # Build constraints
        template_context["constraints"] = ConstraintsGenerator(
            constraint_dict=class_dict.get("constraint", {})
        ).constraints_classes

        template = jinja_env.get_template("class_flag.py.jinja2")

        class_code = template.render(template_context)

        self.generated_class = GeneratedClass(
            code=class_code,
            refs=[
                ImportItem(
                    module="datatypes",
                    classes=set([datatype_class]),
                )
            ],
        )


class InlineFlagClassGenerator:
    def __init__(self, class_dict: dict, refs: dict[str, str]):
        template_context = CommonTopLevelDefinition(
            class_dict=class_dict
        ).common_properties

        # look up the datatype class in the class_dict
        datatype = class_dict["@as-type"]
        datatype_class = refs[datatype]

        template_context["datatype"] = datatype_class

        # Build constraints
        template_context["constraints"] = ConstraintsGenerator(
            constraint_dict=class_dict.get("constraint", {})
        ).constraints_classes

        template = jinja_env.get_template("class_flag.py.jinja2")

        class_code = template.render(template_context)

        self.generated_class = GeneratedClass(
            code=class_code,
            refs=[
                ImportItem(
                    module="datatypes",
                    classes=set([datatype_class]),
                )
            ],
        )
