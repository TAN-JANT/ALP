from all.lexer.lexer import Lexer
from all.common.token_types import TOKEN
from all.common import token_types
from all.parser.parser import Parser
from rich import pretty
from colorama import Fore
from sys import argv



def main():
    file = argv[1]
    
    lexer = Lexer()
    tokens = lexer.lex_src(file)
    pretty.pprint(tokens)
    print(Fore.GREEN + "Lexing completed successfully." + Fore.RESET)
    parser = Parser()
    parsed_data = parser.parse(tokens)
    pretty.pprint(parsed_data)
    print(Fore.GREEN + "Parsing completed successfully." + Fore.RESET)

if __name__ == "__main__":
    main()