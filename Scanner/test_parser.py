import unittest
from parser import Parser

class TestParser(unittest.TestCase):

    def runTestStep(self, label, func):
        try:
            func()
            print(f"✅ [PASSED] {label}")
        except AssertionError as e:
            print(f"❌ [FAILED] {label} -> {str(e)}")
            raise

    def test_parser(self):
        print("\n🚀 Iniciando pruebas para parser.py...\n")

        self.runTestStep("Carga de tabla LL(1)",
            lambda: self.check_table_load())

        self.runTestStep("Carga de FIRST/FOLLOW",
            lambda: self.check_first_follow_load())

        self.runTestStep("Conversion de cadena a conjunto FIRST/FOLLOW",
            lambda: self.check_firstFollow_set())

        self.runTestStep("Parser acepta entrada valida",
            lambda: self.check_parser_valid_input())

        self.runTestStep("Parser detecta errores sintacticos y maneja recuperacion",
            lambda: self.check_parser_error_recovery())

        print("\n🎉 Todas las pruebas de `parser.py` han finalizado.\n")

    def check_table_load(self):
        dummy = Parser([])
        table = dummy.parsing_table
        assert isinstance(table, dict)
        assert len(table) > 0
        assert all(isinstance(k, str) for k in table.keys())

    def check_first_follow_load(self):
        dummy = Parser([])
        first_follow = dummy.FirstFollow
        assert isinstance(first_follow, dict)
        assert len(first_follow) > 0
        assert all(isinstance(v, set) for v in first_follow.values())

    def check_firstFollow_set(self):
        dummy = Parser([])
        result = dummy.firstFollow_set("{$,},int,print")
        assert isinstance(result, set)
        assert "$" in result
        assert "int" in result
        assert "}" in result

    def check_parser_valid_input(self):
        tokens = [
            ('if', 'if', 0), ('(', '(', 0), ('IDENTIFIER', 'a', 0), ('==', '==', 0), ('IDENTIFIER', 'b', 0), (')', ')', 0),
            ('{', '{', 0),
            ('int', 'int', 1), ('IDENTIFIER', 'x', 1), ('=', '=', 1), ('NUMBER', '5', 1), (';', ';', 1),
            ('}', '}', 2),
            ('$', '$', 3)
        ]
        parser = Parser(tokens)
        parser.parser()
        outputs = [t[0] for t in parser.tokens_]
        assert "🟢 ENTRADA ACEPTADA" in outputs or any("TOKEN ACEPTADO" in o for o in outputs)

    def check_parser_error_recovery(self):
        tokens = [
            ('if', 'if', 0), ('(', '(', 0), ('==', '==', 0),  # Falta operandos
            (')', ')', 0), ('{', '{', 0),
            ('float', 'float', 1), ('IDENTIFIER', 'f', 1), ('=', '=', 1),
            ('STRING', '"abc"', 1), (';', ';', 1),
            ('}', '}', 2), ('$', '$', 3)
        ]
        parser = Parser(tokens)
        parser.parser()
        outputs = [t[0] for t in parser.tokens_]
        assert any("🔴 ERROR DE SINTAXIS" in o for o in outputs)
        assert any("🔵 MANEJO ERROR" in o for o in outputs)

if __name__ == '__main__':
    unittest.main()
