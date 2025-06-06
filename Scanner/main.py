import os
from scanner import *
from parser import *
from tabulate import tabulate
from pathlib import Path
# Lectura de codigo

nombre = "code.txt"
ruta_archivo = Path(__file__).resolve().parent
ruta_archivo= ruta_archivo / "Code" / nombre

with open(ruta_archivo) as file:
    code = file.read()

# Realizar Scan
scanner = Scan(code)
tokens = scanner.gettoken()

print("VISUALIZACIÓN DE TOKENS:")
print()
tokens_Table = [(t[1], t[0], *t[2:]) for t in tokens]
headers = ["TokenTYPE","Token", "Inicio", "Fin", "Linea"]
print(tabulate(tokens_Table, headers, tablefmt="grid"))

# Adaptacion de la salida del scanner al parser
ultima_linea = tokens[-1][4] if tokens else 0
tokens = [(t[1], t[0],t[4]) for t in tokens]
tokens.append(('$', '$',ultima_linea))

# Realizar Parseo
print()
print("VISUALIZACIÓN PARSER:")
print()
parser = Parser(tokens)
parser.parser()
parser.showTableParser(False)

print("\nARBOL DE PARSEO:")
parser.print_parse_tree()
parser.export_parse_tree_to_pdf("arbol_de_parseo.pdf")
parser.export_tree_picture("arbol_parseo.png")
