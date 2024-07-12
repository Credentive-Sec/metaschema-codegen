from __future__ import annotations
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing_extensions import Self, Literal
import regex


class MetaschemaException(Exception):
    """
    An exception thrown during instantiation or modification of a class if the object does not conform to the schema or meet the constraints.
    """


class MetaschemaABC(metaclass=ABCMeta):
    """
    Abstract Base Class for object generated from metaschema specifications. Contains empty methods that all derived classes must implement.
    """

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


class Datatype:
    # TODO: since the metaschema datatypes inherit from XMLSchema datatypes, can we infer a type for the datatype (e.g. xs:date -> datetime.date). We would need a dict in here to contain the mapping
    """
    A datatype defined in Metaschema. This will be a string with an associated regular expression.
    """

    # this base class will accept any valid string, this is overridden in subclasses.
    pattern: str = "*"

    @classmethod
    def _match_pattern(cls, input: str) -> bool:
        """
        class method to compare value to pattern. Used by initializer.

        Args:
            input (str): _description_

        Returns:
            bool: _description_
        """

        if regex.match(pattern=cls.pattern, string=input) is not None:
            return True
        else:
            return False

    def __init__(self, input: str):
        """
        Initializer for Metaschema Datatype. This should only be used in subclasses

        Args:
            input (str): a string containing the input to be evaluated against the datatype specification

        Raises:
            MetaschemaException: if the contents of the data do not match the datatype specification

        Returns:
            _type_: None
        """
        # self.__class__ allows this function to work in subclasses that override the pattern class variable
        if self.__class__._match_pattern(input=input):
            self.value = input
        else:
            raise MetaschemaException(
                f"Could not create field. Value ({input}) does not match pattern ({self.__class__.pattern})"
            )

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(pattern={self.__class__.pattern}, value={self.value})"


@dataclass
class Constraint:
    """
    A class representing a constraint defined in a metaschema. These will be contained in assemblies, and will be processed during instantiation.

    Fields:
        target: A metapath expression identifying the node the constraint applies to
    """

    target: str
    type: Literal[
        "let",
        "allowed-values",
        "expect",
        "has-cardinality",
        "index",
        "index-has-key",
        "is-unique",
        "matches",
    ]


class FlagConstraint(Constraint):
    def __init__(self):
        if self.type not in [
            "let",
            "allowed-values",
            "expect",
            "index-has-key",
            "matches",
        ]:
            raise MetaschemaException(
                f"Cannot define a constraint of type {self.type} on a Flag."
            )


class Assembly(MetaschemaABC):
    """
    A class representing a generic Assembly. This is primarily used by the metaschema_python code generator and should not generally be used outside the library.
    """

    def _apply_constraints(self) -> Self:
        """
        This function applies the constraints encoded in the assembly to the contents of the assembly. It must be called whenever an object is instantiated or changed.

        Returns:
            Self: this function returns the object if all constraints were successfully applied. Otherwise an Exception is raised.
        """

        if True:  # TODO: replace this with working code.
            return self
        else:
            # TODO: include information about specific constraint violated
            raise MetaschemaException("Object did not meet constraints.")


class Field(MetaschemaABC):
    """
    A class representing a generic Field. This is primarily used by the metaschema_python code generator and should not generally be used outside the library.
    """


class Flag(MetaschemaABC):
    """
    A class representing a generic Flag. This is primarily used by the metaschema_python code generator and should not generally be used outside the library.
    """
