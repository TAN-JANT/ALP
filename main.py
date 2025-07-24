from all.lexer.lexer import Lexer
from all.common.token_types import TOKEN
from all.common import token_types
from all.parser.parser import Parser
import pprint
from colorama import Fore
from sys import argv



def main():
    file = argv[1]
    
    lexer = Lexer()
    tokens = lexer.lex_src(file)
    pprint.pprint(tokens, indent=4)
    print(Fore.GREEN + "Lexing completed successfully." + Fore.RESET)
    parser = Parser()
    parsed_data = parser.parse(tokens)
    pprint.pprint(parsed_data,indent=4)
    print(Fore.GREEN + "Parsing completed successfully." + Fore.RESET)

if __name__ == "__main__":
    main()