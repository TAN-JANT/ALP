from all.frontend import Lexer , Parser
from json import dumps
from colorama import Fore
from sys import argv
from rich import pretty

def main():
    file = argv[1]

    lexer = Lexer()
    tokens = lexer.lex_src(file)
    pretty.pprint(tokens)
    with open("tokens.json", "w") as f:
        f.write(dumps(tokens, indent=4))
    print(Fore.GREEN + "Lexing completed successfully." + Fore.RESET)
    parser = Parser()
    parsed_data = parser.parse(tokens)
    pretty.pprint(parsed_data)
    with open("parsed.json", "w") as f:
        f.write(dumps(parsed_data, indent=4))

    print(Fore.GREEN + "Parsing completed successfully." + Fore.RESET)

if __name__ == "__main__":
    main()