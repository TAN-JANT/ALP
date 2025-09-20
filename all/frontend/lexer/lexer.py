# type: ignore
from . import errors
from ..common import token_types

"""
Lexer class for ALP language.
Syntax information is avaliable at below
"""


class Lexer:
    def __init__(self):
        pass

    def lex_src(self, source: str):
        with open(source, "r") as f:
            self.source = f.read()
        _ = "/".join(source.split("/")[:-1])
        if _ != "":
            _ += "/"
        self.info = {
            "working_directory": _,
            "file_name": source.split("/")[-1],
        }
        self.position = 0
        self.line = 1
        self.column = 0
        self.current_char = (
            self.source[self.position] if self.position < len(self.source) else None
        )
        return self.__lex()

    def __advance(self):
        if self.current_char == "\n":
            self.line += 1
            self.column = 0
        self.position += 1
        self.column += 1
        self.current_char = (
            self.source[self.position] if self.position < len(self.source) else None
        )

    def advance(self, offset=1):
        for _ in range(offset):
            self.__advance()

    def peek(self, offset=1, size=1):
        if self.position + offset < len(self.source):
            return self.source[self.position + offset : self.position + offset + size]
        return None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def __lex(self):
        tokens = [self.info]
        special_char_map = {
            "<": token_types.TT_LESS_TOKEN,
            ">": token_types.TT_GREATER_TOKEN,
            "!": token_types.TT_NOT_TOKEN,
            "^": token_types.TT_XOR_TOKEN,
            "+": token_types.TT_ADD_TOKEN,
            "-": token_types.TT_SUB_TOKEN,
            "*": token_types.TT_ASTERISK_TOKEN,
            "/": token_types.TT_DIV_TOKEN,
            "%": token_types.TT_MOD_TOKEN,
            "=": token_types.TT_EQUAL_TOKEN,
            ".": token_types.TT_DOT_TOKEN,
            ":": token_types.TT_COLON_TOKEN,
            ",": token_types.TT_COMMA_TOKEN,
            ";": token_types.TT_SEMI_TOKEN,
            "?": token_types.TT_QUESTION_MARK_TOKEN,
            "&": token_types.TT_AND_TOKEN,
            "|": token_types.TT_PIPE_TOKEN,
            "(": token_types.TT_LEFT_PAREN_TOKEN,
            ")": token_types.TT_RIGHT_PAREN_TOKEN,
            "{": token_types.TT_LEFT_BRACE_TOKEN,
            "}": token_types.TT_RIGHT_BRACE_TOKEN,
            "[": token_types.TT_LEFT_SQUARE_PAREN_TOKEN,
            "]": token_types.TT_RIGHT_SQUARE_PAREN_TOKEN,
            "~": token_types.TT_TILDE_TOKEN
        } # (  2 + 3 ) * ( 3 + 5 )

        while True:
            if self.current_char is None:
                break
            prev_line = self.line
            self.skip_whitespace()
            if self.line > prev_line:
                tokens.append(
                    {
                        "type": token_types.TT_NEWLINE_TOKEN,
                        "line": prev_line,
                        "column": self.column,
                        "pos": self.position,
                        "file": self.info["working_directory"] + self.info["file_name"],
                    }
                )
            if self.current_char is None:
                break

            if self.current_char == "/":  # Comments
                peek = self.peek()
                if peek == "/":
                    while self.current_char is not None and self.current_char != "\n":
                        self.advance()
                    continue

                if peek == "*":
                    self.advance(2)
                    while self.current_char is not None and not (
                        self.current_char == "*" and self.peek() == "/"
                    ):
                        self.advance()
                    self.advance(2)
                    continue

            # Double quoted string
            if self.current_char == '"' and self.peek(size=2) == '""':
                start_pos = self.position
                start_line = self.line
                start_column = self.column
                self.advance()
                while (
                    not (self.current_char == '"' and self.peek(size=2) == '""')
                    and self.current_char is not None
                ):
                    if self.current_char == "\\":
                        self.advance()
                    self.advance()
                if self.current_char == '"' and self.peek(size=2) == '""':
                    tokens.append(
                        {
                            "type": token_types.TT_STRING_TOKEN,
                            "line": start_line,
                            "column": start_column,
                            "pos": start_pos,
                            "file": self.info["working_directory"]
                            + self.info["file_name"],
                            "value": self.source[start_pos + 3 : self.position],
                            "data_type": {"value":"@ptr","subtype":[{"value":"i8","subtype":[]}]}
                        }
                    )
                    self.advance(3)
                else:
                    raise Exception("Unterminated string")
                continue

            # Single quoted string
            if self.current_char == "'" and self.peek(size=2) == "''":
                start_pos = self.position
                start_line = self.line
                start_column = self.column
                self.advance()
                while (
                    not (self.current_char == "'" and self.peek(size=2) == "''")
                    and self.current_char is not None
                ):
                    if self.current_char == "\\":
                        self.advance()
                    self.advance()
                if self.current_char == "'" and self.peek(size=2) == "''":
                    tokens.append(
                        {
                            "type": token_types.TT_STRING_TOKEN,
                            "line": start_line,
                            "column": start_column,
                            "pos": start_pos,
                            "file": self.info["working_directory"]
                            + self.info["file_name"],
                            "value": self.source[start_pos + 3 : self.position],
                            "data_type": {"value":"@ptr","subtype":[{"value":"i8","subtype":[]}]}
                        }
                    )
                    self.advance(3)
                else:
                    raise Exception("Unterminated string")
                continue

            # Special characters
            if self.current_char in special_char_map:
                tokens.append(
                    {
                        "type": special_char_map[self.current_char],
                        "line": self.line,
                        "column": self.column,
                        "pos": self.position,
                        "file": self.info["working_directory"] + self.info["file_name"],
                    }
                )
                self.advance()
                continue

            # Numbers: hex, binary, integer
            if self.current_char.isdigit():
                if self.current_char == "0" and self.peek() == "x":
                    start_pos = self.position
                    start_line = self.line
                    start_column = self.column
                    self.advance(2)
                    while self.current_char is not None and self.current_char.isdigit():
                        self.advance()
                    tokens.append(
                        {
                            "type": token_types.TT_HEX_TOKEN,
                            "line": start_line,
                            "column": start_column,
                            "pos": start_pos,
                            "file": self.info["working_directory"]
                            + self.info["file_name"],
                            "value": self.source[start_pos : self.position],
                            "data_type": {"value":"i32","subtype":[]}
                        }
                    )
                    continue

                if self.current_char == "0" and self.peek() == "b":
                    start_pos = self.position
                    start_line = self.line
                    start_column = self.column
                    self.advance(2)
                    while self.current_char is not None and self.current_char.isdigit():
                        self.advance()
                    tokens.append(
                        {
                            "type": token_types.TT_BINARY_TOKEN,
                            "line": start_line,
                            "column": start_column,
                            "pos": start_pos,
                            "file": self.info["working_directory"]
                            + self.info["file_name"],
                            "value": self.source[start_pos : self.position],
                            "data_type": {"value":"i32","subtype":[]}
                        }
                    )
                    continue

                # Integer
                start_pos = self.position
                start_line = self.line
                start_column = self.column
                while self.current_char is not None and self.current_char.isdigit():
                    self.advance()
                tokens.append(
                    {
                        "type": token_types.TT_INTEGER_TOKEN,
                        "line": start_line,
                        "column": start_column,
                        "pos": start_pos,
                        "file": self.info["working_directory"] + self.info["file_name"],
                        "value": self.source[start_pos : self.position],
                        "data_type": {"value":"i32","subtype":[]}
                    }
                )
                continue

                # Identifiers
            if self.current_char.isalpha() or self.current_char == "_" or self.current_char == "@":
                start_pos = self.position
                start_line = self.line
                start_column = self.column
                self.advance()
                while self.current_char is not None and (
                    self.current_char.isalnum() or self.current_char == "_"
                ):
                    self.advance()
                tokens.append(
                    {
                        "type": token_types.TT_IDENTIFIER_TOKEN,
                        "line": start_line,
                        "column": start_column,
                        "pos": start_pos,
                        "file": self.info["working_directory"] + self.info["file_name"],
                        "value": self.source[start_pos : self.position],
                    }
                )
                continue

            # Eğer buraya kadar hiçbir koşula uymadıysa, bilinmeyen karakter
            raise Exception(
                f"Unknown character {self.current_char} at line {self.line}, column {self.column}"
            )

        return tokens
