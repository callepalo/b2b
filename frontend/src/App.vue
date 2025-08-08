<script setup>
import CatalogViewer from './components/CatalogViewer.vue'
</script>

<template>
  <div id="app">
    <CatalogViewer />
  </div>
</template>

<style>
#app {
  font-family: system-ui, -apple-system, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background: var(--color-gray-50);
  min-height: 100vh;
}

/* Reset y estilos base */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  line-height: 1.6;
  color: var(--color-gray-800);
  background: var(--color-gray-50);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

/* Utilidades */
.text-center { text-align: center; }
.text-left { text-align: left; }
.text-right { text-align: right; }

.mt-1 { margin-top: 0.25rem; }
.mt-2 { margin-top: 0.5rem; }
.mt-3 { margin-top: 0.75rem; }
.mt-4 { margin-top: 1rem; }

.mb-1 { margin-bottom: 0.25rem; }
.mb-2 { margin-bottom: 0.5rem; }
.mb-3 { margin-bottom: 0.75rem; }
.mb-4 { margin-bottom: 1rem; }

.p-1 { padding: 0.25rem; }
.p-2 { padding: 0.5rem; }
.p-3 { padding: 0.75rem; }
.p-4 { padding: 1rem; }
</style>

<style scoped>
.app {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  font-family: system-ui, -apple-system, sans-serif;
}

.header {
  text-align: center;
  margin-bottom: 2rem;
}

.header h1 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.status {
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.status.connected {
  background: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.status.error {
  background: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.loading {
  text-align: center;
  padding: 2rem;
  font-size: 1.2rem;
  color: #666;
}

.section {
  margin-bottom: 2rem;
}

.section h2 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.categories, .products {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
}

.card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1rem;
  background: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.card h3 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
}

.card p {
  margin: 0.5rem 0;
  color: #666;
}

.badge {
  background: #e9ecef;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  color: #495057;
}

.price {
  font-weight: bold;
  color: #28a745;
  font-size: 1.2rem;
}

.sku {
  font-size: 0.9rem;
  color: #666;
}

.attributes {
  margin-top: 0.5rem;
}

.attributes span {
  display: inline-block;
  background: #f8f9fa;
  padding: 0.25rem 0.5rem;
  margin: 0.25rem;
  border-radius: 4px;
  font-size: 0.8rem;
}
</style>
