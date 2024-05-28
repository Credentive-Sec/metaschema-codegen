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

The hierarchy of objects can be defined in two ways. Traditional sub and super class relationships based on function, and "Contains / Is contained within" relationships based on the structures of documents and their constituent elements. Much of the complexity of implementing metaschema based schemas in object-oriented languages derives from these two independent hierarchies.