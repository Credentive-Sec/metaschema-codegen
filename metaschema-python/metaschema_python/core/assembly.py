from pathlib import Path
from lxml import etree
import math
import re

msns = ""#'{http://csrc.nist.gov/ns/oscal/metaschema/1.0}'
oscalns = ""#'{http://csrc.nist.gov/ns/oscal/1.0}'

def remNs(str):
    i = 0
    toRet = ""
    for c in str:
        if c == '{':
            i = i + 1
        elif c == '}':
            i = i - 1
        elif i == 0:
            toRet = toRet + c
    return toRet

class XMLTag:
    def __init__(self, xml):
        if xml is None:
            self.type = ""
            self.attr = {}
            self.children = []
            self.text = ""
            return
        self.type = remNs(xml.tag) #aka name?
        self.attr = xml.attrib #aka tags?
        self.children = [] #aka fields/assemblies?
        self.text = xml.text #field values?
        for child in list(xml):
            self.children.append(XMLTag(child))

    def addChild(self,child):
        self.children.append(child)

    def __str__(self):
        attrStr = ""
        for k in self.attr.keys():
            attrStr = attrStr + " "+k+'="'+self.attr[k]+'"'
            #it seems like it might be better to actually concatenete attrStr onto the right end
        t = self.text or ""
        toRet = "<"+ self.type+attrStr+">"+t
        for child in self.children:
            toRet = toRet+"\n"+str(child)
        if len(self.children) > 0:
            toRet = toRet+"\n"
        toRet = toRet + "</"+self.type+">"
        return toRet
    
    @staticmethod
    def fromPath(path):
        parser = etree.XMLParser(load_dtd=True, resolve_entities=True, remove_comments=True)
        xml_tree = etree.parse(path, parser=parser)
        return XMLTag(xml_tree.getroot())
    
    @staticmethod
    def JsonfromStr(instr): #Oh, gosh. Please don't write a JSON parser! Look at the 'json' module (https://docs.python.org/3.8/library/json.html) Apologies if I've misunderstood what I'm looking at.
        if instr[:1] == '{':
            str = instr[1:]
            t = {}

            key = ""
            val = ""
            keyDone = False
            inStr = False
            bracketing = 0
            for char in str:
                if bracketing > 0:
                    if char == '}' or char == ']':
                        bracketing = bracketing - 1
                    if char == '{' or char == '[':
                        bracketing = bracketing + 1
                    val = val + char
                elif char == '"':
                    inStr = not inStr
                elif inStr:
                    if keyDone:
                        val = val+char
                    else:
                        key = key+char
                else:
                    if char == ":":
                        keyDone = True
                    elif char == "," or char == '}':
                        keyDone = False
                        t[key] = XMLTag.JsonfromStr(val)
                        val = ""
                        key = ""
                    elif char == '{' or char == '[':
                        bracketing = bracketing + 1
                        val = val+char
            return t
        elif instr[:1] == '[':
            str = instr[1:]
            t = []

            val = ""
            inStr = False
            bracketing = 0
            for char in str:
                if bracketing > 0:
                    if char == '}' or char == ']':
                        bracketing = bracketing - 1
                    if char == '{' or char == '[':
                        bracketing = bracketing + 1
                    val = val + char
                elif char == '"':
                    inStr = not inStr
                elif inStr:
                    val = val + char
                elif char == ',' or char == ']':
                    t.append(XMLTag.JsonfromStr(val))
                    val = ""
                elif char == '[' or char == '{':
                    bracketing = bracketing + 1
                    val = val + char
            return t
        else:
            return instr
    @staticmethod
    #gets an assembly from json
    def fromJson(json, schema, namespace):
        toRet = XMLTag(None)
        toRet.type = schema.attr.get('name')

        for child in schema.children:
            if child.type == 'flag' or child.type == 'define-flag':
                if child.type == 'flag':
                    flagschema = namespace.get(child.attr['ref'])
                else: #child.type == 'define-flag'
                    flagschema = child
                if json.get(flagschema.attr['name']) is None:
                    if flagschema.attr.get('required') == "yes":
                        raise Exception("missing required flag")
                else:
                    toRet.attr[flagschema.attr['name']] = json[flagschema.attr['name']]
            elif child.type == 'model':
                for element in child.children:
                    toRet.addJsonToModel(json, element, namespace)
                    
        return toRet
    #reads either a field or an assembly from json and adds it to the XMLTag's children
    def addJsonToModel(self, parentjson, schema, namespace):
        #are we dealing with a choice, a reference, or an inline definition?
        if schema.type == 'choice':
            return
        elif schema.type == 'assembly' or schema.type == 'field':
            schemadef = namespace.get(schema.attr['ref'])
        else: #define-assembly or define-field
            schemadef = schema

        grouped = False
        groupName = ""
        useName = schemadef.attr['name'] #this is separate from groupName because of XML
        xmlGrouped = False
        for child in schemadef.children:
            if child.type == 'use-name':
                useName = child.text
        for child in schema.children:
            if child.type == 'group-as':
                if child.attr.get('in-json') == "ARRAY":
                    grouped = True
                if child.attr.get('in-xml') == "GROUPED":
                    xmlGrouped = True
                groupName = child.attr.get('name')
            elif child.type == 'use-name':
                    useName = child.text

        tagToAddTo = self
        if xmlGrouped:
            tagToAddTo = XMLTag(None)
            tagToAddTo.type = groupName
            self.children.append(tagToAddTo)

        #need to do something about <prose>'s in-xml without wrapper

        if grouped:
            if parentjson.get(groupName) is None:
                if schema.attr.get('min-occurs') is not None and int(schema.attr['min-occurs']) > 0:
                    raise Exception(f"could not find group {groupName} in {self.type}")
            else:
                for element in parentjson[groupName]:
                    if schemadef.type == 'define-field':
                        toAdd = XMLTag(None)
                        toAdd.type = useName
                        toAdd.text = element
                        tagToAddTo.children.append(toAdd)
                    else: #schemadef.type = 'define-assembly'
                        toAdd = XMLTag.fromJson(element, schemadef, namespace)
                        toAdd.type = useName
                        tagToAddTo.children.append(toAdd)
        else:
            if parentjson.get(useName) is None:
                if schema.attr.get('min-occurs') is not None and int(schema.attr['min-occurs']) > 0:
                    raise Exception(f"could not find element {useName}")
            else:
                if schemadef.type == 'define-field':
                    toAdd = XMLTag(None)
                    toAdd.type = useName
                    toAdd.text = parentjson[useName]
                    tagToAddTo.children.append(toAdd)
                else: #schemadef.type == 'define-assembly'
                    toAdd = XMLTag.fromJson(parentjson[useName], schemadef, namespace)
                    toAdd.type = useName
                    tagToAddTo.children.append(toAdd)
    
class Context:
    def __init__(self, schemapath):
        if schemapath is not None:
            base_path = Path(Path(schemapath).parent)
            parser = etree.XMLParser(load_dtd=True, resolve_entities=True, remove_comments=True)
            xml_tree = etree.parse(schemapath, parser=parser)
            root = XMLTag(xml_tree.getroot())

        self.types = {}
        self.subspaces = []
        includes = []
        if schemapath is not None:
            for child in root.children:
                if child.type == 'define-assembly':
                    self.types[child.attr['name']] = child
                elif child.type == 'define-field':
                    self.types[child.attr['name']] = child
                elif child.type == 'define-flag':
                    self.types[child.attr['name']] = child
                elif child.type == 'import':
                    includes.append(child.attr.get('href'))
        
            #hunt down includes
            for include in includes:
                self.subspaces.append(Context(str(Path(base_path, include))))

    #get a definition from a context & its children
    def get(self, name):
        if self.types.get(name) is not None:
            return self.types[name]
        for subspace in self.subspaces:
            if subspace.get(name) is not None:
                return subspace.get(name)
        return None
    #get the context that contains a definition
    def parent(self, name):
        if self.types.get(name) is not None:
            return self
        for subspace in self.subspaces:
            if subspace.parent(name) is not None:
                return subspace.parent(name)
        return None

#assemblies have metadata, flags, and (as children, part of the model) fields and assemblies
class Assembly:
    def __init__(self, schema, node, ns={}, inline=False):
        self.schema = schema #we know this is an instance of a metaschema assembly
        self.node = node
        self.namespace = ns
        self.inline = inline
        #if not self.validate():
        #    raise Exception("initialization does not match schema")
    def validate(self):
        si = 0 #schema index
        ni = 0 #node index
        if si < len(self.schema.children) and self.schema.children[si].type == "formal-name":
            si = si + 1
        if si < len(self.schema.children) and self.schema.children[si].type == 'description':
            si = si + 1
        while si < len(self.schema.children) and self.schema.children[si].type == 'prop':
            si = si + 1
        if si < len(self.schema.children) and self.schema.children[si].type == "root-name":
            si = si + 1
        elif si < len(self.schema.children) and self.schema.children[si].type == "use-name":
            si = si + 1
        if si < len(self.schema.children) and self.schema.children[si].type == 'json-key':
            si = si + 1
        if self.inline and si < len(self.schema.children) and self.schema.children[si].type == 'group-as':
            si = si + 1
        
        #now we get to flags
        while si < len(self.schema.children) and (self.schema.children[si].type == 'flag' or self.schema.children[si].type == 'define-flag'):
            if self.schema.children[si].attr.get('required') == "yes":
                flagschema = self.schema.children[si]
                if self.schema.children[si].type == 'flag':
                    flagschema = self.namespace.get(self.schema.children[si].attr['ref'])
                elif self.schema.children[si].type == 'define-flag':
                    flagschema = self.schema.children[si]
                if self.node.attr.get(flagschema.attr['name']) is None:
                    return False
                #TODO: check type
            si = si + 1
        if si < len(self.schema.children) and self.schema.children[si].type == 'model':
            for child in self.schema.children[si].children:
                ni = self.modelValidate(child, ni)
                if ni == -1: #the modelValidate failed
                    return False
            if ni < len(self.node.children):
                return False
            si = si + 1

        if si < len(self.schema.children) and self.schema.children[si].type == 'constraint':
            for constraint in self.schema.children[si].children:
                if not self.constraintSatisfied(self.node, constraint):
                    return False
            si = si + 1
        
        if si < len(self.schema.children) and self.schema.children[si].type == 'remarks':
            si = si + 1
        while si < len(self.schema.children) and self.schema.children[si].type == 'example':
            si = si + 1
        if si < len(self.schema.children):
            print("unparseable children")
            return False
        return True
    
    def modelValidate(self, schema, ni):
        #are we dealing with a choice, a reference, or an inline definition?
        if schema.type == 'choice':
            highestNi = -1
            for child in schema.children:
                thisni = self.modelValidate(child, ni)
                if thisni > highestNi:
                    #simple heuristic for finding the "best" choice
                    highestNi = thisni
            ni = highestNi
            return ni
        schemadef = self.getChildDefinition(schema)

        lni = ni #local node index

        grouped, groupName, useName = self.getChildGroupingAndNames(schema)

        childrenArr = self.node.children

        #need to check through attr to see if this has datatype markup-multiline and if it has in-xml unwrapped
        #i'm not sure what they mean, but <prose> i think requires this
        if schemadef.attr.get("as-type") == "markup-multiline" and schemadef.attr.get("in-xml") == "UNWRAPPED":
            #htmlElements = ["insert", "b", "i", "em", "strong", "code", "q", "sub", "sup", "img", "a"]
            mumlElements = ["insert", "p", "b", "i", "em", "strong", "code", "q", "sub", "sup", "img", "a", "h1", "h2", "h3", "h4", "h5", "h6", "pre", "ol", "ul", "blockquote", "table"]
            while lni < len(childrenArr) and (childrenArr[lni].type in mumlElements or childrenArr[lni].type == useName):
                #it is difficult when reading in a json to remove the <prose> tag, so we should also check for the tag in case it was failed to be removed
                lni = lni + 1
            return lni #FIXME: hack to fix <prose>
        #maybe instead there should be an array of check-for values, which this replaces with htmlElements or mumlElements?


        maxOccurs = schema.attr.get('max-occurs') or 1
        if maxOccurs == "unbounded":
            maxOccurs = math.inf
        else:
            maxOccurs = int(maxOccurs)
        minOccurs = schema.attr.get('min-occurs') or 0
        minOccurs = int(minOccurs)


        if grouped:
            if ni < len(self.node.children) and self.node.children[ni].type == groupName:
                #this node is the wrapper. we'll interpret it
                childrenArr = self.node.children[ni].children
                lni = 0
                ni = ni + 1
            else:
                if minOccurs > 0:
                    print("no wrapper where required at {lni}")
                    return -1
                else:
                    return ni


        count = 0
        #                                                     you don't actually want to check against name, you want to check against the field use-name
        while lni < len(childrenArr) and count < maxOccurs and childrenArr[lni].type == useName:
            if not self.validateChild(schema, childrenArr[lni], str(lni)):
                return -1
            lni = lni + 1
            count = count + 1
        if count < minOccurs: #we did not find enough nodes of this kind
            print("not enough "+useName+"s")
            return -1
        if grouped:
            return ni #if there was a wrapper, we don't want to return lni because our iterations were not over the parent's children array
        return lni
    
    def validateChild(self, schema, node, lni="(unknown)"):
        schemadef = self.getChildDefinition(schema)
        if schema.type == 'assembly' \
        and not Assembly(schemadef, node, self.namespace.parent(schemadef.attr['name'])).validate():
            print(f"{schemadef.attr['name']} at {lni} is invalid")
            return False
        elif schema.type == 'define-assembly' \
        and not Assembly(schemadef, node, self.namespace, True).validate():
            print(f"{schemadef.attr['name']} at {lni} is invalid (inline)")
            return False
        elif schema.type == 'field' or schema.type == 'define-field':
            return self.validateChildField(schemadef, node)
        return True
    
    def validateChildField(self, schema, node):
        t = schema.attr.get('as-type')
        if t is None:
            t = "string"
        if t == "markup-line":
            htmlElements = ["insert", "b", "i", "em", "strong", "code", "q", "sub", "sup", "img", "a"]
            for child in node.children:
                if not child.type in htmlElements:
                    return False
            return True
        if t == "markup-multiline":
            mumlElements = ["insert", "p", "b", "i", "em", "strong", "code", "q", "sub", "sup", "img", "a", "h1", "h2", "h3", "h4", "h5", "h6", "pre", "ol", "ul", "blockquote", "table"]
            for child in node.children:
                if not child.type in mumlElements:
                    return False
            return True
        return Assembly.strMatchesType(node.text, t)
    
    #either find the global definition of a reference, or return the schema if it's an inline definition
    def getChildDefinition(self, schema):
        if schema.type == 'assembly' or schema.type == 'field':
            #reference, get the definition from the namespace
            schemadef = self.namespace.get(schema.attr['ref'])
            if schemadef is None:
                raise Exception("can't find schema definition for "+schema.attr['ref'])
        elif schema.type == 'define-assembly' or schema.type == 'define-field':
            #inline definition
            schemadef = schema
        return schemadef
    
    def getChildGroupingAndNames(self, schema):
        schemadef = self.getChildDefinition(schema)

        grouped = False
        groupName = ""
        useName = schemadef.attr['name']
        for child in schemadef.children:
            if child.type == 'use-name':
                useName = child.text
        #group-as is defined in the reference or in an inline definition, never in a global definition
        for child in schema.children:
            if child.type == 'group-as':
                if child.attr.get('in-xml') == "GROUPED":
                    grouped = True #rather than look for the node outlined by the schema definition directly, look for the wrapper first
                groupName = child.attr.get('name')
            elif child.type == 'use-name': #because this can be given here too!
                useName = child.text #i do this one later so it will overrule the defined one
        return grouped, groupName, useName

    @staticmethod
    def strMatchesType(str, t):
        if t == "dateTime-with-timezone":
            t = "date-time-with-timezone"
        if t == "email":
            t = "email-address"
        pattern = ""
        overrule = False
        match t:
            case 'string':
                pattern = ".*"
            case 'base64':
                pattern = "[0-9A-Za-z+/]+={0,2}"
            case 'boolean':
                pattern = "true|1|false|0"
            case 'date':
                pattern = "(((2000|2400|2800|(19|2[0-9](0[48]|[2468][048]|[13579][26])))-02-29)|(((19|2[0-9])[0-9]{2})-02-(0[1-9]|1[0-9]|2[0-8]))|(((19|2[0-9])[0-9]{2})-(0[13578]|10|12)-(0[1-9]|[12][0-9]|3[01]))|(((19|2[0-9])[0-9]{2})-(0[469]|11)-(0[1-9]|[12][0-9]|30)))(Z|(-((0[0-9]|1[0-2]):00|0[39]:30)|\\+((0[0-9]|1[0-4]):00|(0[34569]|10):30|(0[58]|12):45)))?"
            case 'date-time':
                pattern = "(((2000|2400|2800|(19|2[0-9](0[48]|[2468][048]|[13579][26])))-02-29)|(((19|2[0-9])[0-9]{2})-02-(0[1-9]|1[0-9]|2[0-8]))|(((19|2[0-9])[0-9]{2})-(0[13578]|10|12)-(0[1-9]|[12][0-9]|3[01]))|(((19|2[0-9])[0-9]{2})-(0[469]|11)-(0[1-9]|[12][0-9]|30)))T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\\.[0-9]+)?(Z|(-((0[0-9]|1[0-2]):00|0[39]:30)|\\+((0[0-9]|1[0-4]):00|(0[34569]|10):30|(0[58]|12):45)))?"
            case 'date-time-with-timezone':
                pattern = "(((2000|2400|2800|(19|2[0-9](0[48]|[2468][048]|[13579][26])))-02-29)|(((19|2[0-9])[0-9]{2})-02-(0[1-9]|1[0-9]|2[0-8]))|(((19|2[0-9])[0-9]{2})-(0[13578]|10|12)-(0[1-9]|[12][0-9]|3[01]))|(((19|2[0-9])[0-9]{2})-(0[469]|11)-(0[1-9]|[12][0-9]|30)))T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\\.[0-9]+)?(Z|(-((0[0-9]|1[0-2]):00|0[39]:30)|\\+((0[0-9]|1[0-4]):00|(0[34569]|10):30|(0[58]|12):45)))"
            case 'date-with-timezone':
                pattern = "(((2000|2400|2800|(19|2[0-9](0[48]|[2468][048]|[13579][26])))-02-29)|(((19|2[0-9])[0-9]{2})-02-(0[1-9]|1[0-9]|2[0-8]))|(((19|2[0-9])[0-9]{2})-(0[13578]|10|12)-(0[1-9]|[12][0-9]|3[01]))|(((19|2[0-9])[0-9]{2})-(0[469]|11)-(0[1-9]|[12][0-9]|30)))(Z|(-((0[0-9]|1[0-2]):00|0[39]:30)|\\+((0[0-9]|1[0-4]):00|(0[34569]|10):30|(0[58]|12):45)))"
            case 'day-time-duration':
                pattern = "-?P([0-9]+D(T(([0-9]+H([0-9]+M)?(([0-9]+|[0-9]+(\\.[0-9]+)?)S)?)|([0-9]+M(([0-9]+|[0-9]+(\\.[0-9]+)?)S)?)|([0-9]+|[0-9]+(\\.[0-9]+)?)S))?)|T(([0-9]+H([0-9]+M)?(([0-9]+|[0-9]+(\\.[0-9]+)?)S)?)|([0-9]+M(([0-9]+|[0-9]+(\\.[0-9]+)?)S)?)|([0-9]+|[0-9]+(\\.[0-9]+)?)S)"
            case 'decimal':
                pattern = "\\S(.*\\S)?"
            case 'email-address':
                pattern = ".+@.+"
            case 'hostname':
                pattern = "[A-Za-z\\.]*[A-Za-z]"
            case 'integer':
                pattern = "\\S(.*\\S)?"
            case 'ip-v4-address':
                pattern = "((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9]).){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])"
            case 'ip-v6-address':
                pattern = "(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|[fF][eE]80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::([fF]{4}(:0{1,4}){0,1}:){0,1}((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9]).){3,3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9]).){3,3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9]))"
            case 'non-negative-integer':
                pattern = "\\S(.*\\S)?"
            case 'positive-integer':
                pattern = "\\S(.*\\S)?"
            case 'token':
                pattern = "(\\p{L}|_)(\\p{L}|\\p{N}|[.\\-_])*"
            case 'uri':
                pattern = "[a-zA-Z][a-zA-Z0-9+\\-.]+:.*\\S"
            case 'uri-reference':
                pattern = "\\S(.*\\S)?"
            case 'uuid':
                pattern = "[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[45][0-9A-Fa-f]{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}"
            case _:
                print(f"WARNING: unknown type {t}")
                overrule = True
        return overrule or bool(re.fullmatch(pattern, str))
    
    @staticmethod
    def constraintSatisfied(base, constraint):
        if constraint.type == 'allowed-values':
            if constraint.attr.get('allow-other') == "no":
                targets = Assembly.evalPath(base, constraint.attr.get('target'))
                for val in targets:
                    valAllowed = False
                    for enum in constraint.children:
                        if val == enum.attr['value']:
                            valAllowed = True
                    if not valAllowed:
                        return False
            return True
        elif constraint.type == 'matches':
            targets = Assembly.evalPath(base, constraint.attr.get('target'))
            valid = True
            for val in targets:
                if val is not None:
                    if constraint.attr.get('datatype') is not None:
                        valid = valid and Assembly.strMatchesType(val, constraint.attr.get('datatype'))
                    else:
                        valid = valid and bool(re.fullmatch(constraint.attr.get('regex'), val))
            return valid
        elif constraint.type == 'index-has-key':
            return True
        elif constraint.type == 'expect':
            return True
        elif constraint.type == 'index':
            return True
        elif constraint.type == 'is-unique':
            return True
        elif constraint.type == 'has-cardinality':
            return True
        else:
            print("unknown constraint type "+constraint.type)
            return False
        
    @staticmethod
    def evalPath(base, path):
        if path == '':
            return base
        if not isinstance(base, list):
            base = [base]
        
        #              path
        #name[selector]/remainder
        name = ""
        selector = ""
        remainder = ""
        nameComplete = False
        nesting = 0
        for c in path:
            if nameComplete:
                if nesting == 0:
                    remainder += c
                else:
                    if c == '[':
                        nesting += 1
                    elif c == ']':
                        nesting -= 1
                    selector += c
            else:
                if c == '[':
                    nameComplete = True
                    nesting += 1
                    selector += c
                elif c == '/':
                    nameComplete = True
                else:
                    name += c

        getFrom = []
        if name == '.':
            for node in base:
                getFrom.append(node)
        elif name[0] == '@':
            for node in base:
                getFrom.append(node.attr.get(name[1:]))
        else:
            for node in base:
                for child in node.children:
                    if child.type == name:
                        getFrom.append(child)
        selected = []
        if selector != '':
            selector = selector[1:-1]
            if selector[0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                selected = [getFrom[int(selector)-1]] #xpath specs say that the first in a list is the [1]th.
            elif selector.find('=') != -1:
                for node in getFrom:
                    matches = False
                    for s in Assembly.evalPath(node, selector[:selector.find('=')]):
                        if s == selector[selector.find('=')+1:]:
                            matches = True
                    if matches:
                        selected.append(node)
            else:
                for node in getFrom:
                    if len(Assembly.evalPath(node, selector)) > 0:
                        selected.append(node)
        else:
            selected = getFrom
        if remainder != '':
            return Assembly.evalPath(selected, remainder[1:])
        else:
            return selected
    
    def __str__(self):
        return str(self.node)
    
    def asXML(self):
        return str(self.node)
    
    def asJson(self):
        toRet = {}
        for element in self.schema.children:
            if element.type == 'define-flag' or element.type == 'flag':
                toRet[element.attr.get('name') or element.attr.get('ref')] = self.node.attr.get(element.attr.get('name') or element.attr.get('ref'))
            elif element.type == 'model':
                ni = 0
                for subelement in element.children:
                    iterOver = [subelement]
                    if subelement.type == 'choice':
                        iterOver = subelement.children
                    for child in iterOver:
                        if child.type == 'assembly' or child.type == 'field':
                            schemadef = self.namespace.get(child.attr['ref'])
                        else:
                            schemadef = child

                        grouped = False
                        xmlGrouped = False
                        groupName = ""
                        useName = schemadef.attr['name']
                        for subchild in schemadef.children:
                            if subchild.type == 'use-name':
                                useName = subchild.text
                        for subchild in child.children:
                            if subchild.type == 'use-name':
                                useName = subchild.text
                            elif subchild.type == 'group-as':
                                if subchild.attr.get('in-xml') == 'GROUPED':
                                    xmlGrouped = True
                                if subchild.attr.get('in-json') == 'ARRAY':
                                    grouped = True
                                groupName = subchild.attr.get('name')
                        
                        childrenArr = self.node.children

                        if schemadef.attr.get('in-xml') == 'UNWRAPPED':
                            #need to take children and convert to common mark
                            continue

                        lni = ni
                        if xmlGrouped:
                            if self.node.children[ni].type == groupName:
                                childrenArr = self.node.children[ni].children
                                lni = 0
                                ni = ni + 1
                            else:
                                continue

                        t = []
                        while (grouped or ni == lni) and lni < len(childrenArr) and childrenArr[lni].type == useName:
                            if child.type == 'assembly':
                                t.append(Assembly(schemadef, childrenArr[lni], self.namespace.parent(schemadef.attr['name'])).asJson())
                            elif child.type == 'define-assembly':
                                t.append(Assembly(schemadef, childrenArr[lni], self.namespace, True).asJson())
                            else: #field or define-field
                                #TODO: check if type is markup & convert to common mark
                                t.append(childrenArr[lni].text)
                            lni = lni + 1

                        if len(t) == 0:
                            continue
                        if not xmlGrouped:
                            ni = lni
                        if not grouped:
                            t = t[0]
                            toRet[useName] = t
                        else:
                            toRet[groupName] = t
        return toRet

    def get(self, key):
        if self.node.attr.get(key) is not None:
            return self.node.attr[key]
        for child in self.node.children:
            if child.type == key:
                return child
        return None
    
    def __getitem__(self, key):
        return self.evalPath(self.node, key)
    
    def set(self, key, value):
        if self.node.attr.get(key) is not None:
            self.node.attr[key] = value
        else:
            for i in range(0, len(self.node.children)):
                if self.node.children[i].type == key:
                    self.node.children[i] = value
                    
            
def htmlToMarkup(tagArr):
    toRet = ""
    if len(tagArr) == 0:
        return toRet
    for tag in tagArr:
        if tag.type == "em" or tag.type == "i":
            toRet = toRet+f'*{tag.text}{htmlToMarkup(tag.children)}*'
        elif tag.type == "strong" or tag.type == "b":
            toRet = toRet+f'**{tag.text}{htmlToMarkup(tag.children)}**'
        elif tag.type == "code":
            toRet = toRet+f'`{tag.text}{htmlToMarkup(tag.children)}`'
        elif tag.type == "q":
            toRet = toRet+f'"{tag.text}{htmlToMarkup(tag.children)}"'
        elif tag.type == "sub":
            toRet = toRet+f'~{tag.text}{htmlToMarkup(tag.children)}~'
        elif tag.type == "sup":
            toRet = toRet+f'^{tag.text}{htmlToMarkup(tag.children)}^'
        elif tag.type == "img":
            alt = tag.attr.get("alt") or ""
            url = tag.attr.get("src") or ""
            title = tag.attr.get("title") or ""
            toRet = toRet+f'![{alt}]({url} "{title}")'
        elif tag.type == 'a':
            url = tag.attr.get('href')
            toRet = toRet+f'[{tag.text}]({url})'
        elif tag.type == 'insert':
            t = tag.attr.get('type')
            ref = tag.attr.get('id-ref')
            toRet = toRet+'{{'+f' insert: {t}, {ref}'+'}}'
        elif tag.type == 'h1':
            toRet = toRet+f'# {tag.text}{htmlToMarkup(tag.children)}\n'
        elif tag.type == 'h2':
            toRet = toRet+f'## {tag.text}{htmlToMarkup(tag.children)}\n'
        elif tag.type == 'h3':
            toRet = toRet+f'### {tag.text}{htmlToMarkup(tag.children)}\n'
        elif tag.type == 'h4':
            toRet = toRet+f'#### {tag.text}{htmlToMarkup(tag.children)}\n'
        elif tag.type == 'h5':
            toRet = toRet+f'##### {tag.text}{htmlToMarkup(tag.children)}\n'
        elif tag.type == 'h6':
            toRet = toRet+f'###### {tag.text}{htmlToMarkup(tag.children)}\n'
        elif tag.type == 'pre':
            toRet = toRet+f'```\n{tag.text}{htmlToMarkup(tag.children)}\n```\n'
        elif tag.type == 'ol':
            toRet += '\n'
            index = 1
            for li in tag.children:
                toRet += f'{index}. {tag.text}{htmlToMarkup(tag.children)}\n'
        elif tag.type == 'ul':
            toRet += '\n'
            for li in tag.children:
                toRet += f'- {tag.text}{htmlToMarkup(tag.children)}'
        elif tag.type == 'blockquote':
            toRet = toRet+f'> {tag.text}{htmlToMarkup(tag.children)}\n'
        elif tag.type == 'p':
            toRet = toRet+f'{tag.text}{htmlToMarkup(tag.children)}\n\n'
        # not gonna do tables yet
    return toRet

class WAssembly:
    def __init__(self, node, namespace, schemaname):
        self._asm = Assembly(namespace.get(schemaname), node, namespace, False)
    def __getattr__(self, name: str):
        return self._asm.node.attr[name]
    def __getitem__(self, key):
        gotten = self._asm[key]
        for i in range(0, len(gotten)):
            if len(gotten[i].children) == 0:
                gotten[i] = gotten[i].text
        if len(gotten) == 1:
            gotten = gotten[0]
        elif len(gotten) == 0:
            return None
        return gotten
    def validate(self):
        return self._asm.validate()