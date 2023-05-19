class Error():
    errorType = 'Generic Error:'
    def __init__(self, msg, expr = []):
        self.msg = msg
        self.expr = expr
    def __repr__(self):
        return  f"\033[1;31m{self.msg}\nExpression:{self.expr}\033[0m"

class MissingSymbolError(Error):
    errorType = 'Symbol Error:'
    def __init__(self, msg):
        self.msg = msg
    def __repr__(self):
        return f"Error: Symbol \"{self.msg}\" is not found!";

class NotAProcError(Error):
    errorType = 'Not a procedure Error:'
    pass

class ArgError(Error):
    errorType = 'Argument Amount Error:'
    pass

class MathError(Error):
    errorType = 'Math Error:'
    
    
class UserError(Exception):
    pass

def raise_error(s):
    raise UserError(s)
