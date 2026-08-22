from __future__ import annotations

from . import base_classes


from datatypes import TokenDatatype, StringDatatype

from datatypes import StringDatatype


class ComponentType(base_classes.Flag):
    """
    ComponentType is a flag of type StringDatatype.

    A category describing the purpose of the component.
    """
    name: str = "system_component_type"
    datatype = datatypes.StringDatatype
    constraints = [
        base_classes.AllowedValuesConstraint(
            target = base_classes.Metapath(expr="."),
            level = "ERROR",
            extensible = "external",
            enum = [
                base_classes.AllowedValuesConstraint.AllowedValue(value = "this-system"),
                base_classes.AllowedValuesConstraint.AllowedValue(value = "system"),
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
                base_classes.AllowedValuesConstraint.AllowedValue(value = "network"),
                ]
        )
        ]

class ControlStatementReference(base_classes.Flag):
    """
    ControlStatementReference is a flag of type TokenDatatype.

    {'a': [{'@href': 'https://pages.nist.gov/OSCAL/concepts/identifier-use/#human-oriented', '$': 'human-oriented'}], 'code': ['control statement']}
    """
    name: str = "statement_id"
    datatype = datatypes.TokenDatatype

class ParameterID(base_classes.Flag):
    """
    ParameterID is a flag of type TokenDatatype.

    {'a': [{'@href': 'https://pages.nist.gov/OSCAL/concepts/identifier-use/#human-oriented', '$': 'human-oriented'}], 'code': ['parameter']}
    """
    name: str = "param_id"
    datatype = datatypes.TokenDatatype

class FunctionsPerformed(base_classes.Field):
    """
    FunctionsPerformed is a field of type StringDatatype.

     Describes a function performed for a given authorized privilege by this user class. 

    
    """
    name: str = 
    datatype = datatypes.StringDatatype
    collapsible: bool = "no"

class SystemIdentification(base_classes.Field):
    """
    SystemIdentification is a field of type StringDatatype.

     {'a': [{'@href': 'https://pages.nist.gov/OSCAL/concepts/identifier-use/#human-oriented', '$': 'human-oriented'}, {'@href': 'https://pages.nist.gov/OSCAL/concepts/identifier-use/#globally-unique', '$': 'globally unique'}, {'@href': 'https://pages.nist.gov/OSCAL/concepts/identifier-use/#cross-instance', '$': 'cross-instance'}, {'@href': 'https://pages.nist.gov/OSCAL/concepts/identifier-use/#scope', '$': 'this or other OSCAL instances'}, {'@href': 'https://pages.nist.gov/OSCAL/concepts/identifier-use/#consistency', '$': 'per-subject'}], 'code': ['system identification', 'system identification']} 

    
    """
    name: str = 
    datatype = datatypes.StringDatatype
    collapsible: bool = "no"class IdentificationSystemType(base_classes.Flag):
    """
    IdentificationSystemType is a flag of type URIDatatype.

    Identifies the identification system from which the provided identifier was assigned.
    """
    name: str = "identifier_type"
    datatype = datatypes.URIDatatype
    constraints = [
        base_classes.AllowedValuesConstraint(
            target = base_classes.Metapath(expr="."),
            level = "ERROR",
            extensible = "external",
            enum = [
                base_classes.AllowedValuesConstraint.AllowedValue(value = "https://fedramp.gov"),
                base_classes.AllowedValuesConstraint.AllowedValue(value = "http://fedramp.gov/ns/oscal"),
                base_classes.AllowedValuesConstraint.AllowedValue(value = "https://ietf.org/rfc/rfc4122"),
                base_classes.AllowedValuesConstraint.AllowedValue(value = "http://ietf.org/rfc/rfc4122"),
                ]
        )
        ]