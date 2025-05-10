import csv
import re

def load_FirstFollow(path):
    sync_sets = {}
    with open(path, newline='') as tsvfile:
        reader = csv.DictReader(tsvfile, delimiter='\t')
        for row in reader:
            nt = row['Nonterminal']
            
            # Procesar el conjunto FOLLOW
            follow_str = row['FOLLOW'].strip()
            follow = parse_set(follow_str)
            
            sync_sets[nt] = follow
    return sync_sets

def parse_set(s):
    """Convierte una cadena como '{$,}}' en un conjunto {'$', '}'}"""
    s = s.strip('{}').strip()
    if not s:
        return set()
    
    # Manejar casos especiales
    s = s.replace("'", "").replace('"', '')  # Eliminar comillas si existen
    
    # Separar elementos, manejando comas y caracteres especiales
    elements = []
    current = ''
    in_token = False
    
    for char in s:
        if char == ',':
            if current:
                elements.append(current)
                current = ''
        else:
            current += char
    
    if current:
        elements.append(current)
    
    # Limpiar elementos
    cleaned_elements = []
    for item in elements:
        item = item.strip()
        if item == "$":
            cleaned_elements.append('$')
        elif item == "''":
            cleaned_elements.append('')
        elif item:
            cleaned_elements.append(item)
    
    return set(cleaned_elements)

def printColumms(parsing_table, nonterminal):
    """Imprime un no-terminal específico con formato"""
    if nonterminal in parsing_table:
        print(f"\nProducciones para '{nonterminal}':")
        print("=" * 60)
        for term, prod in parsing_table[nonterminal].items():
            if prod:
                print(f" terminal  '{term}': {prod}")
    else:
        print(f"Error: No terminal '{nonterminal}' no encontrado")

def load_Table(file_path):
    parsing_table = {}
    
    with open(file_path, 'r', newline='') as tsvfile:
        reader = csv.DictReader(tsvfile, delimiter='\t')
        
        for row in reader:
            nonterminal = row['']
            productions = {}
            
            for terminal, production in row.items():
                if terminal != '' and production.strip():
                    productions[terminal] = production.strip()
            
            parsing_table[nonterminal] = productions
    
    return parsing_table

# Cargar tabla de analisis
parsing_table = load_Table('/home/cholo/uni/compiladores/Scanner/ll1_table.tsv')
FirstFollow = load_FirstFollow("/home/cholo/uni/compiladores/Scanner/ll1_First_Follow.tsv")
#printColumms(parsing_table, "IfStmtPrime")

def parser(tokens, parsing_table, start_symbol='Program'):
    """
    tokens: lista de tuplas (tipo, lexema), e.g. ('if','if'), ('IDENTIFIER','x'), ...
    parsing_table: dict de dicts [NonTerminal][Terminal] -> "NT -> RHS"
    """
    # Preparamos la pila y la entrada
    stack = ['$'] + [start_symbol]
    tokens = tokens + [('$','$',-1)]
    index = 0

    while stack:
        top = stack.pop()
        current_token = tokens[index][0]
        #current_lexeme = tokens[index][1]
        current_line = tokens[index][2]

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


def parser2(tokens, parsing_table, FF, start_symbol='Program'):
    """
    tokens: lista de tuplas (tipo, lexema, linea)
    """
    stack = ['$'] + [start_symbol]
    tokens = tokens + [('$', '$', -1)]
    index = 0

    while stack:
        top = stack.pop()
        current_token = tokens[index][0]
        current_lexeme = tokens[index][1]
        current_line = tokens[index][2]+1

        if top == current_token:
            print(f"✔️ Token aceptado: ({current_token}, '{current_lexeme}') en línea {current_line}")
            index += 1
            continue

        if top in ("", "''"):
            continue

        if top in parsing_table:
            row = parsing_table[top]
            if current_token in row:
                prod = row[current_token]
                #print(f"📘 Línea {current_line}: Aplicando regla: {prod}")
                rhs = prod.split('->', 1)[1].strip()
                symbols = [s for s in rhs.split() if s not in ("", "''")]
                for sym in reversed(symbols):
                    stack.append(sym)
                continue
            else:
                print(f"⚠️ Error de sintaxis en línea {current_line}:")
                print(f"   No hay producción para ({top}, {current_token})")
                print(f"   Token: ({current_token}, '{current_lexeme}')")
                # Modo pánico: buscar token en conjunto de sincronización

                sync = set(FF.get(top, set()))
                sync.add(';')

                while current_token not in FF.get(top, set()) and current_token != '$':
                    index += 1
                    current_token = tokens[index][0]
                    current_lexeme = tokens[index][1]
                    current_line = tokens[index][2]
                print(f"🔁 Recuperado en línea {current_line} con token: ({current_token}, '{current_lexeme}')")
                continue  # reiniciar con el símbolo actual del stack
        elif top == '$':
            if current_token == '$':
                print("✅ Entrada aceptada")
            else:
                print(f"❌ Tokens adicionales después del fin: {tokens[index:]}")
            return
        else:
            print(f"❌ Error inesperado: símbolo desconocido en pila '{top}' en línea {current_line}")
            continue

