from scanner import *
from parser import *

# Lectura de codigo
with open("/home/cholo/uni/compiladores/Scanner/code.txt", "r", encoding="utf-8") as file:
    code = file.read()

# Realizar Scan
test = Scan(code)
tokens = test.gettoken()

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
#parser(tokens, parsing_table)
parser2(tokens,parsing_table,FirstFollow)