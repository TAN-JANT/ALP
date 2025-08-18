# Unary expressions
EXPR_LOGICAL_NOT      = "EXPR_LOGICAL_NOT"      # !a
EXPR_BITWISE_NOT      = "EXPR_BITWISE_NOT"      # ~a
EXPR_NEGATE           = "EXPR_NEGATE"           # -a

# Arithmetic binary expressions
EXPR_ADD              = "EXPR_ADD"              # a + b
EXPR_SUB              = "EXPR_SUB"              # a - b
EXPR_MUL              = "EXPR_MUL"              # a * b
EXPR_DIV              = "EXPR_DIV"              # a / b
EXPR_INT_DIV          = "EXPR_INT_DIV"          # a // b
EXPR_MOD              = "EXPR_MOD"              # a % b
EXPR_POW              = "EXPR_POW"              # a ** b

# Comparison expressions
EXPR_EQUAL            = "EXPR_EQUAL"            # a == b
EXPR_NOT_EQUAL        = "EXPR_NOT_EQUAL"        # a != b
EXPR_LESS             = "EXPR_LESS"             # a < b
EXPR_GREATER          = "EXPR_GREATER"          # a > b
EXPR_LESS_EQ          = "EXPR_LESS_EQ"          # a <= b
EXPR_GREATER_EQ       = "EXPR_GREATER_EQ"       # a >= b

# Logical binary expressions
EXPR_LOGICAL_AND      = "EXPR_LOGICAL_AND"      # a && b
EXPR_LOGICAL_OR       = "EXPR_LOGICAL_OR"       # a || b

# Bitwise binary expressions
EXPR_BIT_AND          = "EXPR_BIT_AND"          # a & b
EXPR_BIT_OR           = "EXPR_BIT_OR"           # a | b
EXPR_BIT_XOR          = "EXPR_BIT_XOR"          # a ^ b
EXPR_SHIFT_LEFT       = "EXPR_SHIFT_LEFT"       # a << b
EXPR_SHIFT_RIGHT      = "EXPR_SHIFT_RIGHT"      # a >> b

# Assignment expressions
EXPR_ASSIGN           = "EXPR_ASSIGN"           # a = b
EXPR_ADD_ASSIGN       = "EXPR_ADD_ASSIGN"       # a += b
EXPR_SUB_ASSIGN       = "EXPR_SUB_ASSIGN"       # a -= b
EXPR_MUL_ASSIGN       = "EXPR_MUL_ASSIGN"       # a *= b
EXPR_DIV_ASSIGN       = "EXPR_DIV_ASSIGN"       # a /= b
EXPR_MOD_ASSIGN       = "EXPR_MOD_ASSIGN"       # a %= b
EXPR_POW_ASSIGN       = "EXPR_POW_ASSIGN"       # a **= b
EXPR_AND_ASSIGN       = "EXPR_AND_ASSIGN"       # a &= b
EXPR_OR_ASSIGN        = "EXPR_OR_ASSIGN"        # a |= b
EXPR_XOR_ASSIGN       = "EXPR_XOR_ASSIGN"       # a ^= b
EXPR_SHIFT_LEFT_ASSIGN= "EXPR_SHIFT_LEFT_ASSIGN"# a <<= b
EXPR_SHIFT_RIGHT_ASSIGN="EXPR_SHIFT_RIGHT_ASSIGN"# a >>= b
EXPR_LOGIC_OR_ASSIGN  = "EXPR_LOGIC_OR_ASSIGN"  # a ||= b

# Primary expressions
EXPR_NUMBER           = "EXPR_NUMBER"           # 123, 3.14
EXPR_STRING           = "EXPR_STRING"           # "hello"
EXPR_VARIABLE         = "EXPR_VARIABLE"         # x, y
EXPR_CALL             = "EXPR_CALL"             # foo()
EXPR_MEMBER           = "EXPR_MEMBER"           # obj.field
EXPR_ARRAY            = "EXPR_ARRAY"            # [1,2,3]
EXPR_STRUCT           = "EXPR_STRUCT"           # struct instance
