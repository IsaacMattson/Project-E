import math
from funcs import *
from error import *
import re
            


literal = (int, dict)
isof = isinstance

class Symbol():
    def __init__(self, value):
        self.value = value;
        
    def __repr__(self):
        return f"<{self.value}>";

    def __eq__(self, other):
        return self.__repr__() == other.__repr__()

    def __hash__(self):
        return hash(str(self))
    

class label(Exception): pass
    

class Procedure:

    def __init__(self, parms, body, env, isSpecial = False):
        self.parms = parms
        self.body = body
        self.env = env
        self.isSpecial = isSpecial
        self.argCount = len(parms)

    def __call__(self, *args):
        return eval(self.body, Environment(self.parms, args, self.env))

    
    
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
                   return Error(f"Symbol '{key}' not found!"); 
    def __repr__(self):
        s = ""
        for key in self.keys():
            s = s+f"[{key}: {self[key]}]\n"
        return s[:-1]
                    
def native_env() -> Environment:
    env = Environment()
    env.update({
        Symbol('+'):        add,
        Symbol('-'):        sub,
        Symbol('*'):        mul,
        Symbol('/'):        div,
        Symbol('eq?'):      eq,
        Symbol('car'):      lambda lst : lst[0],
        Symbol('cdr'):      lambda lst : lst[1:],
        Symbol('load'):     lambda p : solve(p),
        Symbol('slurp'):    lambda f : load_prgm(f),
        Symbol('dict'):     lambda x ,y: dict(zip(x,y)),
        Symbol('append-dict!'): add_dict,
        Symbol('display'):  print

    })
    return env

global_env = native_env();


    

def lex(text) -> str:
   
    regex = r'("[^"]*"|\S+)' #This is the regex to create tokens could be changed to accomdate new grammers
    text = text.replace(')', ' ) ').replace('(', ' ( ')
    tokens = re.findall(regex,text)
    
    
        
    return tokens, None

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

def crawl(prgm):
    errors = []

    if isinstance(prgm, list):
        op = prgm[0]
        if prgm[0] == 'if':
            if len(prgm) != 4:
                errors.append(Error("'if' special form requires three arguments!"))
        if op == 'define':
            if len(prgm) != 3:
                errors.append(Error("'define' special form requires two arguments!"))

        for arg in prgm[1:] :
            errors.append(crawl(arg))

    return errors

def eval(expr , env = global_env):
    if isinstance(expr, list) == False:

        if isinstance(expr, Symbol):
            x = env.find(expr)
            if isinstance(x, Environment):           
                return x[expr]
            else:
                return x

        else:
            return expr
    else:
        
        op = expr[0]
        args = expr[1:]
        if isinstance(op, (int, str, dict)):
            return expr
        elif op == Symbol("lambda"):
            return Procedure(expr[1], expr[2], env)
        elif op == Symbol("define"):
            env[args[0]] = eval(args[1], env)
        elif op == Symbol("if"):
            if eval(args[0], env) == False:
                return eval(args[1], env)
            else: return eval(args[2], env)
        elif op == Symbol("quote"):
            return args[0]
        elif op == Symbol("begin"):
            for arg in args[:-1]:
                eval(arg, env)
            return eval(args[-1], env)
        elif op == Symbol("let"):
            bindingClause, letBody = args[0:2]
            newEnv = Environment(parent = env)
            for subClause in bindingClause:
                newEnv[subClause[0]] = subClause[1]
            return eval(letBody, newEnv)
            
        else:        
            procedure = eval(expr[0], env)
            if isinstance(procedure, Error): #Checks if the procedure lookup returned an error
                return procedure
            elif isinstance(procedure, (int, float, dict, str)):
                return Error("Error: Not Callable");
            else:
                values = []
                for arg in expr[1:]:
                    value = eval(arg, env)
                    if isinstance(value, Error): #Checks if any of the variable lookup returned an error
                        return value
                    values.append(value)
                print(f"env: {env} ;\n\nproc: {procedure} ;\n\nargs {values}");
                return procedure(*values)

                    
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
        print(lexed)
        if error != None: raise label
        parsed = parse(lexed)[0]

        #print(crawl(parsed))
    
        result = eval(parsed)
    except label:
        return error
    return result


def repl():

    _input = ""
    solve('(load (slurp "stdlib.lisp"))')
    while True:
        _input = input("Geoff>")
        if _input == "!QUIT":
            break
        else:
            print(solve(_input))
            

lex('(+ 12 34 cat)')
repl();
