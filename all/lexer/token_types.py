# Token class definitions

class INCLUDE_TOKEN:
    def __init__(self, value: str):
        """value is the path to the file to include
        include "path/to/file.all"
        """
        self.value = value

class TYPE_TOKEN:
    def __init__(self, name: str):
        """name is the name of the type
        i8, i16, i32, i64, ptr i8, etc.
        """
        self.name = name

class INTEGER_TOKEN:
    def __init__(self, value: int):
        """value is the integer value
        42, 0, -1, etc.
        """
        self.value = value

class HEX_TOKEN:
    def __init__(self, value: str):
        """value is the hexadecimal value
        0x1A, 0xFF, etc.
        """
        self.value = value

class BINARY_TOKEN:
    def __init__(self, value: str):
        """value is the binary value
        0b1010, 0b1111, etc.
        """
        self.value = value

class DIV_TOKEN:
    def __init__(self):
        """a token to indicate division operation
        10 / 2
        """
        pass

class MUL_TOKEN:
    def __init__(self):
        """a token to indicate multiplication operation
        10 * 2
        """
        pass

class ADD_TOKEN:
    def __init__(self):
        """a token to indicate addition operation
        10 + 2
        """
        pass

class SUB_TOKEN:
    def __init__(self):
        """a token to indicate subtraction operation
        10 - 2
        """
        pass

class POW_TOKEN:
    def __init__(self):
        """a token to indicate exponentiation operation
        2 ** 3
        """
        pass

class ASSIGN_TOKEN:
    def __init__(self):
        """a token to indicate assignment operation
        x = 10
        """
        pass

class IDENTIFIER_TOKEN:
    def __init__(self, value: str):
        """value is the identifier name
        main, person, print, etc.
        """
        self.value = value

class STRING_TOKEN:
    def __init__(self, value: str):
        '''value is the string content
        """Hello, World!"""
        '''
        self.value = value

class EXPORT_TOKEN:
    def __init__(self):
        """a token to indicate that the function is exported
        export func i8 main(){
            return 0;
        }
        """
        pass

class STRUCT_TOKEN:
    def __init__(self):
        """struct definition token
        struct person {
            i8 age
            ptr i8 name
        }
        """
        pass

class FUNC_TOKEN:
    def __init__(self):
        """function definition token
        func i8 main(){
            return 0;
        }
        """
        pass
