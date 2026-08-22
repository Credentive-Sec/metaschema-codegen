from __future__ import annotations

from . import base_classes


from datatypes import TokenDatatype, StringDatatype, UUIDDatatype

from datatypes import UUIDDatatype, DateTimeWithTimezoneDatatype, StringDatatype, TokenDatatype, MarkupMultilineDatatype, EmailAddress


class LocationUniversallyUniqueIdentifierReference(base_classes.Flag):
    """
    LocationUniversallyUniqueIdentifierReference is a flag of type UUIDDatatype.

    Reference to a location by UUID.
    """
    name: str = "location_uuid"
    datatype = datatypes.UUIDDatatype

class MediaType(base_classes.Flag):
    """
    MediaType is a flag of type StringDatatype.

    A label that indicates the nature of a resource, as a data serialization or
            format.
    """
    name: str = "media_type"
    datatype = datatypes.StringDatatype

class AddressType(base_classes.Flag):
    """
    AddressType is a flag of type TokenDatatype.

    Indicates the type of address.
    """
    name: str = "location_type"
    datatype = datatypes.TokenDatatype
    constraints = [
        base_classes.AllowedValuesConstraint(
            target = base_classes.Metapath(expr="."),
            level = "ERROR",
            extensible = "external",
            enum = [
                base_classes.AllowedValuesConstraint.AllowedValue(value = "home"),
                base_classes.AllowedValuesConstraint.AllowedValue(value = "work"),
                ]
        )
        ]

class LocationUniversallyUniqueIdentifierReference(base_classes.Field):
    """
    LocationUniversallyUniqueIdentifierReference is a field of type UUIDDatatype.

     Reference to a location by UUID. 

    
    Class Property: value_type: identifier_reference
    
    Class Property: identifier_type: machine_oriented
    
    Class Property: identifier_scope: cross_instance
    
    """
    name: str = 
    datatype = datatypes.UUIDDatatype
    collapsible: bool = "no"

class PartyUniversallyUniqueIdentifierReference(base_classes.Field):
    """
    PartyUniversallyUniqueIdentifierReference is a field of type UUIDDatatype.

     Reference to a party by UUID. 

    
    Class Property: value_type: identifier_reference
    
    Class Property: identifier_type: machine_oriented
    
    Class Property: identifier_scope: cross_instance
    
    """
    name: str = 
    datatype = datatypes.UUIDDatatype
    collapsible: bool = "no"

class RoleIdentifierReference(base_classes.Field):
    """
    RoleIdentifierReference is a field of type TokenDatatype.

     Reference to a role by UUID. 

    
    Class Property: value_type: identifier_reference
    
    Class Property: identifier_type: human_oriented
    
    Class Property: identifier_scope: cross_instance
    
    """
    name: str = 
    datatype = datatypes.TokenDatatype
    collapsible: bool = "no"

class Hash(base_classes.Field):
    """
    Hash is a field of type StringDatatype.

     A representation of a cryptographic digest generated over a resource using a specified hash algorithm. 

    
    """
    name: str = 
    datatype = datatypes.StringDatatype
    collapsible: bool = "no"class Hashalgorithm(base_classes.Flag):
    """
    Hashalgorithm is a flag of type StringDatatype.

    The digest method by which a hash is derived.
    """
    name: str = "algorithm"
    datatype = datatypes.StringDatatype
    constraints = [
        base_classes.AllowedValuesConstraint(
            target = base_classes.Metapath(expr="."),
            level = "ERROR",
            extensible = "external",
            enum = [
                base_classes.AllowedValuesConstraint.AllowedValue(value = "SHA-224"),
                base_classes.AllowedValuesConstraint.AllowedValue(value = "SHA-256"),
                base_classes.AllowedValuesConstraint.AllowedValue(value = "SHA-384"),
                base_classes.AllowedValuesConstraint.AllowedValue(value = "SHA-512"),
                base_classes.AllowedValuesConstraint.AllowedValue(value = "SHA3-224"),
                base_classes.AllowedValuesConstraint.AllowedValue(value = "SHA3-256"),
                base_classes.AllowedValuesConstraint.AllowedValue(value = "SHA3-384"),
                base_classes.AllowedValuesConstraint.AllowedValue(value = "SHA3-512"),
                ]
        )
        ]

class Remarks(base_classes.Field):
    """
    Remarks is a field of type MarkupMultilineDatatype.

     Additional commentary about the containing object. 

    
    """
    name: str = 
    datatype = datatypes.MarkupMultilineDatatype
    collapsible: bool = "no"

class PublicationTimestamp(base_classes.Field):
    """
    PublicationTimestamp is a field of type DateTimeWithTimezoneDatatype.

     The date and time the document was last made available. 

    
    """
    name: str = 
    datatype = datatypes.DateTimeWithTimezoneDatatype
    collapsible: bool = "no"

class LastModifiedTimestamp(base_classes.Field):
    """
    LastModifiedTimestamp is a field of type DateTimeWithTimezoneDatatype.

     The date and time the document was last stored for later retrieval. 

    
    """
    name: str = 
    datatype = datatypes.DateTimeWithTimezoneDatatype
    collapsible: bool = "no"

class DocumentVersion(base_classes.Field):
    """
    DocumentVersion is a field of type StringDatatype.

     Used to distinguish a specific revision of an OSCAL document from other previous and future versions. 

    
    """
    name: str = 
    datatype = datatypes.StringDatatype
    collapsible: bool = "no"

class OSCALVersion(base_classes.Field):
    """
    OSCALVersion is a field of type StringDatatype.

     The OSCAL model version the document was authored against and will conform to as valid. 

    
    """
    name: str = 
    datatype = datatypes.StringDatatype
    collapsible: bool = "no"

class EmailAddress(base_classes.Field):
    """
    EmailAddress is a field of type EmailAddress.

     {'a': [{'@href': 'https://tools.ietf.org/html/rfc5322#section-3.4.1', '$': 'RFC 5322 Section\n            3.4.1'}]} 

    
    """
    name: str = 
    datatype = datatypes.EmailAddress
    collapsible: bool = "no"

class TelephoneNumber(base_classes.Field):
    """
    TelephoneNumber is a field of type StringDatatype.

     {'a': [{'@href': 'https://www.itu.int/rec/T-REC-E.164-201011-I/en', '$': 'ITU-T E.164'}]} 

    
    """
    name: str = 
    datatype = datatypes.StringDatatype
    collapsible: bool = "no"class typeflag(base_classes.Flag):
    """
    typeflag is a flag of type StringDatatype.

    Indicates the type of phone number.
    """
    name: str = "type"
    datatype = datatypes.StringDatatype
    constraints = [
        base_classes.AllowedValuesConstraint(
            target = base_classes.Metapath(expr="."),
            level = "ERROR",
            extensible = "external",
            enum = [
                base_classes.AllowedValuesConstraint.AllowedValue(value = "home"),
                base_classes.AllowedValuesConstraint.AllowedValue(value = "office"),
                base_classes.AllowedValuesConstraint.AllowedValue(value = "mobile"),
                ]
        )
        ]

class Addressline(base_classes.Field):
    """
    Addressline is a field of type StringDatatype.

     A single line of an address. 

    
    """
    name: str = 
    datatype = datatypes.StringDatatype
    collapsible: bool = "no"

class DocumentIdentifier(base_classes.Field):
    """
    DocumentIdentifier is a field of type StringDatatype.

     {'code': ['scheme']} 

    
    """
    name: str = 
    datatype = datatypes.StringDatatype
    collapsible: bool = "no"class DocumentIdentificationScheme(base_classes.Flag):
    """
    DocumentIdentificationScheme is a flag of type URIDatatype.

    Qualifies the kind of document identifier using a URI. If the scheme is not
                provided the value of the element will be interpreted as a string of
                characters.
    """
    name: str = "scheme"
    datatype = datatypes.URIDatatype
    constraints = [
        base_classes.AllowedValuesConstraint(
            target = base_classes.Metapath(expr="."),
            level = "ERROR",
            extensible = "external",
            enum = [
                base_classes.AllowedValuesConstraint.AllowedValue(value = "http://www.doi.org/"),
                ]
        )
        ]