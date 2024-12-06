# Usar una imagen base de Python
FROM python:3.10-slim

# Crear un directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo requirements.txt para instalar las dependencias
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de los archivos del proyecto
COPY . .

# Exponer el puerto donde Flask correrá
EXPOSE 5000

# Comando para iniciar el servidor Flask
CMD ["python", "main.py"]