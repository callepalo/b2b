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

    <section class="content">
      <ProductsManager v-if="tab === 'products'" />
      <CategoriesManager v-else />
    </section>
  </div>
 </template>

<style scoped>
.app { max-width: 1100px; margin: 0 auto; padding: 12px; }
.tabs { display: flex; gap: 8px; border-bottom: 1px solid #eee; margin-bottom: 12px; }
.tab { padding: 8px 12px; border: 1px solid #ccc; border-bottom: none; background: #fafafa; cursor: pointer; border-top-left-radius: 6px; border-top-right-radius: 6px; }
.tab.active { background: #fff; font-weight: 600; }
.content { background: #fff; }
</style>
