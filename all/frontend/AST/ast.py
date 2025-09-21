class AST_Analyzer:
    def __init__(self, ast):
        self.ast = ast
        self.variables = set()
        self.functions = set()
        self.classes = set()
        
    def __generate_data_type(self,token:dict) -> dict:
        
            
        if token["type"] == token_types.TT_SUB_TOKEN:
            l = token.get("binded_left",None)
            r = token.get("binded_right",None)
            if l is not None and "data_type" not in l.keys():
                l = self.__generate_data_type(l)
            if r is not None and "data_type" not in r.keys():
                r = self.__generate_data_type(r)
            if l is None and r is not None:
                token["type"] = expressions.EXPR_NEGATE
                token["data_type"] = r["data_type"]
            elif l is None:
                pass#raise errors.
            return token