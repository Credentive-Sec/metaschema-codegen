from . import (
    CommonTopLevelDefinition,
    GroupAsParser,
    GeneratedClass,
    ImportItem,
    _initialize_jinja,
)

from .constraint_generator import ConstraintsGenerator

from .flag_generator import InlineFlagClassGenerator

jinja_env = _initialize_jinja()


class TopLevelFieldClassGenerator:
    """
    A class to generate a top-level field object from parsed metaschema field data
    """

    def __init__(self, class_dict: dict, refs: dict[str, str]) -> None:
        template_context = CommonTopLevelDefinition(
            class_dict=class_dict
        ).common_properties

        datatype = class_dict["@as-type"]
        datatype_ref = refs[datatype]
        template_context["data_type"] = datatype_ref

        # collapsible is optional, with a default value of "no"
        template_context["collapsible"] = class_dict.get("@collapsible", "no")

        template_context["default"] = class_dict.get("@default")

        template_context["description"] = class_dict.get("description")

        template_context["json_key"] = class_dict.get("json-key")
        template_context["json_value_key"] = class_dict.get("json-value-key")
        template_context["json_value_key_flag"] = class_dict.get("json-value-key-flag")

        if class_dict.get("@min-occurs", 0) > 0:
            template_context["mandatory"] = True

        if class_dict.get("@max-occurs") is not None:
            if class_dict["@max-occurs"] == "unbounded":
                template_context["bounded"] = 0
            else:
                template_context["bounded"] = class_dict.get("@max-occurs")

        template_context["json_value_key"] = class_dict.get("json-value-key")

        if "group-as" in class_dict.keys():
            template_context["group_as"] = GroupAsParser.parse(class_dict["group-as"])

        # Build constraints
        template_context["constraints"] = ConstraintsGenerator(
            constraint_dict=class_dict.get("constraint", {})
        ).constraints_classes

        inline_flags = []
        if "define-flag" in class_dict.keys():
            for flag in class_dict["define-flag"]:
                inline_flags.append(
                    InlineFlagClassGenerator(class_dict=flag, refs=refs).generated_class
                )

        template_context["inline-flags"] = inline_flags

        template = jinja_env.get_template("class_field.py.jinja2")
        self.generated_class = GeneratedClass(
            code=template.render(template_context),
            refs=[
                ImportItem(
                    module="datatypes",
                    classes=set([datatype_ref]),
                )
            ],
        )
