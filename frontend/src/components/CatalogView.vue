<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from '../services/api'
import { fetchResolvedPrices } from '../services/pricingService'

const products = ref([])
const resolvedPriceMap = ref({}) // { [product_id]: price_resuelto }
const categories = ref([])
const loading = ref(false)
const error = ref('')

const searchQuery = ref('')
const selectedCategory = ref('')
const sortKey = ref('name_asc') // name_asc | price_asc | price_desc

function imageUrl(val) {
  if (!val) return ''
  if (typeof val === 'string') return val
  if (typeof val === 'object') {
    return val.publicUrl || (val.data && val.data.publicUrl) || val.signedUrl || ''
  }
  return ''
}

function formattedPrice(val) {
  return new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP' }).format(val || 0)
}

function getResolvedPrice(p) {
  if (!p || !p.id) return null
  return resolvedPriceMap.value[p.id] ?? null
}

function displayPrice(p) {
  const rp = getResolvedPrice(p)
  if (rp != null) return rp
  return p?.min_price ?? null
}

function hasResolvedPrice(p) {
  return getResolvedPrice(p) != null
}

const productsView = computed(() => {
  let list = [...(products.value || [])]
  const q = searchQuery.value.trim().toLowerCase()
  if (q) {
    list = list.filter(p => `${p.name || ''} ${p.description || ''}`.toLowerCase().includes(q))
  }
  if (selectedCategory.value) {
    list = list.filter(p => p.category_id === selectedCategory.value)
  }
  switch (sortKey.value) {
    case 'price_asc':
      list.sort((a,b) => (displayPrice(a)||0) - (displayPrice(b)||0)); break
    case 'price_desc':
      list.sort((a,b) => (displayPrice(b)||0) - (displayPrice(a)||0)); break
    default:
      list.sort((a,b) => (a.name||'').localeCompare(b.name||'')); break
  }
  return list
})

async function loadCategories() {
  try {
    const res = await api.listCategories()
    categories.value = res.data || []
  } catch {}
}

async function loadProducts() {
  loading.value = true
  error.value = ''
  try {
    const res = await api.listProducts({ per_page: 60, mode: 'catalog', expand: 'packs' })
    products.value = res.data || []
  } catch (e) {
    error.value = e.message || String(e)
  } finally {
    loading.value = false
  }
}

async function loadResolved() {
  try {
    const rows = await fetchResolvedPrices()
    const map = {}
    for (const r of rows) {
      if (r && r.product_id) map[r.product_id] = r.price_resuelto
    }
    resolvedPriceMap.value = map
  } catch (e) {
    // Sin sesión o error: ignoramos silenciosamente en catálogo
    // console.debug('resolved prices not available', e)
  }
}

onMounted(async () => {
  await Promise.all([loadCategories(), loadProducts()])
  // Intentar cargar precios resueltos (requiere sesión). Si falla, no interrumpe el catálogo.
  await loadResolved()
})
</script>

<template>
  <div class="catalog">
    <h1>Catálogo</h1>
    <div v-if="error" class="error">{{ error }}</div>

    <div class="controls">
      <input
        class="ctrl-input"
        v-model="searchQuery"
        type="search"
        placeholder="Buscar por nombre o descripción"
      />
      <select class="ctrl-select" v-model="selectedCategory">
        <option value="">Todas las categorías</option>
        <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.name }}</option>
      </select>
      <select class="ctrl-select" v-model="sortKey">
        <option value="name_asc">Orden: Nombre A→Z</option>
        <option value="price_asc">Orden: Precio menor</option>
        <option value="price_desc">Orden: Precio mayor</option>
      </select>
    </div>

    <div v-if="loading">Cargando...</div>
    <div v-else class="grid">
      <div class="card" v-for="p in productsView" :key="p.id">
        <div class="thumb">
          <img v-if="p.images && p.images.length" :src="imageUrl(p.images[0])" alt="" />
          <div v-else class="thumb-placeholder">Sin imagen</div>
        </div>
        <div class="info">
          <h3 class="name">{{ p.name }}</h3>
          <div class="meta">
            <span class="price" v-if="displayPrice(p) != null">
              <template v-if="hasResolvedPrice(p)">Precio {{ formattedPrice(displayPrice(p)) }}</template>
              <template v-else>Desde {{ formattedPrice(displayPrice(p)) }}</template>
            </span>
            <span class="price" v-else>Precio no disponible</span>
          </div>
          <div class="category">{{ (categories.find(c => c.id === p.category_id)?.name) || '-' }}</div>
          <div class="actions">
            <button type="button">Ver</button>
            <button type="button">Agregar</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.catalog { width: 100%; margin: 16px 0; padding: 0 16px; }
.controls { display: flex; flex-wrap: wrap; gap: 8px; margin: 8px 0 12px; }
.ctrl-input { flex: 1 1 280px; min-width: 200px; }
.ctrl-select { flex: 0 1 200px; }
.grid { display: grid; gap: 16px; grid-template-columns: repeat(4, minmax(0, 1fr)); }
@media (max-width: 1800px) { .grid { grid-template-columns: repeat(3, minmax(0, 1fr)); } }
@media (max-width: 900px) { .grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (max-width: 600px) { .grid { grid-template-columns: repeat(1, minmax(0, 1fr)); } }
.card { border: 1px solid #e6e6e6; border-radius: 10px; overflow: hidden; background: #fff; display: flex; flex-direction: column; transition: box-shadow .2s ease, transform .2s ease; }
.card:hover { box-shadow: 0 6px 20px rgba(0,0,0,0.06); transform: translateY(-2px); }
.thumb { position: relative; width: 100%; aspect-ratio: 4 / 3; background: #fafafa; }
.thumb img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.thumb-placeholder { display: flex; align-items: center; justify-content: center; height: 100%; color: #999; font-size: 12px; }
.info { padding: 10px; display: flex; flex-direction: column; gap: 6px; }
.name { font-size: 14px; margin: 0; }
.meta { display: flex; gap: 8px; align-items: baseline; }
.price { font-weight: 600; }
.category { color: #777; font-size: 12px; }
.actions { display: flex; gap: 8px; margin-top: 8px; }
.error { color: #d33; margin-bottom: 8px; }
</style>
