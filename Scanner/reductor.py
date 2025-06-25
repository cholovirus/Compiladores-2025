from anytree import Node, RenderTree

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
            # Devuelve una lista de hijos si hay varios, o puedes devolver un nodo 'BLOCK' si prefieres
            result = Node("BLOCK", children=reduced_children)
        else:
            result = None

    memo[id(node)] = result
    return result

def clean_ast(node):
    # Limpia hijos primero (post-order)
    for child in list(node.children):
        clean_ast(child)

    # Simplifica condiciones de IF y FOR
    if node.name in {"IF", "FOR"} and len(node.children) >= 2:
        cond = node.children[0]
        # Caso: cond es nodo vacío con dos hijos: IDENTIFIER y [=, IDENTIFIER]
        if cond.name == "" and len(cond.children) == 2:
            left = cond.children[0]
            right_group = cond.children[1]
            if right_group.name == "=" and len(right_group.children) == 1:
                # Reemplaza por ==
                new_cond = Node("==", parent=node)
                Node(left.name, parent=new_cond)
                Node(right_group.children[0].name, parent=new_cond)
                node.children = tuple([new_cond] + list(node.children[1:]))

    # Agrupa cuerpos en BODY
    if node.name in {"IF", "FOR"} and len(node.children) > 1:
        # Si ya hay un BODY, no lo agregues de nuevo
        if node.children[1].name != "BODY":
            body_nodes = node.children[1:]
            body = Node("BODY", parent=node)
            for b in body_nodes:
                b.parent = body
            node.children = tuple([node.children[0], body])

    # Elimina nodos vacíos innecesarios (si solo tienen un hijo, los reemplaza por ese hijo)
    if node.name == "" and len(node.children) == 1:
        only = node.children[0]
        # Reemplaza este nodo por su único hijo en el padre
        if node.parent:
            idx = list(node.parent.children).index(node)
            only.parent = node.parent
            node.parent.children = tuple(
                only if i == idx else c for i, c in enumerate(node.parent.children)
            )

    return node

# Para imprimir el árbol limpio:
def print_tree(node):
    for pre, fill, n in RenderTree(node):
        print(f"{pre}{n.name}")

# Ejemplo de uso:
# cleaned = clean_ast(reduced_ast)
# print_tree(cleaned)