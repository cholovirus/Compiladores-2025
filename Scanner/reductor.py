from anytree import Node

def reduce_tree(node):
    skip_nodes = {
        "Program", "StatementList", "Statement", "NonIfStmt", "VarDecl",
        "Type", "Expression", "AddExpr", "AddTail", "Term", "TermTail",
        "Factor", "RelationalTail", "Params", "ParamsTail", "Param",
        ";", "(", ")", "{", "}"
    }

    def is_leaf_semantic(node):
        if '(' in node.name:
            value, typ = node.name.split('(', 1)
            value = value.strip()
            typ = typ.strip(' )')
            if typ in {"IDENTIFIER", "STRING", "NUMBER", "int", "float"}:
                return value
        if node.name in {"=", "+", "-", "*", "/", "vid", "img"}:
            return node.name
        return None

    node_label = node.name.split()[0]

    if node_label in {"=", "+", "-", "*", "/", "vid", "img"}:
        reduced_children = [reduce_tree(child) for child in node.children]
        reduced_children = [child for child in reduced_children if child]
        return Node(node.name, children=reduced_children)

    leaf_value = is_leaf_semantic(node)
    if leaf_value:
        return Node(leaf_value)

    reduced_children = [reduce_tree(child) for child in node.children]
    reduced_children = [child for child in reduced_children if child]
    if len(reduced_children) == 1:
        return reduced_children[0]
    elif reduced_children:
        return Node("", children=reduced_children)
    else:
        return None