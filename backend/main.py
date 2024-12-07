import argparse
import os
import markdown
from flask import Flask, request, jsonify
from flask_cors import CORS
from jinja2 import Environment, FileSystemLoader

# Lógica de conversión desde la terminal
def convert_markdown_to_html(markdown_content):
    """Convierte el contenido markdown a HTML."""
    return markdown.markdown(markdown_content)

def render_html(template_path, title, content):
    """Renderiza el HTML usando la plantilla Jinja2."""
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')  # Apunta correctamente a backend/templates
    env = Environment(loader=FileSystemLoader(template_dir))
    template_name = os.path.basename(template_path)
    template = env.get_template(template_name)
    return template.render(title=title, content=content)

def process_single_file(markdown_file, output_dir, template):
    """Procesa un solo archivo markdown y lo convierte a HTML."""
    os.makedirs(output_dir, exist_ok=True)

    # Leer archivo markdown
    with open(markdown_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()

    # Convertir markdown a HTML
    html_content = convert_markdown_to_html(markdown_content)

    # Renderizar HTML con la plantilla
    rendered_html = render_html(template, title=os.path.basename(markdown_file), content=html_content)

    # Guardar el archivo HTML
    output_path = os.path.join(output_dir, os.path.basename(markdown_file).replace(".md", ".html"))
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(rendered_html)
    print(f"Archivo convertido: {markdown_file}")

def process_files_from_directory(markdown_dir, output_dir, template):
    """Procesa todos los archivos .md dentro del directorio."""
    for root, _, files in os.walk(markdown_dir):
        for file in files:
            if file.endswith(".md"):  # Solo procesamos archivos .md
                file_path = os.path.join(root, file)
                print(f"Procesando el archivo {file_path}...")
                process_single_file(file_path, output_dir, template)

# Función para gestionar los argumentos de la terminal
def parse_arguments():
    parser = argparse.ArgumentParser(description="ChismePress: Un generador de sitios estáticos.")
    parser.add_argument("file", help="Ruta al archivo Markdown o directorio que se va a convertir.", nargs="?", default=None)  # Argumento de archivo o directorio
    parser.add_argument("-o", "--output", default="output", help="Directorio de salida para los archivos HTML generados.")
    parser.add_argument("-t", "--template", help="Ruta a un archivo de plantilla Jinja2.")
    parser.add_argument("--generate", action='store_true', help="Indica si se debe generar el archivo Markdown a HTML.")  # Agregar el flag --generate
    return parser.parse_args()

# Lógica para procesar archivos desde la terminal
def process_files_from_terminal(args):
    if args.file and os.path.isfile(args.file):  # Si el argumento es un archivo
        print(f"Procesando el archivo {args.file}...")
        process_single_file(args.file, args.output, args.template or "default.html")
    elif args.file and os.path.isdir(args.file):  # Si el argumento es un directorio
        print(f"Procesando todos los archivos .md en {args.file}...")
        process_files_from_directory(args.file, args.output, args.template or "default.html")
    else:
        print(f"La ruta proporcionada no es válida: {args.file}")


# Lógica de la API Flask para el Frontend

app = Flask(__name__)

# Habilitar CORS para todas las rutas
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

# Endpoint para recibir los archivos Markdown y devolver el HTML generado
@app.route('/generate', methods=['POST'])
def generate_html():
    if 'markdown_file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['markdown_file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not file.filename.endswith('.md'):
        return jsonify({"error": "Invalid file type, only .md files are allowed"}), 400

    markdown_content = file.read().decode('utf-8')  # Leer el archivo Markdown como texto
    html_content = markdown.markdown(markdown_content)  # Convertir Markdown a HTML

    return jsonify({"html_content": html_content}), 200


if __name__ == "__main__":
    args = parse_arguments()

    # Si se pasa el flag --generate, procesamos los archivos desde la terminal
    if args.generate:
        process_files_from_terminal(args)
    else:
        # Si no se pasa el flag --generate, arrancamos el servidor Flask
        app.run(host='0.0.0.0', port=5000)
