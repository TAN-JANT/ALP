from . import errors
from . import token_types 

"""
Lexer class for ALP language.
Syntax information is avaliable in the parser
"""

"""
    include "path/to/file.all"
    struct person {
        i8 age
        ptr i8 name
    }

    export func i8 main(){
        return 0;
    }

    func void print(ptr i8 string, i16 len){
        ASM {
            mov rax,rsi
            mov rsi,rdx
            mov rdi,1
            mov rdx,rax
            mov rax,1
            syscall
        }
        return;
    }
"""


class Lexer:
    def __init__(self):
        pass

    def lex_src(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 0
        self.current_char = (
            self.source[self.position] if self.position < len(self.source) else None
        )

    def advance(self):
        """Advances the position in the source code"""
        if self.current_char == "\n":
            self.line += 1
            self.column = 0
        self.position += 1
        self.column += 1
        self.current_char = (
            self.source[self.position] if self.position < len(self.source) else None
        )

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
        tokens = []
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
            
            if self.current_char == '"""':
                # Handle string literals
                start_pos = self.position
                start_line = self.line
                start_column = self.column
                self.advance()
                while self.current_char != '"""' and self.current_char is not None:
                    self.advance()
                if self.current_char == '"""':
                    tokens.append(token_types.STRING_TOKEN(self.source[start_pos + 3 : self.position]))
                    self.advance()
                else:
                    raise errors.Unterminated_String_Error(start_line, start_column, self.line, self.column) # start line column and end line column
            # Add more token handling logic here
            else:
                raise errors.Unknown_Error(self.line, self.column)
        return tokens
