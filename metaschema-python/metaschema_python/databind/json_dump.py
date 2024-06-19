A = [
    {
        "effective-name": "assessment-results",
        "type": "assembly",
        "contents": [
            {
                "effective-name": "uuid",
                "type": "field-or-flag",
                "contents": ["ec0dad37-54e0-40fd-a925-6d0bdea94c0d"],
            },
            {
                "effective-name": "metadata",
                "type": "assembly",
                "contents": [
                    {
                        "effective-name": "title",
                        "type": "field-or-flag",
                        "contents": [
                            "IFA GoodRead Continuous Monitoring Assessment Results June 2023"
                        ],
                    },
                    {
                        "effective-name": "last-modified",
                        "type": "field-or-flag",
                        "contents": ["2024-02-01T13:57:28.355446-04:00"],
                    },
                    {
                        "effective-name": "version",
                        "type": "field-or-flag",
                        "contents": ["202306-002"],
                    },
                    {
                        "effective-name": "oscal-version",
                        "type": "field-or-flag",
                        "contents": ["1.1.2"],
                    },
                    {
                        "group-as-name": "roles",
                        "contents": [
                            {
                                "effective-name": "id",
                                "type": "field-or-flag",
                                "contents": ["assessor"],
                            },
                            {
                                "effective-name": "title",
                                "type": "field-or-flag",
                                "contents": ["IFA Security Controls Assessor"],
                            },
                        ],
                    },
                    {
                        "group-as-name": "parties",
                        "contents": [
                            {
                                "effective-name": "uuid",
                                "type": "field-or-flag",
                                "contents": ["e7730080-71ce-4b20-bec4-84f33136fd58"],
                            },
                            {
                                "effective-name": "type",
                                "type": "field-or-flag",
                                "contents": ["person"],
                            },
                            {
                                "effective-name": "name",
                                "type": "field-or-flag",
                                "contents": ["Amy Assessor"],
                            },
                            {
                                "group-as-name": "member-of-organizations",
                                "contents": ["3a675986-b4ff-4030-b178-e953c2e55d64"],
                            },
                        ],
                    },
                    {
                        "group-as-name": "parties",
                        "contents": [
                            {
                                "effective-name": "uuid",
                                "type": "field-or-flag",
                                "contents": ["3a675986-b4ff-4030-b178-e953c2e55d64"],
                            },
                            {
                                "effective-name": "type",
                                "type": "field-or-flag",
                                "contents": ["organization"],
                            },
                            {
                                "effective-name": "name",
                                "type": "field-or-flag",
                                "contents": ["Important Federal Agency"],
                            },
                            {
                                "effective-name": "short-name",
                                "type": "field-or-flag",
                                "contents": ["IFA"],
                            },
                            {
                                "group-as-name": "links",
                                "contents": [
                                    {
                                        "effective-name": "href",
                                        "type": "field-or-flag",
                                        "contents": ["https://www.ifa.gov"],
                                    },
                                    {
                                        "effective-name": "rel",
                                        "type": "field-or-flag",
                                        "contents": ["website"],
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        "group-as-name": "responsible-parties",
                        "contents": [
                            {
                                "effective-name": "role-id",
                                "type": "field-or-flag",
                                "contents": ["assessor"],
                            },
                            {
                                "group-as-name": "party-uuids",
                                "contents": ["e7730080-71ce-4b20-bec4-84f33136fd58"],
                            },
                        ],
                    },
                ],
            },
            {
                "effective-name": "import-ap",
                "type": "assembly",
                "contents": [
                    {
                        "effective-name": "href",
                        "type": "field-or-flag",
                        "contents": ["./ap.oscal.xml"],
                    }
                ],
            },
            {
                "effective-name": "local-definitions",
                "type": "assembly",
                "contents": [
                    {
                        "group-as-name": "activities",
                        "contents": [
                            {
                                "effective-name": "uuid",
                                "type": "field-or-flag",
                                "contents": ["cf5d53fe-6043-4c68-9ed6-6b258909febf"],
                            },
                            {
                                "effective-name": "title",
                                "type": "field-or-flag",
                                "contents": [
                                    "Test System Elements for Least Privilege Design and Implementation"
                                ],
                            },
                            {
                                "effective-name": "description",
                                "type": "field-or-flag",
                                "contents": [
                                    "The activity and it steps will be performed by the assessor via their security automation platform to test least privilege design and implementation of the system's elements, specifically the cloud account infrastructure, as part of continuous monitoring."
                                ],
                            },
                            {
                                "group-as-name": "props",
                                "contents": [
                                    {
                                        "effective-name": "name",
                                        "type": "field-or-flag",
                                        "contents": ["method"],
                                    },
                                    {
                                        "effective-name": "value",
                                        "type": "field-or-flag",
                                        "contents": ["TEST"],
                                    },
                                ],
                            },
                            {
                                "group-as-name": "steps",
                                "contents": [
                                    {
                                        "effective-name": "uuid",
                                        "type": "field-or-flag",
                                        "contents": [
                                            "57f8cfb8-fc3f-41d3-b938-6ab421c92574"
                                        ],
                                    },
                                    {
                                        "effective-name": "title",
                                        "type": "field-or-flag",
                                        "contents": [
                                            "Configure Cross-Account IAM Role Trust for GoodRead and Assessor AwesomeCloud Accounts"
                                        ],
                                    },
                                    {
                                        "effective-name": "description",
                                        "type": "field-or-flag",
                                        "contents": [
                                            "The GoodRead system engineer will coordinate with the assessor's engineering support staff to configure an IAM role trust. A service account for automation with its own role with the assessor's AwesomeCloud account can assume the role for read-only assessor operations within the GoodRead Product Team's AwesomeCloud account for continuous monitoring of least privilege."
                                        ],
                                    },
                                    {
                                        "effective-name": "remarks",
                                        "type": "field-or-flag",
                                        "contents": [
                                            "This step is complete.\n\nGoodRead Product Team and SCA Engineering Support configured the latter's cross-account role trust and authentication and authorization in to the former's account on May 29, 2023."
                                        ],
                                    },
                                ],
                            },
                            {
                                "group-as-name": "steps",
                                "contents": [
                                    {
                                        "effective-name": "uuid",
                                        "type": "field-or-flag",
                                        "contents": [
                                            "976aadad-b1ce-475b-aa6c-e082537e7902"
                                        ],
                                    },
                                    {
                                        "effective-name": "title",
                                        "type": "field-or-flag",
                                        "contents": [
                                            "Automate Cross-Account Login to GoodRead AwesomeCloud Account"
                                        ],
                                    },
                                    {
                                        "effective-name": "description",
                                        "type": "field-or-flag",
                                        "contents": [
                                            "The assessor's security automation platform will create a session from their dedicated will obtain access to the GoodRead Product Team's AwesomeCloud account with their single sign-on credentials to a read-only assessor role."
                                        ],
                                    },
                                    {
                                        "effective-name": "remarks",
                                        "type": "field-or-flag",
                                        "contents": [
                                            "This step is complete.\n\nGoodRead Product Team and SCA Engineering Support tested scripts from the security automation platform interactively on May 30, 2023, to confirm they work ahead of June 2023 continuous monitoring cycle."
                                        ],
                                    },
                                ],
                            },
                            {
                                "group-as-name": "steps",
                                "contents": [
                                    {
                                        "effective-name": "uuid",
                                        "type": "field-or-flag",
                                        "contents": [
                                            "18ce4e19-7432-4484-8e75-2dd8f05668cf"
                                        ],
                                    },
                                    {
                                        "effective-name": "title",
                                        "type": "field-or-flag",
                                        "contents": [
                                            "Analyze GoodRead Developer and System Engineer Roles for Least Privilege"
                                        ],
                                    },
                                    {
                                        "effective-name": "description",
                                        "type": "field-or-flag",
                                        "contents": [
                                            "Once authenticated and authorized with a cross-account session, the security automation pipeline will execute scripts developed and maintained by the assessor's engineering support staff. It will analyze the permitted actions for the developer and system engineer roles in the GoodRead Product Team's AwesomeCloud account to confirm they are designed and implement to facilitate only least privilege operation. Examples are included below.\n\n* For the GoodRead developer role in their AwesomeCloud account, the developer role may only permit the user with this role to check the IP addresses and status of the Awesome Compute Service server instances. This role will not permit the user to create, change, or delete the instances. Similarly, the developer will permit a user to perform actions to see IP addresses of an Awesome Load Balancer instance, but not add, change, or delete the instances.\n* For the GoodRead system engineer role in their AwesomeCloud account, the system engineer role may only permit actions where the user can add, change, or delete instances for approved services (i.e. Awesome Compute Service, Awesome Load Balancer, et cetera). The role may not permit actions by the user for any other service.\n"
                                        ],
                                    },
                                ],
                            },
                            {
                                "effective-name": "related-controls",
                                "type": "assembly",
                                "contents": [
                                    {
                                        "group-as-name": "control-selections",
                                        "contents": [
                                            {
                                                "group-as-name": "include-controls",
                                                "contents": [
                                                    {
                                                        "effective-name": "control-id",
                                                        "type": "field-or-flag",
                                                        "contents": ["ac-6.1"],
                                                    }
                                                ],
                                            }
                                        ],
                                    }
                                ],
                            },
                            {
                                "group-as-name": "responsible-roles",
                                "contents": [
                                    {
                                        "effective-name": "role-id",
                                        "type": "field-or-flag",
                                        "contents": ["assessor"],
                                    },
                                    {
                                        "group-as-name": "party-uuids",
                                        "contents": [
                                            "e7730080-71ce-4b20-bec4-84f33136fd58"
                                        ],
                                    },
                                ],
                            },
                        ],
                    }
                ],
            },
            {
                "group-as-name": "results",
                "contents": [
                    {
                        "effective-name": "uuid",
                        "type": "field-or-flag",
                        "contents": ["a1d20136-37e0-42aa-9834-4e9d8c36d798"],
                    },
                    {
                        "effective-name": "title",
                        "type": "field-or-flag",
                        "contents": [
                            "IFA GoodRead Continous Monitoring Results June 2023"
                        ],
                    },
                    {
                        "effective-name": "description",
                        "type": "field-or-flag",
                        "contents": [
                            "Automated monthly continuous monitoring of the GoodRead information system's cloud infrastructure recorded observations below. Additionally, contingent upon the confidence level of the observations and possible risks, confirmed findings may be opened."
                        ],
                    },
                    {
                        "effective-name": "start",
                        "type": "field-or-flag",
                        "contents": ["2023-06-02T08:31:20-04:00"],
                    },
                    {
                        "effective-name": "end",
                        "type": "field-or-flag",
                        "contents": ["2023-06-02T08:46:51-04:00"],
                    },
                    {
                        "effective-name": "local-definitions",
                        "type": "assembly",
                        "contents": [
                            {
                                "group-as-name": "tasks",
                                "contents": [
                                    {
                                        "effective-name": "uuid",
                                        "type": "field-or-flag",
                                        "contents": [
                                            "35876484-aa4b-494d-95a2-0d1cc04eb47e"
                                        ],
                                    },
                                    {
                                        "effective-name": "type",
                                        "type": "field-or-flag",
                                        "contents": ["action"],
                                    },
                                    {
                                        "effective-name": "title",
                                        "type": "field-or-flag",
                                        "contents": [
                                            "Test System Elements for Least Privilege Design and Implementation"
                                        ],
                                    },
                                    {
                                        "effective-name": "description",
                                        "type": "field-or-flag",
                                        "contents": [
                                            "The activity and it steps will be performed by the assessor via their security automation platform to test least privilege design and implementation of the system's elements, specifically the cloud account infrastructure, as part of continuous monitoring."
                                        ],
                                    },
                                    {
                                        "group-as-name": "associated-activities",
                                        "contents": [
                                            {
                                                "effective-name": "activity-uuid",
                                                "type": "field-or-flag",
                                                "contents": [
                                                    "cf5d53fe-6043-4c68-9ed6-6b258909febf"
                                                ],
                                            },
                                            {
                                                "group-as-name": "subjects",
                                                "contents": [
                                                    {
                                                        "effective-name": "type",
                                                        "type": "field-or-flag",
                                                        "contents": ["component"],
                                                    },
                                                    {
                                                        "effective-name": "include-all",
                                                        "type": "assembly",
                                                        "contents": [],
                                                    },
                                                ],
                                            },
                                        ],
                                    },
                                ],
                            }
                        ],
                    },
                    {
                        "effective-name": "reviewed-controls",
                        "type": "assembly",
                        "contents": [
                            {
                                "group-as-name": "control-selections",
                                "contents": [
                                    {
                                        "group-as-name": "include-controls",
                                        "contents": [
                                            {
                                                "effective-name": "control-id",
                                                "type": "field-or-flag",
                                                "contents": ["ac-6.1"],
                                            }
                                        ],
                                    }
                                ],
                            }
                        ],
                    },
                    {
                        "group-as-name": "observations",
                        "contents": [
                            {
                                "effective-name": "uuid",
                                "type": "field-or-flag",
                                "contents": ["8807eb6e-0c05-43bc-8438-799739615e34"],
                            },
                            {
                                "effective-name": "title",
                                "type": "field-or-flag",
                                "contents": [
                                    "AwesomeCloud IAM Roles Test - GoodRead System Engineer Role"
                                ],
                            },
                            {
                                "effective-name": "description",
                                "type": "field-or-flag",
                                "contents": [
                                    "Test AwesomeCloud IAM Roles for least privilege design and implementation."
                                ],
                            },
                            {"group-as-name": "methods", "contents": ["TEST"]},
                            {"group-as-name": "types", "contents": ["finding"]},
                            {
                                "group-as-name": "subjects",
                                "contents": [
                                    {
                                        "effective-name": "subject-uuid",
                                        "type": "field-or-flag",
                                        "contents": [
                                            "551b9706-d6a4-4d25-8207-f2ccec548b89"
                                        ],
                                    },
                                    {
                                        "effective-name": "type",
                                        "type": "field-or-flag",
                                        "contents": ["component"],
                                    },
                                ],
                            },
                            {
                                "effective-name": "collected",
                                "type": "field-or-flag",
                                "contents": ["2023-06-02T08:31:20-04:00"],
                            },
                            {
                                "effective-name": "expires",
                                "type": "field-or-flag",
                                "contents": ["2023-07-01T00:00:00-04:00"],
                            },
                            {
                                "effective-name": "remarks",
                                "type": "field-or-flag",
                                "contents": [
                                    "The assessor's security automation platform analyzed all roles specific to the GoodRead Product Team, not those managed by the Office of Information Technology. The `IFA-GoodRead-SystemEnginer` role in their respective AwesomeCloud account permitted use of the following high-risk actions.\n\n* awesomecloud:auditlog:DeleteAccountAuditLog\n* awesomecloud:secmon:AdministerConfigurations\n\n\nBoth of these actions are overly permissive and not appropriate for the business function of the staff member assigned this role."
                                ],
                            },
                        ],
                    },
                    {
                        "group-as-name": "observations",
                        "contents": [
                            {
                                "effective-name": "uuid",
                                "type": "field-or-flag",
                                "contents": ["4a2fb32e-9be9-43cf-b717-e9e47de061bd"],
                            },
                            {
                                "effective-name": "title",
                                "type": "field-or-flag",
                                "contents": [
                                    "AwesomeCloud IAM Roles Test - GoodRead Developer Role"
                                ],
                            },
                            {
                                "effective-name": "description",
                                "type": "field-or-flag",
                                "contents": [
                                    "Test AwesomeCloud IAM Roles for least privilege design and implementation."
                                ],
                            },
                            {"group-as-name": "methods", "contents": ["TEST"]},
                            {"group-as-name": "types", "contents": ["finding"]},
                            {
                                "group-as-name": "subjects",
                                "contents": [
                                    {
                                        "effective-name": "subject-uuid",
                                        "type": "field-or-flag",
                                        "contents": [
                                            "551b9706-d6a4-4d25-8207-f2ccec548b89"
                                        ],
                                    },
                                    {
                                        "effective-name": "type",
                                        "type": "field-or-flag",
                                        "contents": ["component"],
                                    },
                                ],
                            },
                            {
                                "effective-name": "collected",
                                "type": "field-or-flag",
                                "contents": ["2023-06-02T08:31:20-04:00"],
                            },
                            {
                                "effective-name": "expires",
                                "type": "field-or-flag",
                                "contents": ["2023-07-01T00:00:00-04:00"],
                            },
                            {
                                "effective-name": "remarks",
                                "type": "field-or-flag",
                                "contents": [
                                    "The assessor's security automation platform detected that the developer's role is permitted to perform only permissible actions in the GoodRead AwesomeCloud account in accordance with the agency's least privilege policy and procedures."
                                ],
                            },
                        ],
                    },
                    {
                        "group-as-name": "risks",
                        "contents": [
                            {
                                "effective-name": "uuid",
                                "type": "field-or-flag",
                                "contents": ["0cfa750e-3553-47ba-a7ba-cf84a884d261"],
                            },
                            {
                                "effective-name": "title",
                                "type": "field-or-flag",
                                "contents": [
                                    "GoodRead System Engineers Have Over-Privileged Access to Cloud Infrastructure Account"
                                ],
                            },
                            {
                                "effective-name": "description",
                                "type": "field-or-flag",
                                "contents": [
                                    "A user in the GoodRead cloud environment with the privileges of a system engineer can exceed the intended privileges for their related business function. They can delete all historical audit records and remove important security monitoring functions for the IFA Security Operations Center staff."
                                ],
                            },
                            {
                                "effective-name": "statement",
                                "type": "field-or-flag",
                                "contents": [
                                    "An account without proper least privilege design and implementation can be used to surreptitiously add, change, or delete cloud infrastructure to the too managing all links to IFA's communication to public citizens, potentially causing significant harm with no forensic evidence to recover the system. Regardless of the extent and duration of a potential incident, such a configuration greatly increases the risk of an insider threat if there were likely to a potential insider threat in the GoodRead Product Team.\n\nIf such an insider threat existed and acted with this misconfigruatio, the resulting event could cause significant financial and reputational risk to IFA's Administrator, executive staff, and the agency overall."
                                ],
                            },
                            {
                                "effective-name": "status",
                                "type": "field-or-flag",
                                "contents": ["investigating"],
                            },
                        ],
                    },
                    {
                        "group-as-name": "findings",
                        "contents": [
                            {
                                "effective-name": "uuid",
                                "type": "field-or-flag",
                                "contents": ["45d8a6c2-1368-4bad-9ba0-7141f0a32889"],
                            },
                            {
                                "effective-name": "title",
                                "type": "field-or-flag",
                                "contents": [
                                    "GoodRead AwesomeCloud Account's System Engineer Role Permits High Risk Actions"
                                ],
                            },
                            {
                                "effective-name": "description",
                                "type": "field-or-flag",
                                "contents": [
                                    "The assessor's security automation platform detected that the system engineer's role is permitted to perform the following actions in the GoodRead AwesomeCloud account.\n\n* Delete and reset account audit logs.\n* Add, change, or delete security monitoring configurations in the Awesome Security Monitor service used by the IFA Security Operations Center.\n\n\nThe system engineer is not permitted to modify these services and their role was incorrectly configured."
                                ],
                            },
                            {
                                "effective-name": "target",
                                "type": "assembly",
                                "contents": [
                                    {
                                        "effective-name": "type",
                                        "type": "field-or-flag",
                                        "contents": ["objective-id"],
                                    },
                                    {
                                        "effective-name": "target-id",
                                        "type": "field-or-flag",
                                        "contents": ["ac-6.1_obj"],
                                    },
                                    {
                                        "effective-name": "description",
                                        "type": "field-or-flag",
                                        "contents": ["This is a finding."],
                                    },
                                    {
                                        "effective-name": "status",
                                        "type": "assembly",
                                        "contents": [
                                            {
                                                "effective-name": "state",
                                                "type": "field-or-flag",
                                                "contents": ["not-satisfied"],
                                            }
                                        ],
                                    },
                                ],
                            },
                            {
                                "effective-name": "implementation-statement-uuid",
                                "type": "field-or-flag",
                                "contents": ["d5f9b263-965d-440b-99e7-77f5df670a11"],
                            },
                            {
                                "group-as-name": "related-observations",
                                "contents": [
                                    {
                                        "effective-name": "observation-uuid",
                                        "type": "field-or-flag",
                                        "contents": [
                                            "8807eb6e-0c05-43bc-8438-799739615e34"
                                        ],
                                    }
                                ],
                            },
                            {
                                "group-as-name": "related-risks",
                                "contents": [
                                    {
                                        "effective-name": "risk-uuid",
                                        "type": "field-or-flag",
                                        "contents": [
                                            "0cfa750e-3553-47ba-a7ba-cf84a884d261"
                                        ],
                                    }
                                ],
                            },
                        ],
                    },
                ],
            },
        ],
    }
]
