<script setup>
import { ref } from 'vue';
import Productos from './components/Productos.vue';
import Categorias from './components/Categorias.vue';

const currentView = ref('productos');
const isMenuOpen = ref(false);

const setView = (view) => {
  currentView.value = view;
  isMenuOpen.value = false;
  window.scrollTo(0, 0);
};
</script>

<template>
  <div class="app">
    <!-- Header -->
    <header class="header">
      <div class="container">
        <div class="header-content">
          <!-- Logo -->
          <div class="logo">
            <img src="./assets/placeholder_logo.png" alt="Dulpromax" class="logo-img">
          </div>
          
          <!-- Menú de navegación -->
          <nav class="main-nav" :class="{ 'active': isMenuOpen }">
            <ul class="nav-list">
              <li class="nav-item">
                <a href="#" class="nav-link" :class="{ 'active': currentView === 'productos' }" @click.prevent="setView('productos')">
                  Productos
                </a>
              </li>
              <li class="nav-item">
                <a href="#" class="nav-link" :class="{ 'active': currentView === 'categorias' }" @click.prevent="setView('categorias')">
                  Categorías
                </a>
              </li>
            </ul>
          </nav>
          
          <!-- Iconos de usuario/carrito -->
          <div class="header-actions">
            <button class="icon-btn" aria-label="Buscar">
              <i class="fas fa-search"></i>
            </button>
            <button class="icon-btn" aria-label="Carrito">
              <i class="fas fa-shopping-cart"></i>
              <span class="cart-count">0</span>
            </button>
            <button class="menu-toggle" @click="isMenuOpen = !isMenuOpen" aria-label="Menú">
              <i class="fas fa-bars"></i>
            </button>
          </div>
        </div>
      </div>
    </header>
    
    <!-- Contenido principal -->
    <main class="main-content">
      <component :is="currentView === 'productos' ? Productos : Categorias" />
    </main>
    
    <!-- Footer -->
    <footer class="footer">
      <div class="container">
        <div class="footer-content">
          <div class="footer-section">
            <h3>Dulpromax</h3>
            <p>Los mejores productos de repostería y dulces.</p>
          </div>
          <div class="footer-section">
            <h4>Enlaces rápidos</h4>
            <ul>
              <li><a href="#" @click.prevent="setView('productos')">Productos</a></li>
              <li><a href="#" @click.prevent="setView('categorias')">Categorías</a></li>
            </ul>
          </div>
          <div class="footer-section">
            <h4>Contacto</h4>
            <p>Email: info@dulpromax.com</p>
            <p>Teléfono: (123) 456-7890</p>
          </div>
        </div>
        <div class="footer-bottom">
          <p>&copy; 2025 Dulpromax. Todos los derechos reservados.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<style>
/* Variables de colores */
:root {
  --primary: #FFD700;       /* Amarillo */
  --secondary: #F5F5DC;     /* Beige */
  --white: #FFFFFF;         /* Blanco */
  --text: #333333;          /* Texto oscuro */
  --light-gray: #F8F8F8;    /* Fondo gris claro */
  --border: #E0E0E0;        /* Borde gris */
  --success: #4CAF50;       /* Verde */
  --warning: #FF9800;       /* Naranja */
  --danger: #F44336;        /* Rojo */
  --shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  --nav-hover: #3a5169;
  --nav-active: #42b983;
  --text-light: #ffffff;
  --text-muted: #6c757d;
  --font-main: 'Arial', sans-serif;
  --font-heading: 'Georgia', serif;
  --transition: all 0.3s ease;
  --border-radius: 4px;
  --container-width: 1200px;
  --header-height: 80px;
  --footer-height: 200px;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: var(--font-main);
  line-height: 1.6;
  color: var(--text);
  background-color: var(--white);
}

.container {
  width: 100%;
  max-width: var(--container-width);
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
