from __future__ import annotations

import typing
import pathlib
import re
import xml.etree.ElementTree


# Typed Dict to handle Assemblies
class ParsedElement(typing.TypedDict):
    effective_name: str
    type: str
    contents: list[typing.Union[str, ParsedElement]]


# Type Aliases
# Content is a list which can either have a string (for fields) or an Assembly (for assemblies)
ContentType: typing.TypeAlias = list[typing.Union[str, ParsedElement]]


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
        if isinstance(document, str):
            document_path = pathlib.Path(document)
        elif isinstance(document, pathlib.Path):
            document_path = document

        # Check that the path exists, and is a file
        if not document_path.exists or not document_path.is_file:
            raise IOError("Recieved path that does not exist or is not a file.")

        # Read the contents of the file to a string
        input = document_path.read_text()

        # THIS IS A HACK! Strip xmlns out of the string so that we can deal with the raw elements
        # This may break in surprising ways.
        # While we're here, we also strip spaces between tags to "de-prettyprint" the input.
        input = re.sub(
            r'xmlns="http://csrc.nist.gov/ns/oscal/1.0"',
            "",
            re.sub(r">\s+<", "><", input),
        )

        try:
            self.xml_data = xml.etree.ElementTree.fromstring(input)
        except Exception:
            raise IOError(f"Unable to parse contents of {document_path} as XML")

    @property
    def raw_data(self) -> list[typing.Any]:
        return self._parse_raw_data(self.xml_data)

    def _parse_raw_data(
        self, element: xml.etree.ElementTree.Element
    ) -> list[ParsedElement]:
        parsed_input: list[ParsedElement] = []

        # Check to see if the element looks like both a field and an assembly. This is an error condition
        if element.text is not None and len(element) > 0:
            raise Exception(
                "XML Element is invalid. Looks like a field and an assembly"
            )

        # Check to see if this is a field. If the text between the tags is empty, the tag is not a field
        if element.text is not None:
            # Add the contents of the tag after the flags
            parsed_input.append(self._process_field(element=element))

        # Parse all the sub elements
        # Calling Element as a list returns its child elements
        elif len(element) > 0:
            # IF an element has sub-elements, there are two possiblities:
            # 1. It's a markup or markup-multiline with embedded html tags.
            # 2. It's an assembly with sub-[fields|flags|assemblies]

            # check for markup tags in element. Breaking this into little steps for clarity
            plain_tags = [child.tag for child in element]  # get all the tags
            markup_tags_in_element = set(plain_tags).intersection(
                XmlParser.MARKUP_TAGS
            )  # get a list of the sub-tags that are markup tags

            # If any of the sub-tags are markup tags, this is a field with internal markup
            if len(markup_tags_in_element) > 0:
                parsed_input.append(self._process_markup_field(element=element))
            else:
                parsed_input.append(self._process_assembly(element=element))

        # Return whatever we ended up parsing
        return parsed_input

    def _process_flags(self, element: xml.etree.ElementTree.Element) -> ContentType:
        # Parse all the flags in the tag
        parsed_flags = []
        for flag_key in element.keys():  # keys returns XML element flag names
            value = element.get(flag_key)
            # Value would never be None, but we add this check to satisfy the linter
            if value is not None:
                parsed_flags.append(
                    {
                        "effective-name": flag_key,
                        "type": "flag",
                        "contents": value,
                    }
                )

        return parsed_flags

    def _process_field(self, element: xml.etree.ElementTree.Element) -> ParsedElement:
        if element.text is not None:  # Shouldn't happen, but linter can't see that
            parsed_element = ParsedElement(
                effective_name=element.tag,
                type="field",
                contents=self._process_flags(element=element),  # Get flags first
            )
            parsed_element["contents"].append(element.text)
            return parsed_element
        else:
            raise Exception(
                "Somehow called _process_field when text is None. This is a logic error"
            )

    def _process_markup_field(
        self, element: xml.etree.ElementTree.Element
    ) -> ParsedElement:
        contents = self._process_flags(element=element)  # get flags first

        # add the text of the child elements to the content array as the last element
        child_text = ""
        for child in element:
            child_text += xml.etree.ElementTree.tostring(
                element=child, encoding="unicode"
            )
        # strip extra spaces and newlines
        child_text = re.sub(r"\s+", " ", child_text)
        contents.append(child_text)

        return ParsedElement(
            effective_name=element.tag,
            type="field",
            contents=contents,
        )

    def _process_assembly(
        self, element: xml.etree.ElementTree.Element
    ) -> ParsedElement:
        contents = self._process_flags(element=element)  # get flags first
        for child in element:
            contents.extend(self._parse_raw_data(child))
        return ParsedElement(
            effective_name=element.tag,
            type="assembly",
            contents=contents,
        )

    @staticmethod
    def strip_namespace(raw_tag: str) -> str:
        # THis function existed to strip namespaces from tags - not necessary because we
        # Strip the NS out of the xml before processing. Leaving the function here because I
        # don't entirely trust the current approach
        return re.sub(r"{.*}", "", raw_tag)
