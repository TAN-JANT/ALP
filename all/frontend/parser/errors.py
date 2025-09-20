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

class Unparseable_function_Error(Exception):
    def __init__(self, line, column, file="<unknown>"):
        self.line = line
        self.column = column
        self.file = file

    def __str__(self):
        return f"Unparseable function at File {self.file}, line {self.line}, column {self.column}"

class Unparseable_comment_Error(Exception):
    def __init__(self, line, column, file="<unknown>"):
        self.line = line
        self.column = column
        self.file = file

    def __str__(self):
        return f"Unparseable comment at File {self.file}, line {self.line}, column {self.column}"

class Unparseable_if_block_Error(Exception):
    def __init__(self, line, column, file="<unknown>"):
        self.line = line
        self.column = column
        self.file = file

    def __str__(self):
        return f"Unparseable if block at File {self.file}, line {self.line}, column {self.column}"
    
class Unparseable_NOT_error(Exception):
    def __init__(self,line,column,file = "<unknown>"):
        self.line = line
        self.column = column
        self.file = file

    def __str__(self):
        return f"Unparseable not operator at File {self.file}, line {self.line}, column {self.column}"
    
class Unparseable_NEGATE_error(Exception):
    def __init__(self,line,column,file = "<unknown>"):
        self.line = line
        self.column = column
        self.file = file

    def __str__(self):
        return f"Unparseable negative operator at File {self.file}, line {self.line}, column {self.column}"

class Type_mismatch_Error(Exception):
    def __init__(self, expected_type:str, got_type:str, line:int, column:int, file="<unknown>"):
        self.expected_type = expected_type
        self.got_type = got_type
        self.line = line
        self.column = column
        self.file = file

    def __str__(self):
        return f"Type mismatch: Expected {self.expected_type}, got {self.got_type} at File {self.file}, line {self.line}, column {self.column}"

class Undefined_variable_Error(Exception):
    def __init__(self, var_name:str, line:int, column:int, file="<unknown>"):
        self.var_name = var_name
        self.line = line
        self.column = column
        self.file = file

    def __str__(self):
        return f"Undefined variable '{self.var_name}' at File {self.file}, line {self.line}, column {self.column}"
    


class Undefined_field_Error(Exception):
    def __init__(self, field_name:str, struct_name:str, line:int, column:int, file="<unknown>"):
        self.field_name = field_name
        self.struct_name = struct_name
        self.line = line
        self.column = column
        self.file = file

    def __str__(self):
        return f"Undefined field '{self.field_name}' in struct '{self.struct_name}' at File {self.file}, line {self.line}, column {self.column}"