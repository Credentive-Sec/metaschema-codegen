import dataclasses
import typing

@dataclasses.dataclass
class MetaschemaInstance:
    """
    An instance is used to declare an information element child within a parent information element. Each instance is a flag instance, field instance, or assembly instance, and either references an existing top-level definition by name or provides an inline definition.

    In a Metaschema module, an instance appears inside the definition of its parent information element.

    An assembly definition may contain flag, field or assembly instances reflecting the objects to be permitted in that assembly.
    A field definition may only include flag instances.
    A flag definition never contains instances since flags have no children in the model, only values.
    """
    deprecated: str
    ref: str # Actually a token
    formal_name: str
    description: str # Actually markup-line
    prop: typing.Any # defined as "special"? TODO: Replace with specific type reference once implemented
    use_name: str # Actually token
    remarks: typing.Any # defined as "special"
