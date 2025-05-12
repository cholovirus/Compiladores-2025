from scanner import *
from parser import *
from tabulate import tabulate
# Lectura de codigo
with open("C:\\Users\\heibh\\OneDrive\\Desktop\\xXx_C++_xXx\\COMPILADORES\\Compiladores-2025\\Scanner\\code.txt") as file:
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