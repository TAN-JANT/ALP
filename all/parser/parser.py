from turtle import position
from all.common import statements
from ..common import token_types
from . import errors
from ..lexer.lexer import Lexer

class Parser:
    def __init__(self):
        pass

    
    def parse(self, tokens:list):
        
        
        self.parsed_data = tokens.copy()
        
        self.info ,self.parsed_data = self.__parse_include(self.parsed_data.copy(),[self.parsed_data[0]["working_directory"]+self.parsed_data[0]["file_name"]])
        self.parsed_data = self.__parse_bodies()[1]
        self.parsed_data = self.__parse_dots(self.parsed_data)
        return self.parsed_data

    def __parse_include(self,src:list,includeds=[]):
        body = []
        position = 0
        info = src.pop(0)
        while position < len(src):
            token = src[position]
            if isinstance(token, token_types.IDENTIFIER_TOKEN) and token.value == "include":
                if position == len(src) - 1:
                    raise errors.Unparseable_include_Error(token.line, token.column)
                position += 1
                if not isinstance(src[position], token_types.STRING_TOKEN):
                    raise errors.Unparseable_include_Error(token.line, token.column)
                include_file = info["working_directory"] + src[position].value
                if not include_file in includeds:
                    includeds.append(include_file)
                    included_tokens = self.__parse_include(Lexer().lex_src(include_file),includeds)[1]
                    body.extend(included_tokens)
                position += 1
                continue

            body.append(token)
            position += 1

        return [info,body]

    def __parse_bodies(self,opened=False,position=0):
        body = []

        while position < len(self.parsed_data):
            token = self.parsed_data[position]
            if isinstance(token, token_types.LEFT_PAREN_TOKEN):
                opened = True
                position += 1
                position, sub_body = self.__parse_bodies(opened, position)
                body.append(statements.Round_Parenthesis_Statement(token.line, token.column, sub_body))
                continue
            if isinstance(token, token_types.LEFT_SQUARE_PAREN_TOKEN):
                opened = True
                position += 1
                position, sub_body = self.__parse_bodies(opened, position)
                body.append(statements.Square_Parenthesis_Statement(token.line, token.column, sub_body))
                continue
            if isinstance(token, token_types.LEFT_BRACE_TOKEN):
                opened = True
                position += 1
                position , sub_body = self.__parse_bodies(opened, position)
                body.append(statements.Brace_Statement(token.line, token.column, sub_body))
                continue

            if token is not None and (type(token) in [token_types.RIGHT_PAREN_TOKEN, token_types.RIGHT_SQUARE_PAREN_TOKEN, token_types.RIGHT_BRACE_TOKEN]):
                if not opened:
                    raise errors.Unmatched_Parenthesis_Error(token.line, token.column)
                position += 1
                break

            
            
            position += 1
            body.append(token)
        


        return [position, body]

    def __parse_dots(self,src:list):
        position = 0
        body = src.copy()
        while position < len(body):
            token = body[position]
            if isinstance(token, token_types.DOT_TOKEN):
                if position == 0 or position == len(body) - 1:
                    raise errors.Unparseable_dot_access_Error(token.line, token.column)
                body.pop(position)
                left = body.pop(position - 1)   
                right = body.pop(position - 1)
                position -= 1
                if isinstance(left,token_types.INTEGER_TOKEN) and isinstance(right,token_types.INTEGER_TOKEN):
                    body.insert(position,token_types.FLOAT_TOKEN(float(left.value + "." + right.value), left.line, left.column, left.pos))
                elif isinstance(left,token_types.IDENTIFIER_TOKEN) and isinstance(right,token_types.IDENTIFIER_TOKEN):
                    body.insert(position-2,statements.DOT_ACCESS_Statement(left.line, left.column, left.value, right.value))
                elif isinstance(left,statements.DOT_ACCESS_Statement) and isinstance(right,token_types.IDENTIFIER_TOKEN):
                    body.insert(position-2,statements.DOT_ACCESS_Statement(left.line, left.column, left, right.value))
                else:
                    raise errors.Unparseable_dot_access_Error(token.line, token.column)
                
                continue
            if isinstance(token, statements.Round_Parenthesis_Statement) or isinstance(token, statements.Square_Parenthesis_Statement) or isinstance(token, statements.Brace_Statement):
                sub_body = self.__parse_dots(token.body)
                token.body = sub_body
                position += 1
                continue
            position += 1
        return body
    