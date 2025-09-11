# type: ignore
from ..common import expressions, statements, parser_conf 
from ..common import token_types
from . import errors
from ..lexer.lexer import Lexer


class Parser:
    def __init__(self):
        pass

    def parse(self, tokens: list[dict]):
        self.parsed_data = tokens.copy()
        self.struct_list = []
        self.functions = {}
        # Include dosyalarını çözüyoruz
        self.structs = {}
        self.info, self.parsed_data = self.__parse_include(
            self.parsed_data.copy(),
            [
                self.parsed_data[0]["working_directory"]
                + self.parsed_data[0]["file_name"]
            ],
        )
        # Parantez ve süslü parantez bloklarını ayrıştırıyoruz
        self.__separate_comments(self.parsed_data)
        self.parsed_data = self.__parse_dots(self.parsed_data.copy())
        self.parsed_data = self.__parse_bodies()[1]

        self.parsed_data = self.__parse_types(self.parsed_data)
        # struct ayrıştırması kapalı, gerekirse aç
        self.parsed_data = self.__parse_struct(self.parsed_data.copy())
        self.__struct_cycle()
        self.parsed_data = self.__parse_functions(self.parsed_data.copy())
        self.parsed_data = self.__parse_assembly_block(self.parsed_data.copy())
        self.parsed_data = self.__parse_if_else_elif(
            self.parsed_data.copy(), in_func=False
        )
        self.parsed_data = self.__parse_while_for(
            self.parsed_data.copy(), in_func=False
        )
        self.parsed_data = self.__combine_operators(self.parsed_data.copy())
        self.parsed_data = self.__parse_declaration(self.parsed_data.copy())
        self.parsed_data = self.__parse_expr(self.parsed_data.copy())
        return self.parsed_data

    def __separate_comments(self, src: list[dict]):
        position = 0
        comment = False
        token = None
        while position < len(src):
            token = src[position]
            if (
                token["type"] == token_types.TT_DIV_TOKEN
                and (position + 1) < len(src)
                and src[position + 1]["type"] == token_types.TT_ASTERISK_TOKEN
            ):
                comment = True

            if (
                token["type"] == token_types.TT_ASTERISK_TOKEN
                and (position + 1) < len(src)
                and src[position + 1]["type"] == token_types.TT_DIV_TOKEN
            ):
                src.pop(position)
                src.pop(position)
                if not comment:
                    raise errors.Unparseable_comment_Error(
                        token["line"], token["column"], token["file"]
                    )
                comment = False
                src.append(
                    {
                        "type": token_types.TT_NEWLINE_TOKEN,
                        "line": token["line"],
                        "column": token["column"],
                        "file": token["file"],
                    }
                )

            if comment:
                src.pop(position)
            else:
                position += 1

        if comment:
            raise errors.Unparseable_comment_Error(
                token["line"], token["column"], token["file"]
            )

    def __parse_include(self, src: list[dict], includeds=[]):
        body = []
        position = 0
        info = src.pop(0)
        while position < len(src):
            token = src[position]

            if (
                token["type"] == token_types.TT_IDENTIFIER_TOKEN
                and token["value"] == "include"
            ):
                if position == len(src) - 1:
                    raise errors.Unparseable_include_Error(token.line, token.column)
                position += 1
                if src[position]["type"] != token_types.TT_STRING_TOKEN:
                    raise errors.Unparseable_include_Error(token.line, token.column)
                include_file = info["working_directory"] + src[position]["value"]
                if include_file not in includeds:
                    includeds.append(include_file)
                    included_tokens = self.__parse_include(
                        Lexer().lex_src(include_file), includeds
                    )[1]
                    body.extend(included_tokens)
                position += 1
                continue

            body.append(token)
            position += 1

        return [info, body]

    def __parse_bodies(self, opened=False, position=0):
        body = []

        while position < len(self.parsed_data):
            token = self.parsed_data[position]

            if token["type"] == token_types.TT_LEFT_PAREN_TOKEN:
                opened = True
                position += 1
                position, sub_body = self.__parse_bodies(opened, position)
                body.append(
                    {
                        "type": statements.STMT_ROUND_PAREN,
                        "file": token["file"],
                        "line": token["line"],
                        "column": token["column"],
                        "body": sub_body,
                    }
                )
                continue

            if token["type"] == token_types.TT_LEFT_SQUARE_PAREN_TOKEN:
                opened = True
                position += 1
                position, sub_body = self.__parse_bodies(opened, position)
                body.append(
                    {
                        "type": statements.STMT_SQUARE_PAREN,
                        "file": token["file"],
                        "line": token["line"],
                        "column": token["column"],
                        "body": sub_body,
                    }
                )
                continue

            if token["type"] == token_types.TT_LEFT_BRACE_TOKEN:
                opened = True
                position += 1
                position, sub_body = self.__parse_bodies(opened, position)
                body.append(
                    {
                        "type": statements.STMT_BRACE,
                        "file": token["file"],
                        "line": token["line"],
                        "column": token["column"],
                        "body": sub_body,
                    }
                )
                continue

            if token["type"] in [
                token_types.TT_RIGHT_PAREN_TOKEN,
                token_types.TT_RIGHT_SQUARE_PAREN_TOKEN,
                token_types.TT_RIGHT_BRACE_TOKEN,
            ]:
                if not opened:
                    raise errors.Unmatched_Parenthesis_Error(
                        token["line"], token["column"], token["file"]
                    )
                position += 1
                break

            position += 1
            body.append(token)

        return [position, body]
 
    def __parse_struct(self, src: list[dict], global_scope=True):
        position = 0
        body = []

        while position < len(src):
            token = src[position]

            if (
                token["type"] == token_types.TT_IDENTIFIER_TOKEN
                and token["value"] == "struct"
            ):
                if not global_scope:
                    raise errors.Non_Globalscope_Struct_Error(
                        token["line"], token["column"], token["file"]
                    )
                position += 1

                if (
                    position >= len(src)
                    or src[position]["type"] != statements.STMT_TYPE
                ):
                    raise errors.Unparseable_struct_Error(
                        token["line"], token["column"], token["file"]
                    )

                struct_name = src[position]["value"]
                position += 1

                if position >= len(src) or (
                    src[position]["type"] != statements.STMT_BRACE
                    and src[position]["type"] != token_types.TT_NEWLINE_TOKEN
                ):
                    raise errors.Unparseable_struct_Error(
                        token["line"], token["column"], token["file"]
                    )

                if src[position]["type"] == statements.STMT_BRACE:
                    struct_body = src[position]

                    _ = 0
                    fields = {
                        "type": statements.STMT_STRUCT_FIELD,
                        "file": struct_body["file"],
                        "line": struct_body["line"],
                        "column": struct_body["column"],
                        "fields": [],
                    }
                    if struct_body["body"][_]["type"] == token_types.TT_NEWLINE_TOKEN:
                        _ += 1
                    self.structs[struct_name] = []
                    while _ < len(struct_body["body"]):

                        t = struct_body["body"][_]

                        if t["type"] != statements.STMT_TYPE:
                            raise errors.Unparseable_struct_Error(
                                token["line"], token["column"], token["file"]
                            )

                        _ += 1
                        fields["fields"].append(
                            {"type": t, "name": struct_body["body"][_]["value"]}
                        )
                        if t["type"] in self.struct_list:
                            self.structs[struct_name].append(t)
                        _ += 1
                        t = struct_body["body"][_]
                        if t["type"] != token_types.TT_NEWLINE_TOKEN:
                            raise errors.Unparseable_struct_Error(
                                t["line"], t["column"], t["file"]
                            )
                        _ += 1

                    position += 1
                    body.append(
                        {
                            "type": statements.STMT_STRUCT,
                            "file": struct_body["file"],
                            "line": struct_body["line"],
                            "column": struct_body["column"],
                            "name": struct_name,
                            "body": fields,
                        }
                    )

                elif src[position]["type"] == token_types.TT_NEWLINE_TOKEN:
                    position += 1
                    continue

                continue

            if hasattr(token, "body") and isinstance(token["body"], list):
                token["body"] = self.__parse_struct(token["body"], False)
                body.append(token)
                position += 1
                continue

            body.append(token)
            position += 1

        return body

    def __struct_cycle(self, colored=None, current=None):
        if colored is None:
            colored = []

        if current is None:
            for s in self.structs:
                colored = []
                colored.append(s)

                self.__struct_cycle(colored, self.structs[s])
        else:
            for s in current:
                if s["type"] in colored:
                    raise errors.Struct_Cycle_Error(s["line"], s["column"], s["file"])
                colored.append(s["type"])

                self.__struct_cycle(colored, self.structs[s["type"]])

    def __parse_types(self, src: list[dict], position=0, type_list=None):
        if type_list is None:
            type_list = ["i8", "i16", "i32", "i64","u8", "u16", "u32", "u64", "float", "double", "array", "void"]

        body = []

        while position < len(src):
            token = src[position]

            # Yeni struct tipi tanımı
            if (
                token["type"] == token_types.TT_IDENTIFIER_TOKEN
                and token["value"] == "struct"
            ):
                # Yeni struct tipi type_list'a ekle
                if (
                    position + 1 < len(src)
                    and src[position + 1]["type"] == token_types.TT_IDENTIFIER_TOKEN
                ):
                    type_list.append(src[position + 1]["value"])
                    self.struct_list.append(src[position + 1]["value"])
                body.append(token)
                if position + 1 < len(src):
                    body.append(
                        {
                            "type": statements.STMT_TYPE,
                            "file": token["file"],
                            "line": src[position + 1]["line"],
                            "column": src[position + 1]["column"],
                            "value": src[position + 1]["value"],
                            "subtype": [],
                        }
                    )
                    position += 2
                    continue

            # Eğer bu bir type token'ıysa
            if (
                token["type"] == token_types.TT_IDENTIFIER_TOKEN
                and token["value"] in type_list
            ):
                statement = {
                    "type": statements.STMT_TYPE,
                    "file": token["file"],
                    "line": token["line"],
                    "column": token["column"],
                    "value": token["value"],
                    "subtype": [],
                }

                position += 1

                # Jenerik tip kontrolü < ... >
                if (
                    position < len(src)
                    and src[position]["type"] == token_types.TT_LESS_TOKEN
                ):
                    position += 1
                    subtype_tokens = []
                    bracket_depth = 1

                    while position < len(src) and bracket_depth > 0:
                        inner_token = src[position]

                        if inner_token["type"] == token_types.TT_LESS_TOKEN:
                            bracket_depth += 1
                        elif inner_token["type"] == token_types.TT_GREATER_TOKEN:
                            bracket_depth -= 1
                            if bracket_depth == 0:
                                position += 1
                                break

                        subtype_tokens.append(inner_token)
                        position += 1

                    # subtype_tokens'u virgül bazında bölüp parse et
                    subtypes = []
                    current = []
                    for tok in subtype_tokens:
                        if tok["type"] == token_types.TT_COMMA_TOKEN:
                            if current:
                                parsed = self.__parse_types(current)
                                if len(parsed) == 1:
                                    subtypes.append(parsed[0])
                                else:
                                    subtypes.append(parsed)
                                current = []
                        else:
                            current.append(tok)
                    if current:
                        parsed = self.__parse_types(current)
                        if len(parsed) == 1:
                            subtypes.append(parsed[0])
                        else:
                            subtypes.append(parsed)

                    statement["subtype"] = subtypes

                # Pointer tipi kontrolleri *
                while (
                    position < len(src)
                    and src[position]["type"] == token_types.TT_ASTERISK_TOKEN
                ):
                    position += 1
                    statement = {
                        "type": statements.STMT_TYPE,
                        "file": token["file"],
                        "line": token["line"],
                        "column": token["column"],
                        "value": "@ptr",
                        "subtype": [statement],
                    }

                body.append(statement)
                continue

            # Eğer body'li statement'sa (parantez, köşeli parantez, süslü parantez)
            if "body" in token.keys() and isinstance(token["body"], list):
                token["body"] = self.__parse_types(token["body"], 0, type_list)
                body.append(token)
                position += 1
                continue

            # Diğer tokenlar
            body.append(token)
            position += 1

        return body

    def __parse_functions(self, src: list[dict]):
        body = []
        position = 0
        extern = False
        while position < len(src):
            token = src[position]
            if (
                token["type"] == token_types.TT_IDENTIFIER_TOKEN
                and token["value"] == "func"
            ):
                position += 1
                return_type = src[position]
                if return_type["type"] != statements.STMT_TYPE:
                    raise errors.Unparseable_function_Error(
                        token["line"], token["column"], token["file"]
                    )
                position += 1
                func_name = src[position]
                if func_name["type"] != token_types.TT_IDENTIFIER_TOKEN:
                    raise errors.Unparseable_function_Error(
                        token["line"], token["column"], token["file"]
                    )
                func_name = func_name["value"]
                position += 1
                func_params = src[position]
                if func_params["type"] != statements.STMT_ROUND_PAREN:
                    raise errors.Unparseable_function_Error(
                        token["line"], token["column"], token["file"]
                    )
                _ = []
                i = 0
                while i < len(func_params["body"]):
                    if func_params["body"][i]["type"] != statements.STMT_TYPE:
                        raise errors.Unparseable_function_Error(
                            func_params["body"][i]["line"],
                            func_params["body"][i]["column"],
                            func_params["body"][i]["file"],
                        )
                    _type = func_params["body"][i]
                    i += 1
                    if (
                        func_params["body"][i]["type"]
                        != token_types.TT_IDENTIFIER_TOKEN
                    ):
                        raise errors.Unparseable_function_Error(
                            func_params["body"][i]["line"],
                            func_params["body"][i]["column"],
                            func_params["body"][i]["file"],
                        )
                    _name = func_params["body"][i]
                    i += 1
                    _.append(
                        {
                            "type": statements.STMT_FUNC_PARAM,
                            "param_name": _name,
                            "param_type": _type,
                        }
                    )
                    if i == len(func_params["body"]):
                        break
                    elif func_params["body"][i]["type"] != token_types.TT_COMMA_TOKEN:
                        raise errors.Unparseable_function_Error(
                            func_params["body"][i]["line"],
                            func_params["body"][i]["column"],
                            func_params["body"][i]["file"],
                        )
                    i += 1

                func_params = _.copy()
                position += 1
                while (
                    position < len(src)
                    and src[position]["type"] == token_types.TT_NEWLINE_TOKEN
                ):
                    position += 1
                func_body = src[position]
                if (
                    func_body["type"] != statements.STMT_BRACE
                    and func_body["type"] != token_types.TT_SEMI_TOKEN
                ):
                    raise errors.Unparseable_function_Error(
                        token["line"], token["column"], token["file"]
                    )

                if func_body["type"] != token_types.TT_SEMI_TOKEN:
                    func_body = func_body["body"]
                    body.append(
                        {
                            "type": statements.STMT_FUNCTION,
                            "file": token["file"],
                            "line": token["line"],
                            "column": token["column"],
                            "name": func_name,
                            "return_type": return_type,
                            "params": func_params,
                            "body": func_body,
                            "extern": extern,
                        }
                    )

                self.functions[func_name] = {
                    "return_type": return_type,
                    "func_params": func_params,
                }

                extern = False
                position += 1
                continue

            if (
                token["type"] == token_types.TT_IDENTIFIER_TOKEN
                and token["value"] == "extern"
            ):
                extern = True
                position += 1
                continue
            body.append(token)
            position += 1

        return body

    def __parse_assembly_block(self, src: list[dict]):

        position = 0
        while position < len(src):
            token = src[position]
            if token["type"] == statements.STMT_FUNCTION:
                _ = 0
                if "body" in token and isinstance(token["body"], list):
                    while _ < len(token["body"]):

                        if (
                            token["body"][_]["type"] == token_types.TT_IDENTIFIER_TOKEN
                            and token["body"][_]["value"] == "ASM"
                        ):
                            token["body"].pop(_)
                            if token["body"][_]["type"] == statements.STMT_BRACE:
                                token["body"][_] = {
                                    "type": statements.STMT_ASSEMBLY_BLOCK,
                                    "file": token["body"][_]["file"],
                                    "line": token["body"][_]["line"],
                                    "column": token["body"][_]["column"],
                                    "body": token["body"][_]["body"],
                                }
                        _ += 1

            position += 1
        return src

    def __parse_if_else_elif(self, src: list[dict], in_func: bool = False):
        position = 0
        current_if = None
        while position < len(src):
            token = src[position]
            if (
                token["type"] == token_types.TT_IDENTIFIER_TOKEN
                and token["value"] == "if"
            ):
                if not in_func:
                    raise errors.Unparseable_if_block_Error(
                        token["line"], token["column"], token["file"]
                    )

                src.pop(position)
                if (
                    position >= len(src)
                    or src[position]["type"] != statements.STMT_ROUND_PAREN
                ):
                    raise errors.Unparseable_if_block_Error(
                        token["line"], token["column"], token["file"]
                    )
                condition = src.pop(position)["body"]
                if (
                    position >= len(src)
                    or src[position]["type"] != statements.STMT_BRACE
                ):
                    raise errors.Unparseable_if_block_Error(
                        token["line"], token["column"], token["file"]
                    )
                body = self.__parse_if_else_elif(
                    src.pop(position)["body"], in_func=in_func
                )
                current_if = {
                    "type": statements.STMT_IF_BLOCK,
                    "condition": condition,
                    "body": body,
                    "else": None,
                }
                src.insert(position, current_if)
                continue

            if (
                token["type"] == token_types.TT_IDENTIFIER_TOKEN
                and token["value"] == "elif"
            ):
                if not in_func:
                    raise errors.Unparseable_if_block_Error(
                        token["line"], token["column"], token["file"]
                    )

                src.pop(position)
                if (
                    position >= len(src)
                    or src[position]["type"] != statements.STMT_ROUND_PAREN
                ):
                    raise errors.Unparseable_if_block_Error(
                        token["line"], token["column"], token["file"]
                    )
                condition = src.pop(position)["body"]
                if (
                    position >= len(src)
                    or src[position]["type"] != statements.STMT_BRACE
                ):
                    raise errors.Unparseable_if_block_Error(
                        token["line"], token["column"], token["file"]
                    )
                body = self.__parse_if_else_elif(
                    src.pop(position)["body"], in_func=in_func
                )
                if current_if is None:
                    raise errors.Unparseable_if_block_Error(
                        token["line"], token["column"], token["file"]
                    )
                current_if["else"] = {
                    "type": statements.STMT_ELIF_BLOCK,
                    "condition": condition,
                    "body": body,
                    "else": None,
                }
                current_if = current_if["else"]
                continue

            if (
                token["type"] == token_types.TT_IDENTIFIER_TOKEN
                and token["value"] == "else"
            ):
                if not in_func:
                    raise errors.Unparseable_if_block_Error(
                        token["line"], token["column"], token["file"]
                    )

                src.pop(position)
                if (
                    position >= len(src)
                    or src[position]["type"] != statements.STMT_BRACE
                ):
                    raise errors.Unparseable_if_block_Error(
                        token["line"], token["column"], token["file"]
                    )
                body = self.__parse_if_else_elif(
                    src.pop(position)["body"], in_func=in_func
                )
                if current_if is None:
                    raise errors.Unparseable_if_block_Error(
                        token["line"], token["column"], token["file"]
                    )
                current_if["else"] = {"type": statements.STMT_ELSE_BLOCK, "body": body}
                current_if = None

                continue

            if token["type"] == statements.STMT_FUNCTION:
                if in_func:
                    raise errors.Unparseable_function_Error(
                        token["line"], token["column"], token["file"]
                    )
                token["body"] = self.__parse_if_else_elif(token["body"], in_func=True)
                position += 1
                continue

            if token["type"] == statements.STMT_BRACE:
                if not in_func:
                    raise errors.Unparseable_if_block_Error(
                        token["line"], token["column"], token["file"]
                    )
                token["body"] = self.__parse_if_else_elif(
                    token["body"].copy(), in_func=in_func
                )
                position += 1
                continue
            position += 1

        return src

    def __parse_while_for(self, src: list[dict], in_func: bool = False):
        position = 0
        while position < len(src):
            token = src[position]
            if (
                token["type"] == token_types.TT_IDENTIFIER_TOKEN
                and token["value"] == "while"
            ):
                if not in_func:
                    raise errors.Unparseable_while_block_Error(
                        token["line"], token["column"], token["file"]
                    )

                src.pop(position)
                if (
                    position >= len(src)
                    or src[position]["type"] != statements.STMT_ROUND_PAREN
                ):
                    raise errors.Unparseable_while_block_Error(
                        token["line"], token["column"], token["file"]
                    )
                condition = src.pop(position)["body"]
                if (
                    position >= len(src)
                    or src[position]["type"] != statements.STMT_BRACE
                ):
                    raise errors.Unparseable_while_block_Error(
                        token["line"], token["column"], token["file"]
                    )
                body = self.__parse_while_for(
                    src.pop(position)["body"], in_func=in_func
                )
                src.insert(
                    position,
                    {
                        "type": statements.STMT_WHILE_BLOCK,
                        "condition": condition,
                        "body": body,
                    },
                )
                continue

            if (
                token["type"] == token_types.TT_IDENTIFIER_TOKEN
                and token["value"] == "do"
                and position + 1 < len(src)
                and src[position + 1]["type"] == token_types.TT_IDENTIFIER_TOKEN
                and src[position + 1]["value"] == "while"
            ):
                if not in_func:
                    raise errors.Unparseable_while_block_Error(
                        token["line"], token["column"], token["file"]
                    )

                src.pop(position)
                src.pop(position)
                if (
                    position >= len(src)
                    or src[position]["type"] != statements.STMT_ROUND_PAREN
                ):
                    raise errors.Unparseable_while_block_Error(
                        token["line"], token["column"], token["file"]
                    )
                condition = src.pop(position)["body"]
                if (
                    position >= len(src)
                    or src[position]["type"] != statements.STMT_BRACE
                ):
                    raise errors.Unparseable_while_block_Error(
                        token["line"], token["column"], token["file"]
                    )
                body = self.__parse_if_else_elif(
                    src.pop(position)["body"], in_func=in_func
                )
                src.insert(
                    position,
                    {
                        "type": statements.STMT_DO_WHILE_BLOCK,
                        "condition": condition,
                        "body": body,
                    },
                )
                continue

            if (
                token["type"] == token_types.TT_IDENTIFIER_TOKEN
                and token["value"] == "for"
            ):
                if not in_func:
                    raise errors.Unparseable_for_block_Error(
                        token["line"], token["column"], token["file"]
                    )

                src.pop(position)
                if (
                    position >= len(src)
                    or src[position]["type"] != statements.STMT_ROUND_PAREN
                ):
                    raise errors.Unparseable_for_block_Error(
                        token["line"], token["column"], token["file"]
                    )
                condition = src.pop(position)["body"]
                if (
                    position >= len(src)
                    or src[position]["type"] != statements.STMT_BRACE
                ):
                    raise errors.Unparseable_for_block_Error(
                        token["line"], token["column"], token["file"]
                    )
                body = self.__parse_if_else_elif(
                    src.pop(position)["body"], in_func=in_func
                )
                src.insert(
                    position,
                    {
                        "type": statements.STMT_FOR_BLOCK,
                        "condition": condition,
                        "body": body,
                    },
                )
                continue

            if token["type"] == statements.STMT_FUNCTION:
                if in_func:
                    raise errors.Unparseable_function_Error(
                        token["line"], token["column"], token["file"]
                    )
                token["body"] = self.__parse_while_for(token["body"], in_func=True)
                position += 1
                continue

            if token["type"] in [
                statements.STMT_IF_BLOCK,
                statements.STMT_ELSE_BLOCK,
                statements.STMT_ELIF_BLOCK,
            ]:
                if not in_func:
                    raise errors.Unparseable_if_block_Error(
                        token["line"], token["column"], token["file"]
                    )
                token["body"] = self.__parse_while_for(token["body"], in_func=in_func)
                position += 1
                continue

            position += 1

        return src

    def __combine_operators(self, src: list[dict]):
        position = 0

        combine_dict = {
            # +, ++, +=
            token_types.TT_ADD_TOKEN: {
                None: token_types.TT_ADD_TOKEN,
                token_types.TT_ADD_TOKEN: token_types.TT_COMBINED_INC_TOKEN,  # ++
                token_types.TT_EQUAL_TOKEN: token_types.TT_COMBINED_ADD_ASSIGN_TOKEN,  # +=
            },
            # -, --, -=
            token_types.TT_SUB_TOKEN: {
                None: token_types.TT_SUB_TOKEN,
                token_types.TT_SUB_TOKEN: token_types.TT_COMBINED_DEC_TOKEN,  # --
                token_types.TT_EQUAL_TOKEN: token_types.TT_COMBINED_SUB_ASSIGN_TOKEN,  # -=
            },
            # !, !=
            token_types.TT_NOT_TOKEN: {
                None: token_types.TT_NOT_TOKEN,
                token_types.TT_EQUAL_TOKEN: token_types.TT_COMBINED_NOT_EQUAL_TOKEN,  # !=
            },
            # =, ==
            token_types.TT_EQUAL_TOKEN: {
                None: token_types.TT_EQUAL_TOKEN,
                token_types.TT_EQUAL_TOKEN: token_types.TT_COMBINED_EQUAL_TOKEN,  # ==
            },
            # <, <=, <<, <<=
            token_types.TT_LESS_TOKEN: {
                None: token_types.TT_LESS_TOKEN,
                token_types.TT_EQUAL_TOKEN: token_types.TT_COMBINED_LESS_EQUAL_TOKEN,  # <=
                token_types.TT_LESS_TOKEN: {
                    None: token_types.TT_COMBINED_SHIFT_LEFT_TOKEN,  # <<
                    token_types.TT_EQUAL_TOKEN: token_types.TT_COMBINED_SHIFT_LEFT_ASSIGN_TOKEN,  # <<=
                },
            },
            # >, >=, >>, >>=
            token_types.TT_GREATER_TOKEN: {
                None: token_types.TT_GREATER_TOKEN,
                token_types.TT_EQUAL_TOKEN: token_types.TT_COMBINED_GREATER_EQUAL_TOKEN,  # >=
                token_types.TT_GREATER_TOKEN: {
                    None: token_types.TT_COMBINED_SHIFT_RIGHT_TOKEN,  # >>
                    token_types.TT_EQUAL_TOKEN: token_types.TT_COMBINED_SHIFT_RIGHT_ASSIGN_TOKEN,  # >>=
                },
            },
            # &, &&, &=
            token_types.TT_AND_TOKEN: {
                None: token_types.TT_AND_TOKEN,
                token_types.TT_AND_TOKEN: token_types.TT_COMBINED_LOGIC_AND_TOKEN,  # &&
                token_types.TT_EQUAL_TOKEN: token_types.TT_COMBINED_AND_ASSIGN_TOKEN,  # &=
            },
            # |, ||, |=
            token_types.TT_PIPE_TOKEN: {
                None: token_types.TT_PIPE_TOKEN,
                token_types.TT_PIPE_TOKEN: token_types.TT_COMBINED_LOGIC_OR_TOKEN,  # ||
                token_types.TT_EQUAL_TOKEN: token_types.TT_COMBINED_BIT_OR_ASSIGN_TOKEN,  # |=
            },
            # ^, ^=
            token_types.TT_XOR_TOKEN: {
                None: token_types.TT_XOR_TOKEN,
                token_types.TT_EQUAL_TOKEN: token_types.TT_COMBINED_XOR_ASSIGN_TOKEN,  # ^=
            },
            # *, **, *=, **=
            token_types.TT_ASTERISK_TOKEN: {
                None: token_types.TT_ASTERISK_TOKEN,
                token_types.TT_ASTERISK_TOKEN: {
                    None: token_types.TT_COMBINED_POW_TOKEN,  # **
                    token_types.TT_EQUAL_TOKEN: token_types.TT_COMBINED_POW_ASSIGN_TOKEN,  # **=
                },
                token_types.TT_EQUAL_TOKEN: token_types.TT_COMBINED_MUL_ASSIGN_TOKEN,  # *=
            },
            # /, /=, //
            token_types.TT_DIV_TOKEN: {
                None: token_types.TT_DIV_TOKEN,
                token_types.TT_EQUAL_TOKEN: token_types.TT_COMBINED_DIV_ASSIGN_TOKEN,  # /=
                token_types.TT_DIV_TOKEN: token_types.TT_COMBINED_INT_DIVISION_TOKEN,  # //
            },
            # %, %=
            token_types.TT_MOD_TOKEN: {
                None: token_types.TT_MOD_TOKEN,
                token_types.TT_EQUAL_TOKEN: token_types.TT_COMBINED_MOD_ASSIGN_TOKEN,  # %=
            },
        }

        while position < len(src):
            token = src[position]
            current_combine_dict = combine_dict
            if token["type"] in current_combine_dict.keys():
                _ = token
                while 1:
                    if not _["type"] in current_combine_dict.keys():
                        src.insert(
                            position,
                            {
                                "type": current_combine_dict[None],
                                "file": token["file"],
                                "line": token["line"],
                                "column": token["column"],
                            },
                        )
                        break
                    current_combine_dict = current_combine_dict[_["type"]]
                    src.pop(position)
                    if isinstance(current_combine_dict, str):
                        src.insert(
                            position,
                            {
                                "type": current_combine_dict,
                                "file": token["file"],
                                "line": token["line"],
                                "column": token["column"],
                            },
                        )
                        break
                    if not position < len(src):
                        src.insert(
                            position,
                            {
                                "type": current_combine_dict[None],
                                "file": token["file"],
                                "line": token["line"],
                                "column": token["column"],
                            },
                        )
                        break
                    _ = src[position]
                current_combine_dict = combine_dict
                position += 1
                continue

            if "condition" in token.keys():
                token["condition"] = self.__combine_operators(token["condition"])
                

            if "body" in token.keys() and not (
                token["type"] in [statements.STMT_STRUCT]
            ):
                token["body"] = self.__combine_operators(token["body"])
                
            position += 1
        return src

    def __parse_dots(self, src: list[dict]):
        position = 0
        body = src.copy()
        while position < len(body):
            token = body[position]
            if token["type"] == token_types.TT_DOT_TOKEN:
                if position == 0 or position == len(body) - 1:
                    raise errors.Unparseable_dot_access_Error(
                        token["line"], token["column"], token["file"]
                    )

                body.pop(position)  # '.'
                left = body.pop(position - 1)
                right = body.pop(position - 1)
                position -= 1

                # float literal kontrolü
                if (
                    left["type"] == token_types.TT_INTEGER_TOKEN
                    and right["type"] == token_types.TT_INTEGER_TOKEN
                ):
                    float_val = float(left["value"] + "." + right["value"])
                    body.insert(
                        position,
                        {
                            "type": token_types.TT_FLOAT_TOKEN,
                            "value": float_val,
                            "line": left["line"],
                            "column": left["column"],
                            "file": token["file"],
                        },
                    )
                # dot access için identifier-identifier
                elif (
                    left["type"] == token_types.TT_IDENTIFIER_TOKEN
                    and right["type"] == token_types.TT_IDENTIFIER_TOKEN
                ):
                    path = [left["value"], right["value"]]
                    body.insert(
                        position - 2,
                        {
                            "type": statements.STMT_DOT_ACCESS,
                            "line": left["line"],
                            "column": left["column"],
                            "path": path,
                            "file": token["file"],
                        },
                    )

                elif (
                    left["type"] == statements.STMT_DOT_ACCESS
                    and right["type"] == token_types.TT_IDENTIFIER_TOKEN
                ):
                    left["path"].append(right["value"])
                continue

            if hasattr(token, "body") and isinstance(token["body"], list):
                token["body"] = self.__parse_dots(token["body"])
                position += 1
                continue

            position += 1
        return body

    def __parse_expr(self, src: list[dict]):
        # İlk geçiş: binding değerlerini ata ve recursive parse yap
        for token in src:
            token["binding"] = [0, 0]
            _ = parser_conf.CONF_BINDING_NUMBER.get(token["type"], None)
            if _ is not None:
                token["binding"][0] = _[0]  # left binding
                token["binding"][1] = _[1]  # right binding
                token["binded_left"] = None
                token["binded_right"] = None

            if "condition" in token:
                token["condition"] = self.__parse_expr(token["condition"])
            if "body" in token and token["type"] not in [statements.STMT_STRUCT, statements.STMT_ASSEMBLY_BLOCK]:
                token["body"] = self.__parse_expr(token["body"])

        # Binding önceliğine göre bağlama
        while True:
            trigger = False
            right   = None
            token   = None
            left    = None
            pos     = 0
            while True:
                right = src[pos] if pos < len(src) else None 

                if token is not None and token["binding"] == [0,0]:
                    left_p = 0 if left is None else left["binding"][1]
                    right_p = 0 if right is None else right["binding"][0]
                    if left_p == 0 and right_p == 0:
                        pos += 1
                        left = token
                        token = right
                        continue
                    if right_p > left_p:
                        right["binded_left"] = token
                        right["binding"][0] = 0
                        #src[pos] = right

                        src.pop(pos -1)
                        token = None
                        left = right
                        pos += 1
                        trigger = True
                        continue
                    if left is not None:
                        left["binded_right"] = token
                        left["binding"][1] = 0
                        #src[pos-2] = left

                        src.pop(pos-1)
                        token = None
                        left = right
                        pos += 1
                        trigger = True
                        continue
                    
                    
                    
                if right is None and left is None and token is None:
                    break
                
                left = token
                token = right
                pos += 1

            if not trigger:
                break
        return src

    def __parse_declaration(self,src:list[dict],global_scope=True) -> list[dict]:
        position = 0
       
        token = None
        while position < len(src):
            token = src[position]
            
            
            if (token["type"] == statements.STMT_TYPE ):
                if len(src) > position + 2 and src[position +1]["type"] == token_types.TT_IDENTIFIER_TOKEN and src[position +2]["type"] == token_types.TT_EQUAL_TOKEN:
                    token["type"] = statements.STMT_DECLARATION
                    token["variable"] = src[position +1]
                    token["global"]  = global_scope
                


            if ("body" in token.keys() and 
                token["type"] not in [statements.STMT_STRUCT, statements.STMT_ASSEMBLY_BLOCK]):

                token["body"] = self.__parse_declaration(token["body"],False)
                position += 1
                continue
                
            
            position += 1
            pass
        return src

    def __generate_data_type(self,src:list[dict])->list[dict]:
        position = 0
        while position < len(src):
            token = src[position]
            """
            if token["type"] == expressions.EXPR_CAST:
                token["data_type"] = token["body"][0]
            """
            
            if "condition" in token:
                token["condition"] = self.__generate_data_type(token["condition"])
            if "body" in token and token["type"] not in [statements.STMT_STRUCT, statements.STMT_ASSEMBLY_BLOCK]:
                token["body"] = self.__generate_data_type(token["body"])
                
        

    def __generate_ast(self,src:list[dict]) -> dict:
        ast = {
            "functions":{},
            "global_variables":{},
               }

        position = 0
        while position < len(src):
            token       = src[position]
            if token["type"] == token_types.TT_NEWLINE_TOKEN:
                position += 1
                continue
            expr_type   = parser_conf.CONF_BINDING_NUMBER.get(token["type"],None)
            
            
            position += 1

        return ast
        
        

