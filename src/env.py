from main import Symbol

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
        
def gen_global_env() -> Environment:
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