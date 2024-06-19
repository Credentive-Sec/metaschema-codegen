from pathlib import Path
from lxml import etree
import math
import re

from .metaschema_context import MetaschemaContext


class Context:
    def __init__(self, path: str | Path, binding="xml"):
        self.types = {}
        self.subspaces = []

        metaschema = MetaschemaContext()
        self.subspaces.append(metaschema)

        if path is not None:
            base_path = Path(Path(path).parent)
            if binding == "xml":
                parser = etree.XMLParser(
                    load_dtd=True, resolve_entities=True, remove_comments=True
                )
                xml_tree = etree.parse(path, parser=parser)
                root = Assembly.fromXML(
                    xml_tree.getroot(), metaschema.get("METASCHEMA"), self
                )

        METASCHEMA = root
        includes = []

        for include in METASCHEMA["imports"]:
            includes.append(include.href)

        for definition in METASCHEMA["definitions"]:
            self.types[definition.name] = definition

        # remove metaschema default from subspaces
        self.subspaces.clear()
        # hunt down includes
        for include in includes:
            self.subspaces.append(Context(str(Path(base_path, include))))

    # get a definition from a context & its children
    def get(self, name: str) -> "Assembly | None":
        if self.types.get(name) is not None:
            return self.types[name]
        for subspace in self.subspaces:
            if subspace.get(name) is not None:
                return subspace.get(name)
        return None

    # get the context that contains a definition
    def parent(self, name: str) -> "Context | None":
        if self.types.get(name) is not None:
            return self
        for subspace in self.subspaces:
            if subspace.parent(name) is not None:
                return subspace.parent(name)
        return None

    def instantiate(self, type, binding, path):
        if binding == "xml":
            parser = etree.XMLParser(
                load_dtd=True, resolve_entities=True, remove_comments=True
            )
            xml_tree = etree.parse(path, parser=parser)
            root = xml_tree.getroot()
            return ModelObject.fromXML(root, self.get(type), self)


class SchemaObject:
    def __init__(self):
        self._schema = Assembly()
        self._context = None
        self._contents = ""

    def _setschema(self, schema: "Assembly"):
        object.__setattr__(self, "_schema", schema)

    def __str__(self):
        return self._contents

    def validate(self):
        t = self._schema._flags.get("as-type") or "string"
        str = self._contents
        if t == "dateTime-with-timezone":
            t = "date-time-with-timezone"
        if t == "email":
            t = "email-address"
        pattern = ""
        overrule = False
        match t:
            case "string":
                pattern = ".*"
            case "base64":
                pattern = "[0-9A-Za-z+/]+={0,2}"
            case "boolean":
                pattern = "true|1|false|0"
            case "date":
                pattern = "(((2000|2400|2800|(19|2[0-9](0[48]|[2468][048]|[13579][26])))-02-29)|(((19|2[0-9])[0-9]{2})-02-(0[1-9]|1[0-9]|2[0-8]))|(((19|2[0-9])[0-9]{2})-(0[13578]|10|12)-(0[1-9]|[12][0-9]|3[01]))|(((19|2[0-9])[0-9]{2})-(0[469]|11)-(0[1-9]|[12][0-9]|30)))(Z|(-((0[0-9]|1[0-2]):00|0[39]:30)|\\+((0[0-9]|1[0-4]):00|(0[34569]|10):30|(0[58]|12):45)))?"
            case "date-time":
                pattern = "(((2000|2400|2800|(19|2[0-9](0[48]|[2468][048]|[13579][26])))-02-29)|(((19|2[0-9])[0-9]{2})-02-(0[1-9]|1[0-9]|2[0-8]))|(((19|2[0-9])[0-9]{2})-(0[13578]|10|12)-(0[1-9]|[12][0-9]|3[01]))|(((19|2[0-9])[0-9]{2})-(0[469]|11)-(0[1-9]|[12][0-9]|30)))T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\\.[0-9]+)?(Z|(-((0[0-9]|1[0-2]):00|0[39]:30)|\\+((0[0-9]|1[0-4]):00|(0[34569]|10):30|(0[58]|12):45)))?"
            case "date-time-with-timezone":
                pattern = "(((2000|2400|2800|(19|2[0-9](0[48]|[2468][048]|[13579][26])))-02-29)|(((19|2[0-9])[0-9]{2})-02-(0[1-9]|1[0-9]|2[0-8]))|(((19|2[0-9])[0-9]{2})-(0[13578]|10|12)-(0[1-9]|[12][0-9]|3[01]))|(((19|2[0-9])[0-9]{2})-(0[469]|11)-(0[1-9]|[12][0-9]|30)))T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\\.[0-9]+)?(Z|(-((0[0-9]|1[0-2]):00|0[39]:30)|\\+((0[0-9]|1[0-4]):00|(0[34569]|10):30|(0[58]|12):45)))"
            case "date-with-timezone":
                pattern = "(((2000|2400|2800|(19|2[0-9](0[48]|[2468][048]|[13579][26])))-02-29)|(((19|2[0-9])[0-9]{2})-02-(0[1-9]|1[0-9]|2[0-8]))|(((19|2[0-9])[0-9]{2})-(0[13578]|10|12)-(0[1-9]|[12][0-9]|3[01]))|(((19|2[0-9])[0-9]{2})-(0[469]|11)-(0[1-9]|[12][0-9]|30)))(Z|(-((0[0-9]|1[0-2]):00|0[39]:30)|\\+((0[0-9]|1[0-4]):00|(0[34569]|10):30|(0[58]|12):45)))"
            case "day-time-duration":
                pattern = "-?P([0-9]+D(T(([0-9]+H([0-9]+M)?(([0-9]+|[0-9]+(\\.[0-9]+)?)S)?)|([0-9]+M(([0-9]+|[0-9]+(\\.[0-9]+)?)S)?)|([0-9]+|[0-9]+(\\.[0-9]+)?)S))?)|T(([0-9]+H([0-9]+M)?(([0-9]+|[0-9]+(\\.[0-9]+)?)S)?)|([0-9]+M(([0-9]+|[0-9]+(\\.[0-9]+)?)S)?)|([0-9]+|[0-9]+(\\.[0-9]+)?)S)"
            case "decimal":
                pattern = "\\S(.*\\S)?"
            case "email-address":
                pattern = ".+@.+"
            case "hostname":
                pattern = "[A-Za-z\\.]*[A-Za-z]"
            case "integer":
                pattern = "\\S(.*\\S)?"
            case "ip-v4-address":
                pattern = "((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9]).){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])"
            case "ip-v6-address":
                pattern = "(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|[fF][eE]80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::([fF]{4}(:0{1,4}){0,1}:){0,1}((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9]).){3,3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9]).){3,3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9]))"
            case "non-negative-integer":
                pattern = "\\S(.*\\S)?"
            case "positive-integer":
                pattern = "\\S(.*\\S)?"
            case "token":
                pattern = "(\\p{L}|_)(\\p{L}|\\p{N}|[.\\-_])*"
            case "uri":
                pattern = "[a-zA-Z][a-zA-Z0-9+\\-.]+:.*\\S"
            case "uri-reference":
                pattern = "\\S(.*\\S)?"
            case "uuid":
                pattern = "[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[45][0-9A-Fa-f]{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}"
            case _:
                print(f"WARNING: unknown type {t}")
                overrule = True
        return overrule or bool(re.fullmatch(pattern, str))


class Flag(SchemaObject):
    def __init__(self, value):
        self._schema = None
        self._contents = value


class ModelObject(SchemaObject):
    def __init__(self):
        object.__setattr__(self, "_flags", {})
        object.__setattr__(self, "_context", None)
        object.__setattr__(self, "_schema", None)

    def __getattr__(self, name):
        return self._flags.get(name)
        # return self._flags[name]

    def __setattr__(self, name, value):
        self._flags[name] = value

    @staticmethod
    def fromXML(xml, schema, context):
        t = schema._schema.name
        if t == "inline-define-field" or t == "define-field":
            return Field.fromXML(xml, schema, context)
        else:
            return Assembly.fromXML(xml, schema, context)

    @staticmethod
    def XMLevalSchema(xmls, schema, parentcontext):
        if schema is None:
            raise Exception("schema is None!")
        elif schema._schema is None:
            raise Exception("no idea what sort of thing this is supposed to be")
        if schema.name == "any":
            xmls.clear()
            return []  # FIXME
        schemas = [schema]
        if schema._schema.name in ["choice", "choice-group"]:
            schemas = schema["choices"]
        effectiveNames = []
        defs = {}
        ctxs = {}
        subschemas = {}
        for potentialSchema in schemas:
            ctx = parentcontext
            schemadef = potentialSchema
            effectiveName = potentialSchema._getEffectiveName()
            if potentialSchema._schema.name in [
                "field-reference",
                "assembly-reference",
            ]:
                schemadef = parentcontext.get(potentialSchema.ref)
                ctx = parentcontext.parent(potentialSchema.ref)

            effectiveNames.append(effectiveName)
            defs[effectiveName] = schemadef
            ctxs[effectiveName] = ctx
            subschemas[effectiveName] = potentialSchema

        if (
            schema._schema.name in ["inline-define-field", "field-reference"]
            and schema._flags.get("in-xml") == "UNWRAPPED"
        ):
            # need to convert them to markdown
            toRet = Field(Field.convertHTMLtoMarkdown(xmls))
            toRet._setschema(schema)
            return toRet

        maxOccurs = schema._flags.get("max-occurs") or 1
        if maxOccurs == "unbounded":
            maxOccurs = math.inf
        else:
            maxOccurs = int(maxOccurs)

        def remNs(str):
            i = 0
            toRet = ""
            for c in str:
                if c == "{":
                    i = i + 1
                elif c == "}":
                    i = i - 1
                elif i == 0:
                    toRet = toRet + c
            return toRet

        arrtogetfrom = xmls
        if maxOccurs > 1:
            # we need to find a group-name in case it's grouped in xml
            if schema["group-as"] is not None:
                if schema["group-as"]._flags.get("in-xml") == "GROUPED":
                    if len(xmls) == 0:
                        return []
                    if remNs(xmls[0].tag) == schema["group-as"].name:
                        arrtogetfrom = list(xmls.pop(0))
                    else:
                        return []

        count = 0
        listOfInstances = []
        while (
            len(arrtogetfrom) > 0
            and count < maxOccurs
            and remNs(arrtogetfrom[0].tag) in effectiveNames
        ):
            count += 1
            gottenName = remNs(arrtogetfrom[0].tag)
            if schema._schema.name == "choice":
                # we have collapsed the choice, but we may not have fully analyzed the one we took
                # e.g. if its max-occurs > 1.
                # we know that a choice always has max-occurs = 1, though
                # which means it will return None or the ModelObject directly, not wrapped in a list/group
                return ModelObject.XMLevalSchema(
                    arrtogetfrom, subschemas[gottenName], ctxs[gottenName]
                )
            else:
                listOfInstances.append(
                    ModelObject.fromXML(
                        arrtogetfrom.pop(0), defs[gottenName], ctxs[gottenName]
                    )
                )

        toRet = listOfInstances
        if maxOccurs == 1:
            if len(listOfInstances) == 0:
                toRet = None
            else:
                toRet = listOfInstances[0]
        return toRet

    @staticmethod
    def fromJSON(json, schema, context):
        pass

    def __getitem__(self, key):
        raise Exception("Attempted to dereference a field")


class Field(ModelObject):
    def __init__(self, value=None):
        object.__setattr__(self, "_contents", value)
        object.__setattr__(self, "_schema", None)
        object.__setattr__(self, "_flags", {})

    def validate(self):
        for flag in self._flags:
            if not flag.validate():
                return False
        if (
            self._schema._flags.get("as-type") == "markup-line"
            or self._schema._flags.get("as-type") == "markup-multiline"
        ):
            pass
        else:
            return super().validate()

    @staticmethod
    def fromXML(xml, schema, context):
        if schema is None:
            raise Exception("grand failure! no schema!")
        elif schema["flags"] is None:
            raise Exception(
                "failure: "
                + (schema.name or schema.ref)
                + " does not have iterable flags (not a field?)"
            )
        toRet = Field(xml.text)
        object.__setattr__(toRet, "_schema", schema)
        object.__setattr__(toRet, "_context", context)
        for flag in schema["flags"]:
            flagdef = flag
            if flag._schema.name == "flag-reference":
                flagdef = context.get(flag.name)
            effectiveName = flag._getEffectiveName()
            value = xml.attrib.get(effectiveName)
            if value is None:
                if flag.required == "yes" and flagdef.default is None:
                    pass  # THROW ERROR!!!
            toRet._flags[effectiveName] = value
        return toRet

    @staticmethod
    def convertHTMLtoMarkdown(xmls):
        string = ""

        def remNs(str):
            i = 0
            toRet = ""
            for c in str:
                if c == "{":
                    i = i + 1
                elif c == "}":
                    i = i - 1
                elif i == 0:
                    toRet = toRet + c
            return toRet

        htmlElements = [
            "p",
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
            "insert",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "pre",
            "ol",
            "ul",
            "li",
            "blockquote",
            "table",
            "tr",
            "th",
            "td",
        ]
        while len(xmls) > 0 and remNs(xmls[0].tag) in htmlElements:
            xml = xmls.pop(0)
            name = remNs(xml.tag)
            text = xml.text or ""
            tail = xml.tail or ""
            if name == "i":
                name = "em"
            elif name == "b":
                name = "strong"
            match name:
                case "p":
                    string += (
                        text + Field.convertHTMLtoMarkdown(list(xml)) + "\\n\\n" + tail
                    )
                case "em":
                    string += (
                        "*" + text + Field.convertHTMLtoMarkdown(list(xml)) + "*" + tail
                    )
                case "strong":
                    string += (
                        "**"
                        + text
                        + Field.convertHTMLtoMarkdown(list(xml))
                        + "**"
                        + tail
                    )
                case "code":
                    string += (
                        "`" + text + Field.convertHTMLtoMarkdown(list(xml)) + "`" + tail
                    )
                case "q":
                    string += (
                        '"' + text + Field.convertHTMLtoMarkdown(list(xml)) + '"' + tail
                    )
                case "sub":
                    string += (
                        "~" + text + Field.convertHTMLtoMarkdown(list(xml)) + "~" + tail
                    )
                case "sup":
                    string += (
                        "^" + text + Field.convertHTMLtoMarkdown(list(xml)) + "^" + tail
                    )
                case "img":
                    string += (
                        f'![{xml.attrib["alt"]}]({xml.attrib["src"]} "{xml.attrib["title"]}")'
                        + tail
                    )
                case "a":
                    string += f'[{xml.text}](*{xml.attrib["href"]}*)' + tail
                case "insert":
                    string += (
                        "{{ insert: "
                        + xml.attrib["type"]
                        + ", "
                        + xml.attrib["id-ref"]
                        + " }}"
                        + tail
                    )
                case "h1":
                    string += "# " + text + "\n" + tail
                case "h2":
                    string += "## " + text + "\n" + tail
                case "h3":
                    string += "### " + text + "\n" + tail
                case "h4":
                    string += "#### " + text + "\n" + tail
                case "h5":
                    string += "##### " + text + "\n" + tail
                case "h6":
                    string += "###### " + text + "\n" + tail
                case "pre":
                    string += "\n```\n" + text + "\n```\n" + tail
                case "ol":
                    index = 0
                    for subelement in xml:
                        index = index + 1
                        string += str(index) + ". " + subelement.text + "\n"
                    string += tail
                case "ul":
                    for subelement in xml:
                        string += "- " + subelement.text + "\n"
                    string += tail
                case "blockquote":
                    string += "> " + text + "\n" + tail
        return string


class Assembly(ModelObject):
    _contents: list[ModelObject]
    _context: Context

    def __init__(self):
        object.__setattr__(self, "_flags", {})
        object.__setattr__(
            self, "_contents", []
        )  # indexed by numbers corresponding to position in model
        object.__setattr__(self, "_context", None)
        object.__setattr__(
            self, "_schema", None
        )  # assembly representing instance of either inline define assembly, or global define assembly

    @staticmethod
    def fromXML(xml, schema, context: Context):
        toRet = Assembly()
        object.__setattr__(toRet, "_schema", schema)
        object.__setattr__(toRet, "_context", context)
        for flag in schema["flags"]:
            flagdef = flag
            if flag._schema.name == "flag-reference":
                flagdef = context.get(flag.ref)
                if flagdef == None:
                    raise Exception("could not find flag definition for " + flag.ref)
            effectiveName = flag._getEffectiveName()
            value = xml.attrib.get(effectiveName)
            if value is None:
                if flag.required == "yes" and flagdef.default is None:
                    pass  # throw an error
                # if it's not required, or there is a default, all is well.
            toRet._flags[effectiveName] = value

        children = list(xml)
        for child in schema["model"]:
            if child is None or child._schema is None:
                raise Exception("bad schema")
            toRet._contents.append(ModelObject.XMLevalSchema(children, child, context))
        if len(children) > 0:
            print("WARNING: remaining unparsed children")
            # print(f"(could not parse past {children[0].tag} type)")
        return toRet

    @staticmethod
    def fromJSON(json):
        pass

    def _nameToIndex(self, name):
        # code will recurse infinitely if we do not give hard definitions to anchor some types down
        # without these define-assembly will call this function on inline-define-assembly for the name 'model'
        # and in turn inline-define-assembly would call this function on define-assembly for the name 'model'
        # while we're at it, giving them hard definitions, it's nice to include other things as well
        # since you could dereference them by numbers and circumvent calling _nameToIndex altogether, these are really more for programmer readability than anything
        # global definition: formalName, desc, props, usename/rootname, [jsonkey, flags, [model,]] constraints, remarks, example
        # inline definition: formalName, desc, props, jsonkey, ?????
        # references: formalName, desc, props, usename, groupAs, remarks
        if self._schema.name in [
            "define-assembly",
            "define-field",
            "define-flag",
            "inline-define-assembly",
            "inline-define-field",
            "inline-define-flag",
            "assembly-reference",
            "field-reference",
            "flag-reference",
        ]:
            semSource = {
                "define-assembly": {"use-name": 3, "flags": 5, "model": 6},
                "define-field": {"use-name": 3, "flags": 6},
                "define-flag": {"use-name": 3},
                "inline-define-assembly": {"group-as": 4, "flags": 5, "model": 6},
                "inline-define-field": {"group-as": 5, "flags": 6},
                "inline-define-flag": {},
                "assembly-reference": {"use-name": 3, "group-as": 4},
                "field-reference": {"use-name": 3, "group-as": 4},
                "flag-reference": {"use-name": 3, "group-as": 4},
            }
            if semSource[self._schema.name].get(name) is not None:
                return semSource[self._schema.name].get(name)
        index = 0
        for child in self._schema["model"]:
            if child._flags.get("max-occurs") is not None and (
                child._flags["max-occurs"] == "unbounded"
                or int(child._flags["max-occurs"]) > 1
            ):
                if name == child["group-as"].name:
                    return index
            elif child._schema.name == "choice":
                # need to check for each option of the choice
                pass
            else:
                # need to check for a usename
                if name == child._getEffectiveName():
                    return index
            index = index + 1
        return -1

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._contents[key]
        if self._nameToIndex(key) >= len(self._contents) or self._nameToIndex(key) < 0:
            print("a")  # FIXME
        return self._contents[self._nameToIndex(key)]

    def __setitem__(self, key, value):
        if isinstance(key, int):
            self._contents[key] = value
        else:
            self._contents[self._nameToIndex(key)] = value

    # def __iter__(self):
    #    return self._contents.__iter__()
    def validate(self):
        if self._schema == None:
            raise Exception("Assembly cannot validate: Does not know its own schema")
        if self._context == None:
            raise Exception("Assembly cannot validate: No context is set")
        for flag in self._flags:
            if not flag.validate():
                return False
        for child in self:
            if not child.validate():
                return False
        for flag in self[
            "flags"
        ]:  # the 5th element in an assembly def is the list of flagrefs/defs
            flagdef = flag
            if flag["ref"] is not None:
                flagdef = self._context.get(flag["ref"])
            if flagdef["required"] == "yes" and self[flagdef["name"]] is None:
                return False
        index = 0
        for sch in self["model"]:  # 6 is the model
            schdef = sch
            if sch.ref is not None:
                schdef = self.context.get(flag.ref)
            maxOccurs = schdef._flags.get("max-occurs") or 1
            if maxOccurs == "unbounded" or maxOccurs > 1:
                pass
            else:
                if self._contents[index].validate() == False:
                    return False
            index = index + 1
        return True

    def _getEffectiveName(self):  # called on a schema
        # we can only look for a usename in specific types (global definitions & references)
        if self._schema.name in [
            "define-assembly",
            "define-field",
            "define-flag",
            "assembly-reference",
            "field-reference",
            "flag-reference",
        ]:
            if self["use-name"] is not None:
                return self["use-name"]._contents
        if self._schema.name in [
            "flag-reference",
            "field-reference",
            "assembly-reference",
        ]:
            schdef = self._context.get(self.ref)
            if schdef["use-name"] is not None:
                return schdef["use-name"]._contents
            if schdef.name is None:
                print("bweh")
            return schdef.name
            # we only need to check in this if, because everywhere else schdef = self and was checked already
        if self.name is None:
            print("bweh")
        return self.name

    def _initContents(self, num):
        for i in range(0, num):
            self._contents.append(None)
