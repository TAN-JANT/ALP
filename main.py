from all.lexer.lexer import Lexer
from all.lexer.token_types import TOKEN
from all.lexer import token_types
import pprint

a = Lexer()
pprint.pprint(a.lex_src("""
    @include '''path/to/file.all'''
    @struct person {
        @i8 age
        @i8 *name
    }

    @export @func @i8 main(){
        @i32 x = 10
        @i32 y = 20
        @i32 z = x + y
        @return 0
    }

    @func @void print(@i8 *string, @i16 *len){
        @ASM {
            @mov %rax,%rsi
            @mov %rsi,%rdx
            @mov %rdi,1
            @mov %rdx,%rax
            @mov %rax,1
            @syscall
        }
        @return
    }
"""))
