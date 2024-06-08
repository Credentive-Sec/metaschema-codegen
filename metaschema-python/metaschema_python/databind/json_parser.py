import json
import typing
import pathlib


class JsonParser:
    """
    A Parser for documents representing a particular metaschema in JSON.

    Converts JSON documents to a standard set of python-metaschema objects that can be compared against a particular schema
    """
    def __init__(self, document: typing.Union[str | pathlib.Path]):
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
            self.json_data = json.loads(input)
        except Exception as e:
            raise IOError(f"Unable to parse contents of {document_path} as JSON")
        
    @property
    def raw_data(self) -> list[typing.Any]:
        """
        Returns the parsed JSON content as "generic metaschema". This is a format that is easy to compare to a metaschema schema. 

        Returns:
            list[typing.Any]: A list of assemblies
        """
        return self._parse_raw_data(self.json_data)
    
    def _parse_raw_data(self, input: typing.Union[dict, list, str]) -> typing.Any: # TODO - fix type annotations
        """
        Recursively parse raw JSON date elements and return them as "generic metaschema"

        Args:
            input (typing.Union[dict, list, str]): A data element from somewhere inside a JSON structure
        """
        if type(input) == dict:
            parsed_input = []
            for key in input.keys():
                parsed_element = {}
                if type(input[key]) == dict:
                    # this is an assembly
                    parsed_element["effective-name"] = key # "effective-name" because element names can be overridden by "use-name" so we don't know if we're looking at the "name" or "use-name"
                    parsed_element["type"] = "assembly"
                    parsed_element["contents"] = self._parse_raw_data(input[key])
                    parsed_input.append(parsed_element)
                elif type(input[key]) == list:
                    # this is a list, so we pass it to the list parser
                    parsed_input.extend(self._parse_raw_list(name=key, input=input[key]))     
                elif type(input[key]) == str:
                    # This is a flag
                    parsed_element["effective-name"] = key # "effective-name" because element names can be overridden by "use-name" so we don't know if we're looking at the "name" or "use-name"
                    parsed_element["type"] = "flag"
                    parsed_element["contents"] = input[key]
                    parsed_input.append(parsed_element)
                else:
                    raise IOError("Invalid data passed to raw parser. This is a super-secret exception condition you should never see!")    
            return parsed_input    
        else:
            raise IOError("Invalid data passed to raw parser. This is a super-secret exception condition you should never see!")
        

    def _parse_raw_list(self, name: str, input: list[typing.Any]) -> list[dict[str,str]]:
        """
        Parse input when presented as a list in JSON. This needs special processing because metaschema doesn't contain the inherent concept of a list, so we flatten and return it.

        Args:
            name (str): the name of the element containing the list - this will map to the "json-key" element of a metaschema assembly
            input (list[typing.Any]): the list to be processed

        Returns:
            list[dict[str,str]]: the list elements flattened to a list of OSCAL instances
        """
        parsed_input = []
        for element in input:
            parsed_element = {}
            parsed_element["json-key"] = name
            if type(element) == dict:
                parsed_element["contents"] = self._parse_raw_data(element)
            elif type(element) == str:
                parsed_element["contents"] = element
            parsed_input.append(parsed_element)

        return parsed_input

