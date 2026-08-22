from __future__ import annotations

from . import base_classes


from datatypes import StringDatatype


class ComponentType(base_classes.Flag):
    """
    ComponentType is a flag of type StringDatatype.

    A category describing the purpose of the component.
    """
    name: str = "defined_component_type"
    datatype = datatypes.StringDatatype
    constraints = [
        base_classes.AllowedValuesConstraint(
            target = base_classes.Metapath(expr="."),
            level = "ERROR",
            extensible = "external",
            enum = [
                base_classes.AllowedValuesConstraint.AllowedValue(value = "interconnection"),
                base_classes.AllowedValuesConstraint.AllowedValue(value = "software"),
                base_classes.AllowedValuesConstraint.AllowedValue(value = "hardware"),
                base_classes.AllowedValuesConstraint.AllowedValue(value = "service"),
                base_classes.AllowedValuesConstraint.AllowedValue(value = "policy"),
                base_classes.AllowedValuesConstraint.AllowedValue(value = "physical"),
                base_classes.AllowedValuesConstraint.AllowedValue(value = "process-procedure"),
                base_classes.AllowedValuesConstraint.AllowedValue(value = "plan"),
                base_classes.AllowedValuesConstraint.AllowedValue(value = "guidance"),
                base_classes.AllowedValuesConstraint.AllowedValue(value = "standard"),
                base_classes.AllowedValuesConstraint.AllowedValue(value = "validation"),
                ]
        )
        ]