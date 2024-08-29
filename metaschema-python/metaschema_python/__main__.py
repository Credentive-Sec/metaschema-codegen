import argparse
import sys

from .core.schemaparse import MetaschemaSetParser

# from .core.assembly import Context


# Parse the command arguments
parser = argparse.ArgumentParser(
    prog="metaschema_parser",
    description="Parse an XML based metaschema and generate Python objects.",
)
parser.add_argument(
    "location",
    type=str,
    help="A filename or url for the base metaschema file.",
)
parser.add_argument(
    "-B",
    "--base",
    dest="base",
    help="[optional] A base URL or directory for obtaining other child schemas. If this is not provided, it will be inferred from the filename.",
)
parser.add_argument(
    "-S",
    "--schema",
    dest="schema",
    help="[optional] The location of the metaschema xsd file.",
)
parser.add_argument(
    "-N",
    "--name",
    dest="package_name",
    help="The name of the package to generate. This should be the name of the specification (e.g. oscal)",
)

args = parser.parse_args()


# Parse all of the metaschema definitions into trees.
try:
    metaschema_dict = MetaschemaSetParser(metaschema_location=args.location)
except Exception as e:
    print("Error parsing metaschema:", e)
    sys.exit(1)

print("finished")
