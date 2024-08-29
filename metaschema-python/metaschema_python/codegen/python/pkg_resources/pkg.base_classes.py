from __future__ import annotations
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field
from typing_extensions import Self, Literal, TypeAlias, Union
import regex
from .metapath import metapath # type: ignore


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
    target: Metapath
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
    target: Metapath
    min_occurs: int = 0
    max_occurs: int = -1 #special case value for unbounded. math.inf is a float and requires an additional import

    def __init__(self, location, tgtstr: str, mno=0, mxo=-1):
        self.target = Metapath(tgtstr)
        self.min_occurs = mno
        if mxo == "unbounded":
            self.max_occurs = -1
        else:
            self.max_occurs = mxo
        self.location = location

    def validate(self):
        cardinality = len(self.target.eval(self.location))
        if self.min_occurs != 0:
            if cardinality < self.min_occurs:
                return False
        if self.max_occurs != -1:
            if cardinality > self.max_occurs:
                return False
        return True


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

    def eval(self, location):
        #if not isinstance(location, list):
        #    location = [location]
        match(self.type+str(len(self.children))):
            case("S1"):
                #return self.children[0].eval(location).pop()
                return self.children[0].eval(location)
            case("metapath1"):
                return self.children[0].eval(location)
            case("expr1"):
                #return [self.children[0].eval(location)]
                return self.children[0].eval(location)
            case("expr3"):
                #return self.children[0].eval(location).extend(self.children[2].eval(location))
                self.children[0].eval(location)
                return self.children[2].eval(location)
            case("exprsingle1"):
                return self.children[0].eval(location)
            case("orexpr1"):
                return self.children[0].eval(location)
            case("orexpr3"):
                return self.children[0].eval(location) or self.children[2].eval(location)
            case("andexpr1"):
                return self.children[0].eval(location)
            case("andexpr3"):
                return self.children[0].eval(location) and self.children[2].eval(location)
            case("comparisonexpr1"):
                return self.children[0].eval(location)
            case("comparisonexpr3"):
                lhs = self.children[0].eval(location)
                rhs = self.children[2].eval(location)
                match(self.children[1].eval(location)):
                    case("eq" | "="):
                        return lhs == rhs
                    case("ne" | "!="):
                        return lhs != rhs
                    case("lt" | "<"):
                        return lhs < rhs
                    case("le" | "<="):
                        return lhs <= rhs
                    case("gt" | ">"):
                        return lhs > rhs
                    case("ge" | ">="):
                        return lhs >= rhs
            case("stringconcatexpr1"):
                return self.children[0].eval(location)
            case("stringconcatexpr3"):
                return str(self.children[0].eval(location)) + self.children[2].eval(location)
            case("rangeexpr1"):
                return self.children[0].eval(location)
            case("additiveexpr1"):
                return self.children[0].eval(location)
            case("additiveexpr3"):
                if self.children[1].eval(location) == "+":
                    return self.children[0].eval(location) + self.children[2].eval(location)
                else:
                    return self.children[0].eval(location) - self.children[2].eval(location)
            case("multiplicativeexpr1"):
                return self.children[0].eval(location)
            case("multiplicativeexpr3"):
                match(self.children[1].eval(location)):
                    case("*"):
                        return self.children[0].eval(location) * self.children[2].eval(location)
                    case("div"):
                        return self.children[0].eval(location) / self.children[2].eval(location)
                    case("idiv"):
                        return self.children[0].eval(location) // self.children[2].eval(location)
                    case("mod"):
                        return self.children[0].eval(location) % self.children[2].eval(location)
            case("unionexpr1"):
                return self.children[0].eval(location)
            case("intersectexceptexpr1"):
                return self.children[0].eval(location)
            case("arrowexpr1"):
                return self.children[0].eval(location)
            case("unaryexpr1"):
                return self.children[0].eval(location)
            case("valueexpr1"):
                return self.children[0].eval(location)
            case("simplemapexpr1"):
                return self.children[0].eval(location)
            case("pathexpr1"):
                #either this is just / (with nothing following) or it is a relative path
                if self.children[0].type == 'relativepathexpr':
                    #relative path
                    return self.children[0].eval(location)
                else:
                    #just /
                    pass
            case("pathexpr2"):
                pass
            case("relativepathexpr1"):
                #based off of the location
                if self.children[0].children[0].type == 'axisstep':
                    return location._resolve_target(self.children[0].eval(location))
                else: #postfixexpr
                    return self.children[0].eval(location)
            case("relativepathexpr3"):
                base = self.children[0].eval(location) #relativepathexpr: returns a list of locations
                name = self.children[2].eval(location) #stepexpr: returns a string
                toret = []
                for item in base:
                    toret.extend(item._resolve_target(name))
                return toret
            case("relativepathexpr4"):
                base = self.children[0].eval(location)
                toret = []
                for item in base:
                    if self.children[2].eval(item):
                        toret.append(item)
                return toret
            case("stepexpr1"):
                return self.children[0].eval(location)
            case("axisstep1"):
                return self.children[0].eval(location)
            case("forwardstep1"):
                return self.children[0].eval(location)
            case("abbrevforwardstep1"):
                return self.children[0].eval(location)
            case("abbrevforwardstep2"):
                return "@"+self.children[1].eval(location)
            case("reversestep1"):
                pass
            case("abbrevreversestep1"):
                pass
            case("nametest1"):
                return self.children[0].eval(location)
            case("postfixexpr1"):
                return self.children[0].eval(location)
            case("primaryexpr1"):
                return self.children[0].eval(location)
            case("literal1"):
                return self.children[0].eval(location)
            case("numericliteral1"):
                return self.children[0].eval(location)
            # ...
            case("parenthesizedexpr3"):
                return self.children[1].eval(location)
            case("eqname1"):
                #maybe we should pythonize the name here
                return self.children[0].eval(location)
        if self.value is None:
            return self.children[0].eval(location)
        return self.value
    

#just in case, here is an example case that you can drop in and run to check on what this code is doing:
# class ExampleDummy():
#     children: dict
#     def __init__(self):
#         object.__setattr__(self, "children", {})
#     def _resolve_target(self, name):
#         if isinstance(self.children[name], list):
#             return self.children[name]
#         return [self.children[name]]
#     def __getattr__(self, name):
#         return self.children[name]
#     def __setattr__(self, name, value):
#         self.children[name] = value
# root = ExampleDummy()
# root.location = ExampleDummy()
# root.location.subelements = [ExampleDummy(), ExampleDummy(), ExampleDummy()]
# root.location.subelements[0].example = 3
# root.location.subelements[0].selector = 2
# root.location.subelements[1].example = 4
# root.location.subelements[1].selector = 3
# root.location.subelements[2].example = 5
# root.location.subelements[2].selector = 5

# mp = Metapath("location/subelements[selector > 2]/example[0]")
# print(mp.eval(root)[0])