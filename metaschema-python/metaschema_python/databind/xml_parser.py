from __future__ import annotations

import xml
import typing
import pathlib
import xml.etree.ElementTree
import re
import typing


class XmlParser:
    """
    A Parser for documents representing a particular metaschema in XML.

    Converts XML documents to a standard set of python-metaschema objects that can be compared against a particular schema
    """

    # Metaschema allows for embedded HTML in some elements. Since this confuses our XML parser, we need to identify the markup
    # tags so we can process them differently.
    MARKUP_TAGS = [
        "p",
        "ul",
        "li",
        "em",
        "i",
        "strong",
        "b",
        "code",
        "q",
        "sub",
        "sup",
        "img",
        "a",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "pre",
        "ol",
        "blockquote",
    ]

    def __init__(self, document: typing.Union[str, pathlib.Path]):
        """
        Initialize a parser

        Args:
            document (str | Path): The location of the document to be parsed. May be provided as string, or a Path object.
        """

        # Normalize the input so that we are working with a path
        if type(document) == str:
            document_path = pathlib.Path(document)
        elif type(document) == pathlib.Path:
            document_path = document

        # Check that the path exists, and is a file
        if not document_path.exists or not document_path.is_file:
            raise IOError("Recieved path that does not exist or is not a file.")

        # Read the contents of the file to a string
        input = document_path.read_text()

        try:
            self.xml_data = xml.etree.ElementTree.fromstring(input)
        except Exception:
            raise IOError(f"Unable to parse contents of {document_path} as XML")

    @property
    def raw_data(self) -> list[typing.Any]:
        return self._parse_raw_data(self.xml_data)

    def _parse_raw_data(
        self, element: xml.etree.ElementTree.Element
    ) -> list[typing.Any]:
        parsed_input = []
        parsed_element = {}
        parsed_element["effective-name"] = XmlParser.strip_namespace(element.tag)
        parsed_element["contents"] = []

        # Get the content between the start and end tag and strip any leading or trailing whitespace (including newline)
        if element.text is not None and element.text.strip() != "":
            parsed_element["type"] = "field"
            parsed_element["contents"].append(element.text)

        # Parse all the flags in the tag
        for flag_key in element.keys():  # keys returns XML element flag names
            parsed_element["contents"].append(
                {
                    "effective-name": flag_key,
                    "type": "flag",
                    "contents": element.get(flag_key),
                }
            )

        # Parse all the sub elements
        # Calling Element as a list returns its child elements
        if len(element) > 0:
            parsed_element["type"] = "assembly"
            parsed_element["contents"] = []
            for child in element:
                parsed_element["contents"].extend(self._parse_raw_data(child))
        parsed_input.append(parsed_element)
        return parsed_input

    @staticmethod
    def strip_namespace(raw_tag: str) -> str:
        return re.sub(r"{.*}", "", raw_tag)
