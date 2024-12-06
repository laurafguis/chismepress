# Usar una imagen base de Node.js
FROM node:16-alpine

# Crear un directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos package.json y package-lock.json
COPY package*.json ./

# Instalar las dependencias
RUN npm install

# Copiar el resto de los archivos del proyecto
COPY . .

# Exponer el puerto donde Vue.js servirá la aplicación
EXPOSE 8080

# Comando para iniciar el servidor de desarrollo
CMD ["npm", "run", "serve"]
