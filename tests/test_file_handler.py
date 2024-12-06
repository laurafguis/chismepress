import unittest
import os
from utils.file_handler import convert_markdown_to_html, render_html

class TestFileHandler(unittest.TestCase):

    def test_convert_markdown_to_html(self):
        """Prueba que el Markdown se convierta correctamente a HTML."""
        markdown_content = "# Título\nEste es un párrafo en Markdown."
        expected_html = "<h1>Título</h1>\n<p>Este es un párrafo en Markdown.</p>"
        self.assertEqual(convert_markdown_to_html(markdown_content), expected_html)

    def test_render_html(self):
        """Prueba que la plantilla renderice correctamente el HTML."""
        template_path = "default.html"
        title = "Título de prueba"
        content = "<h1>Contenido de prueba</h1>"
        
        # Crear un entorno temporal para simular la carpeta templates
        templates_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
        rendered_html = render_html(template_path, title, content)
        
        # Verificar que el título y contenido están en el HTML generado
        self.assertIn(title, rendered_html)
        self.assertIn(content, rendered_html)

if __name__ == "__main__":
    unittest.main()
