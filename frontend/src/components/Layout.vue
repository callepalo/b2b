<template>
  <div class="layout">
    <!-- Header minimalista -->
    <header class="header">
      <div class="container">
        <div class="header-content">
          <div class="logo">
            <h1>DulproMax</h1>
            <span class="tagline">B2B Catalog</span>
          </div>
          
          <nav class="nav">
            <router-link to="/" class="nav-link active">
              <span class="icon">🏠</span>
              Inicio
            </router-link>
            <router-link to="/categories" class="nav-link">
              <span class="icon">📁</span>
              Categorías
            </router-link>
            <router-link to="/products" class="nav-link">
              <span class="icon">📦</span>
              Productos
            </router-link>
          </nav>

          <div class="header-actions">
            <div class="search-bar">
              <input 
                type="text" 
                placeholder="Buscar productos..."
                class="search-input"
                v-model="searchQuery"
                @input="handleSearch"
              >
              <span class="search-icon">🔍</span>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Main content area -->
    <main class="main">
      <div class="container">
        <div class="page-header" v-if="pageTitle">
          <h2 class="page-title">{{ pageTitle }}</h2>
          <p class="page-description" v-if="pageDescription">
            {{ pageDescription }}
          </p>
        </div>
        
        <slot>
          <!-- Contenido dinámico aquí -->
        </slot>
      </div>
    </main>

    <!-- Footer minimalista -->
    <footer class="footer">
      <div class="container">
        <div class="footer-content">
          <div class="footer-section">
            <h3>DulproMax B2B</h3>
            <p>Catálogo profesional para negocios</p>
          </div>
          
          <div class="footer-section">
            <h4>Enlaces</h4>
            <ul>
              <li><a href="#">Ayuda</a></li>
              <li><a href="#">Contacto</a></li>
              <li><a href="#">Términos</a></li>
            </ul>
          </div>
          
          <div class="footer-section">
            <h4>Contacto</h4>
            <p>info@dulpromax.com</p>
            <p>+1 (555) 123-4567</p>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// Props para personalizar el layout
const props = defineProps({
  pageTitle: {
    type: String,
    default: ''
  },
  pageDescription: {
    type: String,
    default: ''
  }
})

// Estado local
const searchQuery = ref('')

// Métodos
const handleSearch = () => {
  // Emitir evento de búsqueda al componente padre
  emit('search', searchQuery.value)
}

// Emitir eventos
const emit = defineEmits(['search'])
</script>

<style scoped>
.layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  background: var(--color-white);
  border-bottom: 1px solid var(--color-gray-200);
  box-shadow: var(--shadow-sm);
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--spacing-4) 0;
  gap: var(--spacing-4);
}

.logo h1 {
  font-size: var(--text-xl);
  font-weight: 700;
  color: var(--color-primary);
  margin: 0;
}

.logo .tagline {
  font-size: var(--text-sm);
  color: var(--color-gray-500);
  margin-left: var(--spacing-2);
}

.nav {
  display: flex;
  gap: var(--spacing-6);
}

.nav-link {
  display: flex;
  align-items: center;
  gap: var(--spacing-2);
  padding: var(--spacing-2) var(--spacing-4);
  text-decoration: none;
  color: var(--color-gray-600);
  border-radius: var(--border-radius);
  transition: var(--transition);
  font-weight: 500;
}

.nav-link:hover {
  background: var(--color-gray-100);
  color: var(--color-gray-800);
}

.nav-link.active {
  background: var(--color-primary);
  color: var(--color-white);
}

.nav-link .icon {
  font-size: var(--text-sm);
}

.header-actions {
  display: flex;
  align-items: center;
  gap: var(--spacing-4);
}

.search-bar {
  position: relative;
  width: 300px;
}

.search-input {
  width: 100%;
  padding: var(--spacing-2) var(--spacing-4);
  padding-right: var(--spacing-10);
  border: 1px solid var(--color-gray-300);
  border-radius: var(--border-radius-lg);
  font-size: var(--text-sm);
  transition: var(--transition);
}

.search-input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.1);
}

.search-icon {
  position: absolute;
  right: var(--spacing-3);
  top: 50%;
  transform: translateY(-50%);
  color: var(--color-gray-400);
  font-size: var(--text-sm);
}

.main {
  flex: 1;
  padding: var(--spacing-8) 0;
}

.page-header {
  margin-bottom: var(--spacing-8);
  text-align: center;
}

.page-title {
  font-size: var(--text-3xl);
  font-weight: 700;
  color: var(--color-gray-800);
  margin-bottom: var(--spacing-2);
}

.page-description {
  font-size: var(--text-lg);
  color: var(--color-gray-600);
  max-width: 600px;
  margin: 0 auto;
}

.footer {
  margin-top: auto;
  background: var(--color-gray-50);
  border-top: 1px solid var(--color-gray-200);
  padding: var(--spacing-12) 0;
}

.footer-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--spacing-8);
}

.footer-section h3,
.footer-section h4 {
  color: var(--color-gray-800);
  margin-bottom: var(--spacing-4);
}

.footer-section p {
  color: var(--color-gray-600);
  margin-bottom: var(--spacing-2);
}

.footer-section ul {
  list-style: none;
}

.footer-section ul li {
  margin-bottom: var(--spacing-2);
}

.footer-section a {
  color: var(--color-gray-600);
  text-decoration: none;
  transition: var(--transition);
}

.footer-section a:hover {
  color: var(--color-primary);
}

/* Responsive */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    align-items: stretch;
    gap: var(--spacing-4);
  }
  
  .nav {
    flex-direction: column;
    gap: var(--spacing-2);
  }
  
  .search-bar {
    width: 100%;
  }
  
  .footer-content {
    grid-template-columns: 1fr;
    gap: var(--spacing-6);
  }
}
</style>
