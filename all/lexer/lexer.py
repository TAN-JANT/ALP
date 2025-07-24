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
        """Advances the position in the source code"""
        
        if self.current_char == "\n":
            self.line += 1
            self.column = 0
        self.position += 1
        self.column += 1
        self.current_char = (
            self.source[self.position] if self.position < len(self.source) else None
        )
    def advance(self,offset=1):
        """Advances the position in the source code"""
        
        for _ in range(offset):
            self.__advance()

    def peek(self, offset=1, size=1):
        """Peeks at next characters but does not advance the position"""
        if self.position + offset < len(self.source):
            return self.source[self.position + offset : self.position + offset + size]
        return None
    
    def skip_whitespace(self):
        """Skips whitespace characters in the source code"""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def __lex(self):
        """Lexes the source code and returns a list of tokens"""
        tokens = [self.info]
        special_characters = r"<>!^+-*/%=.:,?&|@(){}[]"
        special_character_classes = [
                    token_types.LESS_TOKEN,
                    token_types.GREATER_TOKEN,
                    token_types.NOT_TOKEN,
                    token_types.POW_TOKEN,
                    token_types.ADD_TOKEN,
                    token_types.SUB_TOKEN,
                    token_types.ASTERISK_TOKEN,
                    token_types.DIV_TOKEN,
                    token_types.MOD_TOKEN,
                    token_types.EQUAL_TOKEN,
                    token_types.DOT_TOKEN,
                    token_types.COLON_TOKEN,
                    token_types.COMMA_TOKEN,
                    token_types.QUESTION_MARK_TOKEN,
                    token_types.AND_TOKEN,
                    token_types.PIPE_TOKEN,
                    token_types.DIRECTIVE_TOKEN,
                    token_types.LEFT_PAREN_TOKEN,
                    token_types.RIGHT_PAREN_TOKEN,
                    token_types.LEFT_BRACE_TOKEN,
                    token_types.RIGHT_BRACE_TOKEN,
                    token_types.LEFT_SQUARE_PAREN_TOKEN,
                    token_types.RIGHT_SQUARE_PAREN_TOKEN,
                ]
        while True:
            
            if self.current_char is None:
                break
            prev_line = self.line
            self.skip_whitespace()
            if self.line > prev_line:
                tokens.append(token_types.NEWLINE_TOKEN(prev_line, self.column, self.position))
            if self.current_char is None:
                break
            if self.current_char == "/":  # Comments will be ignored at tokenization
                peek = self.peek()
                if peek == "/":
                    while self.current_char != None and self.current_char != "\n":
                        self.advance()
                    continue
                    
                if peek == "*":
                    self.advance(2)
                    while self.current_char == None or not (self.current_char == "*" and self.peek() == "/"):
                        self.advance()
                    continue

                

            if self.current_char == '"' and self.peek(size=2) == '""':#Double quoted str
                # Handle single-quoted string literals
                start_pos = self.position
                start_line = self.line
                start_column = self.column
                self.advance()
                while not (self.current_char == '"' and self.peek(size=2) == '""') and self.current_char is not None:
                    if self.current_char == "\\":
                        self.advance()
                    self.advance()
                if self.current_char == '"' and self.peek(size=2) == '""':
                    tokens.append(token_types.STRING_TOKEN(self.source[start_pos + 3 : self.position],start_line,start_column,start_pos))
                    self.advance(3)
                else:
                    raise errors.Unterminated_String_Error(start_line, start_column, self.line, self.column) # start line column and end line column
                
                continue
            
            if self.current_char == "'" and self.peek(size=2) == "''":#One quoted str
                # Handle single-quoted string literals
                start_pos = self.position
                start_line = self.line
                start_column = self.column
                self.advance()
                while not (self.current_char == "'" and self.peek(size=2) == "''") and self.current_char is not None:
                    if self.current_char == "\\":
                        self.advance()
                    self.advance()
                if self.current_char == "'" and self.peek(size=2) == "''":
                    tokens.append(token_types.STRING_TOKEN(self.source[start_pos + 3 : self.position],start_line,start_column,start_pos))
                    self.advance(3)
                else:
                    raise errors.Unterminated_String_Error(start_line, start_column, self.line, self.column) # start line column and end line column
                
                continue
                
            
            if self.current_char in special_characters:#Special characters
                tokens.append(special_character_classes[special_characters.index(self.current_char)](self.line,self.column,self.position))
                self.advance()
                continue
            
            if self.current_char.isdigit():#Integers, hexadecimals, Binary numbers
                if self.current_char == "0" and self.peek() == "x":
                    start_pos = self.position
                    start_line = self.line
                    start_column = self.column
                    self.advance()
                    self.advance()
                    while self.current_char is not None and self.current_char.isdigit():
                        self.advance()
                    
                    tokens.append(token_types.HEX_TOKEN(self.source[start_pos:self.position],start_line,start_column,start_pos)) 
                    continue
                
                if self.current_char == "0" and self.peek() == "b":
                    start_pos = self.position
                    start_line = self.line
                    start_column = self.column
                    self.advance()
                    self.advance()
                    while self.current_char is not None and self.current_char.isdigit():
                        self.advance()
                    
                    tokens.append(token_types.BINARY_TOKEN(self.source[start_pos:self.position],start_line,start_column,start_pos)) 
                    continue

                start_pos = self.position
                start_line = self.line
                start_column = self.column
                while self.current_char is not None and self.current_char.isdigit():
                    self.advance()
                
                tokens.append(token_types.INTEGER_TOKEN(self.source[start_pos:self.position],start_line,start_column,start_pos))
                continue

            if self.current_char.isalpha() or self.current_char == "_":
                start_pos = self.position
                start_line = self.line
                start_column = self.column
                self.advance()
                while self.current_char != None and (self.current_char.isalpha() 
                                                     or self.current_char == "_" 
                                                     or self.current_char.isdigit()):
                    self.advance()
                tokens.append(token_types.IDENTIFIER_TOKEN(self.source[start_pos:self.position],start_line,start_column,start_pos))
                    
        return tokens
