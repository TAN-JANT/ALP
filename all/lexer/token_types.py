# Token class definitions

class INCLUDE_TOKEN:
    def __init__(self, value: str):
        """value is the path to the file to include
        include "path/to/file.all"
        """
        self.value = value


class STRING_TOKEN:
    def __init__(self, value: str):
        '''value is the string content
        """Hello, World!"""
        '''
        self.value = value