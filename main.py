import math
from funcs import *
from error import *

Symbol = str              
Number = (int, float)     
Atom   = (Symbol, Number)
List   = list             
Exp    = (Atom, List)        

class symbol():
    def __init__(self, value):
        self.value = value;

class label(Exception): pass
    

class Procedure:

    def __init__(self, parms, body, env):
        self.parms = parms
        self.body = body
        self.env = env

    def __call__(self, *args):
        return eval(self.body, Environment(self.parms, args, self.env))
        


class Environment(dict):

    def __init__(self, keys = (), values = (), parent = None):
        self.update(zip(keys, values));
        self.parent = parent;
        
    def find (self, key):       
            return self if (key in self) else self.parent.find(key)


def native_env() -> Environment:
    env = Environment()
    env.update({
        '+':        add,
        '-':        sub,
        '*':        mul,
        '/':        div,
        'eq?':      eq,
        'car':      lambda lst : lst[0],
        'cdr':      lambda lst : lst[1:],
        'load':     lambda t : solve(load_prgm(t))
    
        
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
            tokens.append(word)
            expr.pop(0)
    return tokens

def crawl(prgm):
    pass

def eval(expr , env = global_env):
    if isinstance(expr, list) == False:
        if isinstance(expr, str):
            return env.find(expr)[expr]
        else:
            return expr
    else:
        
        op = expr[0]
        args = expr[1:]
        if isinstance(op, int):
            return expr
        elif op == "lambda":
            return Procedure(expr[1], expr[2], env)
        elif op == "define":
            env[args[0]] = eval(args[1], env)
        elif op == "if":
            if eval(args[0], env) == "#t":
                return eval(args[1], env)
            else: return eval(args[2], env)
        elif op == "quote":
                return args[0]
        else:        
            procedure = eval(expr[0], env)
            values = [eval(arg, env) for arg in expr[1:]]
            print(f"### op is '{procedure}', args are '{values}'")
            return procedure(*values)

def load_prgm(fileName):
    try:
        file = open(fileName, "r")
    except:
        return Error(f"File {fileName} not found!");
    return file.read()

def solve(text):

    try:
        error = None
        
        try:
            if isinstance(text, Error): error = text; raise label
            lexed,error = lex(text)
            if error != None: raise label
            parsed = parse(lexed)[0]
            result = eval(parsed)
        except label:
            return error
        return result
    except: 
        return '?.' # The experienced user will know what is wrong. 

def repl():

    _input = ""

##    print(solve(load_prgm("test.ls")))
    while True:
        _input = input("Geoff>")
        if _input == "!QUIT":
            break
        else:
            print(solve(_input))
            



repl();
