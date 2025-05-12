import unittest
from io import StringIO
import sys

from scanner import Scan
from parser import Parser
from tabulate import tabulate
#from test_utils import runTestStep

class TestMain(unittest.TestCase):

    def setUp(self):
        # Código de prueba basado en code.txt
        self.test_code = '''if(a == b){
            int a=333333333333333333333333333333333333;
            concat(a,b);
            string stream = vid("ll1_table.mp4");
            if( a == stream) {
                print("iguales");
            }
            image adio = img("pedro.mp4");
            for (a=0a<3;a=a+1;){
            }
            
            image correcto = img("correcto.mp4");
            image reinicio = img("reinicio.mp4");
        }'''
        print("\n🔧 [SETUP] Código de prueba cargado correctamente.\n")


    def runTestStep(self, label, func):
        try:
            func()
            print(f"✅ [PASSED] {label}")
        except AssertionError as e:
            print(f"❌ [FAILED] {label} -> {str(e)}")
            raise


    def test_full_main_pipeline(self):
        print("🚀 Iniciando pruebas para main.py...\n")

        # Paso 1: Escanear código
        self.runTestStep("Scanner genera tokens",
            lambda: self.assertTrue(len(Scan(self.test_code).gettoken()) > 0, "No se generaron tokens"))

        # Paso 2: Verificar contenido de tabla de tokens
        def check_token_table():
            scanner = Scan(self.test_code)
            tokens = scanner.gettoken()
            table = tabulate([(t[1], t[0], *t[2:]) for t in tokens],
                             headers=["TokenTYPE", "Token", "Inicio", "Fin", "Linea"], tablefmt="grid")
            assert "TokenTYPE" in table
            assert any(tok[1] in ("IDENTIFIER", "NUMBER") for tok in tokens)

        self.runTestStep("Tabla de tokens contiene datos validos", check_token_table)

        # Paso 3: Adaptar tokens para parser
        def check_token_adaptation():
            scanner = Scan(self.test_code)
            tokens = scanner.gettoken()
            adapted = [(t[1], t[0], t[4]) for t in tokens]
            ultima = tokens[-1][4] if tokens else 0
            adapted.append(('$', '$', ultima))
            assert adapted[-1][0] == '$'
            assert all(len(t) == 3 for t in adapted)

        self.runTestStep("Tokens adaptados correctamente para el parser", check_token_adaptation)

        # Paso 4: Ejecutar parser y verificar salida
        def check_parser_output():
            scanner = Scan(self.test_code)
            tokens = scanner.gettoken()
            adapted = [(t[1], t[0], t[4]) for t in tokens]
            adapted.append(('$', '$', tokens[-1][4] if tokens else 0))
            parser = Parser(adapted)

            saved_stdout = sys.stdout
            out = StringIO()
            sys.stdout = out
            try:
                parser.parser()
                parser.showTableParser(False)
            finally:
                sys.stdout = saved_stdout

            output = out.getvalue()
            assert "LINEA" in output
            assert "ERROR" in output or "TOKEN ACEPTADO" in output

        self.runTestStep("Parser genera salida valida", check_parser_output)

        print("\n🎉 Todas las pruebas de `main.py` han finalizado.\n")


if __name__ == '__main__':
    unittest.main()
