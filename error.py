class Error():
    errorType = 'Generic Error:'
    def __init__(self, msg):
        self.msg = msg
    def __repr__(self):
        return self.msg

class MissingSymbolError(Error):
    errorType = 'Symbol Error:'
    def __init__(self, msg):
        self.msg = msg
    def __repr__(self):
        return f"Error: Symbol \"{self.msg}\" is not found!";

class NotAProcError(Error):
    errorType = 'Not a procedure Error:'
    pass

class TypeError(Error):
    errorType = 'Type Error:'
    pass

class ArgError(Error):
    errorType = 'Argument Amount Error:'
    pass

class MathError(Error):
    errorType = 'Math Error:'
    
    
