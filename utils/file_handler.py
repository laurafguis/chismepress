import os
import markdown
from jinja2 import Environment, FileSystemLoader

def convert_markdown_to_html(markdown_content):
    """Convierte el contenido markdown a HTML."""
    return markdown.markdown(markdown_content)

from jinja2 import Environment, FileSystemLoader
import os

def render_html(template_path, title, content):
    """Renderiza el HTML usando la plantilla Jinja2."""
    # Obtener el directorio donde está la carpeta templates
    template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
    env = Environment(loader=FileSystemLoader(template_dir))
    
    # Extraer solo el nombre del archivo de la plantilla
    template_name = os.path.basename(template_path)
    
    # Obtener la plantilla
    template = env.get_template(template_name)
    return template.render(title=title, content=content)

def process_files(markdown_dir, output_dir, template):
    """Lee los archivos markdown y los convierte a HTML."""
    os.makedirs(output_dir, exist_ok=True)

    for root, _, files in os.walk(markdown_dir):
        for file in files:
            if file.endswith(".md"):
                # Leer archivo markdown
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    markdown_content = f.read()

                # Convertir markdown a HTML
                html_content = convert_markdown_to_html(markdown_content)

                # Renderizar HTML con la plantilla
                rendered_html = render_html(template, title=file, content=html_content)

                # Guardar el archivo HTML
                output_path = os.path.join(output_dir, file.replace(".md", ".html"))
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(rendered_html)
                print(f"Archivo convertido: {file}")
