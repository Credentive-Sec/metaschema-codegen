import xmlschema
from lxml import etree


class MetaSchemaSchemaParse:
    def __init__(self):
        XSD_FILE = "/workspaces/metaschema-python/metaschema/schema/xml/metaschema.xsd"
        METASCHEMA_XML = "/workspaces/metaschema-python/OSCAL/src/metaschema/oscal_catalog_metaschema.xml"
        self.ms_schema = xmlschema.XMLSchema(source=XSD_FILE)
        parser = etree.XMLParser(resolve_entities=True)
        self.metaschema = etree.parse(METASCHEMA_XML, parser=parser)
