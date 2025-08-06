class Unmatched_Parenthesis_Error(Exception):
    def __init__(self, line, column, file="<unknown>"):
        self.line = line
        self.column = column
        self.file = file

    def __str__(self):
        return f"Unmatched parenthesis at File {self.file}, line {self.line}, column {self.column}"


class Unparseable_float_Error(Exception):
    def __init__(self, line, column, file="<unknown>"):
        self.line = line
        self.column = column
        self.file = file

    def __str__(self):
        return f"Unparseable float at File {self.file}, line {self.line}, column {self.column}"
    

class Unparseable_dot_access_Error(Exception):
    def __init__(self, line, column, file="<unknown>"):
        self.line = line
        self.column = column
        self.file = file

    def __str__(self):
        return f"Unparseable dot access at File {self.file}, line {self.line}, column {self.column}"
    

class Unparseable_include_Error(Exception):
    def __init__(self, line, column, file="<unknown>"):
        self.line = line
        self.column = column
        self.file = file

    def __str__(self):
        return f"Unparseable include at File {self.file}, line {self.line}, column {self.column}"
    

class Unparseable_struct_Error(Exception):
    def __init__(self, line, column, file="<unknown>"):
        self.line = line
        self.column = column
        self.file = file

    def __str__(self):
        return f"Unparseable struct at File {self.file}, line {self.line}, column {self.column}"
    

class Non_Globalscope_Struct_Error(Exception):
    def __init__(self, line, column, file="<unknown>"):
        self.line = line
        self.column = column
        self.file = file

    def __str__(self):
        return f"Structs can only be defined in global scope at File {self.file}, line {self.line}, column {self.column}"
    

class Struct_Cycle_Error(Exception):
    def __init__(self, line, column, file="<unknown>"):
        self.line = line
        self.column = column
        self.file = file

    def __str__(self):
        return f"Struct cycle detected at File {self.file}, line {self.line}, column {self.column}"
