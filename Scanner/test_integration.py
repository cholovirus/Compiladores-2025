import unittest
from io import StringIO
import sys
from scanner import Scan
from parser import Parser
from tabulate import tabulate

class TestIntegracion(unittest.TestCase):

    def runTestStep(self, label, func):
        try:
            func()
            print(f"✅ [PASSED] {label}")
        except AssertionError as e:
            print(f"❌ [FAILED] {label} -> {str(e)}")
            raise

    def test_integracion_total(self):
        print("\n🔄 Iniciando prueba de integracion del scanner y parser...\n")

        self.runTestStep("Flujo completo: codigo valido",
                         lambda: self.check_integration(code_valid=True))

        self.runTestStep("Flujo completo: codigo con errores",
                         lambda: self.check_integration(code_valid=False))

        print("\n🎉 Todas las pruebas de integracion han finalizado.\n")

    def check_integration(self, code_valid=True):
        code = self.valid_code() if code_valid else self.invalid_code()

        # 1. Scanner
        scanner = Scan(code)
        tokens = scanner.gettoken()
        assert len(tokens) > 0, "No se generaron tokens"

        # 2. Mostrar tabla de tokens
        tokens_table = [(t[1], t[0], *t[2:]) for t in tokens]
        tabla = tabulate(tokens_table, headers=["TokenTYPE", "Token", "Inicio", "Fin", "Linea"], tablefmt="grid")
        assert "TokenTYPE" in tabla

        # 3. Adaptación de tokens para parser
        ultima_linea = tokens[-1][4] if tokens else 0
        adapted_tokens = [(t[1], t[0], t[4]) for t in tokens]
        adapted_tokens.append(('$', '$', ultima_linea))

        # 4. Ejecutar parser y capturar salida
        parser = Parser(adapted_tokens)
        saved_stdout = sys.stdout
        sys.stdout = out = StringIO()
        try:
            parser.parser()
            parser.showTableParser(False)
        finally:
            sys.stdout = saved_stdout

        output = out.getvalue()
        assert "LINEA" in output
        if code_valid:
            lines = output.splitlines()
            assert "🟢 ENTRADA ACEPTADA" in output or any("TOKEN ACEPTADO" in line for line in lines)
        else:
            assert "🔴 ERROR DE SINTAXIS" in output or "🔵 MANEJO ERROR" in output

    def valid_code(self):
        return '''
    int x = 5;
    print("ok");'''

    def invalid_code(self):
        return '''
    float = "abc";
    print("fail");'''

if __name__ == "__main__":
    unittest.main()
