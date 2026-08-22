from __future__ import annotations

from . import base_classes


from datatypes import TokenDatatype, UUIDDatatype

from datatypes import TokenDatatype, URIDatatype


class SubjectUniversallyUniqueIdentifierReference(base_classes.Flag):
    """
    SubjectUniversallyUniqueIdentifierReference is a flag of type UUIDDatatype.

    {'a': [{'@href': 'https://pages.nist.gov/OSCAL/concepts/identifier-use/#machine-oriented', '$': 'machine-oriented'}]}
    """
    name: str = "subject_uuid"
    datatype = datatypes.UUIDDatatype

class SubjectUniversallyUniqueIdentifierReferenceType(base_classes.Flag):
    """
    SubjectUniversallyUniqueIdentifierReferenceType is a flag of type TokenDatatype.

    {'code': ['uuid-ref']}
    """
    name: str = "subject_type"
    datatype = datatypes.TokenDatatype
    constraints = [
        base_classes.AllowedValuesConstraint(
            target = base_classes.Metapath(expr="."),
            level = "ERROR",
            extensible = "external",
            enum = [
                base_classes.AllowedValuesConstraint.AllowedValue(value = "component"),
                base_classes.AllowedValuesConstraint.AllowedValue(value = "inventory-item"),
                base_classes.AllowedValuesConstraint.AllowedValue(value = "location"),
                base_classes.AllowedValuesConstraint.AllowedValue(value = "party"),
                base_classes.AllowedValuesConstraint.AllowedValue(value = "user"),
                base_classes.AllowedValuesConstraint.AllowedValue(value = "resource"),
                ]
        )
        ]

class ObjectiveID(base_classes.Flag):
    """
    ObjectiveID is a flag of type TokenDatatype.

    Points to an assessment objective.
    """
    name: str = "objective_id"
    datatype = datatypes.TokenDatatype

class ThreatID(base_classes.Field):
    """
    ThreatID is a field of type URIDatatype.

     A pointer, by ID, to an externally-defined threat. 

    
    """
    name: str = 
    datatype = datatypes.URIDatatype
    collapsible: bool = "no"class ThreatTypeIdentificationSystem(base_classes.Flag):
    """
    ThreatTypeIdentificationSystem is a flag of type URIDatatype.

    Specifies the source of the threat information.
    """
    name: str = "system"
    datatype = datatypes.URIDatatype
    constraints = [
        base_classes.AllowedValuesConstraint(
            target = base_classes.Metapath(expr="."),
            level = "ERROR",
            extensible = "external",
            enum = [
                base_classes.AllowedValuesConstraint.AllowedValue(value = "http://fedramp.gov"),
                base_classes.AllowedValuesConstraint.AllowedValue(value = "http://fedramp.gov/ns/oscal"),
                ]
        )
        ]class ThreatInformationResourceReference(base_classes.Flag):
    """
    ThreatInformationResourceReference is a flag of type URIReferenceDatatype.

    An optional location for the threat data, from which this ID originates.
    """
    name: str = "href"
    datatype = datatypes.URIReferenceDatatype

class RiskStatus(base_classes.Field):
    """
    RiskStatus is a field of type TokenDatatype.

     Describes the status of the associated risk. 

    
    """
    name: str = 
    datatype = datatypes.TokenDatatype
    collapsible: bool = "no"