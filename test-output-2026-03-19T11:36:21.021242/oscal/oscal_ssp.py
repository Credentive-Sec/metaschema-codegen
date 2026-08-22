from __future__ import annotations

from . import base_classes


from datatypes import UUIDDatatype

from datatypes import StringDatatype, MarkupMultilineDatatype, DateDatatype


class ProvidedUUID(base_classes.Flag):
    """
    ProvidedUUID is a flag of type UUIDDatatype.

    {'a': [{'@href': 'https://pages.nist.gov/OSCAL/concepts/identifier-use/#machine-oriented', '$': 'machine-oriented'}]}
    """
    name: str = "provided_uuid"
    datatype = datatypes.UUIDDatatype

class ResponsibilityUUID(base_classes.Flag):
    """
    ResponsibilityUUID is a flag of type UUIDDatatype.

    {'a': [{'@href': 'https://pages.nist.gov/OSCAL/concepts/identifier-use/#machine-oriented', '$': 'machine-oriented'}]}
    """
    name: str = "responsibility_uuid"
    datatype = datatypes.UUIDDatatype

class BaseLevel(base_classes.Field):
    """
    BaseLevel is a field of type StringDatatype.

     The prescribed base (Confidentiality, Integrity, or Availability) security impact level. 

    
    """
    name: str = 
    datatype = datatypes.StringDatatype
    collapsible: bool = "no"

class SelectedLevel(base_classes.Field):
    """
    SelectedLevel is a field of type StringDatatype.

     The selected (Confidentiality, Integrity, or Availability) security impact level. 

    
    """
    name: str = 
    datatype = datatypes.StringDatatype
    collapsible: bool = "no"

class AdjustmentJustification(base_classes.Field):
    """
    AdjustmentJustification is a field of type MarkupMultilineDatatype.

     If the selected security level is different from the base security level, this contains the justification for the change. 

    
    """
    name: str = 
    datatype = datatypes.MarkupMultilineDatatype
    collapsible: bool = "no"

class SystemAuthorizationDate(base_classes.Field):
    """
    SystemAuthorizationDate is a field of type DateDatatype.

     The date the system received its authorization. 

    
    """
    name: str = 
    datatype = datatypes.DateDatatype
    collapsible: bool = "no"