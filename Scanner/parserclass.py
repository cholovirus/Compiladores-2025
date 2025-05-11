import csv
from tabulate import tabulate

class Parser:
    
    def __init__(self,tok):
        self.parsing_table = self.load_Table('/home/cholo/uni/compiladores/Scanner/ll1_table.tsv')
        self.FirstFollow = self.load_FirstFollow("/home/cholo/uni/compiladores/Scanner/ll1_First_Follow.tsv")
        self.tokens_ = []
        self.inputTokens = tok
    
    # Carga la tabla de first y follow
    def load_FirstFollow(self,path):
        sync_sets = {}
        with open(path, newline='') as tsvfile:
            reader = csv.DictReader(tsvfile, delimiter='\t')
            for row in reader:
                nt = row['Nonterminal']
                
                # Procesar el conjunto FOLLOW
                follow_str = row['FOLLOW'].strip()
                follow = self.firstFollow_set(follow_str)
                
                sync_sets[nt] = follow
        return sync_sets
    
    # Set en una biblioteca, se necesita estandarizar por , -> etc
    def firstFollow_set(self,s):
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
    
    # Carga la tabla LL1
    def load_Table(self,file_path):
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
    
    # Proceso del parser
    def parser(self, start_symbol='Program'):
        """
            inputTokens: lista de tuplas (tipo, lexema, linea)
        """
        stack = ['$'] + [start_symbol]
        tokens = self.inputTokens + [('$', '$', -1)]
        index = 0

        while stack:
            top = stack.pop()
            current_token = tokens[index][0]
            current_lexeme = tokens[index][1]
            current_line = tokens[index][2]+1

            if top == current_token:
                self.tokens_.append(("🟢 TOKEN ACEPTADO ",current_token,current_lexeme,f'Linea {current_line}'))
                index += 1
                continue

            if top in ("", "''"):
                continue

            if top in self.parsing_table:
                row = self.parsing_table[top]
                if current_token in row:
                    prod = row[current_token]
                    
                    self.tokens_.append(("⚫ SIMBOLO NO TERMINAL",prod,"",f"Linea {current_line}"))
                    rhs = prod.split('->', 1)[1].strip()
                    
                    symbols = [s for s in rhs.split() if s not in ("", "''")]
                    for sym in reversed(symbols):
                        stack.append(sym)
                    continue
                else:
                    self.tokens_.append(("🔴 ERROR DE SINTAXIS",f"No hay producción: {top} , {current_token}",current_lexeme,f"Linea {current_line}"))
                    
                    while current_token not in self.FirstFollow.get(top, set()) and current_token != '$':
                        index += 1
                        current_token = tokens[index][0]
                        current_lexeme = tokens[index][1]
                        current_line = tokens[index][2]
                
                    self.tokens_.append(("🔵 MANEJO ERROR",current_token,current_lexeme,f"Linea {current_line}"))
                    continue  # reiniciar con el símbolo actual del stack
            elif top == '$':
                if current_token == '$':
                    self.tokens_.append("🟢 ENTRADA ACEPTADA")
                else:
                    self.tokens_.append(f"Tokens luego de fin de cadena: {tokens[index:]}")
                return
            else:
                self.tokens_.append(("🔴 ERROR DE SINTAXIS ",f"No sync producción: {top} != {current_token}",current_lexeme,f"Linea {current_line}"))                
                continue

    def showTableParser(self):
        headers = ["ALERTA","TOKEN", "DERIVACIÓN", "LINEA"]
        print(tabulate(self.tokens_, headers, tablefmt="grid"))