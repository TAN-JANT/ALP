class Unmatched_Parenthesis_Error(Exception):
    def __init__(self, line, column):
        self.line = line
        self.column = column

    def __str__(self):
        return f"Unmatched parenthesis at line {self.line}, column {self.column}"


class Unparseable_float_Error(Exception):
    def __init__(self, line, column):
        self.line = line
        self.column = column

    def __str__(self):
        return f"Unparseable float at line {self.line}, column {self.column}"
    
class Unparseable_dot_access_Error(Exception):
    def __init__(self, line, column):
        self.line = line
        self.column = column

    def __str__(self):
        return f"Unparseable dot access at line {self.line}, column {self.column}"
    

class Unparseable_include_Error(Exception):
    def __init__(self, line, column):
        self.line = line
        self.column = column

    def __str__(self):
        return f"Unparseable include at line {self.line}, column {self.column}"