<template>
  <div id="app">
    <h1>ChismePress - Generador de Sitios Estáticos</h1>
    <form @submit.prevent="submitFile">
      <input type="file" ref="markdownFile" />
      <button type="submit">Generar HTML</button>
    </form>
    <div v-if="htmlContent">
      <h2>Contenido Generado:</h2>
      <pre>{{ htmlContent }}</pre>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'App',
  data() {
    return {
      htmlContent: null,
    };
  },
  methods: {
    async submitFile() {
      const formData = new FormData();
      formData.append('markdown_file', this.$refs.markdownFile.files[0]);

      try {
        const response = await axios.post('http://localhost:5000/generate', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        });

        if (response.status === 200) {
          this.htmlContent = response.data;
        } else {
          alert('Error al generar HTML');
        }
      } catch (error) {
        console.error('Error al conectar con Flask:', error);
      }
    },
  },
};
</script>

<style scoped>
body {
  font-family: Arial, sans-serif;
  background-color: #f4f4f4;
  text-align: center;
}

form {
  margin: 20px 0;
}

button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
}

button:hover {
  background-color: #0056b3;
}

pre {
  background-color: #fff;
  padding: 10px;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>
