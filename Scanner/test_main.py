import unittest
from main import Scan

def load_code_snippets(file_path):
    """Carga los ejemplos de código desde pruebas.txt."""
    with open(file_path, "r") as file:
        content = file.read()
    
    # Dividir el contenido en bloques de código basados en "Código X"
    snippets = []
    blocks = content.split("Código ")
    for block in blocks[1:]:  # Ignorar el primer split vacío
        lines = block.split("\n", 3)  # Dividir en encabezado y contenido
        if len(lines) > 3:
            snippets.append(lines[3].strip())  # Agregar solo el contenido del código
    return snippets

# Cargar los snippets desde pruebas.txt
code_snippets = load_code_snippets("pruebas.txt")

class TestScan(unittest.TestCase):
    def test_code_snippets(self):
        """Test provided code snippets for valid tokens."""
        with open("resultados.txt", "w") as log_file:
            for i, code in enumerate(code_snippets, start=1):
                log_file.write(f"=== Testing Code Snippet {i} ===\n")
                log_file.write(code + "\n\n")
                scanner = Scan(code)
                tokens = scanner.scanning()

                # Log tokens
                log_file.write("Tokens:\n")
                for token in tokens:
                    log_file.write(f"{token}\n")

                # Check for errors
                errors = [token for token in tokens if token[1] == "ERROR"]
                if errors:
                    log_file.write("\nErrors Found:\n")
                    for error in errors:
                        log_file.write(f"{error}\n")
                else:
                    log_file.write("\nNo Errors Found.\n")
                log_file.write("\n")

                # Assert no errors in the tokens
                self.assertEqual(len(errors), 0, f"Errors found in Code Snippet {i}")

if __name__ == "__main__":
    unittest.main()