# API Usage model

## Introduction

This document describes the expected use cases for the API, and proposes code samples that the API should support. This document is intended to guide development of the API by establishing a specification of the end result.

## Use Cases

The Key to understanding how this API will work is to understand it as a data transformation API. Standards expressed in metaschema (such as OSCAL) are designed to present information about their subjects in a consistent and interoperable fashion. The source of data will almost never conform to the metaschema. Often it will be stored as part of a database with additional information, or the output of a process. The job of the programmer in this case is to convert the data from its native format to a metaschema conformant representation for use by other systems. 

In other words, Metaschema specifications describe interchange formats, but do not necessarily impose a data schema on the underlying systems, even if the system can produce OSCAL as an output.

### Example 1: Converting a word document to an OSCAL catalog

[OSCAL PKI Policy Converter](https://github.com/Credentive-Sec/oscal-pki-policy-converter) is a tool that accepts a word document conforming the RFC 3647 Certificate Policy structure, and produces an OSCAL Catalog. The word document is converted into markdown, and then "tokenized" into individual sentances. This markdown document is passed into a parser that produces an OSCAL catalog, leveraging the oscal-pydantic library.

The purpose of the utility is to convert a free-form prose expression of policy requirements into a simple OSCAL catalog.

The majority of the code parses the document into a data structure that is more closely aligned to OSCAL, and then that data structure is broken apart and passed to the oscal-pydantic library to convert into OSCAL fragments, which are assembled into larger structures until it is finally assembled into a catalog, and then a document containing a catalog. 

This highlights a key principal: the programmer will make decisions about how to map the internal representation into OSCAL, and the library's job is to present a idiomatic interface to the underlying OSCAL data structures. The library itself is not responsible for understanding the semantic content of a the data.

In this particular case, the following mappings were defined:

#### Document -> Catalog


```python
from oscal_pydantic import document, catalog

# See code listing in following sections
common_catalog = catalog.Catalog(
    uuid=uuid.uuid4(),
    metadata=metadata, # See code listing in following section
    groups=section_groups,
    back_matter=backmatter, 
)

return document.Document(catalog=common_catalog)
```

#### Document Headings -> Metadata 
(for sections such as revision history)

The following code is a partial listing, showing how data presented in different format can be converted to oscal structures.

```python
from datetime import datetime, timezone
from oscal_pydantic.core import common


for row in revisions[1:]: # The data is presented in a table
    version_id = row[id_column]
    try:
        published_date = (
            datetime.strptime(row[date_column], "%B %d, %Y")
            .replace(tzinfo=timezone.utc)
            .isoformat()
        )
    except ValueError:
        # If we can't parse the date, we're probably in a weird header row
        continue
    revision_details = row[detail_column]
    revision_record = common.Revision(
        version=version_id,
        published=published_date,
        remarks=revision_details,
    )
    revision_list.append(revision_record)


    published = datetime.strptime(
        self.strip_markdown_from_text(line), 
        publication_date_format
    ).replace(tzinfo=timezone.utc)

    return common.Metadata(
        title="Placeholder - will be replaced in calling function",
        published=published.isoformat(),
        version=version,
        oscal_version="1.1.2",  # TODO - get version from oscal-pydantic library
        revisions=revision_list,
    )
```

#### Document Headings -> Group

Each section not containing catalog metadata becomes a group.

#### Document Headings -> Control

If a section has text, it will also be processed as a control. 

#### Document Sentance -> Statement Part

Each individual sentance in the document is processed as a "part" under the control. Sentances are processed differntly depending on whether they contain words normally associated with requirements (e.g. "MUST", "SHOULD", "MAY", etc.). These requirements are encoded as "statements". Statements without these words are encoded as "guidance".

The following code illustrates the creation of a Group from a set of controls which is in turn assembled from statements.

```python
from oscal_pydantic import catalog
from oscal_pydantic.core import common

# If a section has any requirements, they must go into an inner control group
# If a section has no requriements, but some statements, they should be added as parts of the group
# Finally, if a section has no text at all, just return the group.
if normative_statements:
    # The section contains requirements, and must have a control
    # Controls must be inside an inner group since a group can't have both
    # an inner group and inner controls
    section_control_list: list[catalog.Control] = [
        self.section_to_control(
            section_title = section_header,
            control_list=normative_statements,
        )
    ]

    # Under some circumstances
    section_control_group: catalog.Group = catalog.Group(
        id=re.sub("group", "control", group_id),
        title=f"{section_header}: Group for Normative Statements",
    )
    section_control_group.controls = section_control_list

    section_group = self.add_subsection_to_parent(
        section_group, section_control_group
    )
if informative_statements:
    # add informative statements
    informative_parts: list[catalog.BasePart] = []
    for statement_number, overview_statement in enumerate(informative_statements):
        informative_parts.append(
            catalog.GroupPart(
                id=f"{group_id}-{statement_number}",
                name="overview",
                prose=overview_statement,
            )
        )

    section_group.parts = informative_parts

return section_group
```

#### Summary

This example highlights a key point for this implemention. The programmer is responsible for determining how the data they are processing should map to the schema represented in metaschema, the oscal-pydantic library plays no role in this analysis. The function of the library is to ensure output encoded in OSCAL reflects the constraints defined in the metaschema.

### Example 2: Import a Document conforming to a metaschema

The opposite pattern will also be an important use case. When receiving a document purporting to comply to a metaschema, the contents must be parsed and presented in an idiomatic way to the programmer for further processing. Upon receiving a catalog, for example, the controls may be stored in a database with a totally different schema than the one defined in the metaschema.

In this use case, the library should attempt to parse the document. If the document doesn't conform to the metaschema, an informative error should be raised, and the parser should stop. If parsing is successful, the library should present the document in an idiomatic way, or allow the programmer to access the document in a few different ways. Good options may include:

1. An object corresponding to the assembly described in the metaschema, including properties representing the objects elements, and helpful functions (to be defined)
1. A dictionary or other appropriate simple structure (available by calling a method on the object to explicitly convert it, e.g. "catalog.to_dict()")

The following sample code illustrates this pattern from the oscal_pydantic library:

```python
from oscal_pydantic import document, catalog

# Function defined in the test cases
def test_import_catalog(self):
    with open(RESOURCES_PATH.joinpath(Path("NIST_SP-800-53_rev5_catalog.json"))) as catalog_file:
        catalog_bytes = catalog_file.read()
    test_catalog = document.Document.model_validate_json(catalog_bytes)
    assert isinstance(test_catalog, document.Document)

# Example call to dump the model as json
test_catalog.model_dump_json()

# Example call to dump the model to a dict
test_catalog.dict()
```

The likeliest use for the parsed document will be to convert the data to the applications internal schema for storage in a database, or for downstream processing.