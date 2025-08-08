<script setup>
import { ref } from 'vue';
import Productos from './components/Productos.vue';
import Categorias from './components/Categorias.vue';

const currentView = ref('productos');

const setView = (view) => {
  currentView.value = view;
  window.scrollTo(0, 0);
};
</script>

<template>
  <div class="app">
    <header class="app-header">
      <h1>Panel de Administración</h1>
      <nav class="main-nav">
        <button 
          @click="setView('productos')" 
          :class="{ active: currentView === 'productos' }"
        >
          Productos
        </button>
        <button 
          @click="setView('categorias')" 
          :class="{ active: currentView === 'categorias' }"
        >
          Categorías
        </button>
      </nav>
    </header>
    
    <main class="app-main">
      <component :is="currentView === 'productos' ? Productos : Categorias" />
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
  --nav-bg: #2c3e50;
  --nav-hover: #3a5169;
  --nav-active: #42b983;
  --text-light: #ffffff;
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
  background-color: var(--nav-bg);
  color: var(--text-light);
  padding: 1rem;
  margin-bottom: 2rem;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.app-header h1 {
  margin: 0 0 1rem 0;
  font-size: 1.8rem;
  text-align: center;
  color: var(--text-light);
}

.main-nav {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 1rem;
}

.main-nav button {
  background-color: transparent;
  color: var(--text-light);
  border: 1px solid var(--text-light);
  border-radius: 4px;
  padding: 0.5rem 1.5rem;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.main-nav button:hover {
  background-color: var(--nav-hover);
}

.main-nav button.active {
  background-color: var(--primary);
  border-color: var(--primary);
  font-weight: bold;
}

.app-main {
  background: white;
  padding: 1.5rem;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>
