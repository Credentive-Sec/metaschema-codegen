from xml_parser import XmlParser
from json_parser import JsonParser

parser = XmlParser(
    "/workspaces/metaschema-python/oscal-content/examples/ar/xml/ifa_assessment-results-example.xml"
)


# parser = JsonParser(
#     "/workspaces/metaschema-python/oscal-content/examples/ar/json/ifa_assessment-results-example.json"
# )

output = parser.raw_data

print(output)
