"""
The schemagen module contains packages for producing pythonic representations of parsed metaschemas.
"""

# TODO: delete this junk below, it's just for reference = this is what a parsed metaschema looks like.

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
    "globals": {"catalog": "Catalog", "group": "Control Group", "control": "Control"},
    "roots": ["Catalog"],
}

metadata = {
    "file": "oscal_metadata_metaschema.xml",
    "schema_dict": {
        "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "@xmlns": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
        "@abstract": "yes",
        "schema-name": "OSCAL Document Metadata Description",
        "schema-version": "1.1.2",
        "short-name": "oscal-metadata",
        "namespace": "http://csrc.nist.gov/ns/oscal/1.0",
        "json-base-uri": "http://csrc.nist.gov/ns/oscal",
        "define-assembly": [
            {
                "@name": "metadata",
                "@scope": "global",
                "formal-name": "Document Metadata",
                "description": "Provides information about the containing document, and defines concepts that are shared across the document.",
                "model": {
                    "define-field": [
                        {
                            "@name": "title",
                            "@as-type": "markup-line",
                            "@min-occurs": 1,
                            "@collapsible": "no",
                            "@max-occurs": 1,
                            "@in-xml": "WRAPPED",
                            "formal-name": "Document Title",
                            "description": "A name given to the document, which may be used by a tool for display and navigation.",
                        }
                    ],
                    "field": [
                        {
                            "@ref": "published",
                            "@min-occurs": 0,
                            "@max-occurs": 1,
                            "@in-xml": "WRAPPED",
                        },
                        {
                            "@ref": "last-modified",
                            "@min-occurs": 1,
                            "@max-occurs": 1,
                            "@in-xml": "WRAPPED",
                        },
                        {
                            "@ref": "version",
                            "@min-occurs": 1,
                            "@max-occurs": 1,
                            "@in-xml": "WRAPPED",
                        },
                        {
                            "@ref": "oscal-version",
                            "@min-occurs": 1,
                            "@max-occurs": 1,
                            "@in-xml": "WRAPPED",
                        },
                        {
                            "@ref": "document-id",
                            "@max-occurs": "unbounded",
                            "@min-occurs": 0,
                            "@in-xml": "WRAPPED",
                            "group-as": {
                                "@name": "document-ids",
                                "@in-json": "ARRAY",
                                "@in-xml": "UNGROUPED",
                            },
                        },
                        {
                            "@ref": "remarks",
                            "@in-xml": "WITH_WRAPPER",
                            "@min-occurs": 0,
                            "@max-occurs": 1,
                        },
                    ],
                    "define-assembly": [
                        {
                            "@name": "revision",
                            "@max-occurs": "unbounded",
                            "@min-occurs": 0,
                            "formal-name": "Revision History Entry",
                            "description": "An entry in a sequential list of revisions to the containing document, expected to be in reverse chronological order (i.e. latest first).",
                            "group-as": {
                                "@name": "revisions",
                                "@in-xml": "GROUPED",
                                "@in-json": "ARRAY",
                            },
                            "model": {
                                "define-field": [
                                    {
                                        "@name": "title",
                                        "@as-type": "markup-line",
                                        "@collapsible": "no",
                                        "@min-occurs": 0,
                                        "@max-occurs": 1,
                                        "@in-xml": "WRAPPED",
                                        "formal-name": "Document Title",
                                        "description": "A name given to the document revision, which may be used by a tool for display and navigation.",
                                    }
                                ],
                                "field": [
                                    {
                                        "@ref": "published",
                                        "@min-occurs": 0,
                                        "@max-occurs": 1,
                                        "@in-xml": "WRAPPED",
                                    },
                                    {
                                        "@ref": "last-modified",
                                        "@min-occurs": 0,
                                        "@max-occurs": 1,
                                        "@in-xml": "WRAPPED",
                                    },
                                    {
                                        "@ref": "version",
                                        "@min-occurs": 1,
                                        "@max-occurs": 1,
                                        "@in-xml": "WRAPPED",
                                    },
                                    {
                                        "@ref": "oscal-version",
                                        "@min-occurs": 0,
                                        "@max-occurs": 1,
                                        "@in-xml": "WRAPPED",
                                    },
                                    {
                                        "@ref": "remarks",
                                        "@in-xml": "WITH_WRAPPER",
                                        "@min-occurs": 0,
                                        "@max-occurs": 1,
                                    },
                                ],
                                "assembly": [
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
                                ],
                            },
                            "constraint": {
                                "allowed-values": {
                                    "@target": "link/@rel",
                                    "@allow-other": "yes",
                                    "@level": "ERROR",
                                    "@extensible": "external",
                                    "enum": [
                                        {
                                            "@value": "canonical",
                                            "a": [
                                                {
                                                    "@href": "https://tools.ietf.org/html/rfc6596",
                                                    "$": "RFC 6596",
                                                }
                                            ],
                                        },
                                        {
                                            "@value": "alternate",
                                            "a": [
                                                {
                                                    "@href": "https://html.spec.whatwg.org/multipage/links.html#linkTypes",
                                                    "$": "the HTML Living Standard",
                                                }
                                            ],
                                        },
                                        {
                                            "@value": "predecessor-version",
                                            "a": [
                                                {
                                                    "@href": "https://tools.ietf.org/html/rfc5829",
                                                    "$": "RFC 5829",
                                                }
                                            ],
                                        },
                                        {
                                            "@value": "successor-version",
                                            "a": [
                                                {
                                                    "@href": "https://tools.ietf.org/html/rfc5829",
                                                    "$": "RFC 5829",
                                                }
                                            ],
                                        },
                                        {
                                            "@value": "version-history",
                                            "a": [
                                                {
                                                    "@href": "https://tools.ietf.org/html/rfc5829",
                                                    "$": "RFC 5829",
                                                }
                                            ],
                                        },
                                    ],
                                }
                            },
                            "remarks": {
                                "p": [
                                    {
                                        "code": [
                                            "published",
                                            "last-modified",
                                            "oscal-version",
                                            "link",
                                            "rel",
                                        ],
                                        "q": ["source"],
                                    }
                                ]
                            },
                        },
                        {
                            "@name": "role",
                            "@max-occurs": "unbounded",
                            "@min-occurs": 0,
                            "formal-name": "Role",
                            "description": "Defines a function, which might be assigned to a party in a specific situation.",
                            "group-as": {
                                "@name": "roles",
                                "@in-json": "ARRAY",
                                "@in-xml": "UNGROUPED",
                            },
                            "define-flag": [
                                {
                                    "@name": "id",
                                    "@as-type": "token",
                                    "@required": "yes",
                                    "formal-name": "Role Identifier",
                                    "description": "A unique identifier for the role.",
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
                                }
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
                                        "formal-name": "Role Title",
                                        "description": "A name given to the role, which may be used by a tool for display and navigation.",
                                    },
                                    {
                                        "@name": "short-name",
                                        "@as-type": "string",
                                        "@collapsible": "no",
                                        "@min-occurs": 0,
                                        "@max-occurs": 1,
                                        "@in-xml": "WRAPPED",
                                        "formal-name": "Role Short Name",
                                        "description": "A short common name, abbreviation, or acronym for the role.",
                                    },
                                    {
                                        "@name": "description",
                                        "@in-xml": "WITH_WRAPPER",
                                        "@as-type": "markup-multiline",
                                        "@collapsible": "no",
                                        "@min-occurs": 0,
                                        "@max-occurs": 1,
                                        "formal-name": "Role Description",
                                        "description": "A summary of the role's purpose and associated responsibilities.",
                                    },
                                ],
                                "assembly": [
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
                                ],
                                "field": [
                                    {
                                        "@ref": "remarks",
                                        "@in-xml": "WITH_WRAPPER",
                                        "@min-occurs": 0,
                                        "@max-occurs": 1,
                                    }
                                ],
                            },
                            "remarks": {
                                "p": [
                                    "Permissible values to be determined closer to the application (e.g. by a receiving authority).",
                                    "OSCAL has defined a set of standardized roles for consistent use in OSCAL documents. This allows tools consuming OSCAL content to infer specific semantics when these roles are used. These roles are documented in the specific contexts of their use (e.g., responsible-party, responsible-role). When using such a role, it is necessary to define these roles in this list, which will then allow such a role to be referenced.",
                                ]
                            },
                        },
                        {
                            "@name": "location",
                            "@max-occurs": "unbounded",
                            "@min-occurs": 0,
                            "formal-name": "Location",
                            "description": "A physical point of presence, which may be associated with people, organizations, or other concepts within the current or linked OSCAL document.",
                            "group-as": {
                                "@name": "locations",
                                "@in-json": "ARRAY",
                                "@in-xml": "UNGROUPED",
                            },
                            "define-flag": [
                                {
                                    "@name": "uuid",
                                    "@as-type": "uuid",
                                    "@required": "yes",
                                    "formal-name": "Location Universally Unique Identifier",
                                    "description": "A unique ID for the location, for reference.",
                                }
                            ],
                            "model": {
                                "define-field": [
                                    {
                                        "@name": "title",
                                        "@as-type": "markup-line",
                                        "@collapsible": "no",
                                        "@min-occurs": 0,
                                        "@max-occurs": 1,
                                        "@in-xml": "WRAPPED",
                                        "formal-name": "Location Title",
                                        "description": "A name given to the location, which may be used by a tool for display and navigation.",
                                    },
                                    {
                                        "@name": "url",
                                        "@as-type": "uri",
                                        "@max-occurs": "unbounded",
                                        "@deprecated": "1.1.0",
                                        "@collapsible": "no",
                                        "@min-occurs": 0,
                                        "@in-xml": "WRAPPED",
                                        "formal-name": "Location URL",
                                        "description": "The uniform resource locator (URL) for a web site or other resource associated with the location.",
                                        "group-as": {
                                            "@name": "urls",
                                            "@in-json": "ARRAY",
                                            "@in-xml": "UNGROUPED",
                                        },
                                        "remarks": {
                                            "p": [
                                                "This data field is deprecated in favor of using a link with an appropriate relationship."
                                            ]
                                        },
                                    },
                                ],
                                "assembly": [
                                    {
                                        "@ref": "address",
                                        "@min-occurs": 0,
                                        "@max-occurs": 1,
                                        "remarks": {
                                            "p": [
                                                "The physical address of the location, which will provided for physical locations. Virtual locations can omit this data item."
                                            ]
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
                                ],
                                "field": [
                                    {
                                        "@ref": "email-address",
                                        "@max-occurs": "unbounded",
                                        "@min-occurs": 0,
                                        "@in-xml": "WRAPPED",
                                        "group-as": {
                                            "@name": "email-addresses",
                                            "@in-json": "ARRAY",
                                            "@in-xml": "UNGROUPED",
                                        },
                                        "remarks": {
                                            "p": [
                                                "A contact email associated with the location."
                                            ]
                                        },
                                    },
                                    {
                                        "@ref": "telephone-number",
                                        "@max-occurs": "unbounded",
                                        "@min-occurs": 0,
                                        "@in-xml": "WRAPPED",
                                        "group-as": {
                                            "@name": "telephone-numbers",
                                            "@in-json": "ARRAY",
                                            "@in-xml": "UNGROUPED",
                                        },
                                        "remarks": {
                                            "p": [
                                                "A phone number used to contact the location."
                                            ]
                                        },
                                    },
                                    {
                                        "@ref": "remarks",
                                        "@in-xml": "WITH_WRAPPER",
                                        "@min-occurs": 0,
                                        "@max-occurs": 1,
                                    },
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
                                                "@value": "type",
                                                "$": "Characterizes the kind of location.",
                                            }
                                        ],
                                    },
                                    {
                                        "@target": "prop[has-oscal-namespace('http://csrc.nist.gov/ns/oscal') and @name='type']/@value",
                                        "@level": "ERROR",
                                        "@allow-other": "no",
                                        "@extensible": "external",
                                        "enum": [
                                            {
                                                "@value": "data-center",
                                                "code": ["class"],
                                                "em": ["primary", "alternate"],
                                            }
                                        ],
                                    },
                                    {
                                        "@target": "prop[has-oscal-namespace('http://csrc.nist.gov/ns/oscal') and @name='type' and @value='data-center']/@class",
                                        "@level": "ERROR",
                                        "@allow-other": "no",
                                        "@extensible": "external",
                                        "enum": [
                                            {
                                                "@value": "primary",
                                                "$": "The location is a data-center used for normal operations.",
                                            },
                                            {
                                                "@value": "alternate",
                                                "$": "The location is a data-center used for fail-over or backup operations.",
                                            },
                                        ],
                                    },
                                ],
                                "has-cardinality": [
                                    {
                                        "@target": "address",
                                        "@level": "WARNING",
                                        "@min-occurs": 1,
                                        "description": "In most cases, it is useful to define a location. In some cases, defining an explicit location may represent a security risk.",
                                    },
                                    {
                                        "@target": "title|address|email-address|telephone-number",
                                        "@level": "ERROR",
                                        "@min-occurs": 1,
                                        "description": "A location must have at least a title, address, email-address, or telephone number.",
                                    },
                                ],
                            },
                            "remarks": {
                                "p": [
                                    "An address might be sensitive in nature. In such cases a title, mailing address, email-address, and/or phone number may be used instead."
                                ]
                            },
                        },
                        {
                            "@name": "party",
                            "@max-occurs": "unbounded",
                            "@min-occurs": 0,
                            "formal-name": "Party",
                            "description": "An organization or person, which may be associated with roles or other concepts within the current or linked OSCAL document.",
                            "group-as": {
                                "@name": "parties",
                                "@in-json": "ARRAY",
                                "@in-xml": "UNGROUPED",
                            },
                            "define-flag": [
                                {
                                    "@name": "uuid",
                                    "@as-type": "uuid",
                                    "@required": "yes",
                                    "formal-name": "Party Universally Unique Identifier",
                                    "description": "A unique identifier for the party.",
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
                                    "@name": "type",
                                    "@as-type": "string",
                                    "@required": "yes",
                                    "formal-name": "Party Type",
                                    "description": "A category describing the kind of party the object describes.",
                                    "constraint": {
                                        "allowed-values": [
                                            {
                                                "@level": "ERROR",
                                                "@allow-other": "no",
                                                "@extensible": "external",
                                                "enum": [
                                                    {
                                                        "@value": "person",
                                                        "$": "A human being regarded as an individual.",
                                                    },
                                                    {
                                                        "@value": "organization",
                                                        "code": ["person"],
                                                    },
                                                ],
                                            }
                                        ]
                                    },
                                },
                            ],
                            "model": {
                                "define-field": [
                                    {
                                        "@name": "name",
                                        "@as-type": "string",
                                        "@collapsible": "no",
                                        "@min-occurs": 0,
                                        "@max-occurs": 1,
                                        "@in-xml": "WRAPPED",
                                        "formal-name": "Party Name",
                                        "description": "The full name of the party. This is typically the legal name associated with the party.",
                                    },
                                    {
                                        "@name": "short-name",
                                        "@as-type": "string",
                                        "@collapsible": "no",
                                        "@min-occurs": 0,
                                        "@max-occurs": 1,
                                        "@in-xml": "WRAPPED",
                                        "formal-name": "Party Short Name",
                                        "description": "A short common name, abbreviation, or acronym for the party.",
                                    },
                                    {
                                        "@name": "external-id",
                                        "@max-occurs": "unbounded",
                                        "@as-type": "string",
                                        "@collapsible": "no",
                                        "@min-occurs": 0,
                                        "@in-xml": "WRAPPED",
                                        "formal-name": "Party External Identifier",
                                        "description": "An identifier for a person or organization using a designated\n                            scheme. e.g. an Open Researcher and Contributor ID\n                            (ORCID).",
                                        "json-value-key": "id",
                                        "group-as": {
                                            "@name": "external-ids",
                                            "@in-json": "ARRAY",
                                            "@in-xml": "UNGROUPED",
                                        },
                                        "define-flag": [
                                            {
                                                "@name": "scheme",
                                                "@as-type": "uri",
                                                "@required": "yes",
                                                "formal-name": "External Identifier Schema",
                                                "description": "Indicates the type of external identifier.",
                                                "constraint": {
                                                    "allowed-values": [
                                                        {
                                                            "@allow-other": "yes",
                                                            "@level": "ERROR",
                                                            "@extensible": "external",
                                                            "enum": [
                                                                {
                                                                    "@value": "http://orcid.org/",
                                                                    "$": "The identifier is Open Researcher and Contributor ID (ORCID).",
                                                                }
                                                            ],
                                                        }
                                                    ]
                                                },
                                                "remarks": {
                                                    "p": [
                                                        {
                                                            "a": [
                                                                {
                                                                    "@href": "https://pages.nist.gov/OSCAL/concepts/uri-use/#absolute-uri",
                                                                    "$": "absolute URI",
                                                                },
                                                                {
                                                                    "@href": "https://pages.nist.gov/OSCAL/concepts/uri-use/#use-as-a-naming-system-identifier",
                                                                    "$": "naming system identifier",
                                                                },
                                                            ]
                                                        }
                                                    ]
                                                },
                                            }
                                        ],
                                    },
                                    {
                                        "@name": "member-of-organization",
                                        "@as-type": "uuid",
                                        "@max-occurs": "unbounded",
                                        "@collapsible": "no",
                                        "@min-occurs": 0,
                                        "@in-xml": "WRAPPED",
                                        "formal-name": "Organizational Affiliation",
                                        "description": {"code": ["party"]},
                                        "prop": [
                                            {
                                                "@name": "value-type",
                                                "@value": "identifier-reference",
                                                "@namespace": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
                                            },
                                            {
                                                "@name": "identifier-type",
                                                "@value": "machine-oriented",
                                                "@namespace": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
                                            },
                                            {
                                                "@name": "identifier-scope",
                                                "@value": "cross-instance",
                                                "@namespace": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
                                            },
                                        ],
                                        "group-as": {
                                            "@name": "member-of-organizations",
                                            "@in-json": "ARRAY",
                                            "@in-xml": "UNGROUPED",
                                        },
                                        "constraint": {
                                            "index-has-key": {
                                                "@name": "index-metadata-party-organizations-uuid",
                                                "@target": ".",
                                                "@level": "ERROR",
                                                "key-field": [{"@target": "."}],
                                            }
                                        },
                                        "remarks": {
                                            "p": [
                                                {
                                                    "code": ["party", "uuid", "uuid"],
                                                    "a": [
                                                        {
                                                            "@href": "https://pages.nist.gov/OSCAL/concepts/identifier-use/#machine-oriented",
                                                            "$": "machine-oriented",
                                                        }
                                                    ],
                                                },
                                                {
                                                    "code": [
                                                        "person",
                                                        "organization",
                                                        "member-of-organization",
                                                    ]
                                                },
                                            ]
                                        },
                                    },
                                ],
                                "assembly": [
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
                                ],
                                "field": [
                                    {
                                        "@ref": "email-address",
                                        "@max-occurs": "unbounded",
                                        "@min-occurs": 0,
                                        "@in-xml": "WRAPPED",
                                        "group-as": {
                                            "@name": "email-addresses",
                                            "@in-json": "ARRAY",
                                            "@in-xml": "UNGROUPED",
                                        },
                                        "remarks": {
                                            "p": [
                                                "This is a contact email associated with the party."
                                            ]
                                        },
                                    },
                                    {
                                        "@ref": "telephone-number",
                                        "@max-occurs": "unbounded",
                                        "@min-occurs": 0,
                                        "@in-xml": "WRAPPED",
                                        "group-as": {
                                            "@name": "telephone-numbers",
                                            "@in-json": "ARRAY",
                                            "@in-xml": "UNGROUPED",
                                        },
                                        "remarks": {
                                            "p": [
                                                "A phone number used to contact the party."
                                            ]
                                        },
                                    },
                                    {
                                        "@ref": "remarks",
                                        "@in-xml": "WITH_WRAPPER",
                                        "@min-occurs": 0,
                                        "@max-occurs": 1,
                                    },
                                ],
                                "choice": [
                                    {
                                        "assembly": [
                                            {
                                                "@ref": "address",
                                                "@max-occurs": "unbounded",
                                                "@min-occurs": 0,
                                                "group-as": {
                                                    "@name": "addresses",
                                                    "@in-json": "ARRAY",
                                                    "@in-xml": "UNGROUPED",
                                                },
                                            }
                                        ],
                                        "field": [
                                            {
                                                "@ref": "location-uuid",
                                                "@max-occurs": "unbounded",
                                                "@min-occurs": 0,
                                                "@in-xml": "WRAPPED",
                                                "group-as": {
                                                    "@name": "location-uuids",
                                                    "@in-json": "ARRAY",
                                                    "@in-xml": "UNGROUPED",
                                                },
                                            }
                                        ],
                                    }
                                ],
                            },
                            "constraint": {
                                "allowed-values": {
                                    "@target": "prop[has-oscal-namespace('http://csrc.nist.gov/ns/oscal')]/@name",
                                    "@level": "ERROR",
                                    "@allow-other": "no",
                                    "@extensible": "external",
                                    "enum": [
                                        {
                                            "@value": "mail-stop",
                                            "$": "A mail stop associated with the party.",
                                        },
                                        {
                                            "@value": "office",
                                            "$": "The name or number of the party's office.",
                                        },
                                        {
                                            "@value": "job-title",
                                            "$": "The formal job title of a person.",
                                        },
                                    ],
                                }
                            },
                            "remarks": {
                                "p": [
                                    "A party can be optionally associated with either an address or a location. While providing a meaningful location for a party is desired, there are some cases where it might not be possible to provide an exact location or even any location."
                                ]
                            },
                        },
                    ],
                    "assembly": [
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
                            "@ref": "responsible-party",
                            "@max-occurs": "unbounded",
                            "@min-occurs": 0,
                            "group-as": {
                                "@name": "responsible-parties",
                                "@in-json": "ARRAY",
                                "@in-xml": "UNGROUPED",
                            },
                        },
                        {
                            "@ref": "action",
                            "@max-occurs": "unbounded",
                            "@min-occurs": 0,
                            "group-as": {
                                "@name": "actions",
                                "@in-json": "ARRAY",
                                "@in-xml": "UNGROUPED",
                            },
                        },
                    ],
                },
                "constraint": {
                    "index": [
                        {
                            "@id": "index-metadata-roles",
                            "@name": "index-metadata-role-ids",
                            "@target": "role",
                            "@level": "ERROR",
                            "key-field": [{"@target": "@id"}],
                        },
                        {
                            "@id": "index-metadata-property-uuid",
                            "@name": "index-metadata-property-uuid",
                            "@target": ".//prop",
                            "@level": "ERROR",
                            "key-field": [{"@target": "@uuid"}],
                        },
                        {
                            "@id": "index-metadata-role-id",
                            "@name": "index-metadata-role-id",
                            "@target": "role",
                            "@level": "ERROR",
                            "key-field": [{"@target": "@id"}],
                        },
                        {
                            "@id": "index-metadata-location-uuid",
                            "@name": "index-metadata-location-uuid",
                            "@target": "location",
                            "@level": "ERROR",
                            "key-field": [{"@target": "@uuid"}],
                        },
                        {
                            "@id": "index-metadata-party-uuid",
                            "@name": "index-metadata-party-uuid",
                            "@target": "party",
                            "@level": "ERROR",
                            "key-field": [{"@target": "@uuid"}],
                        },
                        {
                            "@id": "index-metadata-party-organizations-uuid",
                            "@name": "index-metadata-party-organizations-uuid",
                            "@target": "party[@type='organization']",
                            "@level": "ERROR",
                            "key-field": [{"@target": "@uuid"}],
                        },
                    ],
                    "is-unique": [
                        {
                            "@id": "unique-metadata-doc-id",
                            "@target": "document-id",
                            "@level": "ERROR",
                            "key-field": [{"@target": "@scheme"}, {"@target": "."}],
                        },
                        {
                            "@id": "unique-metadata-property",
                            "@target": "prop",
                            "@level": "ERROR",
                            "key-field": [
                                {"@target": "@name"},
                                {"@target": "@ns"},
                                {"@target": "@class"},
                                {"@target": "@group"},
                                {"@target": "@value"},
                            ],
                        },
                        {
                            "@id": "unique-metadata-link",
                            "@target": "link",
                            "@level": "ERROR",
                            "key-field": [
                                {"@target": "@href"},
                                {"@target": "@rel"},
                                {"@target": "@media-type"},
                            ],
                        },
                        {
                            "@id": "unique-metadata-responsible-party",
                            "@target": "responsible-party",
                            "@level": "ERROR",
                            "key-field": [{"@target": "@role-id"}],
                            "remarks": {
                                "p": [
                                    {
                                        "code": [
                                            "responsible-party",
                                            "party-uuid",
                                            "role-id",
                                        ]
                                    }
                                ]
                            },
                        },
                        {
                            "@target": "document-id",
                            "@level": "ERROR",
                            "key-field": [{"@target": "@scheme"}, {"@target": "."}],
                            "remarks": {"p": [{"code": ["scheme"]}]},
                        },
                    ],
                    "allowed-values": [
                        {
                            "@id": "allowed-metadata-responsibe-party-role-ids",
                            "@target": "responsible-party/@role-id",
                            "@allow-other": "yes",
                            "@level": "ERROR",
                            "@extensible": "external",
                            "enum": [
                                {
                                    "@value": "creator",
                                    "$": "Indicates the person or organization that created this content.",
                                },
                                {
                                    "@value": "prepared-by",
                                    "$": "Indicates the person or organization that prepared this content.",
                                },
                                {
                                    "@value": "prepared-for",
                                    "$": "Indicates the person or organization for which this content was created.",
                                },
                                {
                                    "@value": "content-approver",
                                    "$": 'Indicates the person or organization responsible for all content represented in the "document".',
                                },
                                {
                                    "@value": "contact",
                                    "$": "Indicates the person or organization to contact for questions or support related to this content.",
                                },
                            ],
                        },
                        {
                            "@target": "prop[has-oscal-namespace('http://csrc.nist.gov/ns/oscal')]/@name",
                            "@level": "ERROR",
                            "@allow-other": "no",
                            "@extensible": "external",
                            "enum": [
                                {
                                    "@value": "keywords",
                                    "$": "The value identifies a comma-seperated listing of keywords associated with this content. These keywords may be used as search terms for indexing and other applications.",
                                }
                            ],
                        },
                        {
                            "@target": "link/@rel",
                            "@allow-other": "yes",
                            "@level": "ERROR",
                            "@extensible": "external",
                            "enum": [
                                {
                                    "@value": "canonical",
                                    "a": [
                                        {
                                            "@href": "https://tools.ietf.org/html/rfc6596",
                                            "$": "RFC 6596",
                                        }
                                    ],
                                },
                                {
                                    "@value": "alternate",
                                    "a": [
                                        {
                                            "@href": "https://html.spec.whatwg.org/multipage/links.html#linkTypes",
                                            "$": "the HTML Living Standard",
                                        }
                                    ],
                                },
                                {
                                    "@value": "latest-version",
                                    "a": [
                                        {
                                            "@href": "https://tools.ietf.org/html/rfc5829",
                                            "$": "RFC 5829",
                                        }
                                    ],
                                },
                                {
                                    "@value": "predecessor-version",
                                    "a": [
                                        {
                                            "@href": "https://tools.ietf.org/html/rfc5829",
                                            "$": "RFC 5829",
                                        }
                                    ],
                                },
                                {
                                    "@value": "successor-version",
                                    "a": [
                                        {
                                            "@href": "https://tools.ietf.org/html/rfc5829",
                                            "$": "RFC 5829",
                                        }
                                    ],
                                },
                            ],
                        },
                    ],
                },
                "remarks": {
                    "p": [
                        "All OSCAL documents use the same metadata structure, that provides a consistent way of expressing OSCAL document metadata across all OSCAL models. The metadata section also includes declarations of individual objects (i.e., roles, location, parties) that may be referenced within and across linked OSCAL documents.",
                        "The metadata in an OSCAL document has few required fields, representing only the bare minimum data needed to differentiate one instance from another. Tools and users creating OSCAL documents may choose to use any of the optional fields, as well as extension mechanisms (e.g., properties, links) to go beyond this minimum to suit their use cases.",
                        {
                            "code": [
                                "published",
                                "last-modified",
                                "version",
                                "revision",
                                "predecessor-version",
                                "successor-version",
                                "link",
                                "revision",
                            ]
                        },
                        {"code": ["responsible-party"]},
                    ]
                },
            },
            {
                "@name": "back-matter",
                "@scope": "global",
                "formal-name": "Back matter",
                "description": "A collection of resources that may be referenced from within the OSCAL document instance.",
                "model": {
                    "define-assembly": [
                        {
                            "@name": "resource",
                            "@max-occurs": "unbounded",
                            "@min-occurs": 0,
                            "formal-name": "Resource",
                            "description": "A resource associated with content in the containing document instance. A resource may be directly included in the document using base64 encoding or may point to one or more equivalent internet resources.",
                            "group-as": {
                                "@name": "resources",
                                "@in-json": "ARRAY",
                                "@in-xml": "UNGROUPED",
                            },
                            "define-flag": [
                                {
                                    "@name": "uuid",
                                    "@as-type": "uuid",
                                    "@required": "yes",
                                    "formal-name": "Resource Universally Unique Identifier",
                                    "description": "A unique identifier for a resource.",
                                }
                            ],
                            "model": {
                                "define-field": [
                                    {
                                        "@name": "title",
                                        "@as-type": "markup-line",
                                        "@collapsible": "no",
                                        "@min-occurs": 0,
                                        "@max-occurs": 1,
                                        "@in-xml": "WRAPPED",
                                        "formal-name": "Resource Title",
                                        "description": "An optional name given to the resource, which may be used by a tool for display and navigation.",
                                    },
                                    {
                                        "@name": "description",
                                        "@in-xml": "WITH_WRAPPER",
                                        "@as-type": "markup-multiline",
                                        "@collapsible": "no",
                                        "@min-occurs": 0,
                                        "@max-occurs": 1,
                                        "formal-name": "Resource Description",
                                        "description": "An optional short summary of the resource used to indicate the purpose of the resource.",
                                    },
                                    {
                                        "@name": "base64",
                                        "@as-type": "base64",
                                        "@collapsible": "no",
                                        "@min-occurs": 0,
                                        "@max-occurs": 1,
                                        "@in-xml": "WRAPPED",
                                        "formal-name": "Base64",
                                        "description": {
                                            "a": [
                                                {
                                                    "@href": "https://www.rfc-editor.org/rfc/rfc2045.html",
                                                    "$": "RFC 2045",
                                                }
                                            ]
                                        },
                                        "json-value-key": "value",
                                        "define-flag": [
                                            {
                                                "@name": "filename",
                                                "@as-type": "token",
                                                "@required": "no",
                                                "formal-name": "File Name",
                                                "description": {"code": ["resource"]},
                                            }
                                        ],
                                        "flag": [
                                            {"@ref": "media-type", "@required": "no"}
                                        ],
                                    },
                                ],
                                "assembly": [
                                    {
                                        "@ref": "property",
                                        "@max-occurs": "unbounded",
                                        "@min-occurs": 0,
                                        "group-as": {
                                            "@name": "props",
                                            "@in-json": "ARRAY",
                                            "@in-xml": "UNGROUPED",
                                        },
                                    }
                                ],
                                "field": [
                                    {
                                        "@ref": "document-id",
                                        "@max-occurs": "unbounded",
                                        "@min-occurs": 0,
                                        "@in-xml": "WRAPPED",
                                        "group-as": {
                                            "@name": "document-ids",
                                            "@in-json": "ARRAY",
                                            "@in-xml": "UNGROUPED",
                                        },
                                    },
                                    {
                                        "@ref": "remarks",
                                        "@in-xml": "WITH_WRAPPER",
                                        "@min-occurs": 0,
                                        "@max-occurs": 1,
                                    },
                                ],
                                "define-assembly": [
                                    {
                                        "@name": "citation",
                                        "@min-occurs": 0,
                                        "@max-occurs": 1,
                                        "formal-name": "Citation",
                                        "description": "An optional citation consisting of end note text using structured markup.",
                                        "model": {
                                            "define-field": [
                                                {
                                                    "@name": "text",
                                                    "@as-type": "markup-line",
                                                    "@min-occurs": 1,
                                                    "@collapsible": "no",
                                                    "@max-occurs": 1,
                                                    "@in-xml": "WRAPPED",
                                                    "formal-name": "Citation Text",
                                                    "description": "A line of citation text.",
                                                }
                                            ],
                                            "assembly": [
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
                                            ],
                                        },
                                    },
                                    {
                                        "@name": "rlink",
                                        "@max-occurs": "unbounded",
                                        "@min-occurs": 0,
                                        "formal-name": "Resource link",
                                        "description": "A URL-based pointer to an external resource with an optional hash for verification and change detection.",
                                        "group-as": {
                                            "@name": "rlinks",
                                            "@in-json": "ARRAY",
                                            "@in-xml": "UNGROUPED",
                                        },
                                        "define-flag": [
                                            {
                                                "@name": "href",
                                                "@as-type": "uri-reference",
                                                "@required": "yes",
                                                "formal-name": "Hypertext Reference",
                                                "description": "A resolvable URL pointing to the referenced resource.",
                                                "remarks": {
                                                    "p": ["This value may be either:"],
                                                    "ol": [
                                                        {
                                                            "li": [
                                                                {
                                                                    "a": [
                                                                        {
                                                                            "@href": "https://pages.nist.gov/OSCAL/concepts/uri-use/#absolute-uri",
                                                                            "$": "absolute URI",
                                                                        }
                                                                    ]
                                                                },
                                                                {
                                                                    "a": [
                                                                        {
                                                                            "@href": "https://pages.nist.gov/OSCAL/concepts/uri-use/#relative-reference",
                                                                            "$": "relative reference",
                                                                        }
                                                                    ]
                                                                },
                                                            ]
                                                        }
                                                    ],
                                                },
                                            }
                                        ],
                                        "flag": [
                                            {"@ref": "media-type", "@required": "no"}
                                        ],
                                        "model": {
                                            "field": [
                                                {
                                                    "@ref": "hash",
                                                    "@max-occurs": "unbounded",
                                                    "@min-occurs": 0,
                                                    "@in-xml": "WRAPPED",
                                                    "description": {"code": ["href"]},
                                                    "group-as": {
                                                        "@name": "hashes",
                                                        "@in-json": "ARRAY",
                                                        "@in-xml": "UNGROUPED",
                                                    },
                                                    "remarks": {
                                                        "p": [
                                                            {"code": ["hash", "href"]}
                                                        ]
                                                    },
                                                }
                                            ]
                                        },
                                        "remarks": {
                                            "p": [
                                                {"code": ["rlink", "rlink"]},
                                                {
                                                    "code": [
                                                        "media-type",
                                                        "media-type",
                                                        "rlink",
                                                    ]
                                                },
                                            ]
                                        },
                                    },
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
                                                "@value": "type",
                                                "$": "Identifies the type of resource represented. The most specific appropriate type value SHOULD be used.",
                                            },
                                            {
                                                "@value": "version",
                                                "$": "For resources representing a published document, this represents the version number of that document.",
                                            },
                                            {
                                                "@value": "published",
                                                "$": "For resources representing a published document, this represents the publication date of that document.",
                                            },
                                        ],
                                    },
                                    {
                                        "@target": "prop[has-oscal-namespace('http://csrc.nist.gov/ns/oscal') and @name='type']/@value",
                                        "@level": "ERROR",
                                        "@allow-other": "no",
                                        "@extensible": "external",
                                        "enum": [
                                            {
                                                "@value": "logo",
                                                "$": "Indicates the resource is an organization's logo.",
                                            },
                                            {
                                                "@value": "image",
                                                "$": "Indicates the resource represents an image.",
                                            },
                                            {
                                                "@value": "screen-shot",
                                                "$": "Indicates the resource represents an image of screen content.",
                                            },
                                            {
                                                "@value": "law",
                                                "$": "Indicates the resource represents an applicable law.",
                                            },
                                            {
                                                "@value": "regulation",
                                                "$": "Indicates the resource represents an applicable regulation.",
                                            },
                                            {
                                                "@value": "standard",
                                                "$": "Indicates the resource represents an applicable standard.",
                                            },
                                            {
                                                "@value": "external-guidance",
                                                "$": "Indicates the resource represents applicable guidance.",
                                            },
                                            {
                                                "@value": "acronyms",
                                                "$": "Indicates the resource provides a list of relevant acronyms.",
                                            },
                                            {
                                                "@value": "citation",
                                                "$": "Indicates the resource cites relevant information.",
                                            },
                                            {
                                                "@value": "policy",
                                                "$": "Indicates the resource is a policy.",
                                            },
                                            {
                                                "@value": "procedure",
                                                "$": "Indicates the resource is a procedure.",
                                            },
                                            {
                                                "@value": "system-guide",
                                                "$": "Indicates the resource is guidance document related to the subject system of an SSP.",
                                            },
                                            {
                                                "@value": "users-guide",
                                                "$": "Indicates the resource is guidance document a user's guide or administrator's guide.",
                                            },
                                            {
                                                "@value": "administrators-guide",
                                                "$": "Indicates the resource is guidance document a administrator's guide.",
                                            },
                                            {
                                                "@value": "rules-of-behavior",
                                                "$": "Indicates the resource represents rules of behavior content.",
                                            },
                                            {
                                                "@value": "plan",
                                                "$": "Indicates the resource represents a plan.",
                                            },
                                            {
                                                "@value": "artifact",
                                                "$": "Indicates the resource represents an artifact, such as may be reviewed by an assessor.",
                                            },
                                            {
                                                "@value": "evidence",
                                                "$": "Indicates the resource represents evidence, such as to support an assessment finding.",
                                            },
                                            {
                                                "@value": "tool-output",
                                                "$": "Indicates the resource represents output from a tool.",
                                            },
                                            {
                                                "@value": "raw-data",
                                                "$": "Indicates the resource represents machine data, which may require a tool or analysis for interpretation or presentation.",
                                            },
                                            {
                                                "@value": "interview-notes",
                                                "$": "Indicates the resource represents notes from an interview, such as may be collected during an assessment.",
                                            },
                                            {
                                                "@value": "questionnaire",
                                                "$": "Indicates the resource is a set of questions, possibly with responses.",
                                            },
                                            {
                                                "@value": "report",
                                                "$": "Indicates the resource is a report.",
                                            },
                                            {
                                                "@value": "agreement",
                                                "$": "Indicates the resource is a formal agreement between two or more parties.",
                                            },
                                        ],
                                    },
                                ],
                                "matches": {
                                    "@target": "prop[has-oscal-namespace('http://csrc.nist.gov/ns/oscal') and @name='published']/@value",
                                    "@datatype": "date-time-with-timezone",
                                    "@level": "ERROR",
                                },
                                "has-cardinality": {
                                    "@level": "WARNING",
                                    "@target": "rlink|base64",
                                    "@min-occurs": 1,
                                    "description": {"code": ["rlink", "base64"]},
                                },
                                "is-unique": [
                                    {
                                        "@id": "unique-resource-rlink-href",
                                        "@target": "rlink",
                                        "@level": "ERROR",
                                        "description": "Ensure that each rlink item references a unique resource.",
                                        "key-field": [
                                            {"@target": "@href"},
                                            {"@target": "@media-type"},
                                        ],
                                    },
                                    {
                                        "@id": "unique-resource-base64-filename",
                                        "@target": "base64",
                                        "@level": "ERROR",
                                        "description": {"code": ["filename"]},
                                        "key-field": [{"@target": "@filename"}],
                                    },
                                ],
                                "expect": {
                                    "@target": ".[citation]",
                                    "@test": "title",
                                    "@level": "ERROR",
                                    "description": {"code": ["title", "citation"]},
                                },
                            },
                            "remarks": {
                                "p": [
                                    {"code": ["rlink", "base64", "rlink", "base64"]},
                                    {
                                        "code": [
                                            "media-type",
                                            "rlink",
                                            "base64",
                                            "media-type",
                                        ]
                                    },
                                    {"code": ["title", "citation"]},
                                ]
                            },
                        }
                    ]
                },
                "constraint": {
                    "index": {
                        "@name": "index-back-matter-resource",
                        "@target": "resource",
                        "@level": "ERROR",
                        "key-field": [{"@target": "@uuid"}],
                    }
                },
                "remarks": {
                    "p": [{"code": ["resource", "link", "rel", "href", "uuid"]}]
                },
                "example": [
                    {
                        "description": "Use of link, citation, and resource",
                        "remarks": {
                            "p": [
                                "The following is a contrived example to show the use of link, citation, and resource."
                            ]
                        },
                        "o:profile": {
                            "@xmlns:o": "http://csrc.nist.gov/ns/oscal/example",
                            "o:metadata": [
                                {
                                    "o:link": [
                                        {
                                            "@rel": "citation",
                                            "@href": "#a53da8f9-4182-4f11-9d1f-50f08ac2117b",
                                            "$": "My citation",
                                        }
                                    ]
                                }
                            ],
                            "o:back-matter": [
                                {
                                    "o:resource": [
                                        {
                                            "@uuid": "a53da8f9-4182-4f11-9d1f-50f08ac2117b",
                                            "o:rlink": [
                                                {
                                                    "@href": "https://example.org/some-resource"
                                                }
                                            ],
                                        }
                                    ]
                                }
                            ],
                        },
                    }
                ],
            },
            {
                "@name": "property",
                "@scope": "global",
                "formal-name": "Property",
                "description": "An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair.",
                "use-name": "prop",
                "define-flag": [
                    {
                        "@name": "name",
                        "@as-type": "token",
                        "@required": "yes",
                        "formal-name": "Property Name",
                        "description": "A textual label, within a namespace, that uniquely identifies a specific attribute, characteristic, or quality of the property's containing object.",
                    },
                    {
                        "@name": "uuid",
                        "@as-type": "uuid",
                        "@required": "no",
                        "formal-name": "Property Universally Unique Identifier",
                        "description": "A unique identifier for a property.",
                    },
                    {
                        "@name": "ns",
                        "@as-type": "uri",
                        "@default": "http://csrc.nist.gov/ns/oscal",
                        "@required": "no",
                        "formal-name": "Property Namespace",
                        "description": "A namespace qualifying the property's name. This allows different organizations to associate distinct semantics with the same name.",
                        "remarks": {
                            "p": [
                                {
                                    "a": [
                                        {
                                            "@href": "https://pages.nist.gov/OSCAL/concepts/uri-use/#absolute-uri",
                                            "$": "absolute URI",
                                        },
                                        {
                                            "@href": "https://pages.nist.gov/OSCAL/concepts/uri-use/#use-as-a-naming-system-identifier",
                                            "$": "naming system identifier",
                                        },
                                    ]
                                },
                                {"code": ["ns", "http://csrc.nist.gov/ns/oscal"]},
                            ]
                        },
                    },
                    {
                        "@name": "value",
                        "@as-type": "string",
                        "@required": "yes",
                        "formal-name": "Property Value",
                        "description": "Indicates the value of the attribute, characteristic, or quality.",
                    },
                    {
                        "@name": "class",
                        "@as-type": "token",
                        "@required": "no",
                        "formal-name": "Property Class",
                        "description": {"code": ["name"]},
                        "remarks": {
                            "p": [
                                {"code": ["name", "ns"]},
                                {"code": ["class", "class", "group"]},
                            ]
                        },
                    },
                    {
                        "@name": "group",
                        "@as-type": "token",
                        "@required": "no",
                        "formal-name": "Property Group",
                        "description": "An identifier for relating distinct sets of properties.",
                        "remarks": {
                            "p": [
                                "Different sets of properties may relate to separate contexts. Declare a group on a property to associate it with one or more other properties in a given context."
                            ]
                        },
                    },
                ],
                "model": {
                    "field": [
                        {
                            "@ref": "remarks",
                            "@in-xml": "WITH_WRAPPER",
                            "@min-occurs": 0,
                            "@max-occurs": 1,
                        }
                    ]
                },
                "constraint": {
                    "allowed-values": {
                        "@target": ".[has-oscal-namespace('http://csrc.nist.gov/ns/oscal')]/@name",
                        "@level": "ERROR",
                        "@allow-other": "no",
                        "@extensible": "external",
                        "enum": [
                            {
                                "@value": "marking",
                                "$": "A label or descriptor that is tied to a sensitivity or classification marking system. An optional class can be used to define the specific marking system used for the associated value.",
                            }
                        ],
                    }
                },
                "remarks": {
                    "p": [
                        "Properties permit the deployment and management of arbitrary controlled values, within OSCAL objects. A property can be included for any purpose useful to an application or implementation. Typically, properties will be used to sort, filter, select, order, and arrange OSCAL content objects, to relate OSCAL objects to one another, or to associate an OSCAL object to class hierarchies, taxonomies, or external authorities. Thus, the lexical composition of properties may be constrained by external processes to ensure consistency.",
                        "Property allows for associated remarks that describe why the specific property value was applied to the containing object, or the significance of the value in the context of the containing object.",
                    ]
                },
            },
            {
                "@name": "link",
                "@scope": "global",
                "formal-name": "Link",
                "description": "A reference to a local or remote resource, that has a specific relation to the containing object.",
                "define-flag": [
                    {
                        "@name": "href",
                        "@as-type": "uri-reference",
                        "@required": "yes",
                        "formal-name": "Hypertext Reference",
                        "description": "A resolvable URL reference to a resource.",
                        "remarks": {
                            "p": ["This value may be one of:"],
                            "ol": [
                                {
                                    "li": [
                                        {
                                            "a": [
                                                {
                                                    "@href": "https://pages.nist.gov/OSCAL/concepts/uri-use/#absolute-uri",
                                                    "$": "absolute URI",
                                                }
                                            ]
                                        },
                                        {
                                            "a": [
                                                {
                                                    "@href": "https://pages.nist.gov/OSCAL/concepts/uri-use/#relative-reference",
                                                    "$": "relative reference",
                                                }
                                            ]
                                        },
                                        {
                                            "a": [
                                                {
                                                    "@href": "https://pages.nist.gov/OSCAL/concepts/uri-use/#linking-to-another-oscal-object",
                                                    "$": "linking to another OSCAL object",
                                                }
                                            ]
                                        },
                                    ]
                                }
                            ],
                        },
                    },
                    {
                        "@name": "rel",
                        "@as-type": "token",
                        "@required": "no",
                        "formal-name": "Link Relation Type",
                        "description": "Describes the type of relationship provided by the link's hypertext reference. This can be an indicator of the link's purpose.",
                        "constraint": {
                            "allowed-values": [
                                {
                                    "@allow-other": "yes",
                                    "@level": "ERROR",
                                    "@extensible": "external",
                                    "enum": [
                                        {"@value": "reference", "code": ["back-matter"]}
                                    ],
                                }
                            ]
                        },
                    },
                    {
                        "@name": "resource-fragment",
                        "@as-type": "string",
                        "@required": "no",
                        "formal-name": "Resource Fragment",
                        "description": {
                            "code": ["href", "back-matter/resource", "rlink"],
                            "a": [
                                {
                                    "@href": "https://www.rfc-editor.org/rfc/rfc3986#section-3.5",
                                    "$": "fragment",
                                },
                                {
                                    "@href": "https://www.rfc-editor.org/rfc/rfc3986#section-2.1",
                                    "$": "URI encoded",
                                },
                            ],
                        },
                    },
                ],
                "flag": [
                    {
                        "@ref": "media-type",
                        "@required": "no",
                        "formal-name": "Link Media Type",
                        "remarks": {
                            "p": [
                                {
                                    "code": ["media-type"],
                                    "a": [
                                        {
                                            "@href": "https://www.iana.org/assignments/media-types/media-types.xhtml",
                                            "$": "IANA Media Types registry",
                                        }
                                    ],
                                }
                            ]
                        },
                    }
                ],
                "model": {
                    "define-field": [
                        {
                            "@name": "text",
                            "@as-type": "markup-line",
                            "@collapsible": "no",
                            "@min-occurs": 0,
                            "@max-occurs": 1,
                            "@in-xml": "WRAPPED",
                            "formal-name": "Link Text",
                            "description": "A textual label to associate with the link, which may be used for presentation in a tool.",
                        }
                    ]
                },
                "constraint": {
                    "expect": {
                        "@target": ".[starts-with(@href,'#')]",
                        "@test": "not(exists(@media-type))",
                        "@level": "ERROR",
                        "description": "A local reference SHOULD NOT have a media-type.",
                        "remarks": {
                            "p": [
                                {
                                    "code": [
                                        "link",
                                        "back-matter/resource",
                                        "media-type",
                                        "media-type",
                                        "link",
                                        "media-type",
                                        "rlink",
                                        "base64",
                                    ]
                                }
                            ]
                        },
                    },
                    "matches": [
                        {
                            "@target": ".[@rel=('reference') and starts-with(@href,'#')]/@href",
                            "@datatype": "uri-reference",
                            "@level": "ERROR",
                        },
                        {
                            "@target": ".[@rel=('reference') and not(starts-with(@href,'#'))]/@href",
                            "@datatype": "uri",
                            "@level": "ERROR",
                        },
                        {
                            "@target": "@resource-fragment",
                            "@regex": "(?:[0-9a-zA-Z-._~/?!$&'()*+,;=:@]|%[0-9A-F][0-9A-F])+",
                            "@level": "ERROR",
                            "remarks": {
                                "p": [
                                    "This pattern is based on the fragment Augmented Backus-Naur form (ABNF) syntax provided in [RFC3986 section 3.5](https://www.rfc-editor.org/rfc/rfc3986#section-3.5). Uppercase alpha hex digits are required, which is the preferred normalized form defined in RFC3986."
                                ]
                            },
                        },
                    ],
                    "index-has-key": {
                        "@name": "index-back-matter-resource",
                        "@target": ".[@rel=('reference') and starts-with(@href,'#')]",
                        "@level": "ERROR",
                        "key-field": [{"@target": "@href", "@pattern": "#(.*)"}],
                    },
                },
                "remarks": {
                    "p": [
                        {"code": ["resource", "rlink/hash"]},
                        {
                            "code": ["link"],
                            "a": [
                                {
                                    "@href": "https://www.w3.org/TR/html401/struct/links.html#edef-LINK",
                                    "$": "link element",
                                }
                            ],
                        },
                    ]
                },
                "example": [
                    {
                        "description": "Providing for link integrity",
                        "remarks": {
                            "p": [
                                "The following is a contrived example to show the use of link, citation, and resource."
                            ]
                        },
                        "o:oscal": {
                            "@xmlns:o": "http://csrc.nist.gov/ns/oscal/example",
                            "o:link": [
                                {
                                    "@rel": "reference",
                                    "@href": "#resource1",
                                    "$": "My Hashed Resource",
                                }
                            ],
                            "o:back-matter": [
                                {
                                    "o:resource": [
                                        {
                                            "@id": "resource1",
                                            "o:rlink": [
                                                {
                                                    "@href": "https://example.org/some-resource",
                                                    "o:hash": [
                                                        {
                                                            "@algorithm": "sha512",
                                                            "$": "C2E9C1..snip..F88D2E",
                                                        }
                                                    ],
                                                }
                                            ],
                                        }
                                    ]
                                }
                            ],
                        },
                    }
                ],
            },
            {
                "@name": "responsible-party",
                "@scope": "global",
                "formal-name": "Responsible Party",
                "description": "A reference to a set of persons and/or organizations that have responsibility for performing the referenced role in the context of the containing object.",
                "define-flag": [
                    {
                        "@required": "yes",
                        "@name": "role-id",
                        "@as-type": "token",
                        "formal-name": "Responsible Role",
                        "description": {"code": ["role", "party"]},
                        "prop": [
                            {
                                "@name": "value-type",
                                "@value": "identifier-reference",
                                "@namespace": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
                            },
                            {
                                "@name": "identifier-type",
                                "@value": "human-oriented",
                                "@namespace": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
                            },
                            {
                                "@name": "identifier-scope",
                                "@value": "cross-instance",
                                "@namespace": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
                            },
                        ],
                    }
                ],
                "model": {
                    "field": [
                        {
                            "@ref": "party-uuid",
                            "@min-occurs": 1,
                            "@max-occurs": "unbounded",
                            "@in-xml": "WRAPPED",
                            "description": {"code": ["role"]},
                            "group-as": {
                                "@name": "party-uuids",
                                "@in-json": "ARRAY",
                                "@in-xml": "UNGROUPED",
                            },
                        },
                        {
                            "@ref": "remarks",
                            "@in-xml": "WITH_WRAPPER",
                            "@min-occurs": 0,
                            "@max-occurs": 1,
                        },
                    ],
                    "assembly": [
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
                    ],
                },
                "constraint": {
                    "index-has-key": {
                        "@name": "index-metadata-role-id",
                        "@target": ".",
                        "@level": "ERROR",
                        "key-field": [{"@target": "@role-id"}],
                    }
                },
                "remarks": {
                    "p": [
                        {
                            "code": [
                                "responsible-party",
                                "party-uuid",
                                "role-id",
                                "responsible-role",
                                "party-uuid",
                            ]
                        },
                        "The scope of use of this object determines if the responsibility has been performed or will be performed in the future. The containing object will describe the intent.",
                    ]
                },
            },
            {
                "@name": "action",
                "@scope": "global",
                "formal-name": "Action",
                "description": "An action applied by a role within a given party to the content.",
                "define-flag": [
                    {
                        "@name": "uuid",
                        "@as-type": "uuid",
                        "@required": "yes",
                        "formal-name": "Action Universally Unique Identifier",
                        "description": "A unique identifier that can be used to reference this defined action elsewhere in an OSCAL document. A UUID should be consistently used for a given location across revisions of the document.",
                    },
                    {
                        "@name": "date",
                        "@as-type": "date-time-with-timezone",
                        "@required": "no",
                        "formal-name": "Action Occurrence Date",
                        "description": "The date and time when the action occurred.",
                    },
                    {
                        "@name": "type",
                        "@as-type": "token",
                        "@required": "yes",
                        "formal-name": "Action Type",
                        "description": "The type of action documented by the assembly, such as an approval.",
                    },
                    {
                        "@name": "system",
                        "@as-type": "uri",
                        "@required": "yes",
                        "formal-name": "Action Type System",
                        "description": "Specifies the action type system used.",
                        "remarks": {
                            "p": [
                                {"code": ["type", "action", "type", "type"]},
                                "An organization MUST use a URI that they have control over. e.g., a domain registered to the organization in a URI, a registered uniform resource names (URN) namespace.",
                            ]
                        },
                    },
                ],
                "model": {
                    "assembly": [
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
                            "@ref": "responsible-party",
                            "@max-occurs": "unbounded",
                            "@min-occurs": 0,
                            "group-as": {
                                "@name": "responsible-parties",
                                "@in-json": "ARRAY",
                                "@in-xml": "UNGROUPED",
                            },
                        },
                    ],
                    "field": [
                        {
                            "@ref": "remarks",
                            "@in-xml": "WITH_WRAPPER",
                            "@min-occurs": 0,
                            "@max-occurs": 1,
                        }
                    ],
                },
                "constraint": {
                    "index-has-key": [
                        {
                            "@name": "index-metadata-role-id",
                            "@target": "responsible-party",
                            "@level": "ERROR",
                            "key-field": [{"@target": "@role-id"}],
                        },
                        {
                            "@name": "index-metadata-party-uuid",
                            "@target": "responsible-party",
                            "@level": "ERROR",
                            "key-field": [{"@target": "party-uuid"}],
                        },
                    ],
                    "allowed-values": [
                        {
                            "@target": "./system/@value",
                            "@allow-other": "yes",
                            "@level": "ERROR",
                            "@extensible": "external",
                            "enum": [
                                {
                                    "@value": "http://csrc.nist.gov/ns/oscal",
                                    "$": "This value identifies action types defined in the NIST OSCAL namespace.",
                                }
                            ],
                        },
                        {
                            "@target": "./type[has-oscal-namespace('http://csrc.nist.gov/ns/oscal')]/@value",
                            "@level": "ERROR",
                            "@allow-other": "no",
                            "@extensible": "external",
                            "enum": [
                                {
                                    "@value": "approval",
                                    "$": "An approval of a document instance's content.",
                                },
                                {
                                    "@value": "request-changes",
                                    "$": "A request from the responisble party or parties to change the content.",
                                },
                            ],
                        },
                    ],
                },
            },
            {
                "@name": "responsible-role",
                "@scope": "global",
                "formal-name": "Responsible Role",
                "description": "A reference to a role with responsibility for performing a function relative to the containing object, optionally associated with a set of persons and/or organizations that perform that role.",
                "define-flag": [
                    {
                        "@name": "role-id",
                        "@as-type": "token",
                        "@required": "yes",
                        "formal-name": "Responsible Role ID",
                        "description": {
                            "a": [
                                {
                                    "@href": "https://pages.nist.gov/OSCAL/concepts/identifier-use/#human-oriented",
                                    "$": "human-oriented",
                                }
                            ],
                            "code": ["role"],
                        },
                    }
                ],
                "model": {
                    "assembly": [
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
                    ],
                    "field": [
                        {
                            "@ref": "party-uuid",
                            "@max-occurs": "unbounded",
                            "@min-occurs": 0,
                            "@in-xml": "WRAPPED",
                            "description": {"code": ["role"]},
                            "group-as": {
                                "@name": "party-uuids",
                                "@in-json": "ARRAY",
                                "@in-xml": "UNGROUPED",
                            },
                        },
                        {
                            "@ref": "remarks",
                            "@in-xml": "WITH_WRAPPER",
                            "@min-occurs": 0,
                            "@max-occurs": 1,
                        },
                    ],
                },
                "remarks": {
                    "p": [
                        {
                            "code": [
                                "responsible-role",
                                "party-uuid",
                                "role-id",
                                "responsible-party",
                                "party-uuid",
                            ]
                        },
                        "The scope of use of this object determines if the responsibility has been performed or will be performed in the future. The containing object will describe the intent.",
                    ]
                },
            },
            {
                "@name": "address",
                "@scope": "local",
                "formal-name": "Address",
                "description": "A postal address for the location.",
                "flag": [
                    {"@ref": "location-type", "@required": "no", "use-name": "type"}
                ],
                "model": {
                    "field": [
                        {
                            "@ref": "addr-line",
                            "@max-occurs": "unbounded",
                            "@min-occurs": 0,
                            "@in-xml": "WRAPPED",
                            "group-as": {
                                "@name": "addr-lines",
                                "@in-json": "ARRAY",
                                "@in-xml": "UNGROUPED",
                            },
                        }
                    ],
                    "define-field": [
                        {
                            "@name": "city",
                            "@as-type": "string",
                            "@collapsible": "no",
                            "@min-occurs": 0,
                            "@max-occurs": 1,
                            "@in-xml": "WRAPPED",
                            "formal-name": "City",
                            "description": "City, town or geographical region for the mailing address.",
                        },
                        {
                            "@name": "state",
                            "@as-type": "string",
                            "@collapsible": "no",
                            "@min-occurs": 0,
                            "@max-occurs": 1,
                            "@in-xml": "WRAPPED",
                            "formal-name": "State",
                            "description": "State, province or analogous geographical region for a mailing\n                    address.",
                        },
                        {
                            "@name": "postal-code",
                            "@as-type": "string",
                            "@collapsible": "no",
                            "@min-occurs": 0,
                            "@max-occurs": 1,
                            "@in-xml": "WRAPPED",
                            "formal-name": "Postal Code",
                            "description": "Postal or ZIP code for mailing address.",
                        },
                        {
                            "@name": "country",
                            "@as-type": "string",
                            "@collapsible": "no",
                            "@min-occurs": 0,
                            "@max-occurs": 1,
                            "@in-xml": "WRAPPED",
                            "formal-name": "Country Code",
                            "description": "The ISO 3166-1 alpha-2 country code for the mailing address.",
                            "constraint": {
                                "matches": {
                                    "@target": ".",
                                    "@regex": "[A-Z]{2}",
                                    "@level": "ERROR",
                                }
                            },
                        },
                    ],
                },
            },
        ],
        "define-flag": [
            {
                "@name": "location-uuid",
                "@as-type": "uuid",
                "@scope": "global",
                "formal-name": "Location Universally Unique Identifier Reference",
                "description": "Reference to a location by UUID.",
                "prop": [
                    {
                        "@name": "value-type",
                        "@value": "identifier-reference",
                        "@namespace": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
                    },
                    {
                        "@name": "identifier-type",
                        "@value": "machine-oriented",
                        "@namespace": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
                    },
                    {
                        "@name": "identifier-scope",
                        "@value": "cross-instance",
                        "@namespace": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
                    },
                ],
                "constraint": {
                    "index-has-key": [
                        {
                            "@name": "index-metadata-location-uuid",
                            "@level": "ERROR",
                            "key-field": [{"@target": "."}],
                        }
                    ]
                },
            },
            {
                "@name": "media-type",
                "@as-type": "string",
                "@scope": "global",
                "formal-name": "Media Type",
                "description": "A label that indicates the nature of a resource, as a data serialization or\n            format.",
                "remarks": {
                    "p": [
                        {
                            "a": [
                                {
                                    "@href": "https://www.iana.org/assignments/media-types/media-types.xhtml",
                                    "$": "Media\n                    Types Registry",
                                }
                            ]
                        },
                        {
                            "code": [
                                "application/oscal+xml",
                                "application/oscal+json",
                                "application/oscal+yaml",
                            ]
                        },
                        {
                            "code": ["application/yaml", "application/oscal+yaml"],
                            "a": [
                                {
                                    "@href": "https://www.rfc-editor.org/rfc/rfc6838.html#section-4.2.8",
                                    "$": "RFC 6838 Section 4.2.8",
                                }
                            ],
                        },
                        {"code": ["application/oscal.catalog+xml"]},
                    ]
                },
            },
            {
                "@name": "location-type",
                "@as-type": "token",
                "@scope": "local",
                "formal-name": "Address Type",
                "description": "Indicates the type of address.",
                "constraint": {
                    "allowed-values": [
                        {
                            "@allow-other": "yes",
                            "@level": "ERROR",
                            "@extensible": "external",
                            "enum": [
                                {"@value": "home", "$": "A home address."},
                                {"@value": "work", "$": "A work address."},
                            ],
                        }
                    ]
                },
            },
        ],
        "define-field": [
            {
                "@name": "location-uuid",
                "@as-type": "uuid",
                "@scope": "global",
                "formal-name": "Location Universally Unique Identifier Reference",
                "description": "Reference to a location by UUID.",
                "prop": [
                    {
                        "@name": "value-type",
                        "@value": "identifier-reference",
                        "@namespace": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
                    },
                    {
                        "@name": "identifier-type",
                        "@value": "machine-oriented",
                        "@namespace": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
                    },
                    {
                        "@name": "identifier-scope",
                        "@value": "cross-instance",
                        "@namespace": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
                    },
                ],
                "constraint": {
                    "index-has-key": {
                        "@name": "index-metadata-location-uuid",
                        "@target": ".",
                        "@level": "ERROR",
                        "key-field": [{"@target": "."}],
                    }
                },
            },
            {
                "@name": "party-uuid",
                "@as-type": "uuid",
                "@scope": "global",
                "formal-name": "Party Universally Unique Identifier Reference",
                "description": "Reference to a party by UUID.",
                "prop": [
                    {
                        "@name": "value-type",
                        "@value": "identifier-reference",
                        "@namespace": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
                    },
                    {
                        "@name": "identifier-type",
                        "@value": "machine-oriented",
                        "@namespace": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
                    },
                    {
                        "@name": "identifier-scope",
                        "@value": "cross-instance",
                        "@namespace": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
                    },
                ],
                "constraint": {
                    "index-has-key": {
                        "@name": "index-metadata-party-uuid",
                        "@target": ".",
                        "@level": "ERROR",
                        "key-field": [{"@target": "."}],
                    }
                },
            },
            {
                "@name": "role-id",
                "@as-type": "token",
                "@scope": "global",
                "formal-name": "Role Identifier Reference",
                "description": "Reference to a role by UUID.",
                "prop": [
                    {
                        "@name": "value-type",
                        "@value": "identifier-reference",
                        "@namespace": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
                    },
                    {
                        "@name": "identifier-type",
                        "@value": "human-oriented",
                        "@namespace": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
                    },
                    {
                        "@name": "identifier-scope",
                        "@value": "cross-instance",
                        "@namespace": "http://csrc.nist.gov/ns/oscal/metaschema/1.0",
                    },
                ],
                "constraint": {
                    "index-has-key": {
                        "@name": "index-metadata-role-id",
                        "@target": ".",
                        "@level": "ERROR",
                        "key-field": [{"@target": "."}],
                    }
                },
            },
            {
                "@name": "hash",
                "@as-type": "string",
                "@scope": "global",
                "formal-name": "Hash",
                "description": "A representation of a cryptographic digest generated over a resource using a specified hash algorithm.",
                "json-value-key": "value",
                "define-flag": [
                    {
                        "@name": "algorithm",
                        "@as-type": "string",
                        "@required": "yes",
                        "formal-name": "Hash algorithm",
                        "description": "The digest method by which a hash is derived.",
                        "constraint": {
                            "allowed-values": [
                                {
                                    "@allow-other": "yes",
                                    "@level": "ERROR",
                                    "@extensible": "external",
                                    "enum": [
                                        {
                                            "@value": "SHA-224",
                                            "a": [
                                                {
                                                    "@href": "https://doi.org/10.6028/NIST.FIPS.180-4",
                                                    "$": "NIST FIPS 180-4",
                                                }
                                            ],
                                        },
                                        {
                                            "@value": "SHA-256",
                                            "a": [
                                                {
                                                    "@href": "https://doi.org/10.6028/NIST.FIPS.180-4",
                                                    "$": "NIST FIPS 180-4",
                                                }
                                            ],
                                        },
                                        {
                                            "@value": "SHA-384",
                                            "a": [
                                                {
                                                    "@href": "https://doi.org/10.6028/NIST.FIPS.180-4",
                                                    "$": "NIST FIPS 180-4",
                                                }
                                            ],
                                        },
                                        {
                                            "@value": "SHA-512",
                                            "a": [
                                                {
                                                    "@href": "https://doi.org/10.6028/NIST.FIPS.180-4",
                                                    "$": "NIST FIPS 180-4",
                                                }
                                            ],
                                        },
                                        {
                                            "@value": "SHA3-224",
                                            "a": [
                                                {
                                                    "@href": "https://doi.org/10.6028/NIST.FIPS.202",
                                                    "$": "NIST FIPS 202",
                                                }
                                            ],
                                        },
                                        {
                                            "@value": "SHA3-256",
                                            "a": [
                                                {
                                                    "@href": "https://doi.org/10.6028/NIST.FIPS.202",
                                                    "$": "NIST FIPS 202",
                                                }
                                            ],
                                        },
                                        {
                                            "@value": "SHA3-384",
                                            "a": [
                                                {
                                                    "@href": "https://doi.org/10.6028/NIST.FIPS.202",
                                                    "$": "NIST FIPS 202",
                                                }
                                            ],
                                        },
                                        {
                                            "@value": "SHA3-512",
                                            "a": [
                                                {
                                                    "@href": "https://doi.org/10.6028/NIST.FIPS.202",
                                                    "$": "NIST FIPS 202",
                                                }
                                            ],
                                        },
                                    ],
                                }
                            ]
                        },
                        "remarks": {
                            "p": [
                                {
                                    "a": [
                                        {
                                            "@href": "https://www.w3.org/TR/xmlsec-algorithms/#digest-method-uris",
                                            "$": "XML Security Algorithm Cross-Reference",
                                        },
                                        {
                                            "@href": "https://tools.ietf.org/html/rfc6931#section-2.1.5",
                                            "$": "RFC 6931 Section 2.1.5",
                                        },
                                    ]
                                }
                            ]
                        },
                    }
                ],
                "constraint": {
                    "matches": [
                        {
                            "@target": ".[@algorithm=('SHA-224','SHA3-224')]",
                            "@regex": "^[0-9a-fA-F]{28}$",
                            "@level": "ERROR",
                        },
                        {
                            "@target": ".[@algorithm=('SHA-256','SHA3-256')]",
                            "@regex": "^[0-9a-fA-F]{32}$",
                            "@level": "ERROR",
                        },
                        {
                            "@target": ".[@algorithm=('SHA-384','SHA3-384')]",
                            "@regex": "^[0-9a-fA-F]{48}$",
                            "@level": "ERROR",
                        },
                        {
                            "@target": ".[@algorithm=('SHA-512','SHA3-512')]",
                            "@regex": "^[0-9a-fA-F]{64}$",
                            "@level": "ERROR",
                        },
                    ]
                },
            },
            {
                "@name": "remarks",
                "@as-type": "markup-multiline",
                "@scope": "global",
                "formal-name": "Remarks",
                "description": "Additional commentary about the containing object.",
                "remarks": {"p": [{"code": ["remarks", "prop", "link"]}]},
            },
            {
                "@name": "published",
                "@as-type": "date-time-with-timezone",
                "@scope": "local",
                "formal-name": "Publication Timestamp",
                "description": "The date and time the document was last made available.",
                "remarks": {
                    "p": [
                        "Typically, this date value will be machine-generated at the time the containing document is published.",
                        {"code": ["published"]},
                    ]
                },
            },
            {
                "@name": "last-modified",
                "@as-type": "date-time-with-timezone",
                "@scope": "local",
                "formal-name": "Last Modified Timestamp",
                "description": "The date and time the document was last stored for later retrieval.",
                "remarks": {
                    "p": [
                        "This value represents the point in time when the OSCAL document was last updated, or at the point of creation the creation date. Typically, this date value will be machine generated at time of creation or modification. Ideally, this field will be managed by the editing tool or service used to make modifications when storing the modified document.",
                        "The intent of the last modified timestamp is to distinguish between significant change milestones when the document may be accessed by multiple entities. This allows a given entity to differentiate between mutiple document states at specific points in time. It is possible to make multiple modifications to the document without storing these changes. In such a case, the last modified timestamp might not be updated until the document is finally stored.",
                        {"code": ["last-modified"]},
                    ]
                },
            },
            {
                "@name": "version",
                "@scope": "local",
                "@as-type": "string",
                "formal-name": "Document Version",
                "description": "Used to distinguish a specific revision of an OSCAL document from other previous and future versions.",
                "remarks": {
                    "p": [
                        "A version may be a release number, sequence number, date, or other identifier sufficient to distinguish between different document revisions.",
                        {
                            "a": [
                                {
                                    "@href": "https://semver.org/spec/v2.0.0.html",
                                    "$": "Semantic Versioning",
                                }
                            ]
                        },
                        "A version is typically set by the document owner or by the tool used to maintain the content.",
                    ]
                },
            },
            {
                "@name": "oscal-version",
                "@scope": "local",
                "@as-type": "string",
                "formal-name": "OSCAL Version",
                "description": "The OSCAL model version the document was authored against and will conform to as valid.",
                "remarks": {
                    "p": [
                        {"q": ["1.1.0", "1.0.0-milestone1"]},
                        "The OSCAL version serves a different purpose from the document version and is used to represent a different concept. If both have the same value, this is coincidental.",
                    ]
                },
            },
            {
                "@name": "email-address",
                "@as-type": "email-address",
                "@scope": "local",
                "formal-name": "Email Address",
                "description": {
                    "a": [
                        {
                            "@href": "https://tools.ietf.org/html/rfc5322#section-3.4.1",
                            "$": "RFC 5322 Section\n            3.4.1",
                        }
                    ]
                },
            },
            {
                "@name": "telephone-number",
                "@scope": "local",
                "@as-type": "string",
                "formal-name": "Telephone Number",
                "description": {
                    "a": [
                        {
                            "@href": "https://www.itu.int/rec/T-REC-E.164-201011-I/en",
                            "$": "ITU-T E.164",
                        }
                    ]
                },
                "json-value-key": "number",
                "define-flag": [
                    {
                        "@name": "type",
                        "@as-type": "string",
                        "@required": "no",
                        "formal-name": "type flag",
                        "description": "Indicates the type of phone number.",
                        "constraint": {
                            "allowed-values": [
                                {
                                    "@allow-other": "yes",
                                    "@level": "ERROR",
                                    "@extensible": "external",
                                    "enum": [
                                        {"@value": "home", "$": "A home phone number."},
                                        {
                                            "@value": "office",
                                            "$": "An office phone number.",
                                        },
                                        {
                                            "@value": "mobile",
                                            "$": "A mobile phone number.",
                                        },
                                    ],
                                }
                            ]
                        },
                    }
                ],
                "constraint": {
                    "matches": {
                        "@level": "WARNING",
                        "@target": ".",
                        "@regex": "^[0-9]{3}[0-9]{1,12}$",
                        "remarks": {
                            "p": [
                                "Providing a country code provides an international means to interpret the phone number."
                            ]
                        },
                    }
                },
            },
            {
                "@name": "addr-line",
                "@scope": "local",
                "@as-type": "string",
                "formal-name": "Address line",
                "description": "A single line of an address.",
            },
            {
                "@name": "document-id",
                "@scope": "local",
                "@as-type": "string",
                "formal-name": "Document Identifier",
                "description": {"code": ["scheme"]},
                "json-value-key": "identifier",
                "define-flag": [
                    {
                        "@name": "scheme",
                        "@as-type": "uri",
                        "@required": "no",
                        "formal-name": "Document Identification Scheme",
                        "description": "Qualifies the kind of document identifier using a URI. If the scheme is not\n                provided the value of the element will be interpreted as a string of\n                characters.",
                        "constraint": {
                            "allowed-values": [
                                {
                                    "@allow-other": "yes",
                                    "@level": "ERROR",
                                    "@extensible": "external",
                                    "enum": [
                                        {
                                            "@value": "http://www.doi.org/",
                                            "a": [
                                                {
                                                    "@href": "https://www.doi.org/hb.html",
                                                    "$": "Digital Object Identifier",
                                                }
                                            ],
                                        }
                                    ],
                                }
                            ]
                        },
                        "remarks": {
                            "p": [
                                {
                                    "a": [
                                        {
                                            "@href": "https://pages.nist.gov/OSCAL/concepts/uri-use/#absolute-uri",
                                            "$": "absolute URI",
                                        },
                                        {
                                            "@href": "https://pages.nist.gov/OSCAL/concepts/uri-use/#use-as-a-naming-system-identifier",
                                            "$": "naming system identifier",
                                        },
                                    ]
                                }
                            ]
                        },
                    }
                ],
                "remarks": {
                    "p": [
                        {
                            "a": [
                                {
                                    "@href": "https://pages.nist.gov/OSCAL/concepts/identifier-use/#globally-unique",
                                    "$": "globally unique",
                                },
                                {
                                    "@href": "https://pages.nist.gov/OSCAL/concepts/identifier-use/#cross-instance",
                                    "$": "cross-instance",
                                },
                            ]
                        },
                        "A document identifier provides an additional data point for identifying a document that can be assigned by a publisher or organization for purposes in a wider system, such as a digital object identifier (DOI) or a local content management system identifier.",
                        {"code": ["document-id"]},
                        {"code": ["uuid"]},
                    ]
                },
            },
        ],
    },
    "short_name": "oscal-metadata",
    "globals": {
        "metadata": "Document Metadata",
        "back-matter": "Back matter",
        "property": "Property",
        "link": "Link",
        "responsible-party": "Responsible Party",
        "action": "Action",
        "responsible-role": "Responsible Role",
        "location-uuid": "Location Universally Unique Identifier Reference",
        "party-uuid": "Party Universally Unique Identifier Reference",
        "role-id": "Role Identifier Reference",
        "hash": "Hash",
        "remarks": "Remarks",
        "media-type": "Media Type",
    },
    "roots": [],
}
