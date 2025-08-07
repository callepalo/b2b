<script setup>
import Productos from './components/Productos.vue';
</script>

<template>
  <div class="app">
    <header class="bg-primary text-white p-3 mb-4">
      <div class="container">
        <h1>Panel de Administración</h1>
      </div>
    </header>
    
    <main class="container">
      <Productos />
    </main>
  </div>
</template>

<style>
/* Estilos globales */
:root {
  --primary: #0d6efd;
  --secondary: #6c757d;
  --success: #198754;
  --info: #0dcaf0;
  --warning: #ffc107;
  --danger: #dc3545;
  --light: #f8f9fa;
  --dark: #212529;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  line-height: 1.5;
  color: #212529;
  background-color: #f8f9fa;
  margin: 0;
  padding: 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 15px;
}

.bg-primary {
  background-color: var(--primary) !important;
}

.text-white {
  color: white !important;
}

.p-3 {
  padding: 1rem !important;
}

.mb-4 {
  margin-bottom: 1.5rem !important;
}

h1 {
  margin: 0;
  font-size: 1.75rem;
  font-weight: 500;
  line-height: 1.2;
}
</style>
