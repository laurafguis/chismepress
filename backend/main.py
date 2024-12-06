import argparse
from utils.file_handler import process_files

def parse_arguments():
    # Definir el parser de argumentos
    parser = argparse.ArgumentParser(description="ChismePress: Un generador de sitios estáticos.")
    
    # Agregar argumento obligatorio para los archivos Markdown
    parser.add_argument("directorio_markdown", help="Ruta al directorio que contiene los archivos Markdown.")
    
    # Agregar argumento opcional para el directorio de salida (por defecto será 'output')
    parser.add_argument("-o", "--output", default="output", help="Directorio de salida para los archivos HTML generados.")
    
    # Agregar argumento opcional para la plantilla Jinja2
    parser.add_argument("-t", "--template", help="Ruta a un archivo de plantilla Jinja2.")
    
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    print(f"Directorio Markdown: {args.directorio_markdown}")
    print(f"Directorio de salida: {args.output}")
    print(f"Plantilla: {args.template if args.template else 'default'}")

# Procesa los archivos Markdown
process_files(args.directorio_markdown, args.output, args.template or "templates/default.html")
