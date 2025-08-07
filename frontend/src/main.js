// Importar estilos globales
import '@/assets/styles/main.scss';

// Importar dependencias principales
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';

// Importar Bootstrap JS
import 'bootstrap';

// Configuración de Axios
import axios from 'axios';

// Configuración global de Axios
axios.defaults.baseURL = import.meta.env.VITE_API_URL || 'https://b2b-wa72.onrender.com';
axios.defaults.headers.common['Content-Type'] = 'application/json';
axios.defaults.withCredentials = false;

// Crear la aplicación Vue
const app = createApp(App);

// Usar el router
app.use(router);

// Hacer Axios disponible globalmente en la aplicación
app.config.globalProperties.$http = axios;

// Montar la aplicación
app.mount('#app');

// Manejo global de errores
app.config.errorHandler = (err, vm, info) => {
  console.error('Error global de Vue:', err);
  console.error('Información del error:', info);
};

// Manejo de errores no capturados
window.onerror = function(message, source, lineno, colno, error) {
  console.error('Error no capturado:', { message, source, lineno, colno, error });
  return true; // Evita que el error se muestre en la consola del navegador
};

// Manejo de promesas no capturadas
window.onunhandledrejection = function(event) {
  console.error('Promesa no capturada:', event.reason);
};
