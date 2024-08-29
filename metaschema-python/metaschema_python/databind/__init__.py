"""
The databind module converts documents into an internal format that can be compared against a particular metaschema schema.

It contains parsers for each supported data format, convert the contents into metaschema_python data structures.

The databind classes do not validate the imported contents against a schema.
"""