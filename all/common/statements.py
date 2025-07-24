from all.common import token_types


class Statement:
    def __init__(self, line, column):
        self.line = line
        self.column = column
    def __repr__(self):
        return f"<{self.__class__.__name__}>"


class Round_Parenthesis_Statement(Statement):
    def __init__(self, line, column, body):
        super().__init__(line, column)
        self.body = body  # içindeki ifadeler
    def __repr__(self):
        return f"<Round_Parenthesis_Statement: {self.body}>"
    
class Square_Parenthesis_Statement(Statement):
    def __init__(self, line, column, body):
        super().__init__(line, column)
        self.body = body  # içindeki ifadeler
    def __repr__(self):
        return f"<Square_Parenthesis_Statement: {self.body}>"
    
class Brace_Statement(Statement):
    def __init__(self, line, column, body):
        super().__init__(line, column)
        self.body = body  # içindeki ifadeler
    def __repr__(self):
        return f"<Brace_Statement: {self.body}>"
    
class DOT_ACCESS_Statement(Statement):
    def __init__(self, line, column, left,right):
        super().__init__(line, column)
        self.left = left  # içindeki ifadeler
        self.right = right
    def __repr__(self):
        return f"<Dot_Access_Statement: {self.left}.{self.right} >"
