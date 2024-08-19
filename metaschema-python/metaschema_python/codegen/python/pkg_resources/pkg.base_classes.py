from __future__ import annotations
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field
from typing_extensions import Self, Literal, TypeAlias, Union
import regex
from ....core.metapath import metapath


class MetaschemaException(Exception):
    """
    An exception thrown during instantiation or modification of a class if the object does not conform to the schema or meet the constraints.
    """


class MetaschemaABC(metaclass=ABCMeta):
    """
    Abstract Base Class for object generated from metaschema specifications. Contains empty methods that all derived classes must implement.
    """

    @abstractmethod
    def to_dict(self) -> dict:
        pass

    @abstractmethod
    def to_json(self) -> str:
        """
        Returns a JSON representation of the object.

        Returns:
            str: A string representing the object as JSON
        """
        ...

    @classmethod
    @abstractmethod
    def from_json(cls, json: str) -> Self:
        """
        Attempts to construct the object from a JSON representation. Will succeed if the object conforms to the specification, or raise a MetaschemaException otherwise.

        Args:
            json (str): a string containing a JSON data object

        Returns:
            An instance of the metaschema object if the input conforms to the schema and passes all constrains. Otherwise, an exception is raised
        """
        ...

    @abstractmethod
    def to_yaml(self) -> str:
        """
        Returns a YAML representation of the object

        Returns:
            str: A string representing the object as YAML
        """
        ...

    @classmethod
    @abstractmethod
    def from_yaml(cls, yaml: str) -> Self:
        """
        Attempts to construct the object from a YAML representation. Will succeed if the object conforms to the specification, or raise a MetaschemaException otherwise.

        Args:
            yaml (str): a string containing a YAML data object

        Returns:
            An instance of the metaschema object if the input conforms to the schema and passes all constrains. Otherwise, an exception is raised
        """
        ...

    @abstractmethod
    def to_xml(self) -> str:
        """
        Returns an XML representation of the object

        Returns:
            str: A string representing the object as XML.
        """
        ...

    @classmethod
    @abstractmethod
    def from_xml(cls, xml: str) -> Self:
        """
        Attempts to construct the object from its XML representation. Will succeed if the object conforms to the specification, or raise a MetaschemaException otherwise.

        Args:
            xml (str): a string containing a XML data object

        Returns:
            An instance of the metaschema object if the input conforms to the schema and passes all constrains. Otherwise, an exception is raised
        """

    @abstractmethod
    def metaschema_spec(self) -> str:
        """
        EXPERIMENTAL - return the metaschema representation of an Assembly, Field or Flag. This will be useful for anyone extending a schema.

        Returns:
            str: A string containing the representation of the schema of an object in metaschema
        """


class Flag(MetaschemaABC):
    """
    A class representing a generic Flag. This is primarily used by the metaschema_python code generator and should not generally be used outside the library.
    """


class Field(MetaschemaABC):
    """
    A class representing a generic Field. This is primarily used by the metaschema_python code generator and should not generally be used outside the library.
    """

    constraints: list[Constraint] = []


class Assembly(MetaschemaABC):
    """
    A class representing a generic Assembly. This is primarily used by the metaschema_python code generator and should not generally be used outside the library.
    """

    constraints: list[AssemblyConstraint] = []

    def _apply_constraints(self) -> Self:
        """
        This function applies the constraints encoded in the assembly to the contents of the assembly. It must be called whenever an object is instantiated or changed.

        Returns:
            Self: this function returns the object if all constraints were successfully applied. Otherwise an Exception is raised.
        """

        if True:  # TODO: replace this with working code.
            for constraint in self.__class__.constraints:
                # process
                pass
            return self
        else:
            # TODO: include information about specific constraint violated
            raise MetaschemaException("Object did not meet constraints.")

    def _resolve_target(self, target: str) -> list[Assembly | Field | Flag]:
        """
        This function is called by a metapath object while validating a constraint. It returns the data elements that
        match the target specified by the metapath, if any.

        Args:
            target (str): A reference to a target that may exist in this object. It must be a valid property of the object

        Returns:
            list[Assembly | Field | Flag]: A list of elements matching the target. If there are no matches, it returns an empty list.
        """
        target_list: list[Assembly | Field | Flag] = []

        # Do some processing

        return target_list


class SimpleDatatype:
    # TODO: since the metaschema datatypes inherit from XMLSchema datatypes, can we infer a type for the datatype (e.g. xs:date -> datetime.date). We would need a dict in here to contain the mapping
    """
    A simple datatype defined in Metaschema. This will be a string with an associated regular expression.

    Class Variables
    ---------------
    PATTERN (str): the pattern associated with the datatype
    BASE_TYPE (type): the python datatype most closely matching the data

    Instance Variables
    ------------------
    value: The value of the variable
    """
    # The pattern associated with the datatype - will be overridden in subclasses
    PATTERN: str = "*"

    # The python datatype of corresponding to the metaschema type - will be overridden in subclass
    BASE_TYPE: type = type(None)

    # TODO investigate using __new__ to actually dynamically cast the object to it's underlying type.

    def __init__(self, raw_value: str):
        # Check to see if the raw value string fits the pattern
        # NB: validate is a class method, so we have to resolve the class with type()
        if type(self).validate(raw_value):
            # if so, try to convert the string value to the underlying type
            try:
                if type(self) == bool:
                    SimpleDatatype.fix_bool(input=raw_value)
                else:
                    self.value = type(self).BASE_TYPE(raw_value)
            except Exception as e:
                raise MetaschemaException(
                    f"{self.value} cannot be instantiated as {type(self).__name__}"
                )

    @staticmethod
    def fix_bool(input: str) -> bool:
        """
        fix_bool is a special method to handle metaschema boolean, which can be 1 or 0 or the literals "true" or "false"

        Args:
            input (str): The thing we think might be a bool

        Returns:
            bool: a bool if the thing is a bool
        """
        if input in ["1", "true"]:
            return True
        elif input in ["0", "false"]:
            return False
        else:
            raise MetaschemaException(
                f"Value {input} is not a valid metaschema boolean."
            )

    @classmethod
    def validate(cls, input: str) -> bool:
        """
        class method to compare value to pattern. Used by initializer.

        Args:
            input (str): _description_

        Returns:
            bool: _description_
        """

        if regex.match(pattern=cls.PATTERN, string=input) is not None:
            return True
        else:
            return False

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.value})"


class ComplexDataType:
    # TODO: since the metaschema datatypes inherit from XMLSchema datatypes, can we infer a type for the datatype (e.g. xs:date -> datetime.date). We would need a dict in here to contain the mapping
    """
    A complex datatype defined in Metaschema. This may be a union type, or it may be a type which embeds other elements (e.g. markup-line).

    Class Variables
    ---------------
    pattern (str): the pattern associated with the datatype TODO: FIX
    """

    # The pattern associated with the datatype - will be overridden in subclasses
    ALLOWED_ELEMENTS: list[str] = []

    @classmethod
    def validate(cls, input: str) -> bool:
        """
        class method to compare value to pattern. Used by initializer.

        Args:
            input (str): the potential data to validate

        Returns:
            bool: true if it passes validation, false otherwise.
        """
        # TODO: how do we do this?
        return True


@dataclass
class Constraint:
    """
    A class representing a constraint defined in a metaschema. These will be contained in assemblies, and will be processed during instantiation.

    Fields:
        target: A metapath expression identifying the node the constraint applies to
    """

    # type: str  # NOTE this may not be necessary if we use subclasses
    target: str
    metapath: str
    # Other values can go here.

    def validate(self, input: MetaschemaABC):
        pass


@dataclass
class LetConstraint(Constraint):
    pass


@dataclass
class AllowedValuesConstraint(Constraint):
    # Inner class to define one of the allowed values
    @dataclass
    class AllowedValue:
        value: str
        description: str

    allow_other: Literal["yes", "no"] = "no"
    extensible: Literal["none", "model", "external"] = "model"
    enum: list[AllowedValuesConstraint.AllowedValue] = field(default_factory=list)


@dataclass
class ExpectConstraint(Constraint):
    pass


@dataclass
class HasCardinalityConstraint(Constraint):
    pass


@dataclass
class IndexConstraint(Constraint):
    pass


@dataclass
class IndexHasKeyConstraint(Constraint):
    pass


@dataclass
class IsUniqueConstraint(Constraint):
    pass


@dataclass
class MatchesConstraint(Constraint):
    pass


# Note that constraints in flags are not allowed to define a target (the default target is .)
FlagConstraint: TypeAlias = Union[
    LetConstraint,
    AllowedValuesConstraint,
    ExpectConstraint,
    IndexHasKeyConstraint,
    MatchesConstraint,
]

# Fields can have the same constraints as flags
FieldConstraint: TypeAlias = FlagConstraint

AssemblyConstraint: TypeAlias = Union[
    FlagConstraint, HasCardinalityConstraint, IndexConstraint, IsUniqueConstraint
]


class Metapath:
    """
    A class representing a metapath expression
    """

    type: str
    children: list[Metapath]
    value: None | str | int

    def __init__(self, expr):
        if isinstance(expr, str):
            syntaxtree = metapath.parse(expr)
            self.type = syntaxtree.name
            self.value = None
            self.children = []
            for child in syntaxtree:
                self.children.append(Metapath(child))
        elif expr.isphrase():
            self.type = expr.name
            self.value = None
            self.children = []
            for child in expr:
                self.children.append(Metapath(child))
        else:
            # expr is a Lex
            self.type = expr.name
            self.value = expr.value
            self.children = []

    def operator(self):
        pass
