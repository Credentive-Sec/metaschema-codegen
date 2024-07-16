import typing
import collections


class SchemaPath(typing.TypedDict):
    base: str
    name: str


# NamedTuple for schema filename and short-name. Using tuple since it can be a dictionary key
SchemaID = collections.namedtuple("SchemaID", ["filename", "shortname"])
