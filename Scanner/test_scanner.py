import unittest
from scanner import Scan


class TestScanner(unittest.TestCase):

    def runTestStep(self, label, func):
        try:
            func()
            print(f"✅ [PASSED] {label}")
        except AssertionError as e:
            print(f"❌ [FAILED] {label} -> {str(e)}")
            raise

    def test_scanner(self):
        print("\n🚀 Iniciando pruebas para scanner.py...\n")

        self.runTestStep("Identificadores y palabras clave",
            lambda: self.check_keywords_and_identifiers())

        self.runTestStep("Tipos de datos y operadores",
            lambda: self.check_types_and_operators())

        self.runTestStep("Deteccion de comentarios",
            lambda: self.check_comments())

        self.runTestStep("Reconocimiento de strings",
            lambda: self.check_string())

        self.runTestStep("Errores por numeros muy largos",
            lambda: self.check_number_overflow())

        print("\n🎉 Todas las pruebas de `scanner.py` han finalizado.\n")

    def check_keywords_and_identifiers(self):
        code = "if else for vid myVariable123"
        tokens = Scan(code).gettoken()
        types = [t[1] for t in tokens]
        assert "if" in types
        assert "else" in types
        assert "for" in types
        assert "vid" in types
        assert "IDENTIFIER" in types

    def check_types_and_operators(self):
        code = "int float string + == >= <= ="
        tokens = Scan(code).gettoken()
        types = [t[1] for t in tokens]
        assert "int" in types
        assert "+" in types
        assert "==" in types
        assert ">=" in types
        assert "=" in types

    def check_comments(self):
        code = "# un comentario\n## bloque ##"
        tokens = Scan(code).gettoken()
        comments = [t for t in tokens if t[1] == "COMMENT"]
        assert len(comments) == 2
        assert comments[0][0].startswith("#")
        assert comments[1][0].startswith("##")

    def check_string(self):
        code = 'print("hola mundo")'
        tokens = Scan(code).gettoken()
        found_string = any(t[1] == "STRING" for t in tokens)
        assert found_string

    def check_number_overflow(self):
        code = "123456789012345678901"  # 21 dígitos
        tokens = Scan(code).gettoken()
        errors = [t for t in tokens if "Overflow" in t[1]]
        assert len(errors) >= 1


if __name__ == "__main__":
    unittest.main()
