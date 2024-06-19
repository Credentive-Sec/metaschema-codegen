A = [
    {
        "effective_name": "assessment-results",
        "type": "assembly",
        "contents": [
            {
                "effective_name": "uuid",
                "type": "flag",
                "contents": "ec0dad37-54e0-40fd-a925-6d0bdea94c0d",
            },
            {
                "effective_name": "metadata",
                "type": "assembly",
                "contents": [
                    {
                        "effective_name": "title",
                        "type": "field",
                        "contents": [
                            "IFA GoodRead Continuous Monitoring Assessment Results June 2023"
                        ],
                    },
                    {
                        "effective_name": "last-modified",
                        "type": "field",
                        "contents": ["2024-02-01T13:57:28.355446-04:00"],
                    },
                    {
                        "effective_name": "version",
                        "type": "field",
                        "contents": ["202306-002"],
                    },
                    {
                        "effective_name": "oscal-version",
                        "type": "field",
                        "contents": ["1.1.2"],
                    },
                    {
                        "effective_name": "role",
                        "type": "assembly",
                        "contents": [
                            {
                                "effective_name": "id",
                                "type": "flag",
                                "contents": "assessor",
                            },
                            {
                                "effective_name": "title",
                                "type": "field",
                                "contents": ["IFA Security Controls Assessor"],
                            },
                        ],
                    },
                    {
                        "effective_name": "party",
                        "type": "assembly",
                        "contents": [
                            {
                                "effective_name": "uuid",
                                "type": "flag",
                                "contents": "e7730080-71ce-4b20-bec4-84f33136fd58",
                            },
                            {
                                "effective_name": "type",
                                "type": "flag",
                                "contents": "person",
                            },
                            {
                                "effective_name": "name",
                                "type": "field",
                                "contents": ["Amy Assessor"],
                            },
                            {
                                "effective_name": "member-of-organization",
                                "type": "field",
                                "contents": ["3a675986-b4ff-4030-b178-e953c2e55d64"],
                            },
                        ],
                    },
                    {
                        "effective_name": "party",
                        "type": "assembly",
                        "contents": [
                            {
                                "effective_name": "uuid",
                                "type": "flag",
                                "contents": "3a675986-b4ff-4030-b178-e953c2e55d64",
                            },
                            {
                                "effective_name": "type",
                                "type": "flag",
                                "contents": "organization",
                            },
                            {
                                "effective_name": "name",
                                "type": "field",
                                "contents": ["Important Federal Agency"],
                            },
                            {
                                "effective_name": "short-name",
                                "type": "field",
                                "contents": ["IFA"],
                            },
                        ],
                    },
                    {
                        "effective_name": "responsible-party",
                        "type": "assembly",
                        "contents": [
                            {
                                "effective_name": "role-id",
                                "type": "flag",
                                "contents": "assessor",
                            },
                            {
                                "effective_name": "party-uuid",
                                "type": "field",
                                "contents": ["e7730080-71ce-4b20-bec4-84f33136fd58"],
                            },
                        ],
                    },
                ],
            },
            {
                "effective_name": "local-definitions",
                "type": "assembly",
                "contents": [
                    {
                        "effective_name": "activity",
                        "type": "assembly",
                        "contents": [
                            {
                                "effective_name": "uuid",
                                "type": "flag",
                                "contents": "cf5d53fe-6043-4c68-9ed6-6b258909febf",
                            },
                            {
                                "effective_name": "title",
                                "type": "field",
                                "contents": [
                                    "Test System Elements for Least Privilege Design and Implementation"
                                ],
                            },
                            {
                                "effective_name": "description",
                                "type": "field",
                                "contents": [
                                    "<p>The activity and it steps will be performed by the assessor via their security automation platform to test least privilege design and implementation of the system's elements, specifically the cloud account infrastructure, as part of continuous monitoring.</p>"
                                ],
                            },
                            {
                                "effective_name": "step",
                                "type": "assembly",
                                "contents": [
                                    {
                                        "effective_name": "uuid",
                                        "type": "flag",
                                        "contents": "57f8cfb8-fc3f-41d3-b938-6ab421c92574",
                                    },
                                    {
                                        "effective_name": "title",
                                        "type": "field",
                                        "contents": [
                                            "Configure Cross-Account IAM Role Trust for GoodRead and Assessor AwesomeCloud\n                    Accounts"
                                        ],
                                    },
                                    {
                                        "effective_name": "description",
                                        "type": "field",
                                        "contents": [
                                            "<p>The GoodRead system engineer will coordinate with the assessor's engineering support staff to configure an IAM role trust. A service account for automation with its own role with the assessor's AwesomeCloud account can assume the role for read-only assessor operations within the GoodRead Product Team's AwesomeCloud account for continuous monitoring of least privilege.</p>"
                                        ],
                                    },
                                    {
                                        "effective_name": "remarks",
                                        "type": "field",
                                        "contents": [
                                            "<p>This step is complete.</p><p>GoodRead Product Team and SCA Engineering Support configured the latter's cross-account role trust and authentication and authorization in to the former's account on May 29, 2023.</p>"
                                        ],
                                    },
                                ],
                            },
                            {
                                "effective_name": "step",
                                "type": "assembly",
                                "contents": [
                                    {
                                        "effective_name": "uuid",
                                        "type": "flag",
                                        "contents": "976aadad-b1ce-475b-aa6c-e082537e7902",
                                    },
                                    {
                                        "effective_name": "title",
                                        "type": "field",
                                        "contents": [
                                            "Automate Cross-Account Login to GoodRead AwesomeCloud Account"
                                        ],
                                    },
                                    {
                                        "effective_name": "description",
                                        "type": "field",
                                        "contents": [
                                            "<p>The assessor's security automation platform will create a session from their dedicated will obtain access to the GoodRead Product Team's AwesomeCloud account with their single sign-on credentials to a read-only assessor role.</p>"
                                        ],
                                    },
                                    {
                                        "effective_name": "remarks",
                                        "type": "field",
                                        "contents": [
                                            "<p>This step is complete.</p><p>GoodRead Product Team and SCA Engineering Support tested scripts from the security automation platform interactively on May 30, 2023, to confirm they work ahead of June 2023 continuous monitoring cycle.</p>"
                                        ],
                                    },
                                ],
                            },
                            {
                                "effective_name": "step",
                                "type": "assembly",
                                "contents": [
                                    {
                                        "effective_name": "uuid",
                                        "type": "flag",
                                        "contents": "18ce4e19-7432-4484-8e75-2dd8f05668cf",
                                    },
                                    {
                                        "effective_name": "title",
                                        "type": "field",
                                        "contents": [
                                            "Analyze GoodRead Developer and System Engineer Roles for Least Privilege"
                                        ],
                                    },
                                    {
                                        "effective_name": "description",
                                        "type": "field",
                                        "contents": [
                                            "<p>Once authenticated and authorized with a cross-account session, the security automation pipeline will execute scripts developed and maintained by the assessor's engineering support staff. It will analyze the permitted actions for the developer and system engineer roles in the GoodRead Product Team's AwesomeCloud account to confirm they are designed and implement to facilitate only least privilege operation. Examples are included below.</p><ul><li>For the GoodRead developer role in their AwesomeCloud account, the developer role may only permit the user with this role to check the IP addresses and status of the Awesome Compute Service server instances. This role will not permit the user to create, change, or delete the instances. Similarly, the developer will permit a user to perform actions to see IP addresses of an Awesome Load Balancer instance, but not add, change, or delete the instances.</li><li>For the GoodRead system engineer role in their AwesomeCloud account, the system engineer role may only permit actions where the user can add, change, or delete instances for approved services (i.e. Awesome Compute Service, Awesome Load Balancer, et cetera). The role may not permit actions by the user for any other service.</li></ul>"
                                        ],
                                    },
                                ],
                            },
                            {
                                "effective_name": "related-controls",
                                "type": "assembly",
                                "contents": [
                                    {
                                        "effective_name": "control-selection",
                                        "type": "assembly",
                                        "contents": [],
                                    }
                                ],
                            },
                            {
                                "effective_name": "responsible-role",
                                "type": "assembly",
                                "contents": [
                                    {
                                        "effective_name": "role-id",
                                        "type": "flag",
                                        "contents": "assessor",
                                    },
                                    {
                                        "effective_name": "party-uuid",
                                        "type": "field",
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
                "effective_name": "result",
                "type": "assembly",
                "contents": [
                    {
                        "effective_name": "uuid",
                        "type": "flag",
                        "contents": "a1d20136-37e0-42aa-9834-4e9d8c36d798",
                    },
                    {
                        "effective_name": "title",
                        "type": "field",
                        "contents": [
                            "IFA GoodRead Continous Monitoring Results June 2023"
                        ],
                    },
                    {
                        "effective_name": "description",
                        "type": "field",
                        "contents": [
                            "<p>Automated monthly continuous monitoring of the GoodRead information system's cloud infrastructure recorded observations below. Additionally, contingent upon the confidence level of the observations and possible risks, confirmed findings may be opened.</p>"
                        ],
                    },
                    {
                        "effective_name": "start",
                        "type": "field",
                        "contents": ["2023-06-02T08:31:20-04:00"],
                    },
                    {
                        "effective_name": "end",
                        "type": "field",
                        "contents": ["2023-06-02T08:46:51-04:00"],
                    },
                    {
                        "effective_name": "local-definitions",
                        "type": "assembly",
                        "contents": [
                            {
                                "effective_name": "assessment-task",
                                "type": "assembly",
                                "contents": [
                                    {
                                        "effective_name": "uuid",
                                        "type": "flag",
                                        "contents": "35876484-aa4b-494d-95a2-0d1cc04eb47e",
                                    },
                                    {
                                        "effective_name": "type",
                                        "type": "flag",
                                        "contents": "action",
                                    },
                                    {
                                        "effective_name": "title",
                                        "type": "field",
                                        "contents": [
                                            "Test System Elements for Least Privilege Design and Implementation"
                                        ],
                                    },
                                    {
                                        "effective_name": "description",
                                        "type": "field",
                                        "contents": [
                                            "<p>The activity and it steps will be performed by the assessor via their security automation platform to test least privilege design and implementation of the system's elements, specifically the cloud account infrastructure, as part of continuous monitoring.</p>"
                                        ],
                                    },
                                    {
                                        "effective_name": "associated-activity",
                                        "type": "assembly",
                                        "contents": [
                                            {
                                                "effective_name": "activity-uuid",
                                                "type": "flag",
                                                "contents": "cf5d53fe-6043-4c68-9ed6-6b258909febf",
                                            },
                                            {
                                                "effective_name": "subject",
                                                "type": "assembly",
                                                "contents": [
                                                    {
                                                        "effective_name": "type",
                                                        "type": "flag",
                                                        "contents": "component",
                                                    }
                                                ],
                                            },
                                        ],
                                    },
                                ],
                            }
                        ],
                    },
                    {
                        "effective_name": "reviewed-controls",
                        "type": "assembly",
                        "contents": [
                            {
                                "effective_name": "control-selection",
                                "type": "assembly",
                                "contents": [],
                            }
                        ],
                    },
                    {
                        "effective_name": "observation",
                        "type": "assembly",
                        "contents": [
                            {
                                "effective_name": "uuid",
                                "type": "flag",
                                "contents": "8807eb6e-0c05-43bc-8438-799739615e34",
                            },
                            {
                                "effective_name": "title",
                                "type": "field",
                                "contents": [
                                    "AwesomeCloud IAM Roles Test - GoodRead System Engineer Role"
                                ],
                            },
                            {
                                "effective_name": "description",
                                "type": "field",
                                "contents": [
                                    "<p>Test AwesomeCloud IAM Roles for least privilege design and implementation.</p>"
                                ],
                            },
                            {
                                "effective_name": "method",
                                "type": "field",
                                "contents": ["TEST"],
                            },
                            {
                                "effective_name": "type",
                                "type": "field",
                                "contents": ["finding"],
                            },
                            {
                                "effective_name": "collected",
                                "type": "field",
                                "contents": ["2023-06-02T08:31:20-04:00"],
                            },
                            {
                                "effective_name": "expires",
                                "type": "field",
                                "contents": ["2023-07-01T00:00:00-04:00"],
                            },
                            {
                                "effective_name": "remarks",
                                "type": "field",
                                "contents": [
                                    "<p>The assessor's security automation platform analyzed all roles specific to the GoodRead Product Team, not those managed by the Office of Information Technology. The <code>IFA-GoodRead-SystemEnginer</code> role in their respective AwesomeCloud account permitted use of the following high-risk actions.</p><ul><li>awesomecloud:auditlog:DeleteAccountAuditLog</li><li>awesomecloud:secmon:AdministerConfigurations</li></ul><p>Both of these actions are overly permissive and not appropriate for the business function of the staff member assigned this role.</p>"
                                ],
                            },
                        ],
                    },
                    {
                        "effective_name": "observation",
                        "type": "assembly",
                        "contents": [
                            {
                                "effective_name": "uuid",
                                "type": "flag",
                                "contents": "4a2fb32e-9be9-43cf-b717-e9e47de061bd",
                            },
                            {
                                "effective_name": "title",
                                "type": "field",
                                "contents": [
                                    "AwesomeCloud IAM Roles Test - GoodRead Developer Role"
                                ],
                            },
                            {
                                "effective_name": "description",
                                "type": "field",
                                "contents": [
                                    "<p>Test AwesomeCloud IAM Roles for least privilege design and implementation.</p>"
                                ],
                            },
                            {
                                "effective_name": "method",
                                "type": "field",
                                "contents": ["TEST"],
                            },
                            {
                                "effective_name": "type",
                                "type": "field",
                                "contents": ["finding"],
                            },
                            {
                                "effective_name": "collected",
                                "type": "field",
                                "contents": ["2023-06-02T08:31:20-04:00"],
                            },
                            {
                                "effective_name": "expires",
                                "type": "field",
                                "contents": ["2023-07-01T00:00:00-04:00"],
                            },
                            {
                                "effective_name": "remarks",
                                "type": "field",
                                "contents": [
                                    "<p>The assessor's security automation platform detected that the developer's role is permitted to perform only permissible actions in the GoodRead AwesomeCloud account in accordance with the agency's least privilege policy and procedures.</p>"
                                ],
                            },
                        ],
                    },
                    {
                        "effective_name": "risk",
                        "type": "assembly",
                        "contents": [
                            {
                                "effective_name": "uuid",
                                "type": "flag",
                                "contents": "0cfa750e-3553-47ba-a7ba-cf84a884d261",
                            },
                            {
                                "effective_name": "title",
                                "type": "field",
                                "contents": [
                                    "GoodRead System Engineers Have Over-Privileged Access to Cloud Infrastructure\n                Account"
                                ],
                            },
                            {
                                "effective_name": "description",
                                "type": "field",
                                "contents": [
                                    "<p>A user in the GoodRead cloud environment with the privileges of a system engineer can exceed the intended privileges for their related business function. They can delete all historical audit records and remove important security monitoring functions for the IFA Security Operations Center staff.</p>"
                                ],
                            },
                            {
                                "effective_name": "statement",
                                "type": "field",
                                "contents": [
                                    "<p>An account without proper least privilege design and implementation can be used to surreptitiously add, change, or delete cloud infrastructure to the too managing all links to IFA's communication to public citizens, potentially causing significant harm with no forensic evidence to recover the system. Regardless of the extent and duration of a potential incident, such a configuration greatly increases the risk of an insider threat if there were likely to a potential insider threat in the GoodRead Product Team.</p><p>If such an insider threat existed and acted with this misconfigruatio, the resulting event could cause significant financial and reputational risk to IFA's Administrator, executive staff, and the agency overall.</p>"
                                ],
                            },
                            {
                                "effective_name": "status",
                                "type": "field",
                                "contents": ["investigating"],
                            },
                        ],
                    },
                    {
                        "effective_name": "finding",
                        "type": "assembly",
                        "contents": [
                            {
                                "effective_name": "uuid",
                                "type": "flag",
                                "contents": "45d8a6c2-1368-4bad-9ba0-7141f0a32889",
                            },
                            {
                                "effective_name": "title",
                                "type": "field",
                                "contents": [
                                    "GoodRead AwesomeCloud Account's System Engineer Role Permits High Risk Actions"
                                ],
                            },
                            {
                                "effective_name": "description",
                                "type": "field",
                                "contents": [
                                    "<p>The assessor's security automation platform detected that the system engineer's role is permitted to perform the following actions in the GoodRead AwesomeCloud account.</p><ul><li>Delete and reset account audit logs.</li><li>Add, change, or delete security monitoring configurations in the Awesome Security Monitor service used by the IFA Security Operations Center.</li></ul><p>The system engineer is not permitted to modify these services and their role was incorrectly configured.</p>"
                                ],
                            },
                            {
                                "effective_name": "target",
                                "type": "assembly",
                                "contents": [
                                    {
                                        "effective_name": "type",
                                        "type": "flag",
                                        "contents": "objective-id",
                                    },
                                    {
                                        "effective_name": "target-id",
                                        "type": "flag",
                                        "contents": "ac-6.1_obj",
                                    },
                                    {
                                        "effective_name": "description",
                                        "type": "field",
                                        "contents": ["<p>This is a finding.</p>"],
                                    },
                                ],
                            },
                            {
                                "effective_name": "implementation-statement-uuid",
                                "type": "field",
                                "contents": ["d5f9b263-965d-440b-99e7-77f5df670a11"],
                            },
                        ],
                    },
                ],
            },
        ],
    }
]
