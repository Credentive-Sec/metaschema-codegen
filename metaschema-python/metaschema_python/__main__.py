import argparse
import sys

from .core.metaschema_parser import MetaschemaParser
from .core.assembly import Assembly, XMLTag, Context


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

args = parser.parse_args()


# Parse all of the metaschema definitions into trees.
try:
    metaschema_parser = MetaschemaParser(
        location=args.location,
        schema_file="/workspaces/metaschema-python/metaschema/schema/xml/metaschema.xsd",
    )
    metaschema_contents = metaschema_parser.parse()


except Exception as e:
    print("Error parsing metaschema:", e)
    sys.exit(1)

ctxt = Context("/workspaces/metaschema-python/OSCAL/src/metaschema/oscal_complete_metaschema.xml")

xml = XMLTag.fromPath("/workspaces/metaschema-python/oscal-content/nist.gov/SP800-53/rev5/xml/NIST_SP-800-53_rev5_catalog.xml")
json = XMLTag.JsonfromStr(open("/workspaces/metaschema-python/oscal-content/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog-min.json").read())
paraxml = XMLTag.fromJson(json.get('catalog'), ctxt.get('catalog'),ctxt) #this line might take a while

#print(xml)
#print(paraxml)

thingy = Assembly(ctxt.get('catalog'), xml, ctxt)
parathingy = Assembly(ctxt.get('catalog'), paraxml, ctxt)

if not thingy.validate():
    print("xml is invalid")

if not parathingy.validate():
    print("json is invalid")

parajson = thingy.asJson()

print("finished")