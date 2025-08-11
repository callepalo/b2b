<script setup>
import { ref } from 'vue'
import ProductsManager from './components/ProductsManager.vue'
import CategoriesManager from './components/CategoriesManager.vue'

const tab = ref('products')
const tabs = [
  { key: 'products', label: 'Productos' },
  { key: 'categories', label: 'Categorías' },
]
</script>

<template>
  <div class="app">
    <header class="header">
      <div class="container">
        <h1 class="brand">Dulpromax Admin</h1>
        <img src="./assets/logo.jpg" alt="Logo" width="350" height="200"/>
        <nav class="tabs">
          <button
            v-for="t in tabs"
            :key="t.key"
            :class="['tab', { active: tab === t.key }]"
            @click="tab = t.key"
          >
            {{ t.label }}
          </button>
        </nav>
      </div>
    </header>

    <main class="main">
      <ProductsManager v-if="tab === 'products'" />
      <CategoriesManager v-else />
    </main>

    <footer class="footer">
      <div class="container">© {{ new Date().getFullYear() }} Dulpromax — Panel de gestión</div>
    </footer>
  </div>
</template>

<style scoped>
.app { min-height: 100vh; display: flex; flex-direction: column; }
.container { max-width: 1880px; margin: 0 auto; padding: 0 16px; }
.header { border-bottom: 1px solid #eee; background: #fff; }
.brand { font-size: 18px; margin: 0; padding: 12px 0; }
.tabs { display: flex; gap: 8px; padding-bottom: 12px; }
.tab { padding: 8px 12px; border: 1px solid #ddd; background: #f9f9f9; cursor: pointer; border-radius: 6px; }
.tab.active { background: #fff; border-color: #bbb; font-weight: 600; }
.main { flex: 1; padding: 16px 0; }
.footer { border-top: 1px solid #eee; padding: 12px 0; background: #fff; font-size: 12px; color: #666; }
</style>
