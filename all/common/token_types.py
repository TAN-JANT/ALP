from typing import Any

class TOKEN:
    def __init__(self, t_type: str, line: int, column: int, pos: int, value: Any, file: str = "<unknown>"):
        self.type = t_type
        self.line = line
        self.column = column
        self.pos = pos
        self.value = value
        self.file = file  # <-- EKLENDİ

    def __repr__(self) -> str:
        return f"{self.type}({self.value} at {self.file}:{self.line},{self.column})"
class DIRECTIVE_TOKEN(TOKEN):
    def __init__(self, line, column, pos, file="<unknown>"):
        super().__init__("DIRECTIVE TOKEN", line, column, pos, "@", file)

class INTEGER_TOKEN(TOKEN):
    def __init__(self, value, line, column, pos, file="<unknown>"):
        super().__init__("INTEGER TOKEN", line, column, pos, value, file)

class HEX_TOKEN(TOKEN):
    def __init__(self, value, line, column, pos, file="<unknown>"):
        super().__init__("HEX TOKEN", line, column, pos, value, file)

class BINARY_TOKEN(TOKEN):
    def __init__(self, value, line, column, pos, file="<unknown>"):
        super().__init__("BINARY TOKEN", line, column, pos, value, file)

class FLOAT_TOKEN(TOKEN):
    def __init__(self, value, line, column, pos, file="<unknown>"):
        super().__init__("FLOAT TOKEN", line, column, pos, value, file)

class STRING_TOKEN(TOKEN):
    def __init__(self, value, line, column, pos, file="<unknown>"):
        super().__init__("STRING TOKEN", line, column, pos, value, file)

class IDENTIFIER_TOKEN(TOKEN):
    def __init__(self, value, line, column, pos, file="<unknown>"):
        super().__init__("IDENTIFIER TOKEN", line, column, pos, value, file)

class NEWLINE_TOKEN(TOKEN):
    def __init__(self, line, column, pos, file="<unknown>"):
        super().__init__("NEWLINE TOKEN", line, column, pos, None, file)

# Symbol tokens
class DIV_TOKEN(TOKEN):
    def __init__(self, line, column, pos, file="<unknown>"):
        super().__init__("DIV TOKEN", line, column, pos, "/", file)

class ASTERISK_TOKEN(TOKEN):
    def __init__(self, line, column, pos, file="<unknown>"):
        super().__init__("ASTERISK TOKEN", line, column, pos, "*", file)

class POW_TOKEN(TOKEN):
    def __init__(self, line, column, pos, file="<unknown>"):
        super().__init__("POW TOKEN", line, column, pos, "**", file)

class MOD_TOKEN(TOKEN):
    def __init__(self, line, column, pos, file="<unknown>"):
        super().__init__("MOD TOKEN", line, column, pos, "%", file)

class ADD_TOKEN(TOKEN):
    def __init__(self, line, column, pos, file="<unknown>"):
        super().__init__("ADD TOKEN", line, column, pos, "+", file)

class SUB_TOKEN(TOKEN):
    def __init__(self, line, column, pos, file="<unknown>"):
        super().__init__("SUB TOKEN", line, column, pos, "-", file)

class LEFT_PAREN_TOKEN(TOKEN):
    def __init__(self, line, column, pos, file="<unknown>"):
        super().__init__("LEFT PAREN TOKEN", line, column, pos, "(", file)

class RIGHT_PAREN_TOKEN(TOKEN):
    def __init__(self, line, column, pos, file="<unknown>"):
        super().__init__("RIGHT PAREN TOKEN", line, column, pos, ")", file)

class LEFT_SQUARE_PAREN_TOKEN(TOKEN):
    def __init__(self, line, column, pos, file="<unknown>"):
        super().__init__("LEFT SQUARE PAREN TOKEN", line, column, pos, "[", file)

class RIGHT_SQUARE_PAREN_TOKEN(TOKEN):
    def __init__(self, line, column, pos, file="<unknown>"):
        super().__init__("RIGHT SQUARE PAREN TOKEN", line, column, pos, "]", file)

class LEFT_BRACE_TOKEN(TOKEN):
    def __init__(self, line, column, pos, file="<unknown>"):
        super().__init__("LEFT BRACE TOKEN", line, column, pos, "{", file)

class RIGHT_BRACE_TOKEN(TOKEN):
    def __init__(self, line, column, pos, file="<unknown>"):
        super().__init__("RIGHT BRACE TOKEN", line, column, pos, "}", file)

class COMMA_TOKEN(TOKEN):
    def __init__(self, line, column, pos, file="<unknown>"):
        super().__init__("COMMA TOKEN", line, column, pos, ",", file)

class EQUAL_TOKEN(TOKEN):
    def __init__(self, line, column, pos, file="<unknown>"):
        super().__init__("EQUAL TOKEN", line, column, pos, "=", file)

class LESS_TOKEN(TOKEN):
    def __init__(self, line, column, pos, file="<unknown>"):
        super().__init__("LESS TOKEN", line, column, pos, "<", file)

class GREATER_TOKEN(TOKEN):
    def __init__(self, line, column, pos, file="<unknown>"):
        super().__init__("GREATER TOKEN", line, column, pos, ">", file)

class AND_TOKEN(TOKEN):
    def __init__(self, line, column, pos, file="<unknown>"):
        super().__init__("AND TOKEN", line, column, pos, "&", file)

class PIPE_TOKEN(TOKEN):
    def __init__(self, line, column, pos, file="<unknown>"):
        super().__init__("PIPE TOKEN", line, column, pos, "|", file)

class NOT_TOKEN(TOKEN):
    def __init__(self, line, column, pos, file="<unknown>"):
        super().__init__("NOT TOKEN", line, column, pos, "!", file)

class COLON_TOKEN(TOKEN):
    def __init__(self, line, column, pos, file="<unknown>"):
        super().__init__("COLON TOKEN", line, column, pos, ":", file)

class DOT_TOKEN(TOKEN):
    def __init__(self, line, column, pos, file="<unknown>"):
        super().__init__("DOT TOKEN", line, column, pos, ".", file)

class QUESTION_MARK_TOKEN(TOKEN):
    def __init__(self, line, column, pos, file="<unknown>"):
        super().__init__("QUESTION MARK TOKEN", line, column, pos, "?", file)
