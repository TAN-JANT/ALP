from dataclasses import dataclass, field
from typing import List, Optional, Union


@dataclass
class Statement:
    file: str
    line: int
    column: int


@dataclass
class Round_Parenthesis_Statement(Statement):
    body: List[Statement] = field(default_factory=list)

    def __repr__(self):
        return f"Round_Parenthesis_Statement([{self.body}])"


@dataclass
class Square_Parenthesis_Statement(Statement):
    body: List[Statement] = field(default_factory=list)

    def __repr__(self):
        return f"Square_Parenthesis_Statement([{self.body}])"


@dataclass
class Brace_Statement(Statement):
    body: List[Statement] = field(default_factory=list)

    def __repr__(self):
        return f"Brace_Statement({self.body})"


@dataclass
class DOT_ACCESS_Statement(Statement):
    left: Statement
    right: Statement

    def __repr__(self):
        return f"DOT_ACCESS_Statement({self.left}.{self.right})"


@dataclass
class Type_Statement(Statement):
    type: str
    subtype: List['Type_Statement'] = field(default_factory=list)

    def __repr__(self):
        return f"Type_Statement({self.type}{self.subtype if self.subtype else ''})"


@dataclass
class Struct_Field_Statement(Statement):
    fields: List[Statement] = field(default_factory=list)

    def __repr__(self):
        return f"Struct_Field_Statement({self.fields})"


@dataclass
class Struct_Statement(Statement):
    name: str
    fields: Struct_Field_Statement

    def __repr__(self):
        return f"Struct_Statement({self.name},{self.fields})"
