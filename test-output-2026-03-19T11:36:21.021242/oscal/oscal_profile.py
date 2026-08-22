from __future__ import annotations

from . import base_classes


from datatypes import TokenDatatype, StringDatatype

from datatypes import TokenDatatype


class IncludeContainedControlswithControl(base_classes.Flag):
    """
    IncludeContainedControlswithControl is a flag of type TokenDatatype.

    When a control is included, whether its child (dependent) controls are also included.
    """
    name: str = "with_child_controls"
    datatype = datatypes.TokenDatatype
    constraints = [
        base_classes.AllowedValuesConstraint(
            target = base_classes.Metapath(expr="."),
            level = "ERROR",
            extensible = "external",
            enum = [
                base_classes.AllowedValuesConstraint.AllowedValue(value = "yes"),
                base_classes.AllowedValuesConstraint.AllowedValue(value = "no"),
                ]
        )
        ]

class Pattern(base_classes.Flag):
    """
    Pattern is a flag of type StringDatatype.

    {'a': [{'@href': 'https://en.wikipedia.org/wiki/Glob_(programming)', '$': 'glob expression'}]}
    """
    name: str = "pattern"
    datatype = datatypes.StringDatatype

class MatchControlsbyIdentifier(base_classes.Field):
    """
    MatchControlsbyIdentifier is a field of type TokenDatatype.

     Selecting a control by its ID given as a literal. 

    
    """
    name: str = 
    datatype = datatypes.TokenDatatype
    collapsible: bool = "no"