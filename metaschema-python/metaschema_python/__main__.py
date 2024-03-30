import argparse
import sys

from .core.metaschema_parser import MetaschemaParser


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
    dest="base_url",
    help="[optional] A base URL for obtaining other child schemas. If this is not provided, it will be inferred from the filename.",
)

args = parser.parse_args()


# Parse the metaschema definition into a tree
try:
    oscal_parser = MetaschemaParser(location=args.location)
    oscal_parser.parse()

except Exception as e:
    print("Error parsing schema:", e)
    sys.exit(1)
