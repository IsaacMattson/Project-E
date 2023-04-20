import math

from funcs import *
from error import *

Symbol = str              
Number = (int, float)     
Atom   = (Symbol, Number)
List   = list             
Exp    = (Atom, List)        

class T:
    STRING = "STRING"
    INT = "INT"
    BOOL = "BOOL"
    SYMBOL = "SYMBOL"

class label(Exception): pass
    
class Token:
    def __init__(self,_type,value):
        self.value = value
        self._type = _type;

    def __str__(self):
        return f"<{self._type}:{self.value}>"
    def __repr__(self):
        return f"<{self._type}:{self.value}>"

class Procedure:

    def __init__(self, parms, body, env):
        self.parms = [parm.value for parm in parms]
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

def parse(program) -> list:  
    tokens = []

    while len(program) != 0:

        word = program[0]
        if word == "(":
            program.pop(0)
            tokens.append(parse(program))
        elif word == ")":
            program.pop(0)
            return tokens
        elif word.isnumeric():
            tokens.append(Token("INT", int(word)))
            program.pop(0)
        elif word == "#t" or word == "#f":
            tokens.append(Token("BOOL", word))
            program.pop(0)
        else:
            tokens.append(Token("SYMBOL", word))
            program.pop(0)
    return tokens

def crawl(prgm):
    

def eval(program: (Token, list), env = global_env):
    if isinstance(program, Token):
        
        if program._type == 'SYMBOL':
            return env.find(program.value)[program.value]
        elif program._type == 'INT' or program._type == 'BOOL':
            return program.value
    elif  isinstance(program[0], list) :
        return eval(program[0], env)
    elif program[0]._type == T.INT or program[0]._type == T.BOOL:
        return [eval(arg, env) for arg in program]
    
    else:
        
        op = program[0].value
        args = program[1:]
    
        if op == "lambda":
            return Procedure(program[1], program[2], env)
        elif op == "define":
            env[program[1].value] = eval(program[2], env)
        elif op == "if":
            if eval(args[0], env) == "#t":
                return eval(args[1], env)
            else: return eval(args[2], env)
        elif op == "quote":
            arg = args[0]
            if isinstance(arg, Token):
                return arg.value
            
                
        else:        
            procedure = eval(program[0], env)
            values = [eval(arg, env) for arg in program[1:]]
            return procedure(*values)

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
        parsed = parse(lexed)
        result = eval(parsed)
    except label:
        return error
    return result
        

def repl():

    _input = ""

    print(solve(load_prgm("test.ls")))
    while True:
        _input = input("Geoff>")
        if _input == "!QUIT":
            break
        else:
            print(solve(_input))
            



repl();
