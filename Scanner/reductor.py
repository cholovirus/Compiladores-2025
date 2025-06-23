from anytree import Node

# Cache para memoización
memo = {}

def reduce_tree(node):
    if id(node) in memo:
        return memo[id(node)]

    semantic_leaf_types = {"IDENTIFIER", "STRING", "NUMBER", "int", "float"}
    important_operators = {"=", "==", "+", "-", "*", "/", "<"}

    def is_leaf_semantic(name):
        if '(' in name:
            value, typ = name.split('(', 1)
            value = value.strip()
            typ = typ.strip(' )')
            if typ in semantic_leaf_types:
                return Node(f"{typ}: {value}")
        return None

    reduced_children = []
    for c in node.children:
        reduced = reduce_tree(c)
        if reduced:
            reduced_children.append(reduced)

    result = None

    if "if (" in node.name or node.name == "if (if)":
        result = Node("IF", children=reduced_children)
        # else
    elif node.name.strip().startswith("else"):
        result = Node("ELSE", children=reduced_children)
    elif "input" in node.name:
        id_node = next((child for child in reduced_children if "IDENTIFIER" in child.name), None)
        result = Node("INPUT", children=[id_node] if id_node else [])

    elif "print" in node.name:
        content_node = next((child for child in reduced_children if any(x in child.name for x in ["IDENTIFIER", "Expression", "STRING"])), None)
        result = Node("PRINT", children=[content_node] if content_node else [])

    elif "for" in node.name:
        result = Node("FOR", children=reduced_children)

    elif any(x in node.name for x in ["vid", "img", "concat"]):
        result = Node(node.name.strip(), children=reduced_children)

    else:
        leaf = is_leaf_semantic(node.name)
        if leaf:
            result = leaf
        elif any(node.name.startswith(op) for op in important_operators):
            left = None
            right = None
            for child in reduced_children:
                if not left and "IDENTIFIER" in child.name:
                    left = child
                else:
                    right = child
            result = Node("=", children=[left, right] if left and right else [])
        elif node.name in important_operators:
            result = Node(node.name, children=reduced_children)
        elif len(reduced_children) == 1:
            result = reduced_children[0]
        elif reduced_children:
            result = Node("", children=reduced_children)
        else:
            result = None

    memo[id(node)] = result
    return result
