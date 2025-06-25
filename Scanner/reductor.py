from anytree import Node
from typing import List
from pathlib import Path

SKIP_NODES = frozenset({
    "Program", "StatementList", "Statement", "NonIfStmt", "VarDecl",
    "Type", "Expression", "AddExpr", "AddTail", "Term", "TermTail",
    "Factor", "RelationalTail", "Params", "ParamsTail", "Param",
    ";", "(", ")", "{", "}", "IfStmt", "IfStmtPrime", "",
})
SEMANTIC_TOKENS = frozenset({
    "if", "else", "for",
    "=", "+", "-", "*", "/", "%",
    "==", "!=", "<", "<=", ">", ">=",
    "vid", "img", "concat", "input", "print", "save"
})
LITERAL_TYPES = {"IDENTIFIER", "STRING", "NUMBER", "int", "float"}


def reduce_tree(node):
    label, *rest = node.name.split(maxsplit=1)
    rest = rest[0] if rest else ""

    # 1) Operadores semánticos (incluye if/for como nodos)
    if label in SEMANTIC_TOKENS:
        children = [reduce_tree(c) for c in node.children]
        children = [c for c in children if c]
        return Node(label, children=children)

    # 2) Literales e identificadores
    if "(" in node.name and ")" in node.name:
        typ, val = node.name.split("(", 1)
        val = val.rstrip(")")
        typ = typ.strip()
        if typ in LITERAL_TYPES:
            return Node(val.strip())

    # 3) Reducir hijos
    children = [reduce_tree(c) for c in node.children]
    children = [c for c in children if c]

    # 4) Si es un grupo donde el primer hijo es semántico, promoverlo
    if len(children) > 1 and children[0].name in SEMANTIC_TOKENS:
        op = children[0].name
        return Node(op, children=children[1:])

    # 5) Elevar único hijo
    if len(children) == 1:
        return children[0]

    # 6) Múltiples hijos no semánticos → grupo
    if children:
        return Node("group", children=children)


    return None
