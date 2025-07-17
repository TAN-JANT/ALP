from typing import Any

class TOKEN:
    def __init__(self, t_type: str, line: int, column: int, pos: int, value: Any):
        self.type = t_type
        self.line = line
        self.column = column
        self.pos = pos
        self.value = value

    def __repr__(self) -> str:
        return f"{self.type} {self.value} at line {self.line}, column {self.column}"

class DIRECTIVE_TOKEN(TOKEN):
    def __init__(self, line: int, column: int, pos: int):
        super().__init__("DIRECTIVE TOKEN", line, column, pos, "@")

class INTEGER_TOKEN(TOKEN):
    def __init__(self, value: int, line: int, column: int, pos: int):
        super().__init__("INTEGER TOKEN", line, column, pos, value)

class HEX_TOKEN(TOKEN):
    def __init__(self, value: int, line: int, column: int, pos: int):
        super().__init__("HEX TOKEN", line, column, pos, value)

class BINARY_TOKEN(TOKEN):
    def __init__(self, value: int, line: int, column: int, pos: int):
        super().__init__("BINARY TOKEN", line, column, pos, value)

class FLOAT_TOKEN(TOKEN):
    def __init__(self, value: float, line: int, column: int, pos: int):
        super().__init__("FLOAT TOKEN", line, column, pos, value)

class STRING_TOKEN(TOKEN):
    def __init__(self, value: str, line: int, column: int, pos: int):
        super().__init__("STRING TOKEN", line, column, pos, value)

class IDENTIFIER_TOKEN(TOKEN):
    def __init__(self, value: str, line: int, column: int, pos: int):
        super().__init__("IDENTIFIER TOKEN", line, column, pos, value)

class NEWLINE_TOKEN(TOKEN):
    def __init__(self, line: int, column: int, pos: int):
        super().__init__("NEWLINE TOKEN", line, column, pos, None)

# Symbol tokens
class DIV_TOKEN(TOKEN):
    def __init__(self, line: int, column: int, pos: int):
        super().__init__("DIV TOKEN", line, column, pos, "/")

class ASTERISK_TOKEN(TOKEN):
    def __init__(self, line: int, column: int, pos: int):
        super().__init__("ASTERISK TOKEN", line, column, pos, "*")

class POW_TOKEN(TOKEN):
    def __init__(self, line: int, column: int, pos: int):
        super().__init__("POW TOKEN", line, column, pos, "**")

class MOD_TOKEN(TOKEN):
    def __init__(self, line: int, column: int, pos: int):
        super().__init__("MOD TOKEN", line, column, pos, "%")

class ADD_TOKEN(TOKEN):
    def __init__(self, line: int, column: int, pos: int):
        super().__init__("ADD TOKEN", line, column, pos, "+")

class SUB_TOKEN(TOKEN):
    def __init__(self, line: int, column: int, pos: int):
        super().__init__("SUB TOKEN", line, column, pos, "-")

class LEFT_PAREN_TOKEN(TOKEN):
    def __init__(self, line: int, column: int, pos: int):
        super().__init__("LEFT PAREN TOKEN", line, column, pos, "(")

class RIGHT_PAREN_TOKEN(TOKEN):
    def __init__(self, line: int, column: int, pos: int):
        super().__init__("RIGHT PAREN TOKEN", line, column, pos, ")")

class LEFT_SQUARE_PAREN_TOKEN(TOKEN):
    def __init__(self, line: int, column: int, pos: int):
        super().__init__("LEFT SQUARE PAREN TOKEN", line, column, pos, "[")

class RIGHT_SQUARE_PAREN_TOKEN(TOKEN):
    def __init__(self, line: int, column: int, pos: int):
        super().__init__("RIGHT SQUARE PAREN TOKEN", line, column, pos, "]")

class LEFT_BRACE_TOKEN(TOKEN):
    def __init__(self, line: int, column: int, pos: int):
        super().__init__("LEFT BRACE TOKEN", line, column, pos, "{")

class RIGHT_BRACE_TOKEN(TOKEN):
    def __init__(self, line: int, column: int, pos: int):
        super().__init__("RIGHT BRACE TOKEN", line, column, pos, "}")

class COMMA_TOKEN(TOKEN):
    def __init__(self, line: int, column: int, pos: int):
        super().__init__("COMMA TOKEN", line, column, pos, ",")

class EQUAL_TOKEN(TOKEN):
    def __init__(self, line: int, column: int, pos: int):
        super().__init__("EQUAL TOKEN", line, column, pos, "=")
class LESS_TOKEN(TOKEN):
    def __init__(self, line: int, column: int, pos: int):
        super().__init__("LESS TOKEN", line, column, pos, "<")

class GREATER_TOKEN(TOKEN):
    def __init__(self, line: int, column: int, pos: int):
        super().__init__("GREATER TOKEN", line, column, pos, ">")

class AND_TOKEN(TOKEN):
    def __init__(self, line: int, column: int, pos: int):
        super().__init__("AND TOKEN", line, column, pos, "&")

class PIPE_TOKEN(TOKEN):
    def __init__(self, line: int, column: int, pos: int):
        super().__init__("PIPE TOKEN", line, column, pos, "|")

class NOT_TOKEN(TOKEN):
    def __init__(self, line: int, column: int, pos: int):
        super().__init__("NOT TOKEN", line, column, pos, "!")

class COLON_TOKEN(TOKEN):
    def __init__(self, line: int, column: int, pos: int):
        super().__init__("COLON TOKEN", line, column, pos, ":")

class DOT_TOKEN(TOKEN):
    def __init__(self, line: int, column: int, pos: int):
        super().__init__("DOT TOKEN", line, column, pos, ".")

class QUESTION_MARK_TOKEN(TOKEN):
    def __init__(self, line: int, column: int, pos: int):
        super().__init__("QUESTION MARK TOKEN", line, column, pos, "?")
        
         

        
        
