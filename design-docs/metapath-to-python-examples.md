# Metaschema to Python Examples

## Introduction

This document identifies patterns for converting metapath into its python equivalent


## Example 1

assessment-common_metaschema
assembly = local objective

### Metapath

```xml
part[has-oscal-namespace('http://csrc.nist.gov/ns/oscal') and @name=('objective','assessment-objective')]
```

### Plain-language translation

Every part field in this component where the oscal namespace is 'http://csrc.nist.gov/ns/oscal' and the name is "objective" or "assessment-objective"

### Python Implementation

**for loop**

```python
matches = []
for part in parts:
    if part.namespace == 'http://csrc.nist.gov/ns/oscal' and part.name in ["objective", "assessment-objective"]:
        matches.append(part)
```

**list comprehension**

```python
matches = [part for part in parts if part.namespace == 'http://csrc.nist.gov/ns/oscal' and part.name in ["objective", "assessment-objective"]]
```

## Example 2

oscal_catalog_metaschema
assembly: catalog

### Metapath

```xml
//part
```

### Plain-language translation

Every part field in this object or any object contained in this object.

### Python implementation

**for loop**

```python
import dataclasses

def find_fields(dc_obj: MetaschemaABC, field_name: str): # Check the type hint can you reference and ABC?
    if not dataclasses.is_dataclass(dc_obj): # if we aren't called with a dataclass, just return empty immediately
        return []

    matching_fields = []
    for field in dc_obj.fields():
        # Add the fields from this dataclass
        if field.name == field_name:
            matching_fields.append(field)

        # recurse into the fields to see if there are matching fields in there
        matching_fields.extend(find_fields(field))

    return matching_fields
```

**list comprehension**

```python
import dataclasses

def find_fields(dc_obj: MetaschemaABC, field_name: str): # Check the type hint can you reference and ABC?
    if not dataclasses.is_dataclass(dc_obj): # if we aren't called with a dataclass, just return empty immediately
        return []
    
    matching_fields = [field.name for field in dc_obj.fields() if field.name == field_name]

    matching_fields.extend(
        [find_fields(dataclass_field) for dataclass_field in dc_obj.fields()]
    )

    return matching_fields
```

## Example 3

oscal_component_metaschema
assembly: defined-component

### Metapath

```xml
responsible-role/@role-id|control-implementation/implemented-requirement/responsible-role/@role-id|control-implementation/implemented-requirement/statement/responsible-role/@role-id
```

### Plain Language Translation

The role-id attribute of this assembly's responsible-role element, or the role-id attribute of the responsible-role element within the implemented-requirement element of this assembly's control-implementation element, or or the role-id attribute of the responsible-role element within the statement element within the implemented-requirement element of this assembly's control-implementation element 

### Python implementation

**for loop**

``` python
role_ids = []

if self.responsible_roles is not None:
    for role in responsible_roles:
        role_ids.append(role.role_id)

if (self.control_implementations is not None 
    and self.control_implementations.implemented_requirements is not None 
    and self.control_implementations.implemented_requirements.responsible_roles is not None):

    for role in self.control_implementations.implemented_requirements.responsible_roles:
        role_ids.append(role.role_id)

if (self.control_implementations is not None 
    and self.control_implementations.implemented_requirements is not None 
    and self.control_implementations.implemented_requirements.statements is not None
    and self.control_implementations.implemented_requirements.statements.responsible_roles is not None):

    for role in self.control_implementations.implemented_requirements.statements.responsible_roles:
        role_ids.append(role.role_id)

return role_ids
```