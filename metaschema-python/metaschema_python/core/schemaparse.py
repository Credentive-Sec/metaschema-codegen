import urllib.parse
import urllib.request
import xmlschema
from lxml import etree
import urllib
from pathlib import Path
from typing import cast


class MetaSchemaXSD:
    """
    This class builds and returns an XML Schema built from the github repo. It should not be necessary to use outside of this library.
    """

    def __init__(self):
        BASE_URL = (
            "https://raw.githubusercontent.com/usnistgov/metaschema/main/schema/xml/"
        )
        BASE_XSD = "metaschema.xsd"
        xsd_contents = urllib.request.urlopen(BASE_URL + BASE_XSD).read()
        self.ms_schema = xmlschema.XMLSchema(source=xsd_contents, base_url=BASE_URL)


class MetaSchema:
    """
    This class represents a parsed metaschema.
    """

    def __init__(
        self,
        metaschema: str | Path,
        baseurl: str | None = None,
        basepath: Path | None = None,
    ):
        """
        Initializer for a MetaSchema instance

        Args:
            metaschema (str | Path): A string representing a file or url, or a Path representing a local file.
            baseurl (str | None, optional): A base URL which will be used to import additional referenced metaschema files if obtained from a remote location. Defaults to None.
            basepath (pathlib.Path | None, optional): A base URL which will be used to import additional referenced metaschema files if obtained from a local re. Defaults to None.
        """
        # TODO: process URLs or local paths
        metaschema_file = "/workspaces/metaschema-python/OSCAL/src/metaschema/oscal_catalog_metaschema.xml"
        parser = etree.XMLParser(resolve_entities=True)
        metaschema_etree = etree.parse(metaschema_file, parser=parser)
        self.schema_dict = MetaSchemaXSD().ms_schema.to_dict(
            cast(xmlschema.XMLResource, metaschema_etree)
        )

        # TODO: chase imports

    def _read_local_schema(
        self, metaschema: str | Path, basepath: Path | None = None
    ) -> str:
        if basepath is not None:
            schema_file = Path(basepath, metaschema)
        else:
            schema_file = Path(metaschema)

        return open(schema_file).read()

    def _read_remote_schema(self, baseurl: str, metaschema: str) -> str:
        return ""
