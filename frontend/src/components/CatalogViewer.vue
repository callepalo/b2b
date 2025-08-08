<template>
  <div class="catalog-viewer">
    <!-- Hero Section -->
    <section class="hero">
      <div class="container">
        <h1 class="hero-title">Catálogo B2B</h1>
        <p class="hero-subtitle">
          Descubre nuestros productos premium para tu negocio
        </p>
        
        <!-- Search Bar -->
        <div class="search-section">
          <div class="search-container">
            <input 
              type="text" 
              placeholder="Buscar productos..."
              class="search-input"
              v-model="searchQuery"
              @input="handleSearch"
            >
            <button class="search-btn">
              <span>🔍</span>
            </button>
          </div>
        </div>

        <!-- Status Bar -->
        <div class="status-bar" v-if="!loading">
          <div class="status-indicator" :class="statusClass">
            <span class="indicator-dot"></span>
            <span class="status-text">{{ statusText }}</span>
          </div>
          <div class="stats">
            <span>{{ totalProducts }} productos</span>
            <span>•</span>
            <span>{{ totalCategories }} categorías</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Content -->
    <div v-if="loading" class="loading-state">
      <div class="loading-spinner"></div>
      <p>Cargando catálogo...</p>
    </div>

    <div v-else-if="error" class="error-state">
      <div class="error-icon">⚠️</div>
      <h3>Error al cargar</h3>
      <p>{{ error }}</p>
      <button class="retry-btn" @click="loadCatalog">
        Reintentar
      </button>
    </div>

    <div v-else class="catalog-content">
      <!-- Categories Section -->
      <section class="categories-section">
        <div class="section-header">
          <h2>Categorías</h2>
          <p>Explora por categoría</p>
        </div>
        
        <div class="categories-grid">
          <div 
            v-for="category in categories" 
            :key="category.id" 
            class="category-card"
            :class="{ active: selectedCategory === category.id }"
            @click="selectCategory(category.id)"
          >
            <div class="category-icon">
              <span>📁</span>
            </div>
            <div class="category-content">
              <h3 class="category-name">{{ category.name }}</h3>
              <p class="category-description">{{ category.description }}</p>
              <span class="category-count">{{ getProductCount(category.id) }} productos</span>
            </div>
          </div>
        </div>
      </section>

      <!-- Products Section -->
      <section class="products-section">
        <div class="section-header">
          <h2>Productos</h2>
          <p>Descubre nuestros mejores productos</p>
        </div>
        
        <div class="products-grid">
          <div 
            v-for="product in filteredProducts" 
            :key="product.id" 
            class="product-card"
          >
            <div class="product-image">
              <div class="image-placeholder">
                <span class="product-icon">📦</span>
              </div>
              <div class="product-badge" v-if="product.is_featured">
                Destacado
              </div>
            </div>
            
            <div class="product-content">
              <div class="product-header">
                <h3 class="product-name">{{ product.name }}</h3>
                <span class="product-sku">{{ product.sku }}</span>
              </div>
              
              <p class="product-description">{{ product.description }}</p>
              
              <div class="product-meta">
                <span class="product-price">${{ product.price }}</span>
                <span class="product-category">{{ getCategoryName(product.category_id) }}</span>
              </div>
              
              <div v-if="product.attributes" class="product-attributes">
                <span 
                  v-for="(value, key) in product.attributes" 
                  :key="key"
                  class="attribute-tag"
                >
                  {{ key }}: {{ value }}
                </span>
              </div>
              
              <div class="product-actions">
                <button class="btn-primary" @click="viewProduct(product)">
                  Ver detalles
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { CategoriesService, ProductsService } from '../services/api.js'

// Estado
const categories = ref([])
const products = ref([])
const loading = ref(true)
const error = ref(null)
const selectedCategory = ref(null)
const searchQuery = ref('')

// Computed
const totalCategories = computed(() => categories.value.length)
const totalProducts = computed(() => products.value.length)
const filteredProducts = computed(() => {
  if (selectedCategory.value) {
    return products.value.filter(product => product.category_id === selectedCategory.value)
  }
  return products.value
})

const statusClass = computed(() => {
  if (loading.value) return 'loading'
  if (error.value) return 'error'
  return 'success'
})

const statusText = computed(() => {
  if (loading.value) return 'Cargando...'
  if (error.value) return 'Error al cargar'
  return 'Conectado'
})

// Métodos
const loadCatalog = async () => {
  try {
    loading.value = true
    error.value = null
    
    const [categoriesData, productsData] = await Promise.all([
      CategoriesService.getAll(),
      ProductsService.getAll()
    ])
    
    categories.value = categoriesData
    products.value = productsData
  } catch (err) {
    error.value = err.message || 'Error al cargar el catálogo'
    console.error('Error loading catalog:', err)
  } finally {
    loading.value = false
  }
}

const selectCategory = (categoryId) => {
  selectedCategory.value = selectedCategory.value === categoryId ? null : categoryId
}

const getProductCount = (categoryId) => {
  return products.value.filter(product => product.category_id === categoryId).length
}

const getCategoryName = (categoryId) => {
  const category = categories.value.find(category => category.id === categoryId)
  return category ? category.name : 'Categoría no encontrada'
}

const viewProduct = (product) => {
  console.log('Ver producto:', product.name)
}

const handleSearch = () => {
  console.log('Buscando:', searchQuery.value)
}

// Lifecycle
onMounted(() => {
  loadCatalog()
})
</script>

<style scoped>
/* Hero Section */
.hero {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 4rem 0;
  text-align: center;
}

.hero-title {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.hero-subtitle {
  font-size: 1.25rem;
  opacity: 0.9;
  margin-bottom: 2rem;
}

.search-section {
  max-width: 600px;
  margin: 0 auto;
}

.search-container {
  position: relative;
  display: flex;
  align-items: center;
}

.search-input {
  width: 100%;
  padding: 1rem 1.5rem;
  border: none;
  border-radius: 50px;
  font-size: 1rem;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.search-input::placeholder {
  color: rgba(255, 255, 255, 0.7);
}

.search-input:focus {
  outline: none;
  background: rgba(255, 255, 255, 0.2);
}

.search-btn {
  position: absolute;
  right: 0.5rem;
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  padding: 0.5rem;
}

/* Status Bar */
.status-bar {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 1rem;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.875rem;
}

.status-indicator.success {
  background: rgba(34, 197, 94, 0.1);
  color: #22c55e;
}

.indicator-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #22c55e;
}

.stats {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  font-size: 0.875rem;
  opacity: 0.8;
}

/* Loading State */
.loading-state,
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 0;
  text-align: center;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--color-gray-200);
  border-top: 3px solid var(--color-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.retry-btn {
  background: var(--color-primary);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: var(--border-radius);
  cursor: pointer;
  margin-top: 1rem;
}

/* Sections */
.catalog-content {
  padding: 4rem 0;
}

.section-header {
  text-align: center;
  margin-bottom: 3rem;
}

.section-header h2 {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--color-gray-800);
  margin-bottom: 0.5rem;
}

.section-header p {
  font-size: 1.125rem;
  color: var(--color-gray-600);
}

/* Categories */
.categories-section {
  margin-bottom: 4rem;
}

.categories-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}

.category-card {
  background: var(--color-white);
  border: 1px solid var(--color-gray-200);
  border-radius: var(--border-radius-lg);
  padding: 2rem;
  cursor: pointer;
  transition: var(--transition);
  text-align: center;
}

.category-card:hover {
  box-shadow: var(--shadow-lg);
  transform: translateY(-2px);
}

.category-card.active {
  border-color: var(--color-primary);
  background: var(--color-primary);
  color: white;
}

.category-icon {
  font-size: 2rem;
  margin-bottom: 1rem;
}

.category-name {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.category-description {
  color: var(--color-gray-600);
  margin-bottom: 1rem;
}

.category-count {
  font-size: 0.875rem;
  color: var(--color-gray-500);
}

/* Products */
.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 2rem;
}

.product-card {
  background: var(--color-white);
  border: 1px solid var(--color-gray-200);
  border-radius: var(--border-radius-lg);
  overflow: hidden;
  transition: var(--transition);
}

.product-card:hover {
  box-shadow: var(--shadow-lg);
  transform: translateY(-2px);
}

.product-image {
  position: relative;
  height: 200px;
  background: var(--color-gray-100);
}

.image-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  font-size: 3rem;
  color: var(--color-gray-400);
}

.product-badge {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: var(--color-primary);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: var(--border-radius);
  font-size: 0.75rem;
  font-weight: 500;
}

.product-content {
  padding: 1.5rem;
}

.product-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 1rem;
}

.product-name {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--color-gray-800);
  margin: 0;
}

.product-sku {
  font-size: 0.875rem;
  color: var(--color-gray-500);
}

.product-description {
  color: var(--color-gray-600);
  margin-bottom: 1rem;
  line-height: 1.5;
}

.product-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.product-price {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-primary);
}

.product-category {
  font-size: 0.875rem;
  color: var(--color-gray-500);
}

.product-attributes {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.attribute-tag {
  background: var(--color-gray-100);
  color: var(--color-gray-700);
  padding: 0.25rem 0.5rem;
  border-radius: var(--border-radius);
  font-size: 0.75rem;
}

.product-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-primary {
  background: var(--color-primary);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: var(--border-radius);
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: var(--transition);
  flex: 1;
}

.btn-primary:hover {
  background: var(--color-primary-dark);
}

/* Responsive */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2rem;
  }
  
  .hero-subtitle {
    font-size: 1rem;
  }
  
  .categories-grid,
  .products-grid {
    grid-template-columns: 1fr;
  }
  
  .search-container {
    max-width: 100%;
  }
}
</style>
