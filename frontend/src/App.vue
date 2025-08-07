<script setup>
import Productos from './components/Productos.vue';
</script>

<template>
  <div class="app">
    <header class="app-header">
      <h1>Panel de Administración</h1>
    </header>
    
    <main class="app-main">
      <Productos />
    </main>
  </div>
</template>

<style>
:root {
  --primary: #42b983;
  --secondary: #2c3e50;
  --background: #f5f5f5;
  --text: #2c3e50;
  --border: #e0e0e0;
  --success: #4caf50;
  --warning: #ff9800;
  --danger: #f44336;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: var(--text);
  background-color: var(--background);
  line-height: 1.6;
}

.app {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.app-header {
  background-color: var(--primary);
  color: white;
  padding: 1rem;
  margin-bottom: 2rem;
  border-radius: 4px;
}

.app-header h1 {
  margin: 0;
  font-size: 1.5rem;
}

.app-main {
  background: white;
  padding: 1.5rem;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>
