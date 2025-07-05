class Unterminated_String_Error(Exception):
    def __init__(self, start_line, start_column, end_line, end_column):
        self.start_line = start_line
        self.start_column = start_column
        self.end_line = end_line
        self.end_column = end_column
        super().__init__(
            f"Unterminated string literal from line {start_line}, column {start_column} to line {end_line}, column {end_column}"
        )
        
class Unknown_Error(Exception):
    def __init__(self, line, column):
        self.line = line
        self.column = column
        super().__init__(f"Unknown error at line {line}, column {column}")