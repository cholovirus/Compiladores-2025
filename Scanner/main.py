from scanner import *
from parser import *

# Lectura de codigo
code = '''
if(a == b){
    concat(a,b);
    string stream = vid("ll1_table.mp4");
    if( a == stream) {
        print("iguales");
    }
    for (a=0;a<3;a=a+1;){
    }
}
'''

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
parse(tokens, parsing_table)