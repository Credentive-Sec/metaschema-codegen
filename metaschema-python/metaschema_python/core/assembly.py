from pathlib import Path
from lxml import etree

#formalNameStr = '{http://csrc.nist.gov/ns/oscal/metaschema/1.0}formal-name'
#descriptionStr = '{http://csrc.nist.gov/ns/oscal/metaschema/1.0}description'
#propStr = '{http://csrc.nist.gov/ns/oscal/metaschema/1.0}prop'
#rootNameStr = '{http://csrc.nist.gov/ns/oscal/metaschema/1.0}root-name'
#useNameStr = '{http://csrc.nist.gov/ns/oscal/metaschema/1.0}use-name'
#jsonKeyStr = '{http://csrc.nist.gov/ns/oscal/metaschema/1.0}json-key'
#remarksStr = '{http://csrc.nist.gov/ns/oscal/metaschema/1.0}remarks'
#exampleStr = '{http://csrc.nist.gov/ns/oscal/metaschema/1.0}example'
#flagStr = '{http://csrc.nist.gov/ns/oscal/metaschema/1.0}flag'
#defineFlagStr = '{http://csrc.nist.gov/ns/oscal/metaschema/1.0}define-flag'
#modelStr = '{http://csrc.nist.gov/ns/oscal/metaschema/1.0}model'
#assemblyStr = '{http://csrc.nist.gov/ns/oscal/metaschema/1.0}assembly'
#fieldStr = '{http://csrc.nist.gov/ns/oscal/metaschema/1.0}field'
#defineAssemblyStr = '{http://csrc.nist.gov/ns/oscal/metaschema/1.0}define-assembly'
#defineFieldStr = '{http://csrc.nist.gov/ns/oscal/metaschema/1.0}define-field'
#choiceStr = '{http://csrc.nist.gov/ns/oscal/metaschema/1.0}choice'
#sconstraintStr = '{http://csrc.nist.gov/ns/oscal/metaschema/1.0}constraint'
msns = '{http://csrc.nist.gov/ns/oscal/metaschema/1.0}'
oscalns = '{http://csrc.nist.gov/ns/oscal/1.0}'

class XMLTag:
    def __init__(self, xml):
        self.type = xml.tag #aka name?
        self.attr = xml.attrib #aka tags?
        self.children = [] #aka fields/assemblies?
        self.text = xml.text #field values?
        for child in list(xml):
            self.children.append(XMLTag(child))

    def addChild(self,child):
        self.children.append(child)

    def __str__(self):
        toRet = "{ "+self.type+":"+self.text
        for child in self.children:
            toRet = toRet+", "+child
        toRet = toRet + "}"
        return toRet
    
    @staticmethod
    def fromPath(path):
        parser = etree.XMLParser(load_dtd=True, resolve_entities=True, remove_comments=True)
        xml_tree = etree.parse(path, parser=parser)
        return XMLTag(xml_tree.getroot())
    
class Namespace:
    def __init__(self, schemapath):
        base_path = Path(Path(schemapath).parent)
        parser = etree.XMLParser(load_dtd=True, resolve_entities=True, remove_comments=True)
        xml_tree = etree.parse(schemapath, parser=parser)
        root = XMLTag(xml_tree.getroot())

        self.types = {}
        self.subspaces = []
        includes = []
        for child in root.children:
            if child.type == msns+'define-assembly':
                self.types[child.attr['name']] = child
            elif child.type == msns+'define-field':
                self.types[child.attr['name']] = child
            elif child.type == msns+'define-flag':
                self.types[child.attr['name']] = child
            elif child.type == msns+'import':
                includes.append(child.attr.get('href'))
        
        #hunt down includes
        for include in includes:
            self.subspaces.append(Namespace(str(Path(base_path, include))))

    def get(self, name):
        if self.types.get(name) is not None:
            return self.types[name]
        for subspace in self.subspaces:
            if subspace.get(name) is not None:
                return subspace.get(name)
        return None
    def parent(self, name):
        if self.types.get(name) is not None:
            return self
        for subspace in self.subspaces:
            if subspace.parent(name) is not None:
                return subspace.parent(name)
        return None

#assemblies have metadata, flags, and (as children, part of the model) fields and assemblies

class MetaschemaGlobalAssembly:
    def __init__(self, schema, node, ns={}):
        self.schema = schema #we know this is an instance of a metaschema assembly
        self.node = node
        self.namespace = ns
        #if not self.validate():
        #    raise Exception("initialization does not match schema")
    def validate(self):
        si = 0 #schema index
        ni = 0 #node index
        if si < len(self.schema.children) and self.schema.children[si].type == msns+"formal-name":
            si = si + 1
        if si < len(self.schema.children) and self.schema.children[si].type == msns+'description':
            si = si + 1
        while si < len(self.schema.children) and self.schema.children[si].type == msns+'prop':
            si = si + 1
        if si < len(self.schema.children) and self.schema.children[si].type == msns+"root-name":
            si = si + 1
        elif si < len(self.schema.children) and self.schema.children[si].type == msns+"use-name":
            si = si + 1
        if si < len(self.schema.children) and self.schema.children[si].type == msns+'json-key':
            si = si + 1
        
        #now we get to flags
        while si < len(self.schema.children) and (self.schema.children[si].type == msns+'flag' or self.schema.children[si].type == msns+'define-flag'):
            if self.schema.children[si].attr.get('required') == "yes":
                flagschema = self.schema.children[si]
                if self.schema.children[si].type == msns+'flag':
                    flagschema = self.namespace.get(self.schema.children[si].attr['ref'])
                elif self.schema.children[si].type == msns+'define-flag':
                    flagschema = self.schema.children[si]
                if self.node.attr.get(flagschema.attr['name']) is None:
                    return False
                #TODO: check type
            si = si + 1
        if si < len(self.schema.children) and self.schema.children[si].type == msns+'model':
            for child in self.schema.children[si].children:
                ni = self.modelValidate(child, ni)
                if ni == -1: #the modelValidate failed
                    return False
            if ni < len(self.node.children):
                return False
            si = si + 1

        if si < len(self.schema.children) and self.schema.children[si].type == msns+'constraint':
            si = si + 1
        
        if si < len(self.schema.children) and self.schema.children[si].type == msns+'remarks':
            si = si + 1
        while si < len(self.schema.children) and self.schema.children[si].type == msns+'example':
            si = si + 1
        if si < len(self.schema.children):
            return False
        return True
    
    def modelValidate(self, schema, ni):
        #are we dealing with a choice, a reference, or an inline definition?
        if schema.type == msns+'choice':
            highestNi = -1
            for child in schema.children:
                thisni = self.modelValidate(child, ni)
                if thisni > highestNi:
                    #simple heuristic for finding the "best" choice
                    highestNi = thisni
            ni = highestNi
            return ni
        elif schema.type == msns+'assembly' or schema.type == msns+'field':
            #reference, get the definition from the namespace
            schemadef = self.namespace.get(schema.attr['ref'])
            if schemadef is None:
                raise Exception("can't find schema definition for "+schema.attr['ref'])
        elif schema.type == msns+'define-assembly' or schema.type == msns+'define-field':
            #inline definition
            schemadef = schema

        lni = ni #local node index

        wrapped = False
        wrappedName = ""
        useName = schemadef.attr['name']
        for child in schemadef.children:
            if child.type == msns+'use-name':
                useName = child.text
        #group-as is defined in the reference or in an inline definition, never in a global definition
        for child in schema.children:
            if child.type == msns+'group-as':
                if child.attr.get('in-xml') == "GROUPED":
                    wrapped = True #rather than look for the node outlined by the schema definition directly, look for the wrapper first
                wrappedName = child.attr.get('name')
            elif child.type == msns+'use-name': #because this can be given here too!
                useName = child.text #i do this one later so it will overrule the defined one

        #need to check through attr to see if this has datatype markup-multiline and if it has in-xml unwrapped



        maxOccurs = schema.attr.get('max-occurs') or 1
        if maxOccurs == "unbounded":
            maxOccurs = 99999999999 #if python has a way to say "a really big number", i don't know it
        else:
            maxOccurs = int(maxOccurs)
        minOccurs = schema.attr.get('min-occurs') or 0
        minOccurs = int(minOccurs)


        childrenArr = self.node.children
        if wrapped:
            if ni < len(self.node.children) and self.node.children[ni].type == oscalns+wrappedName:
                #this node is the wrapper. we'll interpret it                   may want to remove this oscalns here
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
        while lni < len(childrenArr) and count < maxOccurs and childrenArr[lni].type == oscalns+useName:
                                                    #in terms of namespacing, where do we get oscalns from?
            #TODO: check type
            if schema.type == msns+'assembly' \
            and not MetaschemaGlobalAssembly(schemadef, childrenArr[lni], self.namespace.parent(schemadef.attr['name'])).validate():
                #in other words, if it's an invalid assembly of this type
                print(f"{useName} at {lni} is invalid")
                return -1
            lni = lni + 1
            count = count + 1
        if count < minOccurs: #we did not find enough nodes of this kind
            print("not enough "+useName+"s")
            return -1
        if wrapped:
            return ni #if there was a wrapper, we don't want to return lni because our iterations were not over the parent's children array
        return lni




    #def validate(self):
    #    for child in self.schema.children:
    #        if not self.subvalidate(child, self.node, 0):
    #            return False
    #    return True
    #def subvalidate(self, schema, node, index):
    #     if schema.type == 'define-flag':
    #         if schema.attr.get('required') == "yes":
    #             if node.attr.get(schema.attr.get('name')) is not None:
    #                 #TODO: check type
    #                 return True
    #             return False
    #         return True
    #     elif schema.type == 'flag':
    #         #Flags are not children but instead are attributes
    #         if schema.attr.get('required') == "yes":
    #             if node.attr.get(schema.attr.get('name')) is not None:
    #                 #TODO: check type
    #                 return True
    #             return False
    #         return True
    #     elif schema.type == 'model':
    #         for child in schema.children:
    #             if not self.subvalidate(child, node, index):
    #                 #TODO: check type
    #                 return False
    #         return True
    #     elif schema.type == 'assembly':
    #         if not node.children[index].validate():
    #             return False
    #         index = index + 1
    #         return True
    #     elif schema.type == 'field':
    #         if not node.children[index].validate():
    #             return False
    #         index = index + 1
    #         return True
    #     elif schema.type == 'define-assembly':
    #         #TODO
    #         return True
    #     elif schema.type == 'define-field':
    #         #TODO
    #         return True
    #     elif schema.type == 'choice':
    #         for presentChild in schema.children:
    #             if self.subvalidate(presentChild, node, index):
    #                 notPresent = True
    #                 for otherChild in schema.children:
    #                     if not self.subinvalidate(otherChild, node, index):
    #                         notPresent = False
    #                 if notPresent:
    #                     return True
    #         return False
    #     elif schema.type == 'constraints':
    #         #TODO
    #         return True
    #     return True
    
    # #prove that a schema is *invalid* if possible. helps with choices where either one or the other must be picked
    # def subinvalidate(self, schema, node, index):
    #     if schema.type == 'define-flag':
    #         if node.attr.get(schema.attr.get('name')) is None:
    #             return False
    #         return True
    #     elif schema.type == 'flag':
    #         if node.attr.get(schema.attr.get('name')) is None:
    #             return False
    #         return True
    #     elif schema.type == 'model':
    #         for child in schema.children:
    #             if self.subinvalidate(child, node, index):
    #                 return True
    #         return False