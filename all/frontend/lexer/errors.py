class Unterminated_String_Error(Exception):
    def __init__(self, start_line, start_column, end_line, end_column, file="<unknown>"):
        self.start_line = start_line
        self.start_column = start_column
        self.end_line = end_line
        self.end_column = end_column
        self.file = file
        super().__init__(
            f"Unterminated string literal from {file}:{start_line},{start_column} to {end_line},{end_column}"
        )


class Unknown_Error(Exception):
    def __init__(self, line, column, file="<unknown>"):
        self.line = line
        self.column = column
        self.file = file
        super().__init__(f"Unknown error at {file}:{line},{column}")
