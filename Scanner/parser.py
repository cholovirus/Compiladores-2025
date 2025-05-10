class Node:
    def __init__(self, data):
        self.data = data
        self.children = []

    def insert(self, child):
        self.children.append(child)

    def print_tree(self, level=0):
        print("  " * level + str(self.data))
        for child in self.children:
            child.print_tree(level + 1)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current = self.tokens[self.pos] if self.tokens else None
        self.errors = []

    def next_token(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current = self.tokens[self.pos]
        else:
            self.current = None

    def match(self, expected_type):
        if self.current and self.current[1] == expected_type:
            self.next_token()
            return True
        else:
            self.errors.append(f"Expected {expected_type}, found {self.current}")
            return False

    def program(self):
        program_node = Node("PROGRAM")
        while self.current:
            if self.current[1] == "KEYWORD" and self.current[0] == "if":
                program_node.insert(self.if_statement())
            elif self.current[1] == "KEYWORD" and self.current[0] == "for":
                program_node.insert(self.for_loop())
            elif self.current[1] == "IDENTIFIER":
                program_node.insert(self.assignment())
            else:
                self.errors.append(f"Unexpected token {self.current}")
                self.next_token()
        return program_node

    def if_statement(self):
        if_node = Node("IF")
        self.match("KEYWORD")  # match 'if'
        if_node.insert(self.expression())
        self.match("DELIMITER")  # match '('
        if_node.insert(self.block())
        if self.current and self.current[0] == "else":
            self.match("KEYWORD")  # match 'else'
            if_node.insert(self.block())
        return if_node

    def for_loop(self):
        for_node = Node("FOR")
        self.match("KEYWORD")  # match 'for'
        for_node.insert(Node(self.current[0]))  # variable
        self.match("IDENTIFIER")
        self.match("OPERATOR")  # match '='
        for_node.insert(self.expression())
        self.match("DELIMITER")  # match '('
        for_node.insert(self.block())
        return for_node

    def assignment(self):
        assign_node = Node("ASSIGNMENT")
        assign_node.insert(Node(self.current[0]))  # variable
        self.match("IDENTIFIER")
        self.match("OPERATOR")  # match '='
        assign_node.insert(self.expression())
        self.match("DELIMITER")  # match ';'
        return assign_node

    def expression(self):
        expr_node = Node("EXPR")
        expr_node.insert(Node(self.current[0]))  # value
        self.match(self.current[1])  # match type (e.g., INTEGER, STRING)
        while self.current and self.current[1] == "OPERATOR":
            operator_node = Node(self.current[0])
            self.match("OPERATOR")
            operator_node.insert(expr_node)
            operator_node.insert(Node(self.current[0]))
            self.match(self.current[1])
            expr_node = operator_node
        return expr_node

    def block(self):
        block_node = Node("BLOCK")
        while self.current and self.current[1] != "DELIMITER":
            block_node.insert(self.statement())
        return block_node

    def statement(self):
        if self.current[1] == "KEYWORD" and self.current[0] == "if":
            return self.if_statement()
        elif self.current[1] == "KEYWORD" and self.current[0] == "for":
            return self.for_loop()
        elif self.current[1] == "IDENTIFIER":
            return self.assignment()
        else:
            self.errors.append(f"Unexpected token {self.current}")
            self.next_token()
            return Node("ERROR")

    def parse(self):
        ast = self.program()
        if self.errors:
            print("Errors found during parsing:")
            for error in self.errors:
                print(error)
        else:
            print("Parsing completed successfully.")
        return ast


# Example usage
if __name__ == "__main__":
    from tabulate import tabulate

    # Example tokens from the scanner
    tokens = [
        ("if", "KEYWORD", 1, 1, 1),
        ("(", "DELIMITER", 2, 2, 1),
        ("calidad", "IDENTIFIER", 3, 10, 1),
        (">", "OPERATOR", 11, 11, 1),
        ("80", "INTEGER", 12, 13, 1),
        (")", "DELIMITER", 14, 14, 1),
        ("print", "IDENTIFIER", 15, 19, 2),
        ("(", "DELIMITER", 20, 20, 2),
        ("\"Alta calidad\"", "STRING", 21, 34, 2),
        (")", "DELIMITER", 35, 35, 2),
        (";", "DELIMITER", 36, 36, 2),
        ("else", "KEYWORD", 37, 40, 3),
        ("print", "IDENTIFIER", 41, 45, 4),
        ("(", "DELIMITER", 46, 46, 4),
        ("\"Calidad baja\"", "STRING", 47, 60, 4),
        (")", "DELIMITER", 61, 61, 4),
        (";", "DELIMITER", 62, 62, 4),
    ]

    parser = Parser(tokens)
    ast = parser.parse()
    ast.print_tree()