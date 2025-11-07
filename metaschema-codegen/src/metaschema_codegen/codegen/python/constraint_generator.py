import re

from . import _initialize_jinja

from .. import CodeGenException

from typing import cast

jinja_env = _initialize_jinja()

OSCAL_NAMESPACE_RE = re.compile(r".*?has-oscal-namespace\((?P<ns>['\w:\/\. ,\(\)]+?)\)(?P<other_conditions>.*?)\].*?")

class MetaPathParser:
    """
    A class to parse metaschema into a format that support processing
    """
    def __init__(self, target_path: str) -> None:
        """
        Initializes the ConstraintGenerator with the specified target path.
        Args:
        target_path (str): The metapath defined at the "@target" field.        
        """

        # Before processing the path, replace "has-oscal-namespace" with the XPath equivalent
        #  target="field/@ns = 'http://csrc.nist.gov/ns/oscal'" in place of target="fieldt[has-oscal-namespace('http://csrc.nist.gov/ns/oscal')"

        if "has-oscal-namespace" in target_path:
            matches = re.findall(OSCAL_NAMESPACE_RE, target_path)
            for match in matches:
                # cast doesn't do anything, it's just for the type checker
                # We know our regex has multiple capture groups, so will always return tuples
                cast(tuple[str], match) 
                

            pass

class ConstraintsGenerator:
    """
    A class to convert a set of constraints into a format that can be fed to a code generation template.
    """

    def __init__(self, constraint_dict: dict[str, dict]) -> None:
        """
        __init__ Recursively parses a constraint and produces a template context.

        Args:
            constraint_dict (dict): "constraint" dictionary parsed from a metaschema element.
        """

        """
        NOTE: 
        constraints are structured as a dict, with the type as key and the details as value
        if there is only a single constraint of a type, it will be a dict. if there is more than one, it will be a list of dicts
        "constraint" : {
          "type": [ (constraints_by_type)
              {
                  "prop": "value", (constraint_prop, constraint_value)
                  "prop": [
                    "key": "value",
                    "key": "value"
                  ],

                  <...>
              } (constraints_of_type)
          ]
        }
        """

        self.constraints_classes = []
        for constraint_type, constraints_of_type in constraint_dict.items():
            # constraints_of_type can be a list of dicts or a single dict.
            # It's easier to process if they are all the same, so if it's a dict,
            # we make it a list with a single member.
            if isinstance(constraints_of_type, dict):
                constraints_of_type = [constraints_of_type]  # now it's a list :)

            if constraint_type == "allowed-values":
                self.constraints_classes.append(
                    AllowedValueConstraintsGenerator(
                        constraints_of_type
                    ).constraint_classes
                )
            else:
                pass
                # TODO: Uncomment the thing below once we have the core constraints implemented.
                # raise CodeGenException("Unrecognized or unimplemented constraint type")

    @classmethod
    def _generate(cls, template_file: str, template_context: list[dict]) -> str:
        template = jinja_env.get_template(template_file)
        constraint_class = template.render({"constraints": template_context})
        return constraint_class


class AllowedValueConstraintsGenerator:
    def __init__(self, constraints: list[dict]) -> None:
        allowed_values_list = []
        self.constraint_classes: str

        for constraint in constraints:
            target = constraint.get("@target", ".")
            allow_other = constraint.get("@allow-other", "no")
            level = constraint.get("@level", "ERROR")
            extensible = constraint.get("@extensible", "model")

            try:
                constraint_enums = constraint["enum"]
            except KeyError:
                raise CodeGenException(
                    "Allowed-value constraint has no enumerated values"
                )

            processed_enums = []
            for enum in constraint_enums:
                try:
                    # value is mandatory with no default, so it's okay if we raise an exception here
                    value = enum["@value"]
                except KeyError:
                    raise CodeGenException(
                        f"No value in enum under constraint {target}"
                    )
                # TODO: figure out how to handle the contents of the tag (e.g. the description)
                # It is of type MarkupLine, so maybe we could re-use that.
                processed_enums.append({"value": value})

            # We've completed processing, add it to the list
            allowed_values_list.append(
                {
                    "target": target,
                    "allow_other": allow_other,
                    "level": level,
                    "extensible": extensible,
                    "enums": processed_enums,
                }
            )

        # We've processed the data, now we create the class code

        self.constraint_classes = ConstraintsGenerator._generate(
            template_file="allowed-values-constraints.py.jinja2",
            template_context=allowed_values_list,
        )
