from all.frontend.common.expressions import *
from .token_types import *
from .statements import *

# Higher number is higher binding ability
# First number is binding for left,
# second number is binding for right,
# Zero binding number means operator has not binding ability

CONF_BINDING_NUMBER = {

    TT_NOT_TOKEN                    : (EXPR_LOGICAL_NOT ,0  ,90 ), # !a
    TT_TILDE_TOKEN                  : (EXPR_BITWISE_NOT ,0  ,90 ), # ~a
    TT_SUB_TOKEN                    : (EXPR_NEGATE      ,50 ,90 ), # -a    a - b

    TT_ADD_TOKEN                    : (EXPR_ADD         ,50 ,50 ), # a + b
    TT_ASTERISK_TOKEN               : (EXPR_MUL         ,60 ,60 ), # a * b
    TT_DIV_TOKEN                    : (EXPR_DIV         ,60 ,60 ), # a / b
    TT_COMBINED_INT_DIVISION_TOKEN  : (EXPR_INT_DIV     ,60 ,60 ), # a // b
    TT_COMBINED_POW_TOKEN           : (EXPR_POW         ,90 ,90 ), # a ** b

        # Comparison
    TT_COMBINED_EQUAL_TOKEN         : (EXPR_EQUAL       ,40 ,40 ), # a == b
    TT_COMBINED_NOT_EQUAL_TOKEN     : (EXPR_NOT_EQUAL   ,40 ,40 ), # a != b
    TT_LESS_TOKEN                   : (EXPR_LESS        ,40 ,40 ), # a < b
    TT_COMBINED_LESS_EQUAL_TOKEN    : (EXPR_LESS_EQ     ,40 ,40 ), # a <= b
    TT_GREATER_TOKEN                : (EXPR_GREATER     ,40 ,40 ), # a > b
    TT_COMBINED_GREATER_EQUAL_TOKEN : (EXPR_GREATER_EQ  ,40 ,40 ), # a >= b

    # Logical AND / OR
    TT_COMBINED_LOGIC_AND_TOKEN     : (EXPR_LOGICAL_AND ,30 ,30 ), # a && b
    TT_COMBINED_LOGIC_OR_TOKEN      : (EXPR_LOGICAL_OR  ,20 ,20 ), # a || b

    # Bitwise AND / OR / XOR
    TT_AND_TOKEN                    : (EXPR_BIT_AND     ,70 ,70 ), # a & b
    TT_PIPE_TOKEN                   : (EXPR_BIT_OR      ,50 ,50 ), # a | b
    TT_XOR_TOKEN                    : (EXPR_BIT_XOR     ,60 ,60 ), # a ^ b

    # Assignment
    TT_EQUAL_TOKEN                  : (EXPR_ASSIGN      ,10 ,10 ), # a = b
    TT_COMBINED_ADD_ASSIGN_TOKEN    : (EXPR_ADD_ASSIGN  ,10 ,10 ), # a += b
    TT_COMBINED_SUB_ASSIGN_TOKEN    : (EXPR_SUB_ASSIGN  ,10 ,10 ), # a -= b
    TT_COMBINED_MUL_ASSIGN_TOKEN    : (EXPR_MUL_ASSIGN  ,10 ,10 ), # a *= b
    TT_COMBINED_DIV_ASSIGN_TOKEN    : (EXPR_DIV_ASSIGN  ,10 ,10 ), # a /= b

    # Unary increment/decrement (prefix)
    TT_COMBINED_INC_TOKEN           : (EXPR_INC         ,90, 90),  # ++a
    TT_COMBINED_DEC_TOKEN           : (EXPR_DEC         ,90, 90),  # --a


    # Modulus
    TT_MOD_TOKEN                    : (EXPR_MOD, 60, 60),  # a % b

    # Shift
    TT_COMBINED_SHIFT_LEFT_TOKEN    : (EXPR_SHIFT_LEFT, 55, 55),   # a << b
    TT_COMBINED_SHIFT_RIGHT_TOKEN   : (EXPR_SHIFT_RIGHT, 55, 55),  # a >> b

    # Bitwise assignment
    TT_COMBINED_XOR_ASSIGN_TOKEN    : (EXPR_BIT_XOR_ASSIGN, 10, 10),# a ^= b
    TT_COMBINED_BIT_AND_TOKEN       : (EXPR_BIT_AND_ASSIGN, 10, 10),# a &= b
    TT_COMBINED_BIT_OR_ASSIGN_TOKEN : (EXPR_BIT_OR_ASSIGN, 10, 10), # a |= b

    # Power assignment
    TT_COMBINED_POW_ASSIGN_TOKEN    : (EXPR_POW_ASSIGN, 10, 10),    # a **= b

    # Logical assignment
    TT_COMBINED_LOGIC_OR_ASSIGN_TOKEN : (EXPR_LOGIC_OR_ASSIGN, 10, 10), # a ||= b


}