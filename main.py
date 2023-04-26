import math
from funcs import *
from error import *

            


literal = (int, dict)

errors = []

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
        Symbol('load'):     lambda t : solve(load_prgm(t)),
        Symbol('dict'):     lambda x ,y: dict(zip(x,y))

    })
    return env

global_env = native_env();

def lex(text) -> str:
    lexed = text.replace("(", " ( ").replace(")", " ) ").split()
    if lexed.count(')') == lexed.count('('):
        return lexed, None;
    else:
        return None, Error("?");

def parse(expr) -> list:  
    tokens = []

    while len(expr) != 0:

        word = expr[0]
        if word == "(":
            expr.pop(0)
            tokens.append(parse(expr))
        elif word == ")":
            expr.pop(0)
            return tokens
        elif word.isnumeric():
            tokens.append(int(word))
            expr.pop(0)
        elif word == "#t" or word == "#f":
            tokens.append(word)
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
        if isinstance(op, int):
            return expr
        elif op == Symbol("lambda"):
            return Procedure(expr[1], expr[2], env)
        elif op == Symbol("define"):
            env[args[0]] = eval(args[1], env)
        elif op == Symbol("if"):
            if eval(args[0], env) == "#t":
                return eval(args[1], env)
            else: return eval(args[2], env)
        elif op == Symbol("quote"):
            return args[0]
        elif op == Symbol("begin"):
            for arg in args[:-2]: eval(arg)
            return eval(args[-1])
        else:        
            procedure = eval(expr[0], env)
            if isinstance(procedure,Error): #Checks if the procedure lookup returned an error
                return procedure
            else:
                values = []
                for arg in expr[1:]:
                    value = eval(arg, env)
                    if isinstance(value, Error): #Checks if any of the variable lookup returned an error
                        return value
                    values.append(value)
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
        if error != None: raise label
        parsed = parse(lexed)[0]

        print(crawl(parsed))
    
        result = eval(parsed)
    except label:
        return error
    return result


def repl():

    _input = ""
    solve("(load (quote stdlib.lisp))")
    while True:
        _input = input("Geoff>")
        if _input == "!QUIT":
            break
        else:
            print(solve(_input))
            



repl();
