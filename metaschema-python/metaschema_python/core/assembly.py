from pathlib import Path
from lxml import etree
import math
import re

class Context:
    def __init__(self, path: str | Path, binding="xml"):
        self.types = {}
        self.subspaces = []

        metaschema = MetaschemaContext()
        self.subspaces.append(metaschema)

        if path is not None:
            base_path = Path(Path(path).parent)
            if binding == 'xml':
                parser = etree.XMLParser(load_dtd=True, resolve_entities=True, remove_comments=True)
                xml_tree = etree.parse(path, parser=parser)
                root = Assembly.fromXML(xml_tree.getroot(), metaschema.get("METASCHEMA"), self)

        METASCHEMA = root
        includes = []

        for include in METASCHEMA['imports']:
            includes.append(include.href)
        
        for definition in METASCHEMA['definitions']:
            self.types[definition.name] = definition
        
        #remove metaschema default from subspaces
        self.subspaces.clear()
        #hunt down includes
        for include in includes:
            self.subspaces.append(Context(str(Path(base_path, include))))

    #get a definition from a context & its children
    def get(self, name: str) -> 'Assembly | None':
        if self.types.get(name) is not None:
            return self.types[name]
        for subspace in self.subspaces:
            if subspace.get(name) is not None:
                return subspace.get(name)
        return None
    #get the context that contains a definition
    def parent(self, name: str) -> 'Context | None':
        if self.types.get(name) is not None:
            return self
        for subspace in self.subspaces:
            if subspace.parent(name) is not None:
                return subspace.parent(name)
        return None
    
    def instantiate(self, type, binding, path):
        if binding == 'xml':
            parser = etree.XMLParser(load_dtd=True, resolve_entities=True, remove_comments=True)
            xml_tree = etree.parse(path, parser=parser)
            root = xml_tree.getroot()
            return ModelObject.fromXML(root, self.get(type), self)


class SchemaObject:
    def __init__(self):
        self._schema = Assembly()
        self._context = None
        self._contents = ""
    def _setschema(self, schema: 'Assembly'):
        object.__setattr__(self, '_schema', schema)
    def __str__(self):
        return self._contents
    def validate(self):
        t = self._schema._flags.get('as-type') or 'string'
        str = self._contents
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
    
class Flag(SchemaObject):
    def __init__(self):
        self._schema = None
        self._contents = None

class ModelObject(SchemaObject):
    def __init__(self):
        object.__setattr__(self, '_flags', {})
        object.__setattr__(self, '_context', None)
        object.__setattr__(self, '_schema', None)
    def __getattr__(self, name):
        return self._flags.get(name)
        #return self._flags[name]
    def __setattr__(self, name, value):
        self._flags[name] = value
    @staticmethod
    def fromXML(xml, schema, context):
        t = schema._schema.name
        if t == 'inline-define-field' or t == 'define-field':
            return Field.fromXML(xml, schema, context)
        else:
            return Assembly.fromXML(xml, schema, context)
    @staticmethod
    def XMLevalSchema(xmls, schema, parentcontext):
        if schema is None:
            raise Exception("schema is None!")
        elif schema._schema is None:
            raise Exception("no idea what sort of thing this is supposed to be")
        if schema.name == 'any':
            xmls.clear()
            return [] #FIXME
        schemas = [schema]
        if schema._schema.name in ['choice', 'choice-group']:
            schemas = schema['choices']
        effectiveNames = []
        defs = {}
        ctxs = {}
        for potentialSchema in schemas:
            ctx = parentcontext
            schemadef = potentialSchema
            effectiveName = potentialSchema._getEffectiveName()
            if potentialSchema._schema.name in ['field-reference', 'assembly-reference']:
                schemadef = parentcontext.get(potentialSchema.ref)
                ctx = parentcontext.parent(potentialSchema.ref)

            effectiveNames.append(effectiveName)
            defs[effectiveName] = schemadef
            ctxs[effectiveName] = ctx

        if schema._schema.name in ['inline-define-field', 'field-reference'] and schema._flags.get('in-xml') == 'UNWRAPPED':
            #need to convert them to markdown
            toRet = Field(Field.convertHTMLtoMarkdown(xmls))
            toRet._setschema(schema)
            return toRet

        maxOccurs = schema._flags.get('max-occurs') or 1
        if maxOccurs == 'unbounded':
            maxOccurs = math.inf
        else:
            maxOccurs = int(maxOccurs)

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

        arrtogetfrom = xmls
        if maxOccurs > 1:
            #we need to find a group-name in case it's grouped in xml
            if schema['group-as'] is not None:
                if schema['group-as']._flags.get('in-xml') == 'GROUPED':
                    if len(xmls) == 0:
                        return []
                    if remNs(xmls[0].tag) == schema['group-as'].name:
                        arrtogetfrom = list(xmls.pop(0))
                    else:
                        return []

        count = 0
        listOfInstances = []
        while len(arrtogetfrom) > 0 and count < maxOccurs and remNs(arrtogetfrom[0].tag) in effectiveNames:
            count += 1
            gottenName = remNs(arrtogetfrom[0].tag)
            listOfInstances.append(ModelObject.fromXML(arrtogetfrom.pop(0), defs[gottenName], ctxs[gottenName]))
        
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
        object.__setattr__(self, '_contents', value)
        object.__setattr__(self, '_schema', None)
        object.__setattr__(self, '_flags', {})
    def validate(self):
        for flag in self._flags:
            if not flag.validate():
                return False
        if self._schema._flags.get('as-type') == 'markup-line' or self._schema._flags.get('as-type') == 'markup-multiline':
            pass
        else:
            return super().validate()
    @staticmethod
    def fromXML(xml, schema, context):
        if schema is None:
            raise Exception("grand failure! no schema!")
        elif schema['flags'] is None:
            schema['flags']
            raise Exception("failure: "+(schema.name or schema.ref)+" does not have iterable flags (not a field?)")
        toRet = Field(xml.text)
        object.__setattr__(toRet, '_schema', schema)
        object.__setattr__(toRet, '_context', context)
        for flag in schema['flags']:
            flagdef = flag
            if flag._schema.name == 'flag-reference':
                flagdef = context.get(flag.name)
            effectiveName = flag._getEffectiveName()
            value = xml.attrib.get(effectiveName)
            if value is None:
                if flag.required == 'yes' and flagdef.default is None:
                    pass #THROW ERROR!!!
            toRet._flags[effectiveName] = value
        return toRet
    @staticmethod
    def convertHTMLtoMarkdown(xmls):
        string = ""
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
        
        htmlElements = ['p','em', 'i', 'strong', 'b', 'code', 'q', 'sub', 'sup', 'img', 'a', 'insert', 'h1', 'h2', 'h3', 'h4', 'h5','h6','pre','ol','ul', 'li', 'blockquote', 'table', 'tr', 'th', 'td']
        while len(xmls) > 0 and remNs(xmls[0].tag) in htmlElements:
            xml = xmls.pop(0)
            name = remNs(xml.tag)
            text = xml.text or ''
            tail = xml.tail or ''
            if name == 'i':
                name = 'em'
            elif name == 'b':
                name = 'strong'
            match name:
                case 'p':
                    string+=text+Field.convertHTMLtoMarkdown(list(xml))+'\\n\\n'+tail
                case 'em':
                    string+='*'+text+Field.convertHTMLtoMarkdown(list(xml))+'*'+tail
                case 'strong':
                    string+='**'+text+Field.convertHTMLtoMarkdown(list(xml))+'**'+tail
                case 'code':
                    string+='`'+text+Field.convertHTMLtoMarkdown(list(xml))+'`'+tail
                case 'q':
                    string+='"'+text+Field.convertHTMLtoMarkdown(list(xml))+'"'+tail
                case 'sub':
                    string+='~'+text+Field.convertHTMLtoMarkdown(list(xml))+'~'+tail
                case 'sup':
                    string+='^'+text+Field.convertHTMLtoMarkdown(list(xml))+'^'+tail
                case 'img':
                    string+=f'![{xml.attrib["alt"]}]({xml.attrib["src"]} "{xml.attrib["title"]}")'+tail
                case 'a':
                    string+=f'[{xml.text}](*{xml.attrib["href"]}*)'+tail
                case 'insert':
                    string+='{{ insert: '+xml.attrib['type']+', '+xml.attrib['id-ref']+' }}'+tail
                case 'h1':
                    string+='# '+text+'\n'+tail
                case 'h2':
                    string+='## '+text+'\n'+tail
                case 'h3':
                    string+='### '+text+'\n'+tail
                case 'h4':
                    string+='#### '+text+'\n'+tail
                case 'h5':
                    string+='##### '+text+'\n'+tail
                case 'h6':
                    string+='###### '+text+'\n'+tail
                case 'pre':
                    string+='\n```\n'+text+'\n```\n'+tail
                case 'ol':
                    index = 0
                    for subelement in xml:
                        index = index + 1
                        string+=str(index)+'. '+subelement.text+'\n'
                    string+=tail
                case 'ul':
                    for subelement in xml:
                        string+='- '+subelement.text+'\n'
                    string+=tail
                case 'blockquote':
                    string+='> '+text+'\n'+tail
        return string

class Assembly(ModelObject):
    _contents: list[ModelObject]
    _context: Context
    def __init__(self):
        object.__setattr__(self, '_flags', {})
        object.__setattr__(self, '_contents', []) #indexed by numbers corresponding to position in model
        object.__setattr__(self, '_context', None)
        object.__setattr__(self, '_schema', None) #assembly representing instance of either inline define assembly, or global define assembly
    @staticmethod
    def fromXML(xml, schema, context: Context):
        toRet = Assembly()
        object.__setattr__(toRet, '_schema', schema)
        object.__setattr__(toRet, '_context', context)
        for flag in schema['flags']:
            flagdef = flag
            if flag._schema.name == 'flag-reference':
                flagdef = context.get(flag.ref)
                if flagdef == None:
                    raise Exception("could not find flag definition for "+flag.ref)
            effectiveName = flag._getEffectiveName()
            value = xml.attrib.get(effectiveName)
            if value is None:
                if flag.required == 'yes' and flagdef.default is None:
                    pass #throw an error
                #if it's not required, or there is a default, all is well.
            toRet._flags[effectiveName] = value

        children = list(xml)
        for child in schema['model']:
            if child is None or child._schema is None:
                raise Exception("bad schema")
            toRet._contents.append(ModelObject.XMLevalSchema(children, child, context))
        if len(children) > 0:
            print("WARNING: remaining unparsed children")
            #print(f"(could not parse past {children[0].tag} type)")
        return toRet



    @staticmethod
    def fromJSON(json):
        pass
    def _nameToIndex(self, name):
        #code will recurse infinitely if we do not give hard definitions to anchor some types down
        #without these define-assembly will call this function on inline-define-assembly for the name 'model'
        #and in turn inline-define-assembly would call this function on define-assembly for the name 'model'
        #while we're at it, giving them hard definitions, it's nice to include other things as well
        #since you could dereference them by numbers and circumvent calling _nameToIndex altogether, these are really more for programmer readability than anything
        #global definition: formalName, desc, props, usename/rootname, [jsonkey, flags, [model,]] constraints, remarks, example
        #inline definition: formalName, desc, props, jsonkey, ?????
        #references: formalName, desc, props, usename, groupAs, remarks
        if self._schema.name in ['define-assembly', 'define-field', 'define-flag', 'inline-define-assembly','inline-define-field','inline-define-flag','assembly-reference','field-reference','flag-reference']: 
            semSource = {
                'define-assembly':{
                    'use-name':3,
                    'flags':5,
                    'model':6
                },
                'define-field':{
                    'use-name':3,
                    'flags':6
                },
                'define-flag':{
                    'use-name':3
                },
                'inline-define-assembly':{
                    'group-as':4,
                    'flags':5,
                    'model':6
                },
                'inline-define-field':{
                    'group-as':5,
                    'flags':6
                },
                'inline-define-flag':{},
                'assembly-reference':{
                    'use-name':3,
                    'group-as':4
                },
                'field-reference':{
                    'use-name':3,
                    'group-as':4
                },
                'flag-reference':{
                    'use-name':3,
                    'group-as':4
                }
            }
            if semSource[self._schema.name].get(name) is not None:
                return semSource[self._schema.name].get(name)
        index = 0
        for child in self._schema['model']:
            if child._flags.get('max-occurs') is not None and (child._flags['max-occurs'] == 'unbounded' or int(child._flags['max-occurs']) > 1):
                if name == child['group-as'].name:
                    return index
            elif child._schema.name == 'choice':
                #need to check for each option of the choice
                pass
            else:
                #need to check for a usename
                if name == child._getEffectiveName():
                    return index
            index = index + 1
        return -1
    def __getitem__(self, key):
        if isinstance(key, int):
            return self._contents[key]
        if self._nameToIndex(key) >= len(self._contents) or self._nameToIndex(key) < 0:
            print('a') #FIXME
        return self._contents[self._nameToIndex(key)]
    def __setitem__(self, key, value):
        if isinstance(key, int):
            self._contents[key] = value
        else:
            self._contents[self._nameToIndex(key)] = value
    #def __iter__(self):
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
        for flag in self['flags']: #the 5th element in an assembly def is the list of flagrefs/defs
            flagdef = flag
            if flag['ref'] is not None:
                flagdef = self._context.get(flag['ref'])
            if flagdef['required'] == 'yes' and self[flagdef['name']] is None:
                return False
        for sch in self['model']: #6 is the model
            schdef = sch
            if sch.flags.get('ref') is not None:
                schdef = self.context.get(flag.flags.get('ref'))
        return True
    def _getEffectiveName(self): #called on a schema
        #we can only look for a usename in specific types (global definitions & references)
        if self._schema.name in ['define-assembly', 'define-field', 'define-flag', 'assembly-reference', 'field-reference', 'flag-reference']:
            if self['use-name'] is not None:
                return self['use-name']._contents
        if self._schema.name in ['flag-reference', 'field-reference', 'assembly-reference']:
            schdef = self._context.get(self.ref)
            if schdef['use-name'] is not None:
                return schdef['use-name']._contents
            if schdef.name is None:
                print("bweh")
            return schdef.name
            #we only need to check in this if, because everywhere else schdef = self and was checked already
        if self.name is None:
            print("bweh")
        return self.name
    def _initContents(self, num):
        for i in range(0, num):
            self._contents.append(None)

#we can't read a metaschema without some knowledge of what the schema is
#the schema for metaschema itself is no exception
#so we have to hard-code metaschema's model
#(or just enough of it so that the code above can use it as if it were metaschema's model)
#that's what this is
#beyond here be dragons
    
class MetaschemaContext(Context):
    def __init__(self):
        metaschema = Assembly()
        gAsmDef = Assembly()
        gFieldDef = Assembly()
        gFlagDef = Assembly()
        iAsmDef = Assembly()
        iFieldDef = Assembly()
        iFlagDef = Assembly()
        asmRef = Assembly()
        fieldRef = Assembly()
        flagRef = Assembly()
        choice = Assembly()
        self.metaschema = Assembly()

        self.metaschema._setschema(metaschema)
        metaschema._setschema(gAsmDef)
        gAsmDef._setschema(iAsmDef)
        gFieldDef._setschema(iAsmDef)
        gFlagDef._setschema(iAsmDef)
        iAsmDef._setschema(gAsmDef)
        iFieldDef._setschema(gAsmDef)
        iFlagDef._setschema(gAsmDef)
        asmRef._setschema(gAsmDef)
        fieldRef._setschema(gAsmDef)
        flagRef._setschema(gAsmDef)
        choice._setschema(iAsmDef)

        singleChoice = Assembly()
        singleChoice._setschema(gAsmDef)

        gAsmDef.name = 'define-assembly'
        gFieldDef.name ='define-field'
        gFlagDef.name = 'define-flag'
        iAsmDef.name = 'inline-define-assembly'
        iFieldDef.name = 'inline-define-field'
        iFlagDef.name = 'inline-define-flag'
        asmRef.name = 'assembly-reference'
        fieldRef.name = 'field-reference'
        flagRef.name = 'flag-reference'

        def iAsmDefInst(name, flags=[], model=[], groupName=None, rq=False, cstrt=[], fn=None, dsc=None,props=[],jskey=None,rmrks=None,ex=[]):
            toRet = Assembly()
            toRet._setschema(iAsmDef)
            toRet.name = name
            toRet._flags['min-occurs'] = '1' if rq else '0'
            toRet._flags['max-occurs'] = '1' if groupName is None else 'unbounded'
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
                toRet[4]._flags['in-json'] = 'ARRAY'
            toRet[5] = flags
            toRet[6] = model
            toRet[7] = cstrt
            toRet[8] = rmrks
            toRet[9] = ex
            return toRet


        definitionName = Assembly()
        definitionName._setschema(iFlagDef)
        definitionName.name = 'name'
        definitionName.required = 'yes'
        definitionReference = Assembly()
        definitionReference._setschema(iFlagDef)
        definitionReference.name = 'ref'
        definitionReference.required = 'yes'
        defaultValue = Assembly()
        defaultValue._setschema(iFlagDef)
        defaultValue.name = 'default'
        cardinalityMinOccurs = Assembly()
        cardinalityMinOccurs._setschema(iFlagDef)
        cardinalityMinOccurs.name = 'min-occurs'
        cardinalityMinOccurs.default = '0'
        cardinalityMaxOccurs = Assembly()
        cardinalityMaxOccurs._setschema(iFlagDef)
        cardinalityMaxOccurs.name = 'max-occurs'
        cardinalityMaxOccurs.default = '1'

        groupAs = Assembly()

        anyData = iAsmDefInst('any')

        formalName = Assembly()
        formalName._setschema(iFieldDef)
        formalName.name = 'formal-name'
        formalName._initContents(10)
        formalName[2] = []
        formalName['flags'] = []
        description = Assembly()
        description._setschema(iFieldDef)
        description.name = 'description'
        description._initContents(10)
        description['flags'] = []
        props = Assembly()
        props._setschema(iAsmDef)
        props.name = 'prop' #should be property
        props._flags['max-occurs'] = 'unbounded'
        props._initContents(10)
        props['group-as'] = Assembly() #group-as props
        props['group-as']._setschema(groupAs)
        props['group-as'].name = 'props'
        props['group-as']._flags['in-json'] = 'ARRAY'
        props['flags'] = [ Assembly(), Assembly(), Assembly() ]
        props['flags'][0]._setschema(iFlagDef)
        props['flags'][0].name = 'name'
        props['flags'][0]._flags['as-type'] = 'token'
        props['flags'][0].required = 'yes'
        props['flags'][1]._setschema(iFlagDef)
        props['flags'][1].name = 'namespace'
        props['flags'][1]._flags['as-type'] = 'uri'
        props['flags'][1].default = 'http://csrc.nist.gov/ns/oscal/metaschema/1.0'
        props['flags'][2]._setschema(iFlagDef)
        props['flags'][2].name = 'value'
        props['flags'][2]._flags['as-type'] = 'token'
        props['flags'][2].required = 'yes'
        props['model'] = []
        usename = Assembly()
        usename._setschema(iFieldDef)
        usename.name = 'use-name'
        usename._flags['as-type'] = 'token'
        usename._initContents(10)
        usename['flags'] = []
        jsonKey = Assembly()
        jsonKey._setschema(iAsmDef)
        jsonKey.name = 'json-key'
        jsonKey._initContents(10)
        jsonKey['flags'] = [ Assembly() ]
        jsonKey['flags'][0]._setschema(iFlagDef)
        jsonKey['flags'][0].name = 'flag-ref'
        jsonKey['flags'][0]._flags['as-type'] = 'token'
        jsonKey['flags'][0].required = 'yes'
        jsonKey['model'] = []
        groupAs._setschema(iAsmDef)
        groupAs.name = 'group-as'
        groupAs._initContents(10)
        groupAs['flags'] = [ Assembly(), Assembly(), Assembly() ]
        groupAs['flags'][0]._setschema(iFlagDef)
        groupAs['flags'][0].name = 'name'
        groupAs['flags'][0]._flags['as-type'] = 'token'
        groupAs['flags'][0].required = 'yes'
        groupAs['flags'][1]._setschema(iFlagDef)
        groupAs['flags'][1].name = 'in-json'
        groupAs['flags'][1]._flags['as-type'] = 'token'
        groupAs['flags'][1].default = 'SINGLETON_OR_ARRAY'
        groupAs['flags'][2]._setschema(iFlagDef)
        groupAs['flags'][2].name = 'in-xml'
        groupAs['flags'][2]._flags['as-type'] = 'token'
        groupAs['flags'][2].default = 'UNGROUPED'
        groupAs['model'] = []
        remarks = Assembly()
        remarks._setschema(iFieldDef)
        remarks.name = 'remarks'
        remarks._flags['as-type'] = 'markup-multiline'
        remarks._initContents(10)
        remarks['flags'] = [ Assembly() ]
        remarks['flags'][0]._setschema(iFlagDef)
        remarks['flags'][0].name = 'class'
        remarks['flags'][0]._flags['as-type'] = 'token'
        remarks['flags'][0].default = 'ALL'
        example = Assembly()
        example._setschema(iAsmDef)
        example.name = 'example'
        example._initContents(10)
        example[4] = Assembly() #group-as
        example[5] = [] #skipping some for now
        example[6] = [
            description, #define-field description
            remarks, #field remarks
            anyData #any
        ]

        jsonvaluekeyflagchoice = Assembly()
        jsonvaluekeyflagchoice._setschema(singleChoice)
        jsonvaluekeyflagchoice._initContents(1)
        jsonvaluekeyflagchoice[0] = [
            Assembly(), #define-field json-value-key
            Assembly()  #assembly json-value-key-flag
        ]
        jsonvaluekeyflagchoice[0][0]._setschema(iFieldDef)
        jsonvaluekeyflagchoice[0][0].name = 'json-value-key'
        jsonvaluekeyflagchoice[0][0]._flags['as-type'] = 'token'
        jsonvaluekeyflagchoice[0][0]._initContents(10)
        jsonvaluekeyflagchoice[0][0]['flags'] = []
        jsonvaluekeyflagchoice[0][1]._setschema(iAsmDef)
        jsonvaluekeyflagchoice[0][1].name = 'json-value-key-flag'
        jsonvaluekeyflagchoice[0][1]._initContents(10)
        jsonvaluekeyflagchoice[0][1][5] = [ Assembly() ]
        jsonvaluekeyflagchoice[0][1][5][0]._setschema(iFlagDef)
        jsonvaluekeyflagchoice[0][1][5][0].name = 'flag-ref'
        jsonvaluekeyflagchoice[0][1][5][0]._flags['as-type'] = 'token'
        jsonvaluekeyflagchoice[0][1][5][0].required = 'yes'
        jsonvaluekeyflagchoice[0][1][5][0]._initContents(6)

        asTypeSimple = Assembly()
        asTypeSimple._setschema(gFlagDef)
        asTypeSimple.name = 'as-type-simple'
        asTypeSimple._flags['as-type'] = 'token'
        asTypeSimple._initContents(7)
        asTypeSimple[3] = Field('as-type')
        asTypeSimple[3]._setschema(usename)
        #the only other thing it has is constraints.

        constraintLetExpr = Assembly()
        constraintLetExpr._setschema(iAsmDef)
        constraintLetExpr.name = 'let' #'constraint-let-expression'
        constraintLetExpr._initContents(10)
        constraintLetExpr['flags'] = [ Assembly(), Assembly() ]
        constraintLetExpr['flags'][0]._setschema(iFlagDef)
        constraintLetExpr['flags'][0].name = 'var'
        constraintLetExpr['flags'][0]._flags['as-type'] = 'token'
        constraintLetExpr['flags'][0].required = 'yes'
        constraintLetExpr['flags'][1].name = 'expression'
        constraintLetExpr['flags'][1].required = 'yes'
        constraintLetExpr['model'] = [ remarks ]

        cstrtId = Assembly()
        cstrtId._setschema(iFlagDef)
        cstrtId.name = 'id' #'constraint-identifier'
        cstrtId._flags['as-type'] = 'token'
        cstrtSvty = Assembly()
        cstrtSvty._setschema(iFlagDef)
        cstrtSvty.name = 'level'#'constraint-severity-level'
        cstrtSvty._flags['as-type'] = 'token'
        cstrtSvty.default = 'ERROR'
        cstrtAllowOther = Assembly()
        cstrtAllowOther._setschema(iFlagDef)
        cstrtAllowOther.name = 'allow-other' #'constraint-allow-other'
        cstrtAllowOther._flags['as-type'] = 'token'
        cstrtAllowOther.default = 'no'
        cstrtMatchesRegex = Assembly()
        cstrtMatchesRegex._setschema(iFlagDef)
        cstrtMatchesRegex.name = 'regex' #'constraint-matches-regex'

        cstrtEx = Assembly()
        cstrtEx._setschema(iFlagDef)
        cstrtEx.name = 'extensible' #'constraint-extensible'
        cstrtEx._flags['as-type'] = 'token'
        cstrtEx.default = 'external'
        cstrtTg = Assembly()
        cstrtTg._setschema(iFlagDef)
        cstrtTg.name = 'target' #'constraint-target'
        cstrtTg.required = 'yes'
        cstrtValueEnum = Assembly()
        cstrtValueEnum._setschema(iFieldDef)
        cstrtValueEnum.name = 'enum' #'constraint-value-enum'
        cstrtValueEnum._flags['as-type'] = 'markup-line'
        cstrtValueEnum._initContents(10)
        cstrtValueEnum[3] = Field('remarks')
        cstrtValueEnum[3]._setschema(jsonKey)
        cstrtValueEnum[6] = [ Assembly(), Assembly() ]
        cstrtValueEnum[6][0]._setschema(iFlagDef)
        cstrtValueEnum[6][0].name = 'value'
        cstrtValueEnum[6][0].required = 'yes'
        cstrtValueEnum[6][0]._flags['min-occurs'] = '1'
        cstrtValueEnum[6][0]._flags['max-occurs'] = 'unbounded'
        cstrtValueEnum[6][1]._setschema(iFlagDef)
        cstrtValueEnum[6][1].name = 'deprecated'

        expectCstrtMsg = Assembly()
        expectCstrtMsg._setschema(iFieldDef)
        expectCstrtMsg.name = 'message' #expect-constraint-message
        expectCstrtMsg._initContents(10)
        expectCstrtMsg['flags'] = []
        keyCstrtFld = Assembly()
        keyCstrtFld._setschema(iAsmDef)
        keyCstrtFld.name = 'key-field'#'key-constraint-field'
        keyCstrtFld._flags['min-occurs'] = '1'
        keyCstrtFld._flags['max-occurs'] = 'unbounded'
        keyCstrtFld._initContents(10)
        keyCstrtFld[4] = Assembly()
        keyCstrtFld[4]._setschema(groupAs)
        keyCstrtFld[4].name = 'key-fields'
        keyCstrtFld[4]._flags['in-json'] = 'ARRAY'
        keyCstrtFld['flags'] = [ cstrtTg, Assembly() ]
        keyCstrtFld['flags'][1]._setschema(iFlagDef)
        keyCstrtFld['flags'][1].name = 'pattern'
        keyCstrtFld['model'] = [ remarks ]
        indexName = Assembly()
        indexName._setschema(iFlagDef)
        indexName.name = 'name'#'index-name'
        indexName._flags['as-type'] = 'token'
        indexName.required = 'yes'

        flagAllowVals = Assembly()
        flagAllowVals._setschema(iAsmDef)
        flagAllowVals.name = 'allowed-values'
        flagAllowVals._initContents(10)
        flagAllowVals['flags'] = [ cstrtId, cstrtSvty, cstrtAllowOther, cstrtEx ]
        flagAllowVals['model'] = [
            formalName,
            description,
            props,
            cstrtValueEnum, #field constraint-value-enum
            remarks
        ]
        flagAllowVals['model'][3]._setschema(iFieldDef)
        flagAllowVals['model'][3].name = 'enum'
        flagAllowVals['model'][3]._flags['min-occurs'] = '1'
        flagAllowVals['model'][3]._flags['max-occurs'] = 'unbounded'
        flagAllowVals['model'][3]._initContents(10)
        flagAllowVals['model'][3][5] = Assembly()
        flagAllowVals['model'][3][5]._setschema(groupAs)
        flagAllowVals['model'][3][5].name = 'enums'
        flagAllowVals['model'][3][5]._flags['in-json'] = 'ARRAY'
        flagExpect = Assembly()
        flagExpect._setschema(iAsmDef)
        flagExpect.name = 'expect'
        flagExpect._initContents(10)
        flagExpect['flags'] = [ cstrtId, cstrtSvty, cstrtTg ]
        flagExpect['model'] = [
            formalName,
            description,
            props,
            expectCstrtMsg, #field expect-constraint-message
            remarks
        ]
        flagIndexHasKey = Assembly()
        flagIndexHasKey._setschema(iAsmDef)
        flagIndexHasKey.name = 'index-has-key'
        flagIndexHasKey._initContents(10)
        flagIndexHasKey['flags'] = [ cstrtId, cstrtSvty, indexName ]
        flagIndexHasKey['model'] = [
            formalName,
            description,
            props,
            keyCstrtFld, #assembly key-constraint-field
            remarks
        ]
        flagMatches = Assembly()
        flagMatches._setschema(iAsmDef)
        flagMatches.name = 'matches'
        flagMatches._initContents(10)
        flagMatches['flags'] = [ cstrtId, cstrtSvty, cstrtMatchesRegex, asTypeSimple ]
        flagMatches['model'] = [
            formalName,
            description,
            props,
            remarks
        ]

        tgAllowVals = Assembly()
        tgAllowVals._setschema(iAsmDef)
        tgAllowVals.name = 'allowed-values'
        tgAllowVals._initContents(10)
        tgAllowVals['flags'] = [ cstrtId, cstrtSvty, cstrtAllowOther, cstrtEx, cstrtTg ]
        tgAllowVals['model'] = [
            formalName,
            description,
            props,
            cstrtValueEnum, #field constraint-value-enum
            remarks
        ]
        tgAllowVals['model'][3]._setschema(iFieldDef)
        tgAllowVals['model'][3].name = 'enum'
        tgAllowVals['model'][3]._flags['min-occurs'] = '1'
        tgAllowVals['model'][3]._flags['max-occurs'] = 'unbounded'
        tgAllowVals['model'][3]._initContents(10)
        tgAllowVals['model'][3][5] = Assembly()
        tgAllowVals['model'][3][5]._setschema(groupAs)
        tgAllowVals['model'][3][5].name = 'enums'
        tgAllowVals['model'][3][5]._flags['in-json'] = 'ARRAY'
        tgExpect = Assembly()
        tgExpect._setschema(iAsmDef)
        tgExpect.name = 'expect'
        tgExpect._initContents(10)
        tgExpect['flags'] = [ cstrtId, cstrtSvty, cstrtTg, cstrtTg ] #first cstrtTg has use-name test. can't show this with the same inline def...
        tgExpect['model'] = [
            formalName,
            description,
            props,
            expectCstrtMsg, #field expect-constraint-message
            remarks
        ]
        tgIndexHasKey = Assembly()
        tgIndexHasKey._setschema(iAsmDef)
        tgIndexHasKey.name = 'index-has-key'
        tgIndexHasKey._initContents(10)
        tgIndexHasKey['flags'] = [ cstrtId, cstrtSvty, indexName, cstrtTg ]
        tgIndexHasKey['model'] = [
            formalName,
            description,
            props,
            keyCstrtFld, #assembly key-constraint-field
            remarks
        ]
        tgMatches = Assembly()
        tgMatches._setschema(iAsmDef)
        tgMatches.name = 'matches'
        tgMatches._initContents(10)
        tgMatches['flags'] = [ cstrtId, cstrtSvty, cstrtMatchesRegex, asTypeSimple, cstrtTg ]
        tgMatches['model'] = [
            formalName,
            description,
            props,
            remarks
        ]
        tgIsUnique = Assembly()
        tgIsUnique._setschema(iAsmDef)
        tgIsUnique.name = 'is-unique' #targeted-is-unique-constraint
        tgIsUnique._initContents(10)
        tgIsUnique['flags'] = [cstrtId, cstrtSvty, cstrtTg]
        tgIsUnique['model'] = [
            formalName,
            description,
            props,
            keyCstrtFld,
            remarks
        ]
        tgIndex = Assembly()
        tgIndex._setschema(iAsmDef)
        tgIndex.name = 'index' #targeted-index-constraint
        tgIndex._initContents(10)
        tgIndex['flags'] = [cstrtId, cstrtSvty, indexName, cstrtTg]
        tgIndex['model'] = [
            formalName,
            description,
            props,
            keyCstrtFld,
            remarks
        ]
        tgHasCardinality = Assembly()
        tgHasCardinality._setschema(iAsmDef)
        tgHasCardinality.name = 'has-cardinality' #targeted-has-cardinality-constraint
        tgHasCardinality._initContents(10)
        tgHasCardinality['flags'] = [cstrtId, cstrtSvty, cardinalityMinOccurs, cardinalityMaxOccurs, cstrtTg]
        tgHasCardinality['model'] = [
            formalName,
            description,
            props,
            remarks
        ]

        asmConstraints = Assembly()
        asmConstraints._setschema(iAsmDef)
        asmConstraints.name = 'constraint' #assembly-constraints
        asmConstraints._initContents(10)
        asmConstraints['flags'] = []
        asmConstraints['model'] = [
            constraintLetExpr, #assembly constraint-let-expression
            Assembly()  #choice-group rules
        ]
        asmConstraints['model'][1]._setschema(choice)
        asmConstraints['model'][1]._flags['min-occurs'] = '1'
        asmConstraints['model'][1]._flags['max-occurs'] = 'unbounded'
        asmConstraints['model'][1]._initContents(5)
        asmConstraints['model'][1][1] = Assembly()
        asmConstraints['model'][1][1]._setschema(groupAs)
        asmConstraints['model'][1][1].name = 'rules'
        asmConstraints['model'][1][1]._flags['in-json'] = 'ARRAY'
        asmConstraints['model'][1][2] = Field('object-type')
        asmConstraints['model'][1][3] = [
            tgAllowVals, #assembly targeted-allowed-values constraint
            tgExpect, #assembly targeted-expect-constraint
            tgIndexHasKey, #assembly targeted-index-has-key-constraint
            tgMatches, #assembly targeted-matches-constraint
            tgIsUnique, #assembly targeted-is-unique-constraint
            tgIndex, #assembly targeted-index-constraint
            tgHasCardinality  #assembly targeted-has-cardinality-constraint
        ]

        fieldConstraints = Assembly()
        fieldConstraints._setschema(iAsmDef)
        fieldConstraints.name = 'constraint' #field-constraints
        fieldConstraints._initContents(10)
        fieldConstraints['flags'] = []
        fieldConstraints['model'] = [
            constraintLetExpr, #assembly constraint-let-expression
            Assembly()  #choice-group rules
        ]
        fieldConstraints['model'][1]._setschema(choice)
        fieldConstraints['model'][1]._flags['min-occurs'] = '1'
        fieldConstraints['model'][1]._flags['max-occurs'] = 'unbounded'
        fieldConstraints['model'][1]._initContents(5)
        fieldConstraints['model'][1][1] = Assembly()
        fieldConstraints['model'][1][1]._setschema(groupAs)
        fieldConstraints['model'][1][1].name = 'rules'
        fieldConstraints['model'][1][1]._flags['in-json'] = 'ARRAY'
        fieldConstraints['model'][1][2] = Field('object-type')
        fieldConstraints['model'][1][3] = [
            tgAllowVals, #assembly targeted-allowed-values constraint
            tgExpect, #assembly targeted-expect-constraint
            tgIndexHasKey, #assembly targeted-index-has-key-constraint
            tgMatches  #assembly targeted-matches-constraint
        ]
        flagConstraints = Assembly()
        flagConstraints._setschema(iAsmDef)
        flagConstraints.name = 'constraint' #flag-constraints
        flagConstraints._initContents(10)
        flagConstraints['flags'] = []
        flagConstraints['model'] = [
            constraintLetExpr, #assembly constraint-let-expression
            Assembly()  #choice-group rules
        ]
        flagConstraints['model'][1]._setschema(choice)
        flagConstraints['model'][1]._flags['min-occurs'] = '1'
        flagConstraints['model'][1]._flags['max-occurs'] = 'unbounded'
        flagConstraints['model'][1]._initContents(5)
        flagConstraints['model'][1][1] = Assembly()
        flagConstraints['model'][1][1]._setschema(groupAs)
        flagConstraints['model'][1][1].name = 'rules'
        flagConstraints['model'][1][1]._flags['in-json'] = 'ARRAY'
        flagConstraints['model'][1][2] = Field('object-type')
        flagConstraints['model'][1][3] = [
            flagAllowVals, #assembly flag-allowed-values
            flagExpect, #assembly flag-expect
            flagIndexHasKey, #assembly flag-index-has-key
            flagMatches  #assembly flag-matches
        ]

        fieldInXmlFlag = Assembly()
        fieldInXmlFlag._setschema(iFlagDef)
        fieldInXmlFlag.name = 'in-xml'
        fieldInXmlFlag._flags['as-type'] = 'token'
        fieldInXmlFlag.default = 'WRAPPED'

        flags = Assembly()
        flags._setschema(choice)
        flags._flags['min-occurs'] = '0'
        flags._flags['max-occurs'] = 'unbounded'
        flags._initContents(5)
        flags[1] = Assembly()
        flags[1]._setschema(groupAs)
        flags[1].name = 'flags'
        flags[1]._flags['in-json'] = 'ARRAY'
        flags[3] = [
            flagRef,
            iFlagDef
        ]

        model = Assembly()
        model._setschema(choice)
        model._flags['min-occurs'] = '0'
        model._flags['max-occurs'] = 'unbounded'
        model._initContents(5)
        model[1] = Assembly()
        model[1]._setschema(groupAs)
        model[1].name = 'model'
        model[1]._flags['in-json'] = 'ARRAY'
        model[1]._flags['in-xml'] = 'GROUPED'
        model[3] = [
            asmRef,
            iAsmDef,
            fieldRef,
            iFieldDef,
            choice,
            singleChoice
        ]

        gAsmDef.name = 'define-assembly'
        gAsmDef._contents.append(None) #formal-name
        gAsmDef._contents.append(None) #description
        gAsmDef._contents.append([]) #props
        gAsmDef._contents.append(None) #choice?
        gAsmDef._contents.append(None) #json-key
        gAsmDef._contents.append([ definitionName ]) #leaving 3 other flags out for now
        gAsmDef._contents.append([ #model
            formalName, #field formal-name
            description, #field description
            props, #assembly property*
            Assembly(), #choice (use-name/root-name)
            jsonKey, #assembly json-key
            flags, #choice (flags)
            model, #choice (assembly-model)
            asmConstraints, #assembly assembly-constraints
            remarks, #field remarks
            example  #assembly examples
        ])
        gAsmDef[6][3]._setschema(singleChoice)
        gAsmDef[6][3]._initContents(1)
        gAsmDef[6][3][0] = [
            usename,
            Assembly() #define-field root-name
        ]
        gAsmDef[6][3][0][1]._setschema(iFieldDef)
        gAsmDef[6][3][0][1].name = 'root-name'
        gAsmDef[6][3][0][1]._flags['as-type'] = 'token'
        gAsmDef[6][3][0][1]._flags['min-occurs'] = '1'
        gAsmDef[6][3][0][1]._initContents(10)
        gAsmDef[6][3][0][1]['flags'] = [] #actually there is one flag referrenced, alt-name-index

        iAsmDef.name = 'inline-define-assembly'
        object.__setattr__(iAsmDef, '_contents', [None, None, None, None, None, None, None])
        iAsmDef[0] = Field("Inline Assembly Definition") #formal-name
        iAsmDef[3] = Field('define-assembly')
        iAsmDef[5] = [ definitionName, cardinalityMinOccurs, cardinalityMaxOccurs ] #leaving out 3 other keys
        iAsmDef[6] = [
            formalName, #field formal-name
            description, #field description
            props, #assembly property*
            jsonKey, #assembly json-key
            groupAs, #assembly group-as
            flags, #choice-group flags
            model, #choice (assembly-model)
            asmConstraints, #assembly assembly-constraints
            remarks, #field remarks
            example #assembly example
        ]

        gFieldDef.name = 'define-field'
        object.__setattr__(gFieldDef,'_contents',[None, None, None, None, None, None, None])
        gFieldDef[5] = [ definitionName, defaultValue ] #leaving out others i'm sure
        gFieldDef[6] = [
            formalName, #field formal-name
            description, #field description
            props, #assembly property*
            usename, #field use-name
            jsonKey, #assembly json-key
            jsonvaluekeyflagchoice, #choice (json-value-key or json-value-key-flag)
            flags, #choice-group flags
            fieldConstraints, #assembly field-constraints
            remarks, #field remarks
            example #assembly example
        ]

        iFieldDef.name = 'inline-define-field'
        object.__setattr__(iFieldDef,'_contents',[None, None, None, None, None, None, None])
        iFieldDef[3] = Field('define-field')
        iFieldDef[5] = [ definitionName, defaultValue, cardinalityMinOccurs, cardinalityMaxOccurs, fieldInXmlFlag ]
        iFieldDef[6] = [
            formalName, #field formal-name
            description, #field description
            props, #assembly property*
            jsonKey, #json-key
            jsonvaluekeyflagchoice, #choice (json-value-key or json-value-key-flag)
            groupAs, #assembly group-as
            flags, #choice-group (flags)
            fieldConstraints, #assembly field-constraints
            remarks, #field remarks
            example  #assembly examples
        ]

        gFlagDef.name = 'define-flag'
        gFlagDef._initContents(9)
        gFlagDef[5] = [ definitionName, Assembly(), defaultValue ]
        gFlagDef[5][1]._setschema(flagRef)
        gFlagDef[5][1].ref = 'as-type-simple'
        gFlagDef[5][1].default = 'string'
        gFlagDef[5][1]._initContents(6)
        gFlagDef[6] = [
            formalName, #field formal-name
            description, #field description
            props, #assembly property*
            usename, #field use-name
            flagConstraints, #assembly flag-constraints
            remarks, #field remarks
            example  #assembly examples
        ]
        iFlagDef.name = 'inline-define-flag'
        iFlagDef._initContents(10)
        iFlagDef[3] = Field('define-flag')
        iFlagDef[5] = [ definitionName, Assembly(), defaultValue ]
        iFlagDef[5][1]._setschema(flagRef)
        iFlagDef[5][1].ref = 'as-type-simple'
        iFlagDef[5][1].default = 'string'
        iFlagDef[5][1]._initContents(6)
        iFlagDef[6] = [
            formalName, #field formal-name
            description, #field description
            props, #assembly property*
            flagConstraints, #assembly flag-constraints
            remarks, #field remarks
            example  #assembly examples
        ]

        asmRef.name = 'assembly-reference'
        asmRef._initContents(10)
        asmRef[3] = Field('assembly')
        asmRef[5] = [ definitionReference, cardinalityMinOccurs, cardinalityMaxOccurs ]
        asmRef[6] = [
            formalName, #field formal-name
            description, #field description
            props, #assembly property*
            usename, #field use-name
            groupAs, #assembly group-as
            remarks  #field remarks
        ]
        fieldRef.name = 'field-reference'
        fieldRef._initContents(10)
        fieldRef[3] = Field('field')
        fieldRef[5] = [ definitionReference, cardinalityMinOccurs, cardinalityMaxOccurs, fieldInXmlFlag ]
        fieldRef[6] = [
            formalName, #field formal-name
            description, #field description
            props, #assembly property
            usename, #field use-name
            groupAs, #assembly group-as
            remarks  #field remarks
        ]
        flagRef.name = 'flag-reference'
        flagRef._initContents(10)
        flagRef[3] = Field('flag')
        flagRef[5] = [ definitionReference, cardinalityMinOccurs, cardinalityMaxOccurs ]
        flagRef[6] = [
            formalName, #field formal-name
            description, #field description
            props, #assembly property
            usename, #field use-name
            groupAs, #assembly group-as
            remarks  #field remarks
        ]

        discriminator = Assembly()
        discriminator._setschema(iFieldDef)
        discriminator.name = 'discriminator'
        discriminator._flags['as-type'] = 'token'
        discriminator.default = 'object-type'

        choice.name = 'choice-group'
        choice._initContents(10)
        choice['flags'] = [cardinalityMinOccurs, cardinalityMaxOccurs]
        choice['model'] = [
            jsonKey, #assembly json-key
            groupAs, #assembly group-as
            discriminator, #define-field discriminator
            Assembly(), #choice-group
            remarks #field remarks
        ]
        choice['model'][3]._setschema(choice)
        choice['model'][3]._flags['min-occurs'] = '1'
        choice['model'][3]._flags['max-occurs'] = 'unbounded'
        choice['model'][3]._initContents(5)
        choice['model'][3][1] = Assembly()
        choice['model'][3][1]._setschema(groupAs)
        choice['model'][3][1].name = 'choices'
        choice['model'][3][1]._flags['in-json'] = 'ARRAY'
        choice['model'][3][2] = Field('object-type')
        choice['model'][3][3] = [
            asmRef, #define-assembly assembly-reference
            iAsmDef, #define-assembly define-assembly
            fieldRef, #define-assembly field-reference
            iFieldDef  #define-assembly define-field
        ]

        singleChoice._initContents(10)
        singleChoice.name = 'choice'
        singleChoice['flags'] = []
        singleChoice['model'] = [
            Assembly() #choice-group
        ]
        singleChoice['model'][0]._setschema(choice)
        singleChoice['model'][0]._flags['min-occurs'] = '1'
        singleChoice['model'][0]._flags['max-occurs'] = 'unbounded'
        singleChoice['model'][0]._initContents(5)
        singleChoice['model'][0][1] = Assembly()
        singleChoice['model'][0][1]._setschema(groupAs)
        singleChoice['model'][0][1].name = 'choices'
        singleChoice['model'][0][1]._flags['in-json'] = 'ARRAY'
        singleChoice['model'][0][2] = Field('object-type')
        singleChoice['model'][0][3] = [
            asmRef, #assembly assembly-reference
            iAsmDef, #assembly inline-define-assembly
            fieldRef, #assembly field-reference
            iFieldDef  #assembly inline-define-field
            #so, these lack discriminator values, which will be important when binding to json
        ]

        metaschema.name = 'METASCHEMA'
        object.__setattr__(metaschema, '_contents', [None, None, None, None, None, None, None])
        metaschema[0] = None #Field('Metaschema Module')
        metaschema[1] = None #Field("A declaration of the Metaschema Module")
        metaschema[2] = []
        metaschema[3] = None #Field('METASCHEMA')
        metaschema[4] = None #json-key
        metaschema[5] = [ Assembly() ]
        metaschema[5][0]._setschema(iFlagDef)
        metaschema[5][0].name = "abstract"
        metaschema[5][0]._flags['as-type'] = "token"
        metaschema[5][0].default = "no"
        #metaschema[5][0]['formal-name'] = Field("Is Abstract?")
        metaschema[6] = [
            Assembly(), #define-field schema-name
            Assembly(), #define-field schema-version
            Assembly(), #define-field short-name
            Assembly(), #define-field namespace
            Assembly(), #define-field json-base-uri
            remarks, #field remarks
            Assembly(), #define-assembly import
            Assembly(), #choice-group definitions
        ]
        metaschema[6][0]._setschema(iFieldDef)
        metaschema[6][0].name = 'schema-name'
        metaschema[6][0]._initContents(10)
        metaschema[6][0]['flags'] = [] #flags
        metaschema[6][1]._setschema(iFieldDef)
        metaschema[6][1].name = 'schema-version'
        metaschema[6][1]._initContents(10)
        metaschema[6][1]['flags'] = [] #flags
        metaschema[6][2]._setschema(iFieldDef)
        metaschema[6][2].name = 'short-name'
        metaschema[6][2]._initContents(10)
        metaschema[6][2]['flags'] = [] #flags
        metaschema[6][3]._setschema(iFieldDef)
        metaschema[6][3].name = 'namespace'
        metaschema[6][3]._initContents(10)
        metaschema[6][3]['flags'] = [] #flags
        metaschema[6][4]._setschema(iFieldDef)
        metaschema[6][4].name = 'json-base-uri'
        metaschema[6][4]._initContents(10)
        metaschema[6][4]['flags'] = [] #flags
        #metaschema[6][5] = remarks
        metaschema[6][6]._setschema(iAsmDef)
        metaschema[6][6].name = 'import'
        metaschema[6][6]._flags['max-occurs'] = 'unbounded'
        metaschema[6][6]._initContents(10)
        metaschema[6][6]['group-as'] = Assembly()
        metaschema[6][6]['group-as']._setschema(groupAs)
        metaschema[6][6]['group-as'].name = 'imports'
        metaschema[6][6]['group-as']._flags['in-json'] = 'ARRAY'
        metaschema[6][6]['flags'] = [ Assembly() ] #define-flag href
        metaschema[6][6]['flags'][0]._setschema(iFlagDef)
        metaschema[6][6]['flags'][0].name = 'href'
        metaschema[6][6]['flags'][0].required = 'yes'
        metaschema[6][6]['model'] = [] #model
        metaschema[6][7]._setschema(choice)
        metaschema[6][7]._flags['max-occurs'] = 'unbounded'
        metaschema[6][7]._initContents(5)
        metaschema[6][7][1] = Assembly()
        metaschema[6][7][1]._setschema(groupAs)
        metaschema[6][7][1].name = 'definitions'
        metaschema[6][7][1]._flags['in-json'] = 'ARRAY'
        metaschema[6][7][2] = Field('object-type')
        metaschema[6][7][3] = [
            gAsmDef,
            gFieldDef,
            gFlagDef
        ]

        self.metaschema._initContents(8)
        self.metaschema[0] = Field("Metaschema Model") #schema-name
        self.metaschema[1] = Field("1.0.0-M2") #schema-version
        self.metaschema[2] = Field("metaschema-model") #short-name
        self.metaschema[3] = Field("[namespace]") #namespace
        self.metaschema[4] = Field("[json-base-uri]") #json-base-uri
        self.metaschema[5] = None #remarks
        self.metaschema[6] = [] #imports


        self.metaschema[7] = [ #definitions
            metaschema,
            iAsmDef,
            iFieldDef,
            iFlagDef,
            asmRef,
            fieldRef,
            flagRef,
            singleChoice,
            asTypeSimple
        ]

        def bindToContext(node):
            if node is not None:
                if isinstance(node, list):
                    for thing in node:
                        bindToContext(thing)
                elif node._context is None:
                    object.__setattr__(node, '_context', self)
                    if isinstance(node, ModelObject):
                        #for flag in node._flags:
                        #    bindToContext(flag)
                        if isinstance(node, Assembly):
                            for thing in node._contents:
                                bindToContext(thing)

        bindToContext(self.metaschema)
    def get(self, name):
        match name:
            case 'METASCHEMA':
                return self.metaschema[7][0]
            case 'define-assembly':
                return self.metaschema[7][1]
            case 'define-field':
                return self.metaschema[7][2]
            case 'define-flag':
                return self.metaschema[7][3]
            case 'assembly-reference':
                return self.metaschema[7][4]
            case 'field-reference':
                return self.metaschema[7][5]
            case 'flag-reference':
                return self.metaschema[7][6]
            case 'choice':
                return self.metaschema[7][7]
            case 'as-type-simple':
                return self.metaschema[7][8]
        
        #TODO: throw error
        raise Exception("can't find specified type "+name)
    def parent(self, name):
        return self