import unittest
import os
import subprocess

class TestMain(unittest.TestCase):

    def test_main_help(self):
        """Prueba que el comando --help funcione correctamente."""
        result = subprocess.run(["py", "main.py", "--help"], capture_output=True, text=True)
        self.assertIn("ChismePress: Un generador de sitios estáticos.", result.stdout)

    def test_generate_output(self):
        """Prueba que los archivos Markdown se conviertan a HTML correctamente."""
        # Crear un directorio temporal de prueba
        test_docs_dir = os.path.join(os.path.dirname(__file__), "test_docs")
        test_output_dir = os.path.join(os.path.dirname(__file__), "test_output")
        os.makedirs(test_docs_dir, exist_ok=True)
        os.makedirs(test_output_dir, exist_ok=True)
        
        # Crear un archivo Markdown de prueba
        test_markdown_path = os.path.join(test_docs_dir, "test.md")
        with open(test_markdown_path, "w") as f:
            f.write("# Prueba\nEste es un archivo de prueba.")
        
        # Ejecutar el script
        subprocess.run(["py", "main.py", test_docs_dir, "-o", test_output_dir, "-t", "templates/default.html"])
        
        # Verificar que el archivo HTML fue generado
        test_html_path = os.path.join(test_output_dir, "test.html")
        self.assertTrue(os.path.exists(test_html_path))
        
        # Verificar el contenido del archivo HTML generado
        with open(test_html_path, "r") as f:
            html_content = f.read()
            self.assertIn("<h1>Prueba</h1>", html_content)
            self.assertIn("<p>Este es un archivo de prueba.</p>", html_content)

if __name__ == "__main__":
    unittest.main()
