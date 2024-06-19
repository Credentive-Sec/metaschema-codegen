from __future__ import annotations

from .assembly import Assembly, Field, Context

# we can't read a metaschema without some knowledge of what the schema is
# the schema for metaschema itself is no exception
# so we have to hard-code metaschema's model
# (or just enough of it so that the code above can use it as if it were metaschema's model)
# that's what this is
# beyond here be dragons


class MetaschemaContext(Context):
    def __init__(self):
        metaschema = Assembly()
        global_assembly = Assembly()
        global_field = Assembly()
        global_flag = Assembly()
        inline_assembly = Assembly()
        inline_assembly = Assembly()
        inline_flag = Assembly()
        assembly_reference = Assembly()
        field_reference = Assembly()
        flag_reference = Assembly()
        choice = Assembly()
        self.metaschema = Assembly()

        self.metaschema._setschema(metaschema)
        metaschema._setschema(global_assembly)
        global_assembly._setschema(inline_assembly)
        global_field._setschema(inline_assembly)
        global_flag._setschema(inline_assembly)
        inline_assembly._setschema(global_assembly)
        inline_assembly._setschema(global_assembly)
        inline_flag._setschema(global_assembly)
        assembly_reference._setschema(global_assembly)
        field_reference._setschema(global_assembly)
        flag_reference._setschema(global_assembly)
        choice._setschema(inline_assembly)

        singleChoice = Assembly()
        singleChoice._setschema(global_assembly)

        global_assembly.name = "define-assembly"
        global_field.name = "define-field"
        global_flag.name = "define-flag"
        inline_assembly.name = "inline-define-assembly"
        inline_assembly.name = "inline-define-field"
        inline_flag.name = "inline-define-flag"
        assembly_reference.name = "assembly-reference"
        field_reference.name = "field-reference"
        flag_reference.name = "flag-reference"

        def iAsmDefInst(
            name,
            flags=[],
            model=[],
            groupName=None,
            rq=False,
            cstrt=[],
            fn=None,
            dsc=None,
            props=[],
            jskey=None,
            rmrks=None,
            ex=[],
        ):
            toRet = Assembly()
            toRet._setschema(inline_assembly)
            toRet.name = name
            toRet._flags["min-occurs"] = "1" if rq else "0"
            toRet._flags["max-occurs"] = "1" if groupName is None else "unbounded"
            toRet._initContents(10)
            toRet[0] = Field(fn)
            toRet[1] = Field(dsc)
            toRet[2] = props
            toRet[3] = jskey
            if groupName is None:
                toRet[4] = None
            else:
                toRet[4] = Assembly()
                toRet[4]._setschema(groupAs)
                toRet[4].name = groupName
                toRet[4]._flags["in-json"] = "ARRAY"
            toRet[5] = flags
            toRet[6] = model
            toRet[7] = cstrt
            toRet[8] = rmrks
            toRet[9] = ex
            return toRet

        definitionName = Assembly()
        definitionName._setschema(inline_flag)
        definitionName.name = "name"
        definitionName.required = "yes"
        definitionReference = Assembly()
        definitionReference._setschema(inline_flag)
        definitionReference.name = "ref"
        definitionReference.required = "yes"
        defaultValue = Assembly()
        defaultValue._setschema(inline_flag)
        defaultValue.name = "default"
        cardinalityMinOccurs = Assembly()
        cardinalityMinOccurs._setschema(inline_flag)
        cardinalityMinOccurs.name = "min-occurs"
        cardinalityMinOccurs.default = "0"
        cardinalityMaxOccurs = Assembly()
        cardinalityMaxOccurs._setschema(inline_flag)
        cardinalityMaxOccurs.name = "max-occurs"
        cardinalityMaxOccurs.default = "1"

        groupAs = Assembly()

        anyData = iAsmDefInst("any")

        formalName = Assembly()
        formalName._setschema(inline_assembly)
        formalName.name = "formal-name"
        formalName._initContents(10)
        formalName[2] = []
        formalName["flags"] = []
        description = Assembly()
        description._setschema(inline_assembly)
        description.name = "description"
        description._initContents(10)
        description["flags"] = []
        props = Assembly()
        props._setschema(inline_assembly)
        props.name = "prop"  # should be property
        props._flags["max-occurs"] = "unbounded"
        props._initContents(10)
        props["group-as"] = Assembly()  # group-as props
        props["group-as"]._setschema(groupAs)
        props["group-as"].name = "props"
        props["group-as"]._flags["in-json"] = "ARRAY"
        props["flags"] = [Assembly(), Assembly(), Assembly()]
        props["flags"][0]._setschema(inline_flag)
        props["flags"][0].name = "name"
        props["flags"][0]._flags["as-type"] = "token"
        props["flags"][0].required = "yes"
        props["flags"][1]._setschema(inline_flag)
        props["flags"][1].name = "namespace"
        props["flags"][1]._flags["as-type"] = "uri"
        props["flags"][1].default = "http://csrc.nist.gov/ns/oscal/metaschema/1.0"
        props["flags"][2]._setschema(inline_flag)
        props["flags"][2].name = "value"
        props["flags"][2]._flags["as-type"] = "token"
        props["flags"][2].required = "yes"
        props["model"] = []
        usename = Assembly()
        usename._setschema(inline_assembly)
        usename.name = "use-name"
        usename._flags["as-type"] = "token"
        usename._initContents(10)
        usename["flags"] = []
        jsonKey = Assembly()
        jsonKey._setschema(inline_assembly)
        jsonKey.name = "json-key"
        jsonKey._initContents(10)
        jsonKey["flags"] = [Assembly()]
        jsonKey["flags"][0]._setschema(inline_flag)
        jsonKey["flags"][0].name = "flag-ref"
        jsonKey["flags"][0]._flags["as-type"] = "token"
        jsonKey["flags"][0].required = "yes"
        jsonKey["model"] = []
        groupAs._setschema(inline_assembly)
        groupAs.name = "group-as"
        groupAs._initContents(10)
        groupAs["flags"] = [Assembly(), Assembly(), Assembly()]
        groupAs["flags"][0]._setschema(inline_flag)
        groupAs["flags"][0].name = "name"
        groupAs["flags"][0]._flags["as-type"] = "token"
        groupAs["flags"][0].required = "yes"
        groupAs["flags"][1]._setschema(inline_flag)
        groupAs["flags"][1].name = "in-json"
        groupAs["flags"][1]._flags["as-type"] = "token"
        groupAs["flags"][1].default = "SINGLETON_OR_ARRAY"
        groupAs["flags"][2]._setschema(inline_flag)
        groupAs["flags"][2].name = "in-xml"
        groupAs["flags"][2]._flags["as-type"] = "token"
        groupAs["flags"][2].default = "UNGROUPED"
        groupAs["model"] = []
        remarks = Assembly()
        remarks._setschema(inline_assembly)
        remarks.name = "remarks"
        remarks._flags["as-type"] = "markup-multiline"
        remarks._initContents(10)
        remarks["flags"] = [Assembly()]
        remarks["flags"][0]._setschema(inline_flag)
        remarks["flags"][0].name = "class"
        remarks["flags"][0]._flags["as-type"] = "token"
        remarks["flags"][0].default = "ALL"
        example = Assembly()
        example._setschema(inline_assembly)
        example.name = "example"
        example._initContents(10)
        example[4] = Assembly()  # group-as
        example[5] = []  # skipping some for now
        example[6] = [
            description,  # define-field description
            remarks,  # field remarks
            anyData,  # any
        ]

        jsonvaluekeyflagchoice = Assembly()
        jsonvaluekeyflagchoice._setschema(singleChoice)
        jsonvaluekeyflagchoice._initContents(1)
        jsonvaluekeyflagchoice[0] = [
            Assembly(),  # define-field json-value-key
            Assembly(),  # assembly json-value-key-flag
        ]
        jsonvaluekeyflagchoice[0][0]._setschema(inline_assembly)
        jsonvaluekeyflagchoice[0][0].name = "json-value-key"
        jsonvaluekeyflagchoice[0][0]._flags["as-type"] = "token"
        jsonvaluekeyflagchoice[0][0]._initContents(10)
        jsonvaluekeyflagchoice[0][0]["flags"] = []
        jsonvaluekeyflagchoice[0][1]._setschema(inline_assembly)
        jsonvaluekeyflagchoice[0][1].name = "json-value-key-flag"
        jsonvaluekeyflagchoice[0][1]._initContents(10)
        jsonvaluekeyflagchoice[0][1][5] = [Assembly()]
        jsonvaluekeyflagchoice[0][1][5][0]._setschema(inline_flag)
        jsonvaluekeyflagchoice[0][1][5][0].name = "flag-ref"
        jsonvaluekeyflagchoice[0][1][5][0]._flags["as-type"] = "token"
        jsonvaluekeyflagchoice[0][1][5][0].required = "yes"
        jsonvaluekeyflagchoice[0][1][5][0]._initContents(6)

        asTypeSimple = Assembly()
        asTypeSimple._setschema(global_flag)
        asTypeSimple.name = "as-type-simple"
        asTypeSimple._flags["as-type"] = "token"
        asTypeSimple._initContents(7)
        asTypeSimple[3] = Field("as-type")
        asTypeSimple[3]._setschema(usename)
        # the only other thing it has is constraints.

        constraintLetExpr = Assembly()
        constraintLetExpr._setschema(inline_assembly)
        constraintLetExpr.name = "let"  #'constraint-let-expression'
        constraintLetExpr._initContents(10)
        constraintLetExpr["flags"] = [Assembly(), Assembly()]
        constraintLetExpr["flags"][0]._setschema(inline_flag)
        constraintLetExpr["flags"][0].name = "var"
        constraintLetExpr["flags"][0]._flags["as-type"] = "token"
        constraintLetExpr["flags"][0].required = "yes"
        constraintLetExpr["flags"][1].name = "expression"
        constraintLetExpr["flags"][1].required = "yes"
        constraintLetExpr["model"] = [remarks]

        cstrtId = Assembly()
        cstrtId._setschema(inline_flag)
        cstrtId.name = "id"  #'constraint-identifier'
        cstrtId._flags["as-type"] = "token"
        cstrtSvty = Assembly()
        cstrtSvty._setschema(inline_flag)
        cstrtSvty.name = "level"  #'constraint-severity-level'
        cstrtSvty._flags["as-type"] = "token"
        cstrtSvty.default = "ERROR"
        cstrtAllowOther = Assembly()
        cstrtAllowOther._setschema(inline_flag)
        cstrtAllowOther.name = "allow-other"  #'constraint-allow-other'
        cstrtAllowOther._flags["as-type"] = "token"
        cstrtAllowOther.default = "no"
        cstrtMatchesRegex = Assembly()
        cstrtMatchesRegex._setschema(inline_flag)
        cstrtMatchesRegex.name = "regex"  #'constraint-matches-regex'

        cstrtEx = Assembly()
        cstrtEx._setschema(inline_flag)
        cstrtEx.name = "extensible"  #'constraint-extensible'
        cstrtEx._flags["as-type"] = "token"
        cstrtEx.default = "external"
        cstrtTg = Assembly()
        cstrtTg._setschema(inline_flag)
        cstrtTg.name = "target"  #'constraint-target'
        cstrtTg.required = "yes"
        cstrtValueEnum = Assembly()
        cstrtValueEnum._setschema(inline_assembly)
        cstrtValueEnum.name = "enum"  #'constraint-value-enum'
        cstrtValueEnum._flags["as-type"] = "markup-line"
        cstrtValueEnum._initContents(10)
        cstrtValueEnum[3] = Field("remarks")
        cstrtValueEnum[3]._setschema(jsonKey)
        cstrtValueEnum[6] = [Assembly(), Assembly()]
        cstrtValueEnum[6][0]._setschema(inline_flag)
        cstrtValueEnum[6][0].name = "value"
        cstrtValueEnum[6][0].required = "yes"
        cstrtValueEnum[6][0]._flags["min-occurs"] = "1"
        cstrtValueEnum[6][0]._flags["max-occurs"] = "unbounded"
        cstrtValueEnum[6][1]._setschema(inline_flag)
        cstrtValueEnum[6][1].name = "deprecated"

        expectCstrtMsg = Assembly()
        expectCstrtMsg._setschema(inline_assembly)
        expectCstrtMsg.name = "message"  # expect-constraint-message
        expectCstrtMsg._initContents(10)
        expectCstrtMsg["flags"] = []
        keyCstrtFld = Assembly()
        keyCstrtFld._setschema(inline_assembly)
        keyCstrtFld.name = "key-field"  #'key-constraint-field'
        keyCstrtFld._flags["min-occurs"] = "1"
        keyCstrtFld._flags["max-occurs"] = "unbounded"
        keyCstrtFld._initContents(10)
        keyCstrtFld[4] = Assembly()
        keyCstrtFld[4]._setschema(groupAs)
        keyCstrtFld[4].name = "key-fields"
        keyCstrtFld[4]._flags["in-json"] = "ARRAY"
        keyCstrtFld["flags"] = [cstrtTg, Assembly()]
        keyCstrtFld["flags"][1]._setschema(inline_flag)
        keyCstrtFld["flags"][1].name = "pattern"
        keyCstrtFld["model"] = [remarks]
        indexName = Assembly()
        indexName._setschema(inline_flag)
        indexName.name = "name"  #'index-name'
        indexName._flags["as-type"] = "token"
        indexName.required = "yes"

        flagAllowVals = Assembly()
        flagAllowVals._setschema(inline_assembly)
        flagAllowVals.name = "allowed-values"
        flagAllowVals._initContents(10)
        flagAllowVals["flags"] = [cstrtId, cstrtSvty, cstrtAllowOther, cstrtEx]
        flagAllowVals["model"] = [
            formalName,
            description,
            props,
            cstrtValueEnum,  # field constraint-value-enum
            remarks,
        ]
        flagAllowVals["model"][3]._setschema(inline_assembly)
        flagAllowVals["model"][3].name = "enum"
        flagAllowVals["model"][3]._flags["min-occurs"] = "1"
        flagAllowVals["model"][3]._flags["max-occurs"] = "unbounded"
        flagAllowVals["model"][3]._initContents(10)
        flagAllowVals["model"][3][5] = Assembly()
        flagAllowVals["model"][3][5]._setschema(groupAs)
        flagAllowVals["model"][3][5].name = "enums"
        flagAllowVals["model"][3][5]._flags["in-json"] = "ARRAY"
        flagExpect = Assembly()
        flagExpect._setschema(inline_assembly)
        flagExpect.name = "expect"
        flagExpect._initContents(10)
        flagExpect["flags"] = [cstrtId, cstrtSvty, cstrtTg]
        flagExpect["model"] = [
            formalName,
            description,
            props,
            expectCstrtMsg,  # field expect-constraint-message
            remarks,
        ]
        flagIndexHasKey = Assembly()
        flagIndexHasKey._setschema(inline_assembly)
        flagIndexHasKey.name = "index-has-key"
        flagIndexHasKey._initContents(10)
        flagIndexHasKey["flags"] = [cstrtId, cstrtSvty, indexName]
        flagIndexHasKey["model"] = [
            formalName,
            description,
            props,
            keyCstrtFld,  # assembly key-constraint-field
            remarks,
        ]
        flagMatches = Assembly()
        flagMatches._setschema(inline_assembly)
        flagMatches.name = "matches"
        flagMatches._initContents(10)
        flagMatches["flags"] = [cstrtId, cstrtSvty, cstrtMatchesRegex, asTypeSimple]
        flagMatches["model"] = [formalName, description, props, remarks]

        tgAllowVals = Assembly()
        tgAllowVals._setschema(inline_assembly)
        tgAllowVals.name = "allowed-values"
        tgAllowVals._initContents(10)
        tgAllowVals["flags"] = [cstrtId, cstrtSvty, cstrtAllowOther, cstrtEx, cstrtTg]
        tgAllowVals["model"] = [
            formalName,
            description,
            props,
            cstrtValueEnum,  # field constraint-value-enum
            remarks,
        ]
        tgAllowVals["model"][3]._setschema(inline_assembly)
        tgAllowVals["model"][3].name = "enum"
        tgAllowVals["model"][3]._flags["min-occurs"] = "1"
        tgAllowVals["model"][3]._flags["max-occurs"] = "unbounded"
        tgAllowVals["model"][3]._initContents(10)
        tgAllowVals["model"][3][5] = Assembly()
        tgAllowVals["model"][3][5]._setschema(groupAs)
        tgAllowVals["model"][3][5].name = "enums"
        tgAllowVals["model"][3][5]._flags["in-json"] = "ARRAY"
        tgExpect = Assembly()
        tgExpect._setschema(inline_assembly)
        tgExpect.name = "expect"
        tgExpect._initContents(10)
        tgExpect["flags"] = [
            cstrtId,
            cstrtSvty,
            cstrtTg,
            cstrtTg,
        ]  # first cstrtTg has use-name test. can't show this with the same inline def...
        tgExpect["model"] = [
            formalName,
            description,
            props,
            expectCstrtMsg,  # field expect-constraint-message
            remarks,
        ]
        tgIndexHasKey = Assembly()
        tgIndexHasKey._setschema(inline_assembly)
        tgIndexHasKey.name = "index-has-key"
        tgIndexHasKey._initContents(10)
        tgIndexHasKey["flags"] = [cstrtId, cstrtSvty, indexName, cstrtTg]
        tgIndexHasKey["model"] = [
            formalName,
            description,
            props,
            keyCstrtFld,  # assembly key-constraint-field
            remarks,
        ]
        tgMatches = Assembly()
        tgMatches._setschema(inline_assembly)
        tgMatches.name = "matches"
        tgMatches._initContents(10)
        tgMatches["flags"] = [
            cstrtId,
            cstrtSvty,
            cstrtMatchesRegex,
            asTypeSimple,
            cstrtTg,
        ]
        tgMatches["model"] = [formalName, description, props, remarks]
        tgIsUnique = Assembly()
        tgIsUnique._setschema(inline_assembly)
        tgIsUnique.name = "is-unique"  # targeted-is-unique-constraint
        tgIsUnique._initContents(10)
        tgIsUnique["flags"] = [cstrtId, cstrtSvty, cstrtTg]
        tgIsUnique["model"] = [formalName, description, props, keyCstrtFld, remarks]
        tgIndex = Assembly()
        tgIndex._setschema(inline_assembly)
        tgIndex.name = "index"  # targeted-index-constraint
        tgIndex._initContents(10)
        tgIndex["flags"] = [cstrtId, cstrtSvty, indexName, cstrtTg]
        tgIndex["model"] = [formalName, description, props, keyCstrtFld, remarks]
        tgHasCardinality = Assembly()
        tgHasCardinality._setschema(inline_assembly)
        tgHasCardinality.name = "has-cardinality"  # targeted-has-cardinality-constraint
        tgHasCardinality._initContents(10)
        tgHasCardinality["flags"] = [
            cstrtId,
            cstrtSvty,
            cardinalityMinOccurs,
            cardinalityMaxOccurs,
            cstrtTg,
        ]
        tgHasCardinality["model"] = [formalName, description, props, remarks]

        asmConstraints = Assembly()
        asmConstraints._setschema(inline_assembly)
        asmConstraints.name = "constraint"  # assembly-constraints
        asmConstraints._initContents(10)
        asmConstraints["flags"] = []
        asmConstraints["model"] = [
            constraintLetExpr,  # assembly constraint-let-expression
            Assembly(),  # choice-group rules
        ]
        asmConstraints["model"][1]._setschema(choice)
        asmConstraints["model"][1]._flags["min-occurs"] = "1"
        asmConstraints["model"][1]._flags["max-occurs"] = "unbounded"
        asmConstraints["model"][1]._initContents(5)
        asmConstraints["model"][1][1] = Assembly()
        asmConstraints["model"][1][1]._setschema(groupAs)
        asmConstraints["model"][1][1].name = "rules"
        asmConstraints["model"][1][1]._flags["in-json"] = "ARRAY"
        asmConstraints["model"][1][2] = Field("object-type")
        asmConstraints["model"][1][3] = [
            tgAllowVals,  # assembly targeted-allowed-values constraint
            tgExpect,  # assembly targeted-expect-constraint
            tgIndexHasKey,  # assembly targeted-index-has-key-constraint
            tgMatches,  # assembly targeted-matches-constraint
            tgIsUnique,  # assembly targeted-is-unique-constraint
            tgIndex,  # assembly targeted-index-constraint
            tgHasCardinality,  # assembly targeted-has-cardinality-constraint
        ]

        fieldConstraints = Assembly()
        fieldConstraints._setschema(inline_assembly)
        fieldConstraints.name = "constraint"  # field-constraints
        fieldConstraints._initContents(10)
        fieldConstraints["flags"] = []
        fieldConstraints["model"] = [
            constraintLetExpr,  # assembly constraint-let-expression
            Assembly(),  # choice-group rules
        ]
        fieldConstraints["model"][1]._setschema(choice)
        fieldConstraints["model"][1]._flags["min-occurs"] = "1"
        fieldConstraints["model"][1]._flags["max-occurs"] = "unbounded"
        fieldConstraints["model"][1]._initContents(5)
        fieldConstraints["model"][1][1] = Assembly()
        fieldConstraints["model"][1][1]._setschema(groupAs)
        fieldConstraints["model"][1][1].name = "rules"
        fieldConstraints["model"][1][1]._flags["in-json"] = "ARRAY"
        fieldConstraints["model"][1][2] = Field("object-type")
        fieldConstraints["model"][1][3] = [
            tgAllowVals,  # assembly targeted-allowed-values constraint
            tgExpect,  # assembly targeted-expect-constraint
            tgIndexHasKey,  # assembly targeted-index-has-key-constraint
            tgMatches,  # assembly targeted-matches-constraint
        ]
        flagConstraints = Assembly()
        flagConstraints._setschema(inline_assembly)
        flagConstraints.name = "constraint"  # flag-constraints
        flagConstraints._initContents(10)
        flagConstraints["flags"] = []
        flagConstraints["model"] = [
            constraintLetExpr,  # assembly constraint-let-expression
            Assembly(),  # choice-group rules
        ]
        flagConstraints["model"][1]._setschema(choice)
        flagConstraints["model"][1]._flags["min-occurs"] = "1"
        flagConstraints["model"][1]._flags["max-occurs"] = "unbounded"
        flagConstraints["model"][1]._initContents(5)
        flagConstraints["model"][1][1] = Assembly()
        flagConstraints["model"][1][1]._setschema(groupAs)
        flagConstraints["model"][1][1].name = "rules"
        flagConstraints["model"][1][1]._flags["in-json"] = "ARRAY"
        flagConstraints["model"][1][2] = Field("object-type")
        flagConstraints["model"][1][3] = [
            flagAllowVals,  # assembly flag-allowed-values
            flagExpect,  # assembly flag-expect
            flagIndexHasKey,  # assembly flag-index-has-key
            flagMatches,  # assembly flag-matches
        ]

        fieldInXmlFlag = Assembly()
        fieldInXmlFlag._setschema(inline_flag)
        fieldInXmlFlag.name = "in-xml"
        fieldInXmlFlag._flags["as-type"] = "token"
        fieldInXmlFlag.default = "WRAPPED"

        flags = Assembly()
        flags._setschema(choice)
        flags._flags["min-occurs"] = "0"
        flags._flags["max-occurs"] = "unbounded"
        flags._initContents(5)
        flags[1] = Assembly()
        flags[1]._setschema(groupAs)
        flags[1].name = "flags"
        flags[1]._flags["in-json"] = "ARRAY"
        flags[3] = [flag_reference, inline_flag]

        model = Assembly()
        model._setschema(choice)
        model._flags["min-occurs"] = "0"
        model._flags["max-occurs"] = "unbounded"
        model._initContents(5)
        model[1] = Assembly()
        model[1]._setschema(groupAs)
        model[1].name = "model"
        model[1]._flags["in-json"] = "ARRAY"
        model[1]._flags["in-xml"] = "GROUPED"
        model[3] = [
            assembly_reference,
            inline_assembly,
            field_reference,
            inline_assembly,
            choice,
            singleChoice,
        ]

        global_assembly.name = "define-assembly"
        global_assembly._contents.append(None)  # formal-name
        global_assembly._contents.append(None)  # description
        global_assembly._contents.append([])  # props
        global_assembly._contents.append(None)  # choice?
        global_assembly._contents.append(None)  # json-key
        global_assembly._contents.append(
            [definitionName]
        )  # leaving 3 other flags out for now
        global_assembly._contents.append(
            [  # model
                formalName,  # field formal-name
                description,  # field description
                props,  # assembly property*
                Assembly(),  # choice (use-name/root-name)
                jsonKey,  # assembly json-key
                flags,  # choice (flags)
                model,  # choice (assembly-model)
                asmConstraints,  # assembly assembly-constraints
                remarks,  # field remarks
                example,  # assembly examples
            ]
        )
        global_assembly[6][3]._setschema(singleChoice)
        global_assembly[6][3]._initContents(1)
        global_assembly[6][3][0] = [usename, Assembly()]  # define-field root-name
        global_assembly[6][3][0][1]._setschema(inline_assembly)
        global_assembly[6][3][0][1].name = "root-name"
        global_assembly[6][3][0][1]._flags["as-type"] = "token"
        global_assembly[6][3][0][1]._flags["min-occurs"] = "1"
        global_assembly[6][3][0][1]._initContents(10)
        global_assembly[6][3][0][1][
            "flags"
        ] = []  # actually there is one flag referrenced, alt-name-index

        inline_assembly.name = "inline-define-assembly"
        object.__setattr__(
            inline_assembly, "_contents", [None, None, None, None, None, None, None]
        )
        inline_assembly[0] = Field("Inline Assembly Definition")  # formal-name
        inline_assembly[3] = Field("define-assembly")
        inline_assembly[5] = [
            definitionName,
            cardinalityMinOccurs,
            cardinalityMaxOccurs,
        ]  # leaving out 3 other keys
        inline_assembly[6] = [
            formalName,  # field formal-name
            description,  # field description
            props,  # assembly property*
            jsonKey,  # assembly json-key
            groupAs,  # assembly group-as
            flags,  # choice-group flags
            model,  # choice (assembly-model)
            asmConstraints,  # assembly assembly-constraints
            remarks,  # field remarks
            example,  # assembly example
        ]

        global_field.name = "define-field"
        object.__setattr__(
            global_field, "_contents", [None, None, None, None, None, None, None]
        )
        global_field[5] = [definitionName, defaultValue]  # leaving out others i'm sure
        global_field[6] = [
            formalName,  # field formal-name
            description,  # field description
            props,  # assembly property*
            usename,  # field use-name
            jsonKey,  # assembly json-key
            jsonvaluekeyflagchoice,  # choice (json-value-key or json-value-key-flag)
            flags,  # choice-group flags
            fieldConstraints,  # assembly field-constraints
            remarks,  # field remarks
            example,  # assembly example
        ]

        inline_assembly.name = "inline-define-field"
        object.__setattr__(
            inline_assembly, "_contents", [None, None, None, None, None, None, None]
        )
        inline_assembly[3] = Field("define-field")
        inline_assembly[5] = [
            definitionName,
            defaultValue,
            cardinalityMinOccurs,
            cardinalityMaxOccurs,
            fieldInXmlFlag,
        ]
        inline_assembly[6] = [
            formalName,  # field formal-name
            description,  # field description
            props,  # assembly property*
            jsonKey,  # json-key
            jsonvaluekeyflagchoice,  # choice (json-value-key or json-value-key-flag)
            groupAs,  # assembly group-as
            flags,  # choice-group (flags)
            fieldConstraints,  # assembly field-constraints
            remarks,  # field remarks
            example,  # assembly examples
        ]

        global_flag.name = "define-flag"
        global_flag._initContents(9)
        global_flag[5] = [definitionName, Assembly(), defaultValue]
        global_flag[5][1]._setschema(flag_reference)
        global_flag[5][1].ref = "as-type-simple"
        global_flag[5][1].default = "string"
        global_flag[5][1]._initContents(6)
        global_flag[6] = [
            formalName,  # field formal-name
            description,  # field description
            props,  # assembly property*
            usename,  # field use-name
            flagConstraints,  # assembly flag-constraints
            remarks,  # field remarks
            example,  # assembly examples
        ]
        inline_flag.name = "inline-define-flag"
        inline_flag._initContents(10)
        inline_flag[3] = Field("define-flag")
        inline_flag[5] = [definitionName, Assembly(), defaultValue]
        inline_flag[5][1]._setschema(flag_reference)
        inline_flag[5][1].ref = "as-type-simple"
        inline_flag[5][1].default = "string"
        inline_flag[5][1]._initContents(6)
        inline_flag[6] = [
            formalName,  # field formal-name
            description,  # field description
            props,  # assembly property*
            flagConstraints,  # assembly flag-constraints
            remarks,  # field remarks
            example,  # assembly examples
        ]

        assembly_reference.name = "assembly-reference"
        assembly_reference._initContents(10)
        assembly_reference[3] = Field("assembly")
        assembly_reference[5] = [
            definitionReference,
            cardinalityMinOccurs,
            cardinalityMaxOccurs,
        ]
        assembly_reference[6] = [
            formalName,  # field formal-name
            description,  # field description
            props,  # assembly property*
            usename,  # field use-name
            groupAs,  # assembly group-as
            remarks,  # field remarks
        ]
        field_reference.name = "field-reference"
        field_reference._initContents(10)
        field_reference[3] = Field("field")
        field_reference[5] = [
            definitionReference,
            cardinalityMinOccurs,
            cardinalityMaxOccurs,
            fieldInXmlFlag,
        ]
        field_reference[6] = [
            formalName,  # field formal-name
            description,  # field description
            props,  # assembly property
            usename,  # field use-name
            groupAs,  # assembly group-as
            remarks,  # field remarks
        ]
        flag_reference.name = "flag-reference"
        flag_reference._initContents(10)
        flag_reference[3] = Field("flag")
        flag_reference[5] = [
            definitionReference,
            cardinalityMinOccurs,
            cardinalityMaxOccurs,
        ]
        flag_reference[6] = [
            formalName,  # field formal-name
            description,  # field description
            props,  # assembly property
            usename,  # field use-name
            groupAs,  # assembly group-as
            remarks,  # field remarks
        ]

        discriminator = Assembly()
        discriminator._setschema(inline_assembly)
        discriminator.name = "discriminator"
        discriminator._flags["as-type"] = "token"
        discriminator.default = "object-type"

        choice.name = "choice-group"
        choice._initContents(10)
        choice["flags"] = [cardinalityMinOccurs, cardinalityMaxOccurs]
        choice["model"] = [
            jsonKey,  # assembly json-key
            groupAs,  # assembly group-as
            discriminator,  # define-field discriminator
            Assembly(),  # choice-group
            remarks,  # field remarks
        ]
        choice["model"][3]._setschema(choice)
        choice["model"][3]._flags["min-occurs"] = "1"
        choice["model"][3]._flags["max-occurs"] = "unbounded"
        choice["model"][3]._initContents(5)
        choice["model"][3][1] = Assembly()
        choice["model"][3][1]._setschema(groupAs)
        choice["model"][3][1].name = "choices"
        choice["model"][3][1]._flags["in-json"] = "ARRAY"
        choice["model"][3][2] = Field("object-type")
        choice["model"][3][3] = [
            assembly_reference,  # define-assembly assembly-reference
            inline_assembly,  # define-assembly define-assembly
            field_reference,  # define-assembly field-reference
            inline_assembly,  # define-assembly define-field
        ]

        singleChoice._initContents(10)
        singleChoice.name = "choice"
        singleChoice["flags"] = []
        singleChoice["model"] = [Assembly()]  # choice-group
        singleChoice["model"][0]._setschema(choice)
        singleChoice["model"][0]._flags["min-occurs"] = "1"
        singleChoice["model"][0]._flags["max-occurs"] = "unbounded"
        singleChoice["model"][0]._initContents(5)
        singleChoice["model"][0][1] = Assembly()
        singleChoice["model"][0][1]._setschema(groupAs)
        singleChoice["model"][0][1].name = "choices"
        singleChoice["model"][0][1]._flags["in-json"] = "ARRAY"
        singleChoice["model"][0][2] = Field("object-type")
        singleChoice["model"][0][3] = [
            assembly_reference,  # assembly assembly-reference
            inline_assembly,  # assembly inline-define-assembly
            field_reference,  # assembly field-reference
            inline_assembly,  # assembly inline-define-field
            # so, these lack discriminator values, which will be important when binding to json
        ]

        metaschema.name = "METASCHEMA"
        object.__setattr__(
            metaschema, "_contents", [None, None, None, None, None, None, None]
        )
        metaschema[0] = None  # Field('Metaschema Module')
        metaschema[1] = None  # Field("A declaration of the Metaschema Module")
        metaschema[2] = []
        metaschema[3] = None  # Field('METASCHEMA')
        metaschema[4] = None  # json-key
        metaschema[5] = [Assembly()]
        metaschema[5][0]._setschema(inline_flag)
        metaschema[5][0].name = "abstract"
        metaschema[5][0]._flags["as-type"] = "token"
        metaschema[5][0].default = "no"
        # metaschema[5][0]['formal-name'] = Field("Is Abstract?")
        metaschema[6] = [
            Assembly(),  # define-field schema-name
            Assembly(),  # define-field schema-version
            Assembly(),  # define-field short-name
            Assembly(),  # define-field namespace
            Assembly(),  # define-field json-base-uri
            remarks,  # field remarks
            Assembly(),  # define-assembly import
            Assembly(),  # choice-group definitions
        ]
        metaschema[6][0]._setschema(inline_assembly)
        metaschema[6][0].name = "schema-name"
        metaschema[6][0]._initContents(10)
        metaschema[6][0]["flags"] = []  # flags
        metaschema[6][1]._setschema(inline_assembly)
        metaschema[6][1].name = "schema-version"
        metaschema[6][1]._initContents(10)
        metaschema[6][1]["flags"] = []  # flags
        metaschema[6][2]._setschema(inline_assembly)
        metaschema[6][2].name = "short-name"
        metaschema[6][2]._initContents(10)
        metaschema[6][2]["flags"] = []  # flags
        metaschema[6][3]._setschema(inline_assembly)
        metaschema[6][3].name = "namespace"
        metaschema[6][3]._initContents(10)
        metaschema[6][3]["flags"] = []  # flags
        metaschema[6][4]._setschema(inline_assembly)
        metaschema[6][4].name = "json-base-uri"
        metaschema[6][4]._initContents(10)
        metaschema[6][4]["flags"] = []  # flags
        # metaschema[6][5] = remarks
        metaschema[6][6]._setschema(inline_assembly)
        metaschema[6][6].name = "import"
        metaschema[6][6]._flags["max-occurs"] = "unbounded"
        metaschema[6][6]._initContents(10)
        metaschema[6][6]["group-as"] = Assembly()
        metaschema[6][6]["group-as"]._setschema(groupAs)
        metaschema[6][6]["group-as"].name = "imports"
        metaschema[6][6]["group-as"]._flags["in-json"] = "ARRAY"
        metaschema[6][6]["flags"] = [Assembly()]  # define-flag href
        metaschema[6][6]["flags"][0]._setschema(inline_flag)
        metaschema[6][6]["flags"][0].name = "href"
        metaschema[6][6]["flags"][0].required = "yes"
        metaschema[6][6]["model"] = []  # model
        metaschema[6][7]._setschema(choice)
        metaschema[6][7]._flags["max-occurs"] = "unbounded"
        metaschema[6][7]._initContents(5)
        metaschema[6][7][1] = Assembly()
        metaschema[6][7][1]._setschema(groupAs)
        metaschema[6][7][1].name = "definitions"
        metaschema[6][7][1]._flags["in-json"] = "ARRAY"
        metaschema[6][7][2] = Field("object-type")
        metaschema[6][7][3] = [global_assembly, global_field, global_flag]

        self.metaschema._initContents(8)
        self.metaschema[0] = Field("Metaschema Model")  # schema-name
        self.metaschema[1] = Field("1.0.0-M2")  # schema-version
        self.metaschema[2] = Field("metaschema-model")  # short-name
        self.metaschema[3] = Field("[namespace]")  # namespace
        self.metaschema[4] = Field("[json-base-uri]")  # json-base-uri
        self.metaschema[5] = None  # remarks
        self.metaschema[6] = []  # imports

        self.metaschema[7] = [  # definitions
            metaschema,
            inline_assembly,
            inline_assembly,
            inline_flag,
            assembly_reference,
            field_reference,
            flag_reference,
            singleChoice,
            asTypeSimple,
        ]

        def bindToContext(node):
            if node is not None:
                if isinstance(node, list):
                    for thing in node:
                        bindToContext(thing)
                elif node._context is None:
                    object.__setattr__(node, "_context", self)
                    if isinstance(node, ModelObject):
                        # for flag in node._flags:
                        #    bindToContext(flag)
                        if isinstance(node, Assembly):
                            for thing in node._contents:
                                bindToContext(thing)

        bindToContext(self.metaschema)

    def get(self, name):
        match name:
            case "METASCHEMA":
                return self.metaschema[7][0]
            case "define-assembly":
                return self.metaschema[7][1]
            case "define-field":
                return self.metaschema[7][2]
            case "define-flag":
                return self.metaschema[7][3]
            case "assembly-reference":
                return self.metaschema[7][4]
            case "field-reference":
                return self.metaschema[7][5]
            case "flag-reference":
                return self.metaschema[7][6]
            case "choice":
                return self.metaschema[7][7]
            case "as-type-simple":
                return self.metaschema[7][8]

        # TODO: throw error
        raise Exception("can't find specified type " + name)

    def parent(self, name):
        return self


class InlineAssemblyDefinition(Assembly):
    pass
