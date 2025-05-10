import csv
from main import temp
def print_specific_nonterminal(parsing_table, nonterminal):
    """Imprime un no-terminal específico con formato"""
    if nonterminal in parsing_table:
        print(f"\nProducciones para '{nonterminal}':")
        print("=" * 60)
        for term, prod in parsing_table[nonterminal].items():
            if prod:
                print(f" terminal  '{term}': {prod}")
    else:
        print(f"Error: No terminal '{nonterminal}' no encontrado")



def load_parsing_table(file_path):
    parsing_table = {}
    
    with open(file_path, 'r', newline='') as tsvfile:
        reader = csv.DictReader(tsvfile, delimiter='\t')
        
        for row in reader:
            nonterminal = row['']
            productions = {}
            
            for terminal, production in row.items():
                if terminal != '' and production.strip():  # Ignorar columna vacía y celdas vacías
                    productions[terminal] = production.strip()
            
            parsing_table[nonterminal] = productions
    
    return parsing_table

# Cargar tabla de analisis
parsing_table = load_parsing_table('/home/cholo/uni/compiladores/Scanner/ll1_table.tsv')

#print_specific_nonterminal(parsing_table, "IfStmtPrime")

def parse(tokens, parsing_table, start_symbol='Program'):
    """
    tokens: lista de tuplas (tipo, lexema), e.g. ('if','if'), ('IDENTIFIER','x'), ...
    parsing_table: dict de dicts [NonTerminal][Terminal] -> "NT -> RHS"
    """
    # Preparamos la pila y la entrada
    stack = ['$'] + [start_symbol]
    tokens = tokens + [('$','$')]
    index = 0

    while stack:
        top = stack.pop()
        current_token = tokens[index][0]
        current_lexeme = tokens[index][1]

        # Caso 1: terminal coincide
        if top == current_token:
            print(f"✔️ Token aceptado: {tokens[index]}")
            index += 1
            continue

        # Caso 2: epsilon
        if top == "''" or top == '':
            continue

        # Caso 3: no terminal → buscamos en la tabla
        if top in parsing_table:
            row = parsing_table[top]
            if current_token in row:
                prod = row[current_token]
                # print(f"📘 Aplicando regla: {prod}")
                # prod tiene la forma "NT -> X Y Z"; nos quedamos con la parte derecha
                rhs = prod.split('->',1)[1].strip()
                # separamos en símbolos, ignorando epsilones
                symbols = [s for s in rhs.split() if s not in ("''", '')]
                # los volvemos a poner en la pila en orden inverso
                for sym in reversed(symbols):
                    stack.append(sym)
                continue
            else:
                # No hay producción para este par (top, current_token)
                print(f"❌ Error de sintaxis: no hay producción para ({top}, {current_token})")
                print(f"   Token problemático: {tokens[index]}")
                return
        else:
            # top no es terminal válido ni no-terminal
            print(f"❌ Error de sintaxis: símbolo inesperado en pila: {top}")
            return

    # Si consume todo
    if tokens[index][0] == '$':
        print("✅ Entrada aceptada")
    else:
        print("❌ Quedaron tokens sin consumir:", tokens[index:])


tokens = [
    ('if', 'if'),
    ('(', '('),
    ('IDENTIFIER', 'a'),
    ('==', '=='),
    ('IDENTIFIER', 'b'),
    (')', ')'),
    ('{', '{'),
    ('concat', 'concat'),
    ('(', '('),
    ('IDENTIFIER', 'a'),
    (',', ','),
    ('IDENTIFIER', 'b'),
    (')', ')'),
    (';', ';'),
    ('video', 'video'),
    ('IDENTIFIER', 'viedo'),
    ('=', '='),
    ('vid', 'vid'),
    ('(', '('),
    ('STRING', '"ll1_table.mp4"'),
    (')', ')'),
    (';', ';'),
    ('}', '}'),
    ('$', '$')
]

tokens = temp

parse(tokens, parsing_table)