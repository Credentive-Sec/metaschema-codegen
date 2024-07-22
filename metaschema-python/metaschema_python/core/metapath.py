import re

class Lex():
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def __eq__(self, value):
        if isinstance(value, str):
            return self.name == value
        return self.name == value.name
    @staticmethod
    def tokenize(string, lexer):
        string = re.sub('\n+', ' ', string)
        string = re.sub(' +', ' ', string)
        string = re.sub(r'([`\-=[]\\;\',./~!@#$%^&*()_+{}|:"<>?])', ' \1', string)
        toRet = []
        for item in string.split(' '):
            type = lexer.get(item) or 'raw'
            toRet.append(Lex(type, item))
        return toRet
    
    def __repr__(self):
        return f"{self.name}({self.value})"

class Phrase():
    def __init__(self, name: str, subphrases):
        self.name = name
        self.sub = subphrases
    def __len__(self):
        return len(self.sub)
    def __iter__(self):
        return self.sub.__iter__()
    def __eq__(self, value):
        if isinstance(value, str):
            return self.name == value
        return (isinstance(value, Phrase) or isinstance(value, Lex)) and self.name == value.name
    def __repr__(self):
        return f"{self.name} {self.sub}"
    
class Grammar():
    def __init__(self):
        self.rules = []
    def addRule(self, fr, to):
        self.rules.append((fr, to))
    def r(self, fr, to):
        self.addRule(fr, to)
    def __iter__(self):
        return self.rules.__iter__()
    

class OnTheFlyAutomaton():
    """
    Automaton for LR parsing that generates states with each call to shift, as opposed to calculating all possible states ahead of time.
    """
    def __init__(self, rules):
        self.rules = rules
        self.state = []
        self.addToClosure(('TOP', ['S'], 0))
    def rulesEqual(self, a, b):
        if a[0] == b[0] and a[2] == b[2] and len(a[1]) == len(b[1]):
            for i in range(0, len(a[1])):
                if a[1][i] != b[1][i]:
                    return False
            return True
        return False
    def addToClosure(self, rule):
        for rle in self.state:
            if self.rulesEqual(rule, rle):
                return
        self.state.append(rule)
        if len(rule[1]) >rule[2]:
            postdot = rule[1][rule[2]]
            for rle in filter(lambda x: x[0] == postdot, self.rules):
                self.addToClosure((rle[0], rle[1], 0))
    def followEdge(self, symbol):
        if isinstance(symbol, Phrase) or isinstance(symbol, Lex):
            symbol = symbol.name
        oldstate = self.state
        self.state = []
        for rule in oldstate:
            if len(rule[1]) > rule[2]:
                postdot = rule[1][rule[2]]
                if postdot == symbol:
                    self.addToClosure((rule[0], rule[1], rule[2]+1))
    def resetState(self):
        self.state = []
        self.addToClosure(('S', ['S'], 0))
    def setState(self, state):
        self.state = state
    def getState(self):
        return self.state
    def isTermState(self):
        return len(self.state) == 1 and len(self.state[0][1]) == self.state[0][2]
    def possibleShifts(self):
        toRet = []
        for rule in self.state:
            if len(rule[1]) > rule[2]:
                if not rule[1][rule[2]] in toRet:
                    toRet.append(rule[1][rule[2]])
        return toRet
    def possibleReductions(self):
        return filter(lambda rule: rule[2] == len(rule[1]),self.state)
    
class TreeStack():
    def __init__(self):
        self.roots = []
        self.keepTrackOfChildren = True
    def add(self, parent, contents):
        if self.keepTrackOfChildren:
            if parent == None:
                self.roots.append({
                    'parent': None,
                    'children': [],
                    'contents':[item.copy() for item in contents]
                })
                return self.roots[-1]
            else:
                parent['children'].append({
                    'parent':parent,
                    'children':[],
                    'contents':[item.copy() for item in contents]
                })
                return parent['children'][-1]
        else:
            return {'parent': parent, 'contents':[item.copy() for item in contents]}

class Queue():
    def __init__(self):
        self.queue = []
    def push(self, data):
        self.queue.append(data)
    def pop(self):
        return self.queue.pop(0)
    def empty(self):
        return len(self.queue) == 0

class GLR():
    def __init__(self, grammar):
        self.rules = grammar
        self.input = []
        self.workspace = []
        self.stack = TreeStack()
        self.nodesToEval = Queue()
        self.autmtn = OnTheFlyAutomaton(grammar)

        self.finishedInterpretations = []

    def parse(self, input):
        self.input = input.copy()
        currentState = self.compileState()
        stackroot = self.stack.add(None, currentState)
        self.nodesToEval.push(stackroot)
        while not self.nodesToEval.empty():
            self.eval(self.nodesToEval.pop())
        if len(self.finishedInterpretations) == 0:
            raise Exception('no valid interpretations of given string found')
        return self.finishedInterpretations[0]

        
    def eval(self,stackelem):
        state = stackelem['contents']
        #evaluate a specific state & add all valid children state to the queue
        self.loadState(state)

        #check sentinel case: workspace contains 'S' and input is empty
        if len(self.input) == 0 and len(self.workspace) == 1 and self.workspace[0] == 'S':
            self.finishedInterpretations.append(self.workspace[0])
            return

        #check action from automaton
        if len(self.input) > 0:
            symbol = self.input[0]
            if symbol in self.autmtn.possibleShifts():
                #shift state according to symbol
                self.workspace.append(self.input[0])
                self.autmtn.followEdge(self.input.pop(0))
                newstate = self.stack.add(stackelem, self.compileState())
                self.nodesToEval.push(newstate)
            self.loadState(state)
        
        #check for possible reductions
        for rule in self.autmtn.possibleReductions():
            #apply reductions
            self.loadState(state)
            seq = []
            valid = True
            index = len(self.workspace)-len(rule[1])
            automatonRollback = stackelem
            for symbol in rule[1]:
                seq.append(self.workspace.pop(index))
                valid = valid and symbol == seq[-1]
                automatonRollback = automatonRollback['parent']
            #self.input.insert(0, rule[0])
            self.input.insert(0, Phrase(rule[0], seq))

            #roll back automaton len(rule[1]) states
            self.autmtn.setState(automatonRollback['contents'][2])
            if valid:
                newstate = self.stack.add(automatonRollback['parent'], self.compileState())
                self.nodesToEval.push(newstate)
    
    def loadState(self, state):
        self.workspace = state[0].copy()
        self.input = state[1].copy()
        self.autmtn.setState(state[2])

    def compileState(self):
        return ([item for item in self.workspace], [item for item in self.input], self.autmtn.getState())


class Tokenizer():
    def __init__(self):
        self.patterns = []
    def addToken(self, token, pattern):
        self.patterns.append((token, pattern))
    def tokenize(self, string):
        string = re.sub(r'(\w)(\W)', r'\1 \2', string)
        string = re.sub(r'(\W)(\w)', r'\1 \2', string)
        string = re.sub(r'(\W)(\W)', r'\1 \2', string)
        string = re.sub(r'\n+', r' ', string)
        string = re.sub(r' +', r' ', string)
        toRet = []
        for item in string.split(' '):
            toRet.append(self.tokenizeOne(item))
        return toRet
    def tokenizeOne(self, string):
        for pattern in self.patterns:
            if re.fullmatch(pattern[1], string) is not None:
                return Lex(pattern[0],string)
        return Lex(string, string)

class Language():
    def __init__(self, lexicon=None, grammar=None, interpreter=None):
        if lexicon is None:
            self.lexicon = Tokenizer()
        else:
            self.lexicon = lexicon

        if grammar is None:
            self.parser = Grammar()
        else:
            self.parser = GLR(grammar)

        self.interpretNode = interpreter
        self.ready = lexicon is not None and grammar is not None and interpreter is not None
    def interpret(self, string):
        if not self.ready or self.exec is None or isinstance(self.parser, Grammar):
            raise Exception('Language has uninitialized components')
        tokens = self.lexicon.tokenize(string)
        tree = self.parser.parse(tokens)
        return self.exec(tree)
    
    def setFunc(self, func):
        self.interpretNode = func

    def exec(self, node):
        if not self.ready or self.interpretNode is None:
            raise Exception('no walker given')
        if isinstance(node, Lex):
            return self.interpretNode(node.name, [node.value])
        args = []
        for subnode in node.sub:
            args.append(self.exec(subnode))
        return self.interpretNode(node.name, args)
    
    def setExec(self, func):
        self.interpretNode = func
        

    def tokenRule(self, token, pattern):
        if self.ready:
            raise Exception('cannot add rules once finalized')
        self.lexicon.addToken(token, pattern)

    def syntaxRule(self, fr, to):
        if self.ready or isinstance(self.parser, GLR):
            raise Exception('cannot add rules once finalized')
        self.parser.addRule(fr, to)

    def t(self, token, pattern):
        self.tokenRule(token, pattern)

    def kws(self, keywords):
        for kw in keywords:
            self.tokenRule(kw, kw)

    def r(self, fr, to):
        self.syntaxRule(fr, to)

    def ror(self, fr, tos): #expand fr into *any* of to (i.e., the tos are all or'd together)
        for to in tos:
            if isinstance(to, str):
                to = [to]
            self.r(fr, to)


    def finalize(self):
        if self.ready:
            return
        if self.exec is None:
            raise Exception('no interpreter set')
        self.parser = GLR(self.parser)
        self.ready = True

metapath = Language()
metapath.kws(['or', 'and', 'div', 'idiv', 'mod', 'child', 'descendant', 'self', 'parent', 'ancestor'])
metapath.t('IntegerLiteral', r'[0-9]+')
metapath.t('DecimalLiteral', r'[0-9]*\.[0-9]+')
metapath.t('DoubleLiteral', r'[0-9]*\.[0-9]+[eE][+-]?[0-9]+')
metapath.t('StringLiteral', r'"[^"]*"|\'[^\']*\'')
metapath.t('token', r'\w+')

metapath.r('S', ['metapath'])
metapath.r('metapath', ['expr'])

metapath.r('expr', ['expr', ',', 'exprsingle'])
metapath.r('expr', ['exprsingle'])

metapath.r('exprsingle', ['forexpr'])
metapath.r('exprsingle', ['letexpr'])
metapath.r('exprsingle', ['quantifiedexpr'])
metapath.r('exprsingle', ['ifexpr'])
metapath.r('exprsingle', ['orexpr'])

metapath.r('orexpr', ['andexpr'])
metapath.r('orexpr', ['orexpr', 'or', 'andexpr'])

metapath.r('andexpr', ['comparisonexpr'])
metapath.r('andexpr', ['andexpr', 'and', 'comparisonexpr'])

metapath.r('comparisonexpr', ['stringconcatexpr'])

metapath.r('stringconcatexpr', ['rangeexpr'])

metapath.r('rangeexpr', ['additiveexpr'])

metapath.r('additiveexpr', ['multiplicativeexpr'])
metapath.r('additiveexpr', ['additiveexpr', '+', 'multiplicativeexpr'])
metapath.r('additiveexpr', ['additiveexpr', '-', 'multiplicativeexpr'])

metapath.r('multiplicativeexpr', ['unionexpr'])
metapath.r('multiplicativeexpr', ['multiplicativeexpr', '*', 'unionexpr'])
metapath.r('multiplicativeexpr', ['multiplicativeexpr', 'div', 'unionexpr'])
metapath.r('multiplicativeexpr', ['multiplicativeexpr', 'idiv', 'unionexpr'])
metapath.r('multiplicativeexpr', ['multiplicativeexpr', 'mod', 'unionexpr'])

metapath.r('unionexpr', ['intersectexceptexpr'])
metapath.r('intersectexceptexpr', ['arrowexpr'])
metapath.r('arrowexpr', ['unaryexpr'])
metapath.r('unaryexpr', ['valueexpr'])
metapath.r('valueexpr', ['simplemapexpr'])
metapath.r('simplemapexpr', ['pathexpr'])

metapath.r('pathexpr', ['/'])
metapath.r('pathexpr', ['/', 'relativepathexpr'])
metapath.r('pathexpr', ['//', 'relativepathexpr'])
metapath.r('pathexpr', ['relativepathexpr'])

metapath.r('relativepathexpr', ['stepexpr'])
metapath.r('relativepathexpr', ['relativepathexpr', '/', 'stepexpr'])
metapath.r('relativepathexpr', ['relativepathexpr', '//', 'stepexpr'])

metapath.r('stepexpr', ['postfixexpr'])
metapath.r('stepexpr', ['axisstep'])

metapath.r('axisstep', ['reversestep'])
metapath.r('axisstep', ['reversestep', 'predicatelist'])
metapath.r('axisstep', ['forwardstep'])
metapath.r('axisstep', ['forwardstep', 'predicatelist'])

metapath.r('forwardstep', ['abbrevforwardstep'])
metapath.r('forwardstep', ['forwardaxis', 'nametest'])
metapath.r('forwardaxis', ['child', '::'])
metapath.r('forwardaxis', ['descendant', '::'])
metapath.r('forwardaxis', ['self', '::'])
metapath.r('forwardaxis', ['descendantorself', '::'])
metapath.r('abbrevforwardstep', ['nametest'])
metapath.r('abbrevforwardstep', ['@', 'nametest'])
metapath.r('reversestep', ['abbrevreversestep'])
metapath.r('reversestep', ['reverseaxis', 'nametest'])
metapath.r('reverseaxis', ['parent', '::'])
metapath.r('reverseaxis', ['ancestor', '::'])
metapath.r('reverseaxis', ['ancestororself', '::'])
metapath.r('abbrevreversestep', ['..'])

metapath.ror('nametest', ['eqname', '*'])

metapath.r('postfixexpr', ['postfixexpr', 'predicate'])
metapath.r('postfixexpr', ['primaryexpr'])
metapath.r('predicatelist', ['predicatelist', 'predicate'])
metapath.r('predicatelist', ['predicate'])
metapath.r('predicate', ['[', 'expr', ']'])
metapath.ror('primaryexpr', ['literal', 'varref', 'parenthesizedexpr', 'contextitemexpr', 'functioncall'])
metapath.ror('literal', ['numericliteral', 'StringLiteral'])
metapath.ror('numericliteral', ['IntegerLiteral', 'DecimalLiteral', 'DoubleLiteral'])
metapath.r('varref', ['$', 'varname'])
metapath.r('varname', ['eqname'])
metapath.r('parenthesizedexpr', ['(', 'expr', ')'])

metapath.r('eqname', ['token'])

def metapathwalker(node, args):
    def binop(args):
        if len(args) == 1:
            return args[0]
        else:
            match(args[1]):
                case('+'):
                    return args[0] + args[2]
                case('-'):
                    return args[0] - args[2]
                case('*'):
                    return args[0] * args[2]

    match(node):
        case 'IntegerLiteral':
            return int(args[0])
        case 'DecimalLiteral':
            return float(args[0])
        case 'additiveexpr':
            return binop(args)
        case 'multiplicativeexpr':
            return binop(args)
    return args[0]

def metapathtopythonwalker(node, args):
    if len(args) == 1:
        return args[0]
    match(node):
        case 'additiveexpr':
            return f'{args[0]} {args[1]} {args[2]}'
        case 'multiplicativeexpr':
            op = '*'
            if args[1] == 'div':
                op = '/'
            elif args[1] == 'idiv':
                op = '//'
            elif args[1] == 'mod':
                op = '%'
            return f'{args[0]} {op} {args[2]}'
        case 'unaryexpr':
            return f'{args[0]}{args[1]}'
        case 'pathexpr':
            return f'({args[1]})'
        case 'relativepathexpr':
            return f'{args[0]}[{args[2]}]'
        case 'parenthesizedexpr':
            return f'({args[1]})'
    return args[0]

metapath.setExec(metapathtopythonwalker)
metapath.finalize()
