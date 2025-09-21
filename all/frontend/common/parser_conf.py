from all.frontend.common.expressions import *
from .token_types import *
from .statements import *

# Higher number is higher binding ability
# First number is binding for left,
# second number is binding for right,
# Zero binding number means operator has not binding ability

CONF_BINDING_NUMBER = {

    TT_NOT_TOKEN                    : (0  ,90 ), # !a
    TT_TILDE_TOKEN                  : (0  ,90 ), # ~a
    TT_SUB_TOKEN                    : (50 ,90 ), # -a    a - b

    TT_ADD_TOKEN                    : (50 ,50 ), # a + b
    TT_ASTERISK_TOKEN               : (60 ,60 ), # a * b
    TT_DIV_TOKEN                    : (60 ,60 ), # a / b
    TT_COMBINED_INT_DIVISION_TOKEN  : (60 ,60 ), # a // b
    TT_COMBINED_POW_TOKEN           : (90 ,90 ), # a ** b

        # Comparison
    TT_COMBINED_EQUAL_TOKEN         : (40 ,40 ), # a == b
    TT_COMBINED_NOT_EQUAL_TOKEN     : (40 ,40 ), # a != b
    TT_LESS_TOKEN                   : (40 ,40 ), # a < b
    TT_COMBINED_LESS_EQUAL_TOKEN    : (40 ,40 ), # a <= b
    TT_GREATER_TOKEN                : (40 ,40 ), # a > b
    TT_COMBINED_GREATER_EQUAL_TOKEN : (40 ,40 ), # a >= b

    # Logical AND / OR
    TT_COMBINED_LOGIC_AND_TOKEN     : (30 ,30 ), # a && b
    TT_COMBINED_LOGIC_OR_TOKEN      : (20 ,20 ), # a || b

    # Bitwise AND / OR / XOR
    TT_AND_TOKEN                    : (70 ,70 ), # a & b
    TT_PIPE_TOKEN                   : (50 ,50 ), # a | b
    TT_XOR_TOKEN                    : (60 ,60 ), # a ^ b

    # Assignment
    TT_EQUAL_TOKEN                  : (10 ,10 ), # a = b
    TT_COMBINED_ADD_ASSIGN_TOKEN    : (10 ,10 ), # a += b
    TT_COMBINED_SUB_ASSIGN_TOKEN    : (10 ,10 ), # a -= b
    TT_COMBINED_MUL_ASSIGN_TOKEN    : (10 ,10 ), # a *= b
    TT_COMBINED_DIV_ASSIGN_TOKEN    : (10 ,10 ), # a /= b
    STMT_TYPE                       : (0  ,9 ), # i8 (a)

    # Unary increment/decrement (prefix)
    TT_COMBINED_INC_TOKEN           : (90 ,90 ), # ++a
    TT_COMBINED_DEC_TOKEN           : (90 ,90 ), # --a


    # Modulus
    TT_MOD_TOKEN                    : (60 ,60 ), # a % b

    # Shift
    TT_COMBINED_SHIFT_LEFT_TOKEN    : (55 ,55 ), # a << b
    TT_COMBINED_SHIFT_RIGHT_TOKEN   : (55 ,55 ), # a >> b

    # Bitwise assignment
    TT_COMBINED_XOR_ASSIGN_TOKEN    : (10, 10),# a ^= b
    TT_COMBINED_BIT_AND_TOKEN       : (10, 10),# a &= b
    TT_COMBINED_BIT_OR_ASSIGN_TOKEN : (10, 10), # a |= b

    # Power assignment
    TT_COMBINED_POW_ASSIGN_TOKEN    : (10, 10),    # a **= b

    # Logical assignment
    TT_COMBINED_LOGIC_OR_ASSIGN_TOKEN : (10, 10), # a ||= b

    # Index access
    STMT_SQUARE_PAREN               : (100,0 )   # a[b]                                 
    
}
CONF_KEYWORDS = {
    "if",
    "else",
    "elif",
    "do",
    "while",
    "for",
    "return",
    "break",
    "continue",
    "struct",
    "func",
    "const",
    "true",
    "false",
    "import",
}   

CONF_TOKEN_GROUPS = {
    "LOGIC_TOKENS" : [
        TT_COMBINED_AND_TOKEN,
        TT_COMBINED_LOGIC_OR_TOKEN,
        TT_NOT_TOKEN,
        TT_COMBINED_EQUAL_TOKEN,
        TT_COMBINED_NOT_EQUAL_TOKEN,
        TT_COMBINED_GREATER_EQUAL_TOKEN,
        TT_COMBINED_LESS_EQUAL_TOKEN,
        TT_GREATER_TOKEN ,
        TT_LESS_TOKEN 
    ],
    "MATH_TOKENS":[
        TT_SUB_TOKEN ,
        TT_ADD_TOKEN,
        TT_ASTERISK_TOKEN ,
        TT_DIV_TOKEN,
        TT_MOD_TOKEN ,
        TT_COMBINED_INT_DIVISION_TOKEN,
        TT_COMBINED_POW_TOKEN ,
        TT_XOR_TOKEN  ,
        TT_PIPE_TOKEN  ,
        TT_AND_TOKEN,
        ],

    "BIT_SHIFT_TOKENS":[
        TT_COMBINED_SHIFT_LEFT_TOKEN,
        TT_COMBINED_SHIFT_RIGHT_TOKEN
    ],

    "UNARY_TOKENS":[
        TT_NOT_TOKEN,
        TT_TILDE_TOKEN,
        TT_SUB_TOKEN,
        TT_COMBINED_INC_TOKEN,
        TT_COMBINED_DEC_TOKEN
    ],
    
}
