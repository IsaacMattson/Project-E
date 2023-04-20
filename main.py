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
        return solve(self.body, Environment(self.parms, args, self.env))
        


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
        'quote':    lambda lst : lst
        
    })
    return env

global_env = native_env();

def lex(text) -> str:
    lexed = text.replace("(", " ( ").replace(")", " ) ").split()
    if lexed.count(')') == lexed.count('('):
        return lexed;
    else:
        return Error("?");

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

def solve(program: (Token, list), env = global_env):
    if isinstance(program, Token):
        
        if program._type == 'SYMBOL':
            return env.find(program.value)[program.value]
        elif program._type == 'INT' or program._type == 'BOOL':
            return program.value
    elif  isinstance(program[0], list) :
        return solve(program[0], env)
    elif program[0]._type == T.INT or program[0]._type == T.BOOL:
        return [solve(arg, env) for arg in program]
    
    else:
        
        op = program[0].value
        args = program[1:]
    
        if op == "lambda":
            return Procedure(program[1], program[2], env)
        elif op == "define":
            env[program[1].value] = solve(program[2], env)
        elif op == "if":
            if solve(args[0], env) == "#t":
                return solve(args[1], env)
            else: return solve(args[2], env)
                
        else:        
            procedure = solve(program[0], env)
            values = [solve(arg, env) for arg in program[1:]]
            return procedure(*values)

def repl():

    _input = ""
    while True:
        _input = input("Geoff>")
        if _input == "!QUIT":
            break
        else:
            lexed = lex(_input)
            if isinstance(lexed, Error):
                print(lexed)
            else:
                parsed = parse(lexed)
                print(solve(parsed))
            

repl();
