from typing import Optional

from lxml import etree, objectify
import urllib


class MetaschemaParser:
    def __init__(self, location: str, base_url: Optional[str] = None):
        self.tree = objectify.parse(location, base_url=base_url)

        if self.tree is None:
            raise FileNotFoundError("Unable to parse xml at ", location)

    def parse(self):
        data = objectify.dump(self.tree.getroot())
        print(data)
        return data
