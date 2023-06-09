import math
from funcs import *
from error import *
from env import *
from sys import argv, stdout
import re

            


literal = (int, dict)
isof = isinstance

class Pair():
    def __init__(self, car, cdr = None):
        self.car = car
        self.cdr = cdr
    
    def __repr__(self):
        return f"{self.car} | {self.cdr}"

class Symbol():
    def __init__(self, value):
        self.value = value;
        
    def __repr__(self):
        return f"<{self.value}>";

    def __eq__(self, other):
        return self.__repr__() == other.__repr__()

    def __hash__(self):
        return hash(self.__repr__())
       
    def __str__(self):
        return self.value
    

class label(Exception): pass
    

class Proc:

    def __init__(self, parms, body, env, isMacro = False):
        self.parms = parms
        self.body = body
        self.env = env
        self.isMacro = isMacro
        self.argCount = len(parms)

    def apply(self, *args):
        return self.body, Environment(self.parms, args, self.env)

   
class Environment(dict):

    def __init__(self, keys = (), values = (), parent = None):
        self.update(zip(keys, values));
        self.parent = parent;
        
    def find (self, key):
            if key in self:
                return self
            else:
                if self.parent != None:
                    return self.parent.find(key)
                else:
                    raise NameError

    def __repr__(self):
        s = ""
        for key in self.keys():
            s = s+f"[{key}: {self[key]}]\n"
        return s[:-1]
                    
                        
       
def sour(expr:list) -> list : # Will take a lisp program, and convert all the syntactical sugar to valid code, kinda like macros
    if isof(expr, list) == False: return expr
    
    i = 0
    while i < len(expr):
        if isof(expr[i], list):
            expr[i] = sour(expr[i])
        elif isof(expr[i], Symbol):
            if expr[i].value == 'define' and isof(expr[i+1], list): #Shorthand for lambda
                newBody = [Symbol('lambda'), expr[i+1][1:], expr[i+2]]
                expr[i+2] = newBody
                expr[i+1] = expr[i+1][0]
            elif expr[i].value == "`":
                newArg = [Symbol('quote'), expr[i+1]]
                expr[i] = newArg
                expr.pop(i+1)
        
        i += 1
                
                
    
    return expr
    
                    
def output(expr): #convert python to lisp code

    string = ''

    if isof(expr, list) == False: #expr not a list
 
        string = ''
        if expr == True and isof(expr, bool):
            string += '#t'
        elif expr == False and isof(expr, bool):
            string += '#f'
        else:
            string += str(expr)
        return string
    else: #expr is a list
        string+= '('
        while len(expr) != 0:
            if isof(expr[0], list):
                
                string += str(output(expr[0]))
                
            else:
                string += ' '
                if expr[0] == True and isof(expr[0], bool):
                    string += '#t'
                elif expr[0] == False and isof(expr[0], bool):
                    string += '#f'
                else:
                    string += str(output(expr[0]))
            expr.pop(0)
        string+= ')'
            
    return string  
    
def lib(name):
    global globalEnv
    lib = __import__(name)
    globalEnv.update(lib.lib_env)
                 
def gen_globalEnv() -> Environment:
    env = Environment()
    env.update({
        Symbol('+'):        add,
        Symbol('-'):        sub,
        Symbol('*'):        mul,
        Symbol('/'):        div,
        Symbol('car'):      lambda lst : lst[0],
        Symbol('cdr'):      lambda lst : lst[1:],
        Symbol('load'):     lambda p : solve(p),
        Symbol('slurp'):    lambda f : load_prgm(f),
        Symbol('dict'):     lambda x ,y: dict(zip(x,y)),
        Symbol('append-dict!'):
                            add_dict,
        Symbol('display'):  print,
        Symbol('input'):    lambda x: input(x),
        Symbol('throw'):    raise_error,
        Symbol('format'):   output,
        Symbol('load-lib'): lib,
    
        #bool
        Symbol('='):        eq,
        Symbol('<'):        lambda a, b: True if a < b else False,
        Symbol('not'):      lambda b: False if b else True,
        Symbol('and'):      lambda a, b: True if a and b else False,
        Symbol('or'):       lambda a, b: True if a or b else False,
        Symbol('lst?'):     lambda s : isinstance(s, list),
        Symbol('null?'):    lambda s : s == None,
        Symbol('string?'):  lambda x : isinstance(x, str),
        Symbol('dict?'):    lambda x : isinstance(x, dict),
        

        #Strings
        Symbol('combine-strings'):
                            lambda a,b : str(a)+str(b),
        Symbol('substring'):lambda s, a, b: s[a:b],

        

        #dicts
        Symbol('combine-dicts'):
                            lambda a, b: a|b,

        #lists
        Symbol("len"):      len,
        Symbol("list"):     lambda *x: list(x),

        #conversions
        Symbol("string->list"): lambda s: [x for x in s]

            })
    return env

globalEnv = gen_globalEnv();


def strip_coms(text) -> str:
    regex = r';.*\n'    # Matches to all comments, that
                        # are a ';' token, with zero or more of any token, and \
                        # end with a '\n' token.
    text = re.sub(regex, ' ', text )
    return text

def lex(text) -> list:
    text = strip_coms(text)
    regex = r'("[^"]*"|\S+)' #This is a regex that does cool stuff.
    text = text.replace(')', ' ) ').replace('(', ' ( ').replace('\n', ' ').replace('\t', ' ').replace('\\x1b', '\x1b').replace('`', ' ` ')
    tokens = re.findall(regex,text)
    
    
        
    return tokens, None
    
def isFloat(a) -> bool:
    try:
        float(a)
        return True
    except:
        return False

def parse(expr) -> list:  
    tokens = []

    while len(expr) != 0:

        word = expr[0]
        if word == '':
            expr.pop(0)
        elif word == "(":
            expr.pop(0)
            tokens.append(parse(expr))
        elif word == ")":
            expr.pop(0)
            return tokens
        elif word.isnumeric():
            tokens.append(int(word))
            expr.pop(0)
        elif isFloat(word):
            tokens.append(float(word))
            expr.pop(0)
        elif word[0] == '"':
            tokens.append(word[1:-1])
            expr.pop(0)
        elif word == "#t" or word == "#f":
            tokens.append(True if word == "#t" else False)
            expr.pop(0)
        else:
            tokens.append(Symbol(word))
            expr.pop(0)
    return tokens

def crawl(prgm) -> list:
    errors = []
    counter = 0

    if isinstance(prgm, list) and prgm != []:
        op = prgm[0]
        if isof(op, list):
            errors += crawl(op)
        if prgm[0] == Symbol('if'):
            if len(prgm) != 4:
                errors.append(Error("'if' special form requires three arguments!", output(prgm)))
        if op == Symbol('define'):
            if len(prgm) < 3:
                errors.append(Error("'define' special form requires two arguments!", output(prgm)))

        for arg in prgm[1:] :
                errors = errors + crawl(arg)

                
                

    return errors

def eval(expr , env = globalEnv) -> (list, int, float, list, Proc):
    while True:
        try:
            if isinstance(expr, list) == False:

                if isinstance(expr, Symbol):
                    x = env.find(expr)
                    return x[expr]
                else:
                    return expr
            elif expr == []:
                return None
            elif isinstance(expr[0], list):
                return eval(expr[0], env)
            else:      
                op = expr[0]
                args = expr[1:]
                if isinstance(op, (int, str, dict)):
                    return expr
                elif op == Symbol("lambda"):
                    return Proc(expr[1], expr[2], env)
                elif op == Symbol('macro'):
                    return Proc(expr[1], expr[2], env, True)
                elif op == Symbol("define"):
                    #print(f"env: {env} ;\n\nproc: {args}");
                    env[expr[1]] = eval(expr[2], env)
                    return None
                elif op == Symbol("if"):
                
                    if eval(args[0], env) == True:
                        expr = args[1]
                    else: expr = args[2]
                    
                elif op == Symbol("quote"):
                    return args[0]
                elif op == Symbol("begin"):
                    for arg in args[:-1]:
                        eval(arg, env)
                        
                    expr = args[-1]
                elif op == Symbol("let"):
                    bindingClause, letBody = args[0:2]
                    newEnv = Environment(parent = env)
                    for subClause in bindingClause:
                        newEnv[subClause[0]] = subClause[1]
                    return eval(letBody, newEnv)
                elif op == Symbol("set!"):
                    var, value = args[0], args[1]
                    try:
                        env[var]
                        env[var] = value
                    except:
                        return MissingSymbolError(var)
                elif op == Symbol('eval'):
                    return eval(expr[1], env)
                        
                else:        # APPLY
                    procedure = eval(expr[0], env)
                    if isinstance(procedure, Error): #Checks if the procedure lookup returned an error
                        return procedure
                    elif isinstance(procedure, (int, float, dict, str, list)): #ensures it is a procedure/macro
                        return Error("Error: Not Callable", output(expr));
                        
                    elif hasattr(procedure, 'isMacro') and procedure.isMacro == True :   #MACROS                          
                        expr, env = procedure.apply(*expr[1:])
                        expr = eval(expr,env)
                        
                    else:                                                                #PROCEDURES
                        values = []
                        for arg in expr[1:]:
                            value = eval(arg, env)
                            if isinstance(value, Error): #Checks if any of the variable lookup returned an error
                                return value
                            values.append(value)
                        
                        if isof(procedure, Proc):
                            expr, env = procedure.apply(*values)
                            
                        else:
                            return procedure(*values)
                    
        except ArithmeticError:
            return Error("Math Error: Did math wrong!", output(expr))
        except RecursionError:
            return Error("Stack Overflow: Oops!", output(expr))
        except TypeError:
            return Error(
                "Type Error: Illegal procedure on some type! Good Luck :)", output(expr))
        except NameError:
            return Error("Symbol Error: Symbol Unknown!", output(expr) )
        except UserError as e:
            return Error(str(e), expr)
                    
def print_errors():
    global errors

def load_prgm(fileName):
    try:
        file = open(fileName, "r")
    except:
        return Error(f"File {fileName} not found!");
    return file.read()

def solve(text):


    error = None
    
    try:
        if isinstance(text, Error): error = text; raise label
        lexed,error = lex(text)
        
        if error != None: raise label
        #try:
        parsed = parse(lexed)[0] 
        
        crawled  = crawl(parsed)
        
        if crawled != []:
            for error in crawled:print(error) 
            return None
        else:
            
            parsed = sour(parsed)
            result = eval(parsed)
        
        #except:
         #   result = None
        
    except label:
        return error
    return result

def repl(prompt = 'Geoff> '):

    print("\n\x1b[5mGeoff Lisp-like Interpreter!\x1b[0m\n")
    _input = ""
    solve('(load (slurp "stdlib.lisp"))')
    
    
    while True:
        _input = input(prompt)
        if _input == "!QUIT":
            break
        else:
            res = solve(_input)
            print(f"\033[34m{output(res)}\033[0m") if res != None else None
            

lex('(+ 12 34 cat)')

def start():
    if len(argv) == 1:
        repl()
    else:
        file = load_prgm(argv[1])
        solve(file) if isinstance(file, str) else print(file)
        repl()


if __name__ == "__main__":
    start()

