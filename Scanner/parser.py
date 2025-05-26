import os
import csv
from tabulate import tabulate
from anytree import Node, RenderTree
from anytree.exporter import DotExporter
from anytree.exporter import UniqueDotExporter
from pathlib import Path

class Parser:
    
    def __init__(self,tok):
        ruta_archivo = Path(__file__).resolve().parent
        
        self.parsing_table = self.load_Table(ruta_archivo / "ll1_table.tsv")
        self.FirstFollow = self.load_FirstFollow(ruta_archivo / "ll1_First_Follow.tsv")

        #self.parsing_table = self.load_Table('/home/cholo/uni/compiladores/Scanner/ll1_table.tsv')
        #self.FirstFollow = self.load_FirstFollow("/home/cholo/uni/compiladores/Scanner/ll1_First_Follow.tsv")
        self.tokens_ = []
        self.inputTokens = tok

        self.root = None
        self.current_nodes_stack = [] # Pila de nodos actuales
    
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
    
    # expandir nodos
    def expand_node(self, parent, symbols):
        """
            Expande un nodo con un nuevo símbolo.
        """
        children = []
        for symbol in symbols:
            node = Node(symbol, parent=parent)
            children.append(node)
        return children

    # Imprimir el arbol
    def print_parse_tree(self):
        """
            Imprime el árbol de análisis sintáctico.
        """
        if self.root:
            for pre, fill, node in RenderTree(self.root):
                print(f"{pre}{node.name}")

    # Exportar el arbol a un archivo .dot
    def export_parse_tree_to_pdf(self, filename="parse_tree.pdf"):
        if self.root:
            carpeta_salida = Path(__file__).resolve().parent / "archivos"
            carpeta_salida.mkdir(exist_ok=True)  # Crea la carpeta si no existe
            ruta_dot = carpeta_salida / "tree.dot"
            ruta_pdf = carpeta_salida / filename

            print("[INFO] Generando archivo DOT...")
            DotExporter(self.root).to_dotfile(ruta_dot)
            print("[INFO] Ejecutando Graphviz para generar PDF...")
            result = os.system(f"dot -Tpdf \"{ruta_dot}\" -o \"{ruta_pdf}\"")
            if result == 0:
                print(f"[OK] Árbol de parseo exportado como {filename}")
            else:
                print("[ERROR] Falló la generación del PDF. ¿Está Graphviz instalado y en el PATH?")

    # Exportar el arbol a un archivo a .jpg
    def export_tree_picture(self, filename="arbol_parseo.png"):
        if self.root:
            carpeta_salida = Path(__file__).resolve().parent / "archivos"
            carpeta_salida.mkdir(exist_ok=True)  # Crea la carpeta si no existe
            ruta_dot = carpeta_salida / "safe_tree.dot"
            ruta_png = carpeta_salida / filename

            UniqueDotExporter(self.root).to_dotfile(ruta_dot)
            os.system(f"dot -Tpng \"{ruta_dot}\" -o \"{ruta_png}\"")

            print(f"[OK] Árbol de parseo guardado en {filename}")
        else:
            print("[ERROR] Árbol no construido.")

    # Proceso del parser
    def parser(self, start_symbol='Program'):
        """
            inputTokens: lista de tuplas (tipo, lexema, linea)
        """
        stack = ['$'] + [start_symbol]
        tokens = self.inputTokens + [('$', '$', -1)]
        index = 0

        self.root = Node(start_symbol)
        self.current_nodes_stack = [self.root]

        while stack:
            top = stack.pop()
            current_token = tokens[index][0]
            current_lexeme = tokens[index][1]
            current_line = tokens[index][2]+1

            if top == current_token:
                self.tokens_.append(("🟢 TOKEN ACEPTADO ",current_token,current_lexeme,f'Linea {current_line}'))

                if self.current_nodes_stack:
                    matched_node = self.current_nodes_stack.pop()
                    matched_node.name += f" ({current_token})"
                else:
                    print(f"[WARNING] Nodo para '{current_token}' no encontrado en la pila de nodos actuales.")

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

                    if self.current_nodes_stack:
                        parent = self.current_nodes_stack.pop()
                        children = self.expand_node(parent, symbols)
                        self.current_nodes_stack.extend(reversed(children))
                    else:
                        print(f"[WARNING] No hay nodo padre para la producción '{prod}'.")

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

    def showTableParser(self,NT=True):
        headers = ["ALERTA","TOKEN", "DERIVACIÓN", "LINEA"]
        if(NT):
            print(tabulate(self.tokens_, headers, tablefmt="grid"))
        else:
            filtro = [t for t in self.tokens_ if t[0] != "⚫ SIMBOLO NO TERMINAL"]
            print(tabulate(filtro, headers, tablefmt="grid"))