import argparse
from flask import Flask, request, jsonify  # type: ignore
from utils.file_handler import process_files
import os
import markdown

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

# Endpoint para recibir los archivos Markdown y devolver el HTML generado
@app.route('/generate', methods=['POST'])
def generate_html():
    # Verificar si el archivo está presente en la solicitud
    if 'markdown_file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['markdown_file']

    # Verificar que el archivo tiene una extensión válida
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not file.filename.endswith('.md'):
        return jsonify({"error": "Invalid file type, only .md files are allowed"}), 400

    # Procesar el archivo
    markdown_content = file.read().decode('utf-8')  # Leer el archivo Markdown como texto
    html_content = process_markdown_to_html(markdown_content)  # Convertir Markdown a HTML

    # Puedes hacer aquí lo que necesites con el contenido HTML, como guardarlo o enviarlo al frontend
    return jsonify({"html_content": html_content}), 200

def process_markdown_to_html(markdown_content):
    return markdown.markdown(markdown_content)

def parse_arguments():
    # Definir el parser de argumentos para la línea de comandos (si lo necesitas)
    parser = argparse.ArgumentParser(description="ChismePress: Un generador de sitios estáticos.")
    parser.add_argument("directorio_markdown", help="Ruta al directorio que contiene los archivos Markdown.")
    parser.add_argument("-o", "--output", default="output", help="Directorio de salida para los archivos HTML generados.")
    parser.add_argument("-t", "--template", help="Ruta a un archivo de plantilla Jinja2.")
    return parser.parse_args()

# Función para iniciar el servidor Flask
def run_flask_server():
    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    # Si deseas que el servidor Flask se inicie siempre, puedes usar este código
    run_flask_server()
    
    # Si deseas seguir con la funcionalidad de línea de comandos:
    args = parse_arguments()
    print(f"Directorio Markdown: {args.directorio_markdown}")
    print(f"Directorio de salida: {args.output}")
    print(f"Plantilla: {args.template if args.template else 'default'}")

    if os.path.isdir(args.directorio_markdown):
        print("Procesando los archivos Markdown...")
        process_files(args.directorio_markdown, args.output, args.template or "templates/default.html")
    else:
        print(f"La ruta proporcionada no es un directorio válido: {args.directorio_markdown}")
