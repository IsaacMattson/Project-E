class Error():
    def __init__(self, msg):
        self.msg = msg
    def __repr__(self):
        return self.msg

class MissingSymbolError(Error):
    def __init__(self, msg):
        self.msg = msg
    def __repr__(self):
        return f"Error: Symbol \"{self.error}\" is not found!";


    
