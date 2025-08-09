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
            <a href="#" @click="showSection('catalog')" :class="{ active: currentSection === 'catalog' }" class="nav-link">
              <span class="icon">🏠</span>
              Catálogo
            </a>
            <a href="#" @click="showSection('categories')" :class="{ active: currentSection === 'categories' }" class="nav-link">
              <span class="icon">📁</span>
              Categorías
            </a>
            <a href="#" @click="showSection('products')" :class="{ active: currentSection === 'products' }" class="nav-link">
              <span class="icon">📦</span>
              Productos
            </a>
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
        <main class="main-content">
          <CatalogViewer v-if="currentSection === 'catalog'" />
          <CategoriesManager v-if="currentSection === 'categories'" />
          <div v-if="currentSection === 'products'" class="section-placeholder">
            <h2>Gestión de Productos</h2>
            <p>Próximamente disponible...</p>
          </div>
        </main>
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
import CatalogViewer from './CatalogViewer.vue'
import CategoriesManager from './CategoriesManager.vue'

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
const currentSection = ref('catalog')

// Métodos
const handleSearch = () => {
  // Emitir evento de búsqueda al componente padre
  emit('search', searchQuery.value)
}

const showSection = (section) => {
  currentSection.value = section
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
  background: #fef3c7;
  border-bottom: 2px solid #fbbf24;
  padding: 1rem 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 0;
  gap: 1rem;
}

.logo h1 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #d97706;
  text-decoration: none;
  margin: 0;
}

.logo .tagline {
  font-size: 0.875rem;
  color: #666;
  margin-left: 0.5rem;
}

.nav {
  display: flex;
  gap: 1rem;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  text-decoration: none;
  color: #666;
  border-radius: 0.25rem;
  transition: all 0.3s ease;
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
  padding: 0.75rem 1rem;
  border: 2px solid #fbbf24;
  border-radius: 8px;
  font-size: 0.875rem;
  background: white;
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
  background: #fef3c7;
  border-top: 2px solid #fbbf24;
  padding: 2rem 0;
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
  color: #92400e;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
}

.footer-section a:hover {
  color: #d97706;
}

/* Responsive */
@media (max-width: 1200px) {
  .header-content {
    padding: 0 1rem;
  }
  
  .main-content {
    padding: 1rem;
  }
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 1rem;
    padding: 0 1rem;
  }
  
  nav {
    flex-wrap: wrap;
    justify-content: center;
    gap: 1rem;
  }
  
  .search-bar {
    max-width: 100%;
  }
  
  .logo {
    font-size: 1.25rem;
  }
  
  footer {
    padding: 1.5rem 1rem;
  }
}

@media (max-width: 768px) {
  .footer-content {
    grid-template-columns: 1fr;
    gap: var(--spacing-6);
  }
}
</style>
