"""
The schemagen module contains packages for producing pythonic representations of parsed metaschemas.
"""

# TODO: delete this junk below, it's just for reference
A = {
    "@xmlns": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
    "@abstract": "no",
    "schema-name": "OSCAL Control Catalog Model",
    "schema-version": "1.1.2",
    "short-name": "oscal-catalog",
    "namespace": "http://csrc.nist.gov/ns/oscal/1.0",
    "json-base-uri": "http://csrc.nist.gov/ns/oscal",
    "remarks": {"p": [{"code": ["catalog"]}]},
    "import": [
        {"@href": "oscal_control-common_metaschema.xml"},
        {"@href": "oscal_metadata_metaschema.xml"},
    ],
    "define-assembly": [
        {
            "@name": "catalog",
            "@scope": "global",
            "formal-name": "Catalog",
            "description": {
                "a": [
                    {
                        "@href": "https://pages.nist.gov/OSCAL/concepts/terminology/#catalog",
                        "$": "organized collection",
                    }
                ]
            },
            "root-name": "catalog",
            "define-flag": [
                {
                    "@name": "uuid",
                    "@as-type": "uuid",
                    "@required": "yes",
                    "formal-name": "Catalog Universally Unique Identifier",
                    "description": "Provides a globally unique means to identify a given catalog instance.",
                    "prop": [
                        {
                            "@name": "value-type",
                            "@value": "identifier",
                            "@namespace": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
                        },
                        {
                            "@name": "identifier-type",
                            "@value": "machine-oriented",
                            "@namespace": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
                        },
                        {
                            "@name": "identifier-uniqueness",
                            "@value": "global",
                            "@namespace": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
                        },
                        {
                            "@name": "identifier-scope",
                            "@value": "cross-instance",
                            "@namespace": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
                        },
                        {
                            "@name": "identifier-persistence",
                            "@value": "change-on-write",
                            "@namespace": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
                        },
                    ],
                }
            ],
            "model": {
                "assembly": [
                    {"@ref": "metadata", "@min-occurs": 1, "@max-occurs": 1},
                    {
                        "@ref": "parameter",
                        "@max-occurs": "unbounded",
                        "@min-occurs": 0,
                        "group-as": {
                            "@name": "params",
                            "@in-json": "ARRAY",
                            "@in-xml": "UNGROUPED",
                        },
                    },
                    {
                        "@ref": "control",
                        "@max-occurs": "unbounded",
                        "@min-occurs": 0,
                        "group-as": {
                            "@name": "controls",
                            "@in-json": "ARRAY",
                            "@in-xml": "UNGROUPED",
                        },
                    },
                    {
                        "@ref": "group",
                        "@max-occurs": "unbounded",
                        "@min-occurs": 0,
                        "group-as": {
                            "@name": "groups",
                            "@in-json": "ARRAY",
                            "@in-xml": "UNGROUPED",
                        },
                    },
                    {
                        "@ref": "back-matter",
                        "@min-occurs": 0,
                        "@max-occurs": 1,
                        "remarks": {
                            "p": ["Back matter including references and resources."]
                        },
                    },
                ]
            },
            "constraint": {
                "allowed-values": [
                    {
                        "@target": "metadata/prop[has-oscal-namespace('http://csrc.nist.gov/ns/oscal')]/@name",
                        "@level": "ERROR",
                        "@allow-other": "no",
                        "@extensible": "external",
                        "enum": [
                            {
                                "@value": "resolution-tool",
                                "$": "The tool used to produce a resolved profile.",
                            },
                            {
                                "@value": "source-profile-uuid",
                                "code": ["uuid"],
                                "a": [
                                    {
                                        "@href": "https://pages.nist.gov/OSCAL/concepts/processing/profile-resolution/",
                                        "$": "profile resolution",
                                    }
                                ],
                            },
                        ],
                    },
                    {
                        "@target": "metadata/link/@rel",
                        "@allow-other": "yes",
                        "@level": "ERROR",
                        "@extensible": "external",
                        "enum": [
                            {
                                "@value": "source-profile",
                                "a": [
                                    {
                                        "@href": "https://pages.nist.gov/OSCAL/concepts/processing/profile-resolution/",
                                        "$": "profile resolution",
                                    }
                                ],
                            },
                            {
                                "@value": "source-profile-uuid",
                                "code": ["uuid"],
                                "a": [
                                    {
                                        "@href": "https://pages.nist.gov/OSCAL/concepts/processing/profile-resolution/",
                                        "$": "profile resolution",
                                    }
                                ],
                            },
                        ],
                    },
                ],
                "index": [
                    {
                        "@name": "catalog-parts",
                        "@target": "//part",
                        "@level": "ERROR",
                        "key-field": [{"@target": "@id"}],
                    },
                    {
                        "@name": "catalog-props",
                        "@target": "//prop",
                        "@level": "ERROR",
                        "key-field": [{"@target": "@uuid"}],
                    },
                    {
                        "@name": "catalog-groups-controls-parts",
                        "@target": "//(control|group|part)",
                        "@level": "ERROR",
                        "key-field": [{"@target": "@id"}],
                    },
                    {
                        "@name": "catalog-controls",
                        "@target": "//control",
                        "@level": "ERROR",
                        "key-field": [{"@target": "@id"}],
                    },
                    {
                        "@name": "catalog-params",
                        "@target": "//param",
                        "@level": "ERROR",
                        "key-field": [{"@target": "@id"}],
                    },
                    {
                        "@name": "catalog-groups",
                        "@target": "//group",
                        "@level": "ERROR",
                        "key-field": [{"@target": "@id"}],
                    },
                ],
            },
            "remarks": {"p": [{"code": ["group"]}]},
            "example": [
                {
                    "description": "A small catalog with a single control.",
                    "catalog": {
                        "@xmlns": "http://csrc.nist.gov/ns/oscal/1.0",
                        "@uuid": "35566cd4-7331-43ba-b023-988c38d62673",
                        "title": ["A Miniature Catalog"],
                        "control": [{"@id": "single", "title": ["A Single Control"]}],
                    },
                }
            ],
        },
        {
            "@name": "group",
            "@scope": "global",
            "formal-name": "Control Group",
            "description": "A group of controls, or of groups of controls.",
            "define-flag": [
                {
                    "@name": "id",
                    "@as-type": "token",
                    "@required": "no",
                    "formal-name": "Group Identifier",
                    "description": "Identifies the group for the purpose of cross-linking within the defining instance or from other instances that reference the catalog.",
                    "prop": [
                        {
                            "@name": "value-type",
                            "@value": "identifier",
                            "@namespace": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
                        },
                        {
                            "@name": "identifier-type",
                            "@value": "human-oriented",
                            "@namespace": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
                        },
                        {
                            "@name": "identifier-uniqueness",
                            "@value": "instance",
                            "@namespace": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
                        },
                        {
                            "@name": "identifier-scope",
                            "@value": "cross-instance",
                            "@namespace": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
                        },
                        {
                            "@name": "identifier-persistence",
                            "@value": "per-subject",
                            "@namespace": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
                        },
                    ],
                },
                {
                    "@name": "class",
                    "@as-type": "token",
                    "@required": "no",
                    "formal-name": "Group Class",
                    "description": "A textual label that provides a sub-type or characterization of the group.",
                    "remarks": {
                        "p": [{"code": ["class", "class"]}, {"code": ["class"]}]
                    },
                },
            ],
            "model": {
                "define-field": [
                    {
                        "@name": "title",
                        "@as-type": "markup-line",
                        "@min-occurs": 1,
                        "@collapsible": "no",
                        "@max-occurs": 1,
                        "@in-xml": "WRAPPED",
                        "formal-name": "Group Title",
                        "description": "A name given to the group, which may be used by a tool for display and navigation.",
                    }
                ],
                "assembly": [
                    {
                        "@ref": "parameter",
                        "@max-occurs": "unbounded",
                        "@min-occurs": 0,
                        "group-as": {
                            "@name": "params",
                            "@in-json": "ARRAY",
                            "@in-xml": "UNGROUPED",
                        },
                    },
                    {
                        "@ref": "property",
                        "@max-occurs": "unbounded",
                        "@min-occurs": 0,
                        "group-as": {
                            "@name": "props",
                            "@in-json": "ARRAY",
                            "@in-xml": "UNGROUPED",
                        },
                    },
                    {
                        "@ref": "link",
                        "@max-occurs": "unbounded",
                        "@min-occurs": 0,
                        "group-as": {
                            "@name": "links",
                            "@in-json": "ARRAY",
                            "@in-xml": "UNGROUPED",
                        },
                    },
                    {
                        "@ref": "part",
                        "@max-occurs": "unbounded",
                        "@min-occurs": 0,
                        "group-as": {
                            "@name": "parts",
                            "@in-json": "ARRAY",
                            "@in-xml": "UNGROUPED",
                        },
                    },
                ],
                "choice": [
                    {
                        "assembly": [
                            {
                                "@ref": "group",
                                "@max-occurs": "unbounded",
                                "@min-occurs": 0,
                                "group-as": {
                                    "@name": "groups",
                                    "@in-json": "ARRAY",
                                    "@in-xml": "UNGROUPED",
                                },
                            },
                            {
                                "@ref": "control",
                                "@max-occurs": "unbounded",
                                "@min-occurs": 0,
                                "group-as": {
                                    "@name": "controls",
                                    "@in-json": "ARRAY",
                                    "@in-xml": "UNGROUPED",
                                },
                            },
                        ]
                    }
                ],
            },
            "constraint": {
                "allowed-values": [
                    {
                        "@target": "prop[has-oscal-namespace('http://csrc.nist.gov/ns/oscal')]/@name",
                        "@level": "ERROR",
                        "@allow-other": "no",
                        "@extensible": "external",
                        "enum": [
                            {
                                "@value": "label",
                                "$": "A human-readable label for the parent context, which may be rendered in place of the actual identifier for some use cases.",
                            },
                            {
                                "@value": "sort-id",
                                "$": "An alternative identifier, whose value is easily sortable among other such values in the document.",
                            },
                            {
                                "@value": "alt-identifier",
                                "$": "An alternate or aliased identifier for the parent context.",
                            },
                        ],
                    },
                    {
                        "@target": "part[has-oscal-namespace('http://csrc.nist.gov/ns/oscal')]/@name",
                        "@level": "ERROR",
                        "@allow-other": "no",
                        "@extensible": "external",
                        "enum": [
                            {
                                "@value": "overview",
                                "$": "An introduction to a control or a group of controls.",
                            },
                            {
                                "@value": "instruction",
                                "$": "Information providing directions for a control or a group of controls.",
                            },
                        ],
                    },
                ]
            },
            "remarks": {"p": [{"code": ["group"]}, {"code": ["group"]}]},
            "example": [
                {
                    "group": {
                        "@xmlns": "http://csrc.nist.gov/ns/oscal/1.0",
                        "@id": "xyz",
                        "title": ["My Group"],
                        "prop": [{"@name": "required", "@value": "some value"}],
                        "control": [{"@id": "xyz1", "title": ["Control"]}],
                    }
                }
            ],
        },
        {
            "@name": "control",
            "@scope": "global",
            "formal-name": "Control",
            "description": {
                "a": [
                    {
                        "@href": "https://pages.nist.gov/OSCAL/concepts/terminology/#control",
                        "$": "structured object",
                    }
                ]
            },
            "define-flag": [
                {
                    "@name": "id",
                    "@as-type": "token",
                    "@required": "yes",
                    "formal-name": "Control Identifier",
                    "description": "Identifies a control such that it can be referenced in the defining\n                        catalog and other OSCAL instances (e.g., profiles).",
                    "prop": [
                        {
                            "@name": "value-type",
                            "@value": "identifier",
                            "@namespace": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
                        },
                        {
                            "@name": "identifier-type",
                            "@value": "human-oriented",
                            "@namespace": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
                        },
                        {
                            "@name": "identifier-uniqueness",
                            "@value": "local",
                            "@namespace": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
                        },
                        {
                            "@name": "identifier-scope",
                            "@value": "instance",
                            "@namespace": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
                        },
                        {
                            "@name": "identifier-persistence",
                            "@value": "per-subject",
                            "@namespace": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
                        },
                    ],
                },
                {
                    "@name": "class",
                    "@as-type": "token",
                    "@required": "no",
                    "formal-name": "Control Class",
                    "description": "A textual label that provides a sub-type or characterization of the\n                        control.",
                    "remarks": {
                        "p": [{"code": ["class", "class"]}, {"code": ["class"]}]
                    },
                },
            ],
            "model": {
                "define-field": [
                    {
                        "@name": "title",
                        "@as-type": "markup-line",
                        "@min-occurs": 1,
                        "@collapsible": "no",
                        "@max-occurs": 1,
                        "@in-xml": "WRAPPED",
                        "formal-name": "Control Title",
                        "description": "A name given to the control, which may be used by a tool for\n                              display and navigation.",
                    }
                ],
                "assembly": [
                    {
                        "@ref": "parameter",
                        "@max-occurs": "unbounded",
                        "@min-occurs": 0,
                        "group-as": {
                            "@name": "params",
                            "@in-json": "ARRAY",
                            "@in-xml": "UNGROUPED",
                        },
                    },
                    {
                        "@ref": "property",
                        "@max-occurs": "unbounded",
                        "@min-occurs": 0,
                        "group-as": {
                            "@name": "props",
                            "@in-json": "ARRAY",
                            "@in-xml": "UNGROUPED",
                        },
                    },
                    {
                        "@ref": "link",
                        "@max-occurs": "unbounded",
                        "@min-occurs": 0,
                        "group-as": {
                            "@name": "links",
                            "@in-json": "ARRAY",
                            "@in-xml": "UNGROUPED",
                        },
                    },
                    {
                        "@ref": "part",
                        "@max-occurs": "unbounded",
                        "@min-occurs": 0,
                        "group-as": {
                            "@name": "parts",
                            "@in-json": "ARRAY",
                            "@in-xml": "UNGROUPED",
                        },
                    },
                    {
                        "@ref": "control",
                        "@max-occurs": "unbounded",
                        "@min-occurs": 0,
                        "group-as": {
                            "@name": "controls",
                            "@in-json": "ARRAY",
                            "@in-xml": "UNGROUPED",
                        },
                    },
                ],
            },
            "constraint": {
                "expect": [
                    {
                        "@id": "catalog-control-require-statement-when-not-withdrawn",
                        "@target": ".",
                        "@test": "prop[@name='status']/@value=('withdrawn','Withdrawn') or part[@name='statement']",
                        "@level": "ERROR",
                    },
                    {
                        "@level": "WARNING",
                        "@target": "part[has-oscal-namespace('http://csrc.nist.gov/ns/oscal') and @name=('assessment','assessment-method')]",
                        "@test": "prop[has-oscal-namespace(('http://csrc.nist.gov/ns/oscal','http://csrc.nist.gov/ns/rmf')) and @name='method']",
                    },
                ],
                "allowed-values": [
                    {
                        "@target": "prop[has-oscal-namespace('http://csrc.nist.gov/ns/oscal')]/@name",
                        "@level": "ERROR",
                        "@allow-other": "no",
                        "@extensible": "external",
                        "enum": [
                            {
                                "@value": "label",
                                "$": "A human-readable label for the parent context, which may be rendered in place of the actual identifier for some use cases.",
                            },
                            {
                                "@value": "sort-id",
                                "$": "An alternative identifier, whose value is easily sortable among other such values in the document.",
                            },
                            {
                                "@value": "alt-identifier",
                                "$": "An alternate or aliased identifier for the parent context.",
                            },
                            {"@value": "status", "code": ["control", "control"]},
                        ],
                    },
                    {
                        "@target": "prop[has-oscal-namespace('http://csrc.nist.gov/ns/oscal') and @name='status']/@value",
                        "@level": "ERROR",
                        "@allow-other": "no",
                        "@extensible": "external",
                        "enum": [
                            {
                                "@value": "withdrawn",
                                "$": "The control is no longer used.",
                            },
                            {
                                "@value": "Withdrawn",
                                "@deprecated": "1.0.0",
                                "$": "**(deprecated)*** Use 'withdrawn'\n                              instead.",
                            },
                        ],
                    },
                    {
                        "@target": "link/@rel",
                        "@allow-other": "yes",
                        "@level": "ERROR",
                        "@extensible": "external",
                        "enum": [
                            {
                                "@value": "reference",
                                "$": "The link cites an external resource related to this\n                              control.",
                            },
                            {
                                "@value": "related",
                                "$": "The link identifies another control with bearing to\n                              this control.",
                            },
                            {
                                "@value": "required",
                                "$": "The link identifies another control that must be\n                              present if this control is present.",
                            },
                            {
                                "@value": "incorporated-into",
                                "$": "The link identifies other control content\n                              where this control content is now addressed.",
                            },
                            {
                                "@value": "moved-to",
                                "$": "The containing control definition was moved to the\n                              referenced control.",
                            },
                        ],
                    },
                    {
                        "@target": "part[has-oscal-namespace('http://csrc.nist.gov/ns/oscal')]/@name",
                        "@level": "ERROR",
                        "@allow-other": "no",
                        "@extensible": "external",
                        "enum": [
                            {
                                "@value": "overview",
                                "$": "An introduction to a control or a group of\n                              controls.",
                            },
                            {
                                "@value": "statement",
                                "$": "A set of implementation requirements or recommendations.",
                            },
                            {
                                "@value": "guidance",
                                "$": "Additional information to consider when selecting,\n                              implementing, assessing, and monitoring a control.",
                            },
                            {
                                "@value": "example",
                                "$": "An example of an implemented requirement or control statement.",
                            },
                            {
                                "@value": "assessment",
                                "@deprecated": "1.0.1",
                                "$": "**(deprecated)** Use\n                              'assessment-method' instead.",
                            },
                            {
                                "@value": "assessment-method",
                                "$": "The part describes a method-based assessment\n                              over a set of assessment objects.",
                            },
                        ],
                    },
                    {
                        "@target": "part[has-oscal-namespace('http://csrc.nist.gov/ns/oscal') and @name='statement']//part[has-oscal-namespace('http://csrc.nist.gov/ns/oscal')]/@name",
                        "@level": "ERROR",
                        "@allow-other": "no",
                        "@extensible": "external",
                        "enum": [
                            {
                                "@value": "item",
                                "$": "An individual item within a control statement.",
                            }
                        ],
                        "remarks": {"p": ['Nested statement parts are "item" parts.']},
                    },
                    {
                        "@target": ".//part[has-oscal-namespace('http://csrc.nist.gov/ns/oscal')]/@name",
                        "@level": "ERROR",
                        "@allow-other": "no",
                        "@extensible": "external",
                        "enum": [
                            {
                                "@value": "objective",
                                "@deprecated": "1.0.1",
                                "$": "**(deprecated)** Use\n                              'assessment-objective' instead.",
                            },
                            {
                                "@value": "assessment-objective",
                                "$": "The part describes a set of assessment\n                              objectives.",
                            },
                        ],
                        "remarks": {"p": ["Objectives can be nested."]},
                    },
                    {
                        "@target": "part[has-oscal-namespace('http://csrc.nist.gov/ns/oscal') and @name=('assessment','assessment-method')]/part[has-oscal-namespace('http://csrc.nist.gov/ns/oscal')]/@name",
                        "@level": "ERROR",
                        "@allow-other": "no",
                        "@extensible": "external",
                        "enum": [
                            {
                                "@value": "objects",
                                "@deprecated": "1.0.1",
                                "$": "**(deprecated)** Use\n                              'assessment-objects' instead.",
                            },
                            {
                                "@value": "assessment-objects",
                                "$": "Provides a listing of assessment\n                              objects.",
                            },
                        ],
                        "remarks": {
                            "p": ["Assessment objects appear on assessment methods."]
                        },
                    },
                    {
                        "@target": "part[has-oscal-namespace('http://csrc.nist.gov/ns/oscal') and @name=('assessment','assessment-method')]/prop[has-oscal-namespace('http://csrc.nist.gov/ns/oscal')]/@name",
                        "@level": "ERROR",
                        "@allow-other": "no",
                        "@extensible": "external",
                        "enum": [
                            {
                                "@value": "method",
                                "@deprecated": "1.0.1",
                                "$": "**(deprecated)** Use 'method' in the 'http://csrc.nist.gov/ns/rmf' namespace. The assessment method to use. This typically appears on parts with the name \"assessment-method\".",
                            }
                        ],
                    },
                    {
                        "@target": "part[has-oscal-namespace('http://csrc.nist.gov/ns/oscal') and @name=('assessment','assessment-method')]/prop[has-oscal-namespace('http://csrc.nist.gov/ns/rmf')]/@name",
                        "@level": "ERROR",
                        "@allow-other": "no",
                        "@extensible": "external",
                        "enum": [
                            {
                                "@value": "method",
                                "$": 'The assessment method to use. This typically appears on\n                              parts with the name "assessment-method".',
                            }
                        ],
                    },
                    {
                        "@target": "part[has-oscal-namespace('http://csrc.nist.gov/ns/oscal') and @name=('assessment','assessment-method')]/prop[has-oscal-namespace(('http://csrc.nist.gov/ns/oscal','http://csrc.nist.gov/ns/rmf')) and @name='method']/@value",
                        "@level": "ERROR",
                        "@allow-other": "no",
                        "@extensible": "external",
                        "enum": [
                            {
                                "@value": "INTERVIEW",
                                "$": "The process of holding discussions with individuals or groups of individuals within an organization to once again, facilitate assessor understanding, achieve clarification, or obtain evidence.",
                            },
                            {
                                "@value": "EXAMINE",
                                "$": "The process of reviewing, inspecting, observing, studying, or analyzing one or more assessment objects (i.e., specifications, mechanisms, or activities).",
                            },
                            {
                                "@value": "TEST",
                                "$": "The process of exercising one or more assessment objects (i.e., activities or mechanisms) under specified conditions to compare actual with expected behavior.",
                            },
                        ],
                    },
                ],
                "index-has-key": {
                    "@name": "catalog-groups-controls-parts",
                    "@target": "link[@rel=('related','required','incorporated-into','moved-to') and starts-with(@href,'#')]",
                    "@level": "ERROR",
                    "key-field": [{"@target": "@href", "@pattern": "#(.*)"}],
                },
            },
            "remarks": {
                "p": [
                    {"code": ["control", "part", "group"]},
                    'Control structures in OSCAL will also exhibit regularities and rules that are not codified in OSCAL but in its applications or domains of application. For example, for catalogs describing controls as defined by NIST SP 800-53, a control must have a part with the name "statement", which represents the textual narrative of the control. This "statement" part must occur only once, but may have nested parts to allow for multiple paragraphs or sections of text. This organization supports addressability of this data content as long as, and only insofar as, it is consistently implemented across the control set. As given with these model definitions, constraints defined and assigned here can aid in ensuring this regularity; but other such constraints and other useful patterns of use remain to be discovered and described.',
                ]
            },
            "example": [
                {
                    "control": {
                        "@xmlns": "http://csrc.nist.gov/ns/oscal/1.0",
                        "@id": "x",
                        "title": ["Control 1"],
                    }
                }
            ],
        },
    ],
}

catalog = {
    "file": "oscal_catalog_metaschema.xml",
    "schema_dict": {
        "@xmlns": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
        "@abstract": "no",
        "schema-name": "OSCAL Control Catalog Model",
        "schema-version": "1.1.2",
        "short-name": "oscal-catalog",
        "namespace": "http://csrc.nist.gov/ns/oscal/1.0",
        "json-base-uri": "http://csrc.nist.gov/ns/oscal",
        "remarks": {"p": [{"code": ["catalog"]}]},
        "import": [
            {"@href": "oscal_control-common_metaschema.xml"},
            {"@href": "oscal_metadata_metaschema.xml"},
        ],
        "define-assembly": [
            {
                "@name": "catalog",
                "@scope": "global",
                "formal-name": "Catalog",
                "description": {
                    "a": [
                        {
                            "@href": "https://pages.nist.gov/OSCAL/concepts/terminology/#catalog",
                            "$": "organized collection",
                        }
                    ]
                },
                "root-name": "catalog",
                "define-flag": [
                    {
                        "@name": "uuid",
                        "@as-type": "uuid",
                        "@required": "yes",
                        "formal-name": "Catalog Universally Unique Identifier",
                        "description": "Provides a globally unique means to identify a given catalog instance.",
                        "prop": [
                            {
                                "@name": "value-type",
                                "@value": "identifier",
                                "@namespace": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
                            },
                            {
                                "@name": "identifier-type",
                                "@value": "machine-oriented",
                                "@namespace": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
                            },
                            {
                                "@name": "identifier-uniqueness",
                                "@value": "global",
                                "@namespace": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
                            },
                            {
                                "@name": "identifier-scope",
                                "@value": "cross-instance",
                                "@namespace": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
                            },
                            {
                                "@name": "identifier-persistence",
                                "@value": "change-on-write",
                                "@namespace": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
                            },
                        ],
                    }
                ],
                "model": {
                    "assembly": [
                        {"@ref": "metadata", "@min-occurs": 1, "@max-occurs": 1},
                        {
                            "@ref": "parameter",
                            "@max-occurs": "unbounded",
                            "@min-occurs": 0,
                            "group-as": {
                                "@name": "params",
                                "@in-json": "ARRAY",
                                "@in-xml": "UNGROUPED",
                            },
                        },
                        {
                            "@ref": "control",
                            "@max-occurs": "unbounded",
                            "@min-occurs": 0,
                            "group-as": {
                                "@name": "controls",
                                "@in-json": "ARRAY",
                                "@in-xml": "UNGROUPED",
                            },
                        },
                        {
                            "@ref": "group",
                            "@max-occurs": "unbounded",
                            "@min-occurs": 0,
                            "group-as": {
                                "@name": "groups",
                                "@in-json": "ARRAY",
                                "@in-xml": "UNGROUPED",
                            },
                        },
                        {
                            "@ref": "back-matter",
                            "@min-occurs": 0,
                            "@max-occurs": 1,
                            "remarks": {
                                "p": ["Back matter including references and resources."]
                            },
                        },
                    ]
                },
                "constraint": {
                    "allowed-values": [
                        {
                            "@target": "metadata/prop[has-oscal-namespace('http://csrc.nist.gov/ns/oscal')]/@name",
                            "@level": "ERROR",
                            "@allow-other": "no",
                            "@extensible": "external",
                            "enum": [
                                {
                                    "@value": "resolution-tool",
                                    "$": "The tool used to produce a resolved profile.",
                                },
                                {
                                    "@value": "source-profile-uuid",
                                    "code": ["uuid"],
                                    "a": [
                                        {
                                            "@href": "https://pages.nist.gov/OSCAL/concepts/processing/profile-resolution/",
                                            "$": "profile resolution",
                                        }
                                    ],
                                },
                            ],
                        },
                        {
                            "@target": "metadata/link/@rel",
                            "@allow-other": "yes",
                            "@level": "ERROR",
                            "@extensible": "external",
                            "enum": [
                                {
                                    "@value": "source-profile",
                                    "a": [
                                        {
                                            "@href": "https://pages.nist.gov/OSCAL/concepts/processing/profile-resolution/",
                                            "$": "profile resolution",
                                        }
                                    ],
                                },
                                {
                                    "@value": "source-profile-uuid",
                                    "code": ["uuid"],
                                    "a": [
                                        {
                                            "@href": "https://pages.nist.gov/OSCAL/concepts/processing/profile-resolution/",
                                            "$": "profile resolution",
                                        }
                                    ],
                                },
                            ],
                        },
                    ],
                    "index": [
                        {
                            "@name": "catalog-parts",
                            "@target": "//part",
                            "@level": "ERROR",
                            "key-field": [{"@target": "@id"}],
                        },
                        {
                            "@name": "catalog-props",
                            "@target": "//prop",
                            "@level": "ERROR",
                            "key-field": [{"@target": "@uuid"}],
                        },
                        {
                            "@name": "catalog-groups-controls-parts",
                            "@target": "//(control|group|part)",
                            "@level": "ERROR",
                            "key-field": [{"@target": "@id"}],
                        },
                        {
                            "@name": "catalog-controls",
                            "@target": "//control",
                            "@level": "ERROR",
                            "key-field": [{"@target": "@id"}],
                        },
                        {
                            "@name": "catalog-params",
                            "@target": "//param",
                            "@level": "ERROR",
                            "key-field": [{"@target": "@id"}],
                        },
                        {
                            "@name": "catalog-groups",
                            "@target": "//group",
                            "@level": "ERROR",
                            "key-field": [{"@target": "@id"}],
                        },
                    ],
                },
                "remarks": {"p": [{"code": ["group"]}]},
                "example": [
                    {
                        "description": "A small catalog with a single control.",
                        "catalog": {
                            "@xmlns": "http://csrc.nist.gov/ns/oscal/1.0",
                            "@uuid": "35566cd4-7331-43ba-b023-988c38d62673",
                            "title": ["A Miniature Catalog"],
                            "control": [
                                {"@id": "single", "title": ["A Single Control"]}
                            ],
                        },
                    }
                ],
            },
            {
                "@name": "group",
                "@scope": "global",
                "formal-name": "Control Group",
                "description": "A group of controls, or of groups of controls.",
                "define-flag": [
                    {
                        "@name": "id",
                        "@as-type": "token",
                        "@required": "no",
                        "formal-name": "Group Identifier",
                        "description": "Identifies the group for the purpose of cross-linking within the defining instance or from other instances that reference the catalog.",
                        "prop": [
                            {
                                "@name": "value-type",
                                "@value": "identifier",
                                "@namespace": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
                            },
                            {
                                "@name": "identifier-type",
                                "@value": "human-oriented",
                                "@namespace": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
                            },
                            {
                                "@name": "identifier-uniqueness",
                                "@value": "instance",
                                "@namespace": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
                            },
                            {
                                "@name": "identifier-scope",
                                "@value": "cross-instance",
                                "@namespace": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
                            },
                            {
                                "@name": "identifier-persistence",
                                "@value": "per-subject",
                                "@namespace": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
                            },
                        ],
                    },
                    {
                        "@name": "class",
                        "@as-type": "token",
                        "@required": "no",
                        "formal-name": "Group Class",
                        "description": "A textual label that provides a sub-type or characterization of the group.",
                        "remarks": {
                            "p": [{"code": ["class", "class"]}, {"code": ["class"]}]
                        },
                    },
                ],
                "model": {
                    "define-field": [
                        {
                            "@name": "title",
                            "@as-type": "markup-line",
                            "@min-occurs": 1,
                            "@collapsible": "no",
                            "@max-occurs": 1,
                            "@in-xml": "WRAPPED",
                            "formal-name": "Group Title",
                            "description": "A name given to the group, which may be used by a tool for display and navigation.",
                        }
                    ],
                    "assembly": [
                        {
                            "@ref": "parameter",
                            "@max-occurs": "unbounded",
                            "@min-occurs": 0,
                            "group-as": {
                                "@name": "params",
                                "@in-json": "ARRAY",
                                "@in-xml": "UNGROUPED",
                            },
                        },
                        {
                            "@ref": "property",
                            "@max-occurs": "unbounded",
                            "@min-occurs": 0,
                            "group-as": {
                                "@name": "props",
                                "@in-json": "ARRAY",
                                "@in-xml": "UNGROUPED",
                            },
                        },
                        {
                            "@ref": "link",
                            "@max-occurs": "unbounded",
                            "@min-occurs": 0,
                            "group-as": {
                                "@name": "links",
                                "@in-json": "ARRAY",
                                "@in-xml": "UNGROUPED",
                            },
                        },
                        {
                            "@ref": "part",
                            "@max-occurs": "unbounded",
                            "@min-occurs": 0,
                            "group-as": {
                                "@name": "parts",
                                "@in-json": "ARRAY",
                                "@in-xml": "UNGROUPED",
                            },
                        },
                    ],
                    "choice": [
                        {
                            "assembly": [
                                {
                                    "@ref": "group",
                                    "@max-occurs": "unbounded",
                                    "@min-occurs": 0,
                                    "group-as": {
                                        "@name": "groups",
                                        "@in-json": "ARRAY",
                                        "@in-xml": "UNGROUPED",
                                    },
                                },
                                {
                                    "@ref": "control",
                                    "@max-occurs": "unbounded",
                                    "@min-occurs": 0,
                                    "group-as": {
                                        "@name": "controls",
                                        "@in-json": "ARRAY",
                                        "@in-xml": "UNGROUPED",
                                    },
                                },
                            ]
                        }
                    ],
                },
                "constraint": {
                    "allowed-values": [
                        {
                            "@target": "prop[has-oscal-namespace('http://csrc.nist.gov/ns/oscal')]/@name",
                            "@level": "ERROR",
                            "@allow-other": "no",
                            "@extensible": "external",
                            "enum": [
                                {
                                    "@value": "label",
                                    "$": "A human-readable label for the parent context, which may be rendered in place of the actual identifier for some use cases.",
                                },
                                {
                                    "@value": "sort-id",
                                    "$": "An alternative identifier, whose value is easily sortable among other such values in the document.",
                                },
                                {
                                    "@value": "alt-identifier",
                                    "$": "An alternate or aliased identifier for the parent context.",
                                },
                            ],
                        },
                        {
                            "@target": "part[has-oscal-namespace('http://csrc.nist.gov/ns/oscal')]/@name",
                            "@level": "ERROR",
                            "@allow-other": "no",
                            "@extensible": "external",
                            "enum": [
                                {
                                    "@value": "overview",
                                    "$": "An introduction to a control or a group of controls.",
                                },
                                {
                                    "@value": "instruction",
                                    "$": "Information providing directions for a control or a group of controls.",
                                },
                            ],
                        },
                    ]
                },
                "remarks": {"p": [{"code": ["group"]}, {"code": ["group"]}]},
                "example": [
                    {
                        "group": {
                            "@xmlns": "http://csrc.nist.gov/ns/oscal/1.0",
                            "@id": "xyz",
                            "title": ["My Group"],
                            "prop": [{"@name": "required", "@value": "some value"}],
                            "control": [{"@id": "xyz1", "title": ["Control"]}],
                        }
                    }
                ],
            },
            {
                "@name": "control",
                "@scope": "global",
                "formal-name": "Control",
                "description": {
                    "a": [
                        {
                            "@href": "https://pages.nist.gov/OSCAL/concepts/terminology/#control",
                            "$": "structured object",
                        }
                    ]
                },
                "define-flag": [
                    {
                        "@name": "id",
                        "@as-type": "token",
                        "@required": "yes",
                        "formal-name": "Control Identifier",
                        "description": "Identifies a control such that it can be referenced in the defining\n                        catalog and other OSCAL instances (e.g., profiles).",
                        "prop": [
                            {
                                "@name": "value-type",
                                "@value": "identifier",
                                "@namespace": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
                            },
                            {
                                "@name": "identifier-type",
                                "@value": "human-oriented",
                                "@namespace": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
                            },
                            {
                                "@name": "identifier-uniqueness",
                                "@value": "local",
                                "@namespace": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
                            },
                            {
                                "@name": "identifier-scope",
                                "@value": "instance",
                                "@namespace": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
                            },
                            {
                                "@name": "identifier-persistence",
                                "@value": "per-subject",
                                "@namespace": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
                            },
                        ],
                    },
                    {
                        "@name": "class",
                        "@as-type": "token",
                        "@required": "no",
                        "formal-name": "Control Class",
                        "description": "A textual label that provides a sub-type or characterization of the\n                        control.",
                        "remarks": {
                            "p": [{"code": ["class", "class"]}, {"code": ["class"]}]
                        },
                    },
                ],
                "model": {
                    "define-field": [
                        {
                            "@name": "title",
                            "@as-type": "markup-line",
                            "@min-occurs": 1,
                            "@collapsible": "no",
                            "@max-occurs": 1,
                            "@in-xml": "WRAPPED",
                            "formal-name": "Control Title",
                            "description": "A name given to the control, which may be used by a tool for\n                              display and navigation.",
                        }
                    ],
                    "assembly": [
                        {
                            "@ref": "parameter",
                            "@max-occurs": "unbounded",
                            "@min-occurs": 0,
                            "group-as": {
                                "@name": "params",
                                "@in-json": "ARRAY",
                                "@in-xml": "UNGROUPED",
                            },
                        },
                        {
                            "@ref": "property",
                            "@max-occurs": "unbounded",
                            "@min-occurs": 0,
                            "group-as": {
                                "@name": "props",
                                "@in-json": "ARRAY",
                                "@in-xml": "UNGROUPED",
                            },
                        },
                        {
                            "@ref": "link",
                            "@max-occurs": "unbounded",
                            "@min-occurs": 0,
                            "group-as": {
                                "@name": "links",
                                "@in-json": "ARRAY",
                                "@in-xml": "UNGROUPED",
                            },
                        },
                        {
                            "@ref": "part",
                            "@max-occurs": "unbounded",
                            "@min-occurs": 0,
                            "group-as": {
                                "@name": "parts",
                                "@in-json": "ARRAY",
                                "@in-xml": "UNGROUPED",
                            },
                        },
                        {
                            "@ref": "control",
                            "@max-occurs": "unbounded",
                            "@min-occurs": 0,
                            "group-as": {
                                "@name": "controls",
                                "@in-json": "ARRAY",
                                "@in-xml": "UNGROUPED",
                            },
                        },
                    ],
                },
                "constraint": {
                    "expect": [
                        {
                            "@id": "catalog-control-require-statement-when-not-withdrawn",
                            "@target": ".",
                            "@test": "prop[@name='status']/@value=('withdrawn','Withdrawn') or part[@name='statement']",
                            "@level": "ERROR",
                        },
                        {
                            "@level": "WARNING",
                            "@target": "part[has-oscal-namespace('http://csrc.nist.gov/ns/oscal') and @name=('assessment','assessment-method')]",
                            "@test": "prop[has-oscal-namespace(('http://csrc.nist.gov/ns/oscal','http://csrc.nist.gov/ns/rmf')) and @name='method']",
                        },
                    ],
                    "allowed-values": [
                        {
                            "@target": "prop[has-oscal-namespace('http://csrc.nist.gov/ns/oscal')]/@name",
                            "@level": "ERROR",
                            "@allow-other": "no",
                            "@extensible": "external",
                            "enum": [
                                {
                                    "@value": "label",
                                    "$": "A human-readable label for the parent context, which may be rendered in place of the actual identifier for some use cases.",
                                },
                                {
                                    "@value": "sort-id",
                                    "$": "An alternative identifier, whose value is easily sortable among other such values in the document.",
                                },
                                {
                                    "@value": "alt-identifier",
                                    "$": "An alternate or aliased identifier for the parent context.",
                                },
                                {"@value": "status", "code": ["control", "control"]},
                            ],
                        },
                        {
                            "@target": "prop[has-oscal-namespace('http://csrc.nist.gov/ns/oscal') and @name='status']/@value",
                            "@level": "ERROR",
                            "@allow-other": "no",
                            "@extensible": "external",
                            "enum": [
                                {
                                    "@value": "withdrawn",
                                    "$": "The control is no longer used.",
                                },
                                {
                                    "@value": "Withdrawn",
                                    "@deprecated": "1.0.0",
                                    "$": "**(deprecated)*** Use 'withdrawn'\n                              instead.",
                                },
                            ],
                        },
                        {
                            "@target": "link/@rel",
                            "@allow-other": "yes",
                            "@level": "ERROR",
                            "@extensible": "external",
                            "enum": [
                                {
                                    "@value": "reference",
                                    "$": "The link cites an external resource related to this\n                              control.",
                                },
                                {
                                    "@value": "related",
                                    "$": "The link identifies another control with bearing to\n                              this control.",
                                },
                                {
                                    "@value": "required",
                                    "$": "The link identifies another control that must be\n                              present if this control is present.",
                                },
                                {
                                    "@value": "incorporated-into",
                                    "$": "The link identifies other control content\n                              where this control content is now addressed.",
                                },
                                {
                                    "@value": "moved-to",
                                    "$": "The containing control definition was moved to the\n                              referenced control.",
                                },
                            ],
                        },
                        {
                            "@target": "part[has-oscal-namespace('http://csrc.nist.gov/ns/oscal')]/@name",
                            "@level": "ERROR",
                            "@allow-other": "no",
                            "@extensible": "external",
                            "enum": [
                                {
                                    "@value": "overview",
                                    "$": "An introduction to a control or a group of\n                              controls.",
                                },
                                {
                                    "@value": "statement",
                                    "$": "A set of implementation requirements or recommendations.",
                                },
                                {
                                    "@value": "guidance",
                                    "$": "Additional information to consider when selecting,\n                              implementing, assessing, and monitoring a control.",
                                },
                                {
                                    "@value": "example",
                                    "$": "An example of an implemented requirement or control statement.",
                                },
                                {
                                    "@value": "assessment",
                                    "@deprecated": "1.0.1",
                                    "$": "**(deprecated)** Use\n                              'assessment-method' instead.",
                                },
                                {
                                    "@value": "assessment-method",
                                    "$": "The part describes a method-based assessment\n                              over a set of assessment objects.",
                                },
                            ],
                        },
                        {
                            "@target": "part[has-oscal-namespace('http://csrc.nist.gov/ns/oscal') and @name='statement']//part[has-oscal-namespace('http://csrc.nist.gov/ns/oscal')]/@name",
                            "@level": "ERROR",
                            "@allow-other": "no",
                            "@extensible": "external",
                            "enum": [
                                {
                                    "@value": "item",
                                    "$": "An individual item within a control statement.",
                                }
                            ],
                            "remarks": {
                                "p": ['Nested statement parts are "item" parts.']
                            },
                        },
                        {
                            "@target": ".//part[has-oscal-namespace('http://csrc.nist.gov/ns/oscal')]/@name",
                            "@level": "ERROR",
                            "@allow-other": "no",
                            "@extensible": "external",
                            "enum": [
                                {
                                    "@value": "objective",
                                    "@deprecated": "1.0.1",
                                    "$": "**(deprecated)** Use\n                              'assessment-objective' instead.",
                                },
                                {
                                    "@value": "assessment-objective",
                                    "$": "The part describes a set of assessment\n                              objectives.",
                                },
                            ],
                            "remarks": {"p": ["Objectives can be nested."]},
                        },
                        {
                            "@target": "part[has-oscal-namespace('http://csrc.nist.gov/ns/oscal') and @name=('assessment','assessment-method')]/part[has-oscal-namespace('http://csrc.nist.gov/ns/oscal')]/@name",
                            "@level": "ERROR",
                            "@allow-other": "no",
                            "@extensible": "external",
                            "enum": [
                                {
                                    "@value": "objects",
                                    "@deprecated": "1.0.1",
                                    "$": "**(deprecated)** Use\n                              'assessment-objects' instead.",
                                },
                                {
                                    "@value": "assessment-objects",
                                    "$": "Provides a listing of assessment\n                              objects.",
                                },
                            ],
                            "remarks": {
                                "p": [
                                    "Assessment objects appear on assessment methods."
                                ]
                            },
                        },
                        {
                            "@target": "part[has-oscal-namespace('http://csrc.nist.gov/ns/oscal') and @name=('assessment','assessment-method')]/prop[has-oscal-namespace('http://csrc.nist.gov/ns/oscal')]/@name",
                            "@level": "ERROR",
                            "@allow-other": "no",
                            "@extensible": "external",
                            "enum": [
                                {
                                    "@value": "method",
                                    "@deprecated": "1.0.1",
                                    "$": "**(deprecated)** Use 'method' in the 'http://csrc.nist.gov/ns/rmf' namespace. The assessment method to use. This typically appears on parts with the name \"assessment-method\".",
                                }
                            ],
                        },
                        {
                            "@target": "part[has-oscal-namespace('http://csrc.nist.gov/ns/oscal') and @name=('assessment','assessment-method')]/prop[has-oscal-namespace('http://csrc.nist.gov/ns/rmf')]/@name",
                            "@level": "ERROR",
                            "@allow-other": "no",
                            "@extensible": "external",
                            "enum": [
                                {
                                    "@value": "method",
                                    "$": 'The assessment method to use. This typically appears on\n                              parts with the name "assessment-method".',
                                }
                            ],
                        },
                        {
                            "@target": "part[has-oscal-namespace('http://csrc.nist.gov/ns/oscal') and @name=('assessment','assessment-method')]/prop[has-oscal-namespace(('http://csrc.nist.gov/ns/oscal','http://csrc.nist.gov/ns/rmf')) and @name='method']/@value",
                            "@level": "ERROR",
                            "@allow-other": "no",
                            "@extensible": "external",
                            "enum": [
                                {
                                    "@value": "INTERVIEW",
                                    "$": "The process of holding discussions with individuals or groups of individuals within an organization to once again, facilitate assessor understanding, achieve clarification, or obtain evidence.",
                                },
                                {
                                    "@value": "EXAMINE",
                                    "$": "The process of reviewing, inspecting, observing, studying, or analyzing one or more assessment objects (i.e., specifications, mechanisms, or activities).",
                                },
                                {
                                    "@value": "TEST",
                                    "$": "The process of exercising one or more assessment objects (i.e., activities or mechanisms) under specified conditions to compare actual with expected behavior.",
                                },
                            ],
                        },
                    ],
                    "index-has-key": {
                        "@name": "catalog-groups-controls-parts",
                        "@target": "link[@rel=('related','required','incorporated-into','moved-to') and starts-with(@href,'#')]",
                        "@level": "ERROR",
                        "key-field": [{"@target": "@href", "@pattern": "#(.*)"}],
                    },
                },
                "remarks": {
                    "p": [
                        {"code": ["control", "part", "group"]},
                        'Control structures in OSCAL will also exhibit regularities and rules that are not codified in OSCAL but in its applications or domains of application. For example, for catalogs describing controls as defined by NIST SP 800-53, a control must have a part with the name "statement", which represents the textual narrative of the control. This "statement" part must occur only once, but may have nested parts to allow for multiple paragraphs or sections of text. This organization supports addressability of this data content as long as, and only insofar as, it is consistently implemented across the control set. As given with these model definitions, constraints defined and assigned here can aid in ensuring this regularity; but other such constraints and other useful patterns of use remain to be discovered and described.',
                    ]
                },
                "example": [
                    {
                        "control": {
                            "@xmlns": "http://csrc.nist.gov/ns/oscal/1.0",
                            "@id": "x",
                            "title": ["Control 1"],
                        }
                    }
                ],
            },
        ],
    },
    "short_name": "oscal-catalog",
    "globals": ["Catalog", "Control Group", "Control"],
    "roots": ["Catalog"],
}
