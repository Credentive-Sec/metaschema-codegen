# New API design

Every object is defined as either a simple data type, or a container. 

The programmer can just provide the required data to an object, which will create the object.

A simple data type will can be instantiated with a string, which must conform to the appropriate regular expression.

A container type must be instantiated with a set of object, which must be instances of the appropriate data type or container.

Field, Flag and Assembly are representations of the data object. The representation of the data object is determined as late as possible during the process of encoding the data.

The metaschema definitions of an object determine which representations it might have. Where more than one representation is possible, the representation will be determined by the "type" of the reference (flag, field or assembly)

# Example

## Location-UUID

In the oscal_metadata_metaschema specification, two top level definitions exist, which have the same name, but different types.

```xml
<define-flag name="location-uuid" as-type="uuid">
    <formal-name>Location Universally Unique Identifier Reference</formal-name>
    <!-- Identifier Reference -->
    <description>Reference to a location by UUID.</description>
    <prop name="value-type" value="identifier-reference"/>
    <prop name="identifier-type" value="machine-oriented"/>
    <prop name="identifier-scope" value="cross-instance"/>
    <constraint>
        <!-- TODO: Dave to resolve syntax error. Likely requires updated metaschema schema -->
        <index-has-key name="index-metadata-location-uuid">
            <!-- TODO: This is impacted by cross-document cross-references We need to relocate or localize this constraint. -->
            <key-field target="."/>
        </index-has-key>
    </constraint>
</define-flag>

<define-field name="location-uuid" as-type="uuid">
    <formal-name>Location Universally Unique Identifier Reference</formal-name>
    <!-- Identifier Reference -->
    <description>Reference to a location by UUID.</description>
    <prop name="value-type" value="identifier-reference"/>
    <prop name="identifier-type" value="machine-oriented"/>
    <prop name="identifier-scope" value="cross-instance"/>
    <constraint>
        <index-has-key name="index-metadata-location-uuid" target=".">
            <!-- TODO: This is impacted by cross-document cross-references We need to relocate or localize this constraint. -->
            <key-field target="."/>
        </index-has-key>
    </constraint>
</define-field>
```

This is valid XML and valid metaschema, but presents an impossible conundrom for an application author. To resolve this annoyance, it is necessary to define location-uuid as a abstract and independent object "location-uuid" that exists in a superposition of field and flag until it is observed as part of another instance.

A pseudocode implementation of this idea follows

```py
class LocationUUID:
    function initialize(string input):
        if input matches type defintion uuid:
            instance.value = input

    
    def as_flag:
        return Flag(input)

    def as_field:
        return Field(input)
```

Location UUID would be referenced in a larger assembly like this:

```xml
<field ref='location-uuid'>
```

Pseudocode representing this is

```py
class Party:
    function initialize(dictionary input):
        instance.location_uuid = input[location_uuid].as_field()

```