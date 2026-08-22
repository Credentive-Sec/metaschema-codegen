from __future__ import annotations

from . import base_classes


from datatypes import TokenDatatype

from datatypes import StringDatatype


class ControlIdentifierReference(base_classes.Flag):
    """
    ControlIdentifierReference is a flag of type TokenDatatype.

    {'code': ['id', 'control', 'Control Identifier Reference']}
    """
    name: str = "control_id"
    datatype = datatypes.TokenDatatype

class ParameterValue(base_classes.Field):
    """
    ParameterValue is a field of type StringDatatype.

     A parameter value or set of values. 

    
    """
    name: str = 
    datatype = datatypes.StringDatatype
    collapsible: bool = "no"