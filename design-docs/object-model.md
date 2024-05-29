# Introduction

This document describes the basic object model for the python metaschema library

# Base Classes
Implementation of a metaschema specification in an object oriented language like Python requires implementation of three base classes.

- Datatypes: Defines the fundamental datatypes built into the metaschema specification
- Assemblies: Captures the concept of a generic Assembly
- Lists: Defines a structure containing multiple assemblies of a single type

These classes provide the following core functions:

1. Serialization/Deserialization
1. Validation of the structure and contents of an assembly
1. For lists/assemblies, a method to discover which class implements the substructure.
1. Conversion of python code back to metaschema.

# Subclasses

A particular schema described in metaschema will be expressed as subclasses of the appropriate base class, with the customizations defined below.

## Datatypes

Subclasses of Datatype will provide the regular expression constraining the datatype's values.

## Assembly

A specific Assembly subclass will contain three pieces of information

1. Mandatory Flags/Fields and their associated classes
2. Optional Flags/Fields and their associated classes
3. Constraints associated with the Assembly 

## Lists

A subclass of List will identify the class describing it's constituent elements.

# Namespaces and identifiers

The structure of an element associated with a tag in metaschema may change between or even inside of models. For this reason, it is imperative that every model has the capacity to override the flag/field -> Class mapping, but there are several high level objects that are re-used in several objects.

The hierarchy of objects can be defined in two ways. Traditional inheritance relationships, and "Contains / Is contained within" relationships based on the structures of documents and their constituent elements. Much of the complexity of implementing metaschema based schemas in object-oriented languages derives from these two independent hierarchies.

The inheritance relationship within the library will be simple, with only 1 base class for each type of oscal entity (datatype, assembly, list)

"Contains/Is contained within" will be modeled with packages and modules. Inline assemblies may be modeled as inner classes.

# Approaches to enabling access with python

Two potential approaches have been identified for enabling access to metaschema defined schemas within python.

- Code Generation
- Metaclasses

## Code Generation

Code Generation may be the simplest mechanism to convert from Metaschema specifications to python classes. This approach involves creation of traditional text files containing python code, available in a traditional library format. Code can either be generated using traditional string processing, or may use a templating engine such as [Jinja](https://jinja.palletsprojects.com/en/3.0.x/).

An example of code generation with Jinja is provided by the [Datamodel Code Generator Project](https://github.com/koxudaxi/datamodel-code-generator/tree/main/datamodel_code_generator)

This approach is relatively simple and straitforward, and can produce code that will integrate very well into traditional development environments. However, the generation function must be run every time the specification is updated. Likely the package will be distributed with a command line interface for execution, probably using something like the following:

```
$ python2metaschema <Metaschema file>
```

To convert custom made python objects back to metaschema, a function should be exposed within the base classes that can generate metaschema files from a given class:

```
metaschema_output: str = CustomClass.generate_metaschema()
```

## Metaclasses

An alternative approach is the use of metaprogramming via the python metaclass. In this approach, classes may be dynamically constructed without the generation of actual python code files. This approach has the advantage of being completely dynamic, but also complex. Furthermore, it is uncertain how virtual classes will be supported by traditional IDEs, even with language servers in place.

For this approach, a single library will be provided, and loading a schema defined in metaschema will be an API call, similar to the following:

```
schema = metaschema_python.generate("<Metaschema File>")
```

The contents of the schema could be exposed as attributes that return classes or functions implementing the desired functionality as documented here.

Extension of the schema would require additional functions exposed as callables within the schema. The design of this api is a future task, and may be very complicated.