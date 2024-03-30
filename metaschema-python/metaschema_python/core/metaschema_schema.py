from lxml import etree, objectify
from urllib import request


class MetaschemaSchemaParser:
    METASCHEMA_SCHEMA_URL = "https://raw.githubusercontent.com/usnistgov/metaschema/main/schema/xml/metaschema.xsd"

    def __init__(self):
        try:
            with request.urlopen(self.METASCHEMA_SCHEMA_URL) as ms_req:
                ms_schema = ms_req.read()

            metaschema_schema = etree.XMLSchema(etree.fromstring(ms_schema))
            # TODO - START HERE

        except Exception as e:
            raise e

        pass
