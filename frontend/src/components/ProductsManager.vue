<script setup>
import { ref, onMounted, computed } from 'vue'
import { api } from '../services/api'

const products = ref([])
const categories = ref([])
const loading = ref(false)
const error = ref('')
const showForm = ref(false)
const packs = ref([]) // Presentaciones del producto (frontend-only por ahora)
const originalPackIds = ref([]) // IDs originales para detectar eliminaciones

const editingId = ref(null)
const form = ref({
  name: '',
  description: '',
  price: 0,
  stock_quantity: 0,
  category_id: ''
})
const imageFile = ref(null)

const isEditing = computed(() => !!editingId.value)
const hasPacks = computed(() => (packs.value?.length || 0) > 0)
const minPackPrice = computed(() => {
  const active = (packs.value || []).filter(p => p && (p.is_active ?? true) && p.price != null)
  if (!active.length) return null
  return Math.min(...active.map(p => Number(p.price) || 0))
})

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

// Controles de catálogo (búsqueda, filtro, orden)
const searchQuery = ref('')
const selectedCategory = ref('')
const sortKey = ref('name_asc') // name_asc | price_asc | price_desc | stock_desc

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
      list.sort((a,b) => (a.price||0) - (b.price||0)); break
    case 'price_desc':
      list.sort((a,b) => (b.price||0) - (a.price||0)); break
    case 'stock_desc':
      list.sort((a,b) => (b.stock_quantity||0) - (a.stock_quantity||0)); break
    default:
      list.sort((a,b) => (a.name||'').localeCompare(b.name||'')); break
  }
  return list
})

async function loadProducts() {
  loading.value = true
  error.value = ''
  try {
    const res = await api.listProducts({ per_page: 50 })
    products.value = res.data || []
  } catch (e) {
    error.value = e.message || String(e)
  } finally {
    loading.value = false
  }
}

async function loadCategories() {
  try {
    const res = await api.listCategories()
    categories.value = res.data || []
  } catch (e) {
    // no-op
  }
}

function resetForm() {
  editingId.value = null
  form.value = {
    name: '',
    description: '',
    price: 0,
    stock_quantity: 0,
    category_id: ''
  }
  imageFile.value = null
  showForm.value = false
  packs.value = []
  originalPackIds.value = []
}

async function submitForm() {
  error.value = ''
  try {
    const payload = { ...form.value }
    // Convert empty category to null
    if (!payload.category_id) payload.category_id = null
    // Si hay presentaciones, derivar precio base como el menor precio activo
    if (hasPacks.value && minPackPrice.value != null) {
      payload.price = minPackPrice.value
    }

    let productId = editingId.value
    if (isEditing.value) {
      const updated = await api.updateProduct(editingId.value, payload)
      productId = updated.id
    } else {
      const created = await api.createProduct(payload)
      productId = created.id
    }

    // If image selected, upload it
    if (imageFile.value) {
      await api.uploadProductImage(productId, imageFile.value)
    }
    // Sincronizar packs con backend (crear/actualizar/eliminar)
    try {
      // Eliminar packs que ya no estén
      const currentIds = new Set((packs.value || []).map(p => p.id).filter(Boolean))
      for (const oldId of originalPackIds.value || []) {
        if (!currentIds.has(oldId)) {
          await api.deleteProductPack(productId, oldId)
        }
      }
      // Crear o actualizar packs actuales
      for (const pk of packs.value || []) {
        const payloadPk = { pack_size: Number(pk.pack_size) || 0, price: Number(pk.price) || 0, is_active: !!pk.is_active }
        if (pk.id) {
          await api.updateProductPack(productId, pk.id, payloadPk)
        } else {
          const created = await api.createProductPack(productId, payloadPk)
          pk.id = created.id
        }
      }
    } catch (e) {
      console.warn('Error sincronizando presentaciones:', e)
      // No hacemos throw para no bloquear el guardado del producto; mostramos error en UI
      error.value = (error.value ? error.value + ' | ' : '') + (e.message || String(e))
    }
    resetForm()
    await loadProducts()
  } catch (e) {
    error.value = e.message || String(e)
  }
}

function addPack() {
  packs.value.push({ pack_size: null, price: null, is_active: true })
}

function removePack(idx) {
  packs.value.splice(idx, 1)
}

function startEdit(p) {
  editingId.value = p.id
  form.value = {
    name: p.name || '',
    description: p.description || '',
    price: p.price ?? 0,
    stock_quantity: p.stock_quantity ?? 0,
    category_id: p.category_id || ''
  }
  imageFile.value = null
  showForm.value = true
  // Cargar packs reales del producto
  packs.value = []
  originalPackIds.value = []
  api.listProductPacks(p.id).then((rows) => {
    packs.value = Array.isArray(rows) ? rows : []
    originalPackIds.value = (packs.value || []).map(r => r.id).filter(Boolean)
  }).catch(() => { /* ignore */ })
}

function onFileChange(e) {
  const files = e?.target?.files
  imageFile.value = files && files.length ? files[0] : null
}

async function removeProduct(id) {
  if (!confirm('¿Eliminar este producto?')) return
  try {
    await api.deleteProduct(id)
    await loadProducts()
  } catch (e) {
    alert(e.message || String(e))
  }
}

onMounted(async () => {
  await Promise.all([loadProducts(), loadCategories()])
})
</script>

<template>
  <div class="pm">
    <h1>Productos</h1>

    <div v-if="error" class="error">{{ error }}</div>

    <div class="toolbar">
      <button v-if="!isEditing" @click="showForm = !showForm" type="button">
        {{ showForm ? 'Cerrar' : 'Crear producto' }}
      </button>
      <button v-else type="button" @click="resetForm">Salir de edición</button>
    </div>

    <form v-if="showForm || isEditing" class="form" @submit.prevent="submitForm">
      <h2>{{ isEditing ? 'Editar producto' : 'Crear producto' }}</h2>
      <div class="row">
        <label>Nombre</label>
        <input v-model="form.name" required />
      </div>
      <div class="row">
        <label>Descripción</label>
        <textarea v-model="form.description" rows="3" />
      </div>
      <div class="row two">
        <div v-if="!hasPacks">
          <label>Precio</label>
          <input v-model.number="form.price" type="number" step="0.01" min="0" required />
        </div>
        <div v-else>
          <label>Precio base</label>
          <input :value="minPackPrice != null ? minPackPrice : 0" type="number" step="0.01" min="0" disabled />
        </div>
        <div>
          <label>Stock</label>
          <input v-model.number="form.stock_quantity" type="number" min="0" />
        </div>
      </div>
      <div class="row">
        <label>Categoría</label>
        <select v-model="form.category_id">
          <option value="">(sin categoría)</option>
          <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.name }}</option>
        </select>
      </div>
      <div class="row">
        <label>Imagen</label>
        <input type="file" accept="image/*" @change="onFileChange" />
      </div>

      <div class="row">
        <label>Presentaciones (empaques)</label>
        <div class="packs">
          <div class="packs-head">
            <span>Empaque</span>
            <span>Precio</span>
            <span>Activo</span>
            <span></span>
          </div>
          <div v-if="!packs.length" class="packs-empty">No hay presentaciones agregadas.</div>
          <div v-for="(pk, idx) in packs" :key="idx" class="packs-row">
            <input type="number" min="1" step="1" v-model.number="pk.pack_size" placeholder="Ej: 10" />
            <input type="number" min="0" step="0.01" v-model.number="pk.price" placeholder="Precio" />
            <input type="checkbox" v-model="pk.is_active" />
            <button type="button" class="danger" @click="removePack(idx)">Quitar</button>
          </div>
          <div class="packs-actions">
            <button type="button" @click="addPack">Añadir presentación</button>
          </div>
        </div>
        <small class="hint">Ejemplos: 10, 50, 100. Más adelante el cliente podrá elegir la presentación al hacer el pedido.</small>
      </div>

      <div class="actions">
        <button type="submit">{{ isEditing ? 'Guardar cambios' : 'Crear' }}</button>
        <button type="button" v-if="isEditing" @click="resetForm">Cancelar</button>
      </div>
    </form>

    <div class="list">
      <h2>Catálogo (admin)</h2>
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
          <option value="stock_desc">Orden: Stock mayor</option>
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
              <span class="price">{{ formattedPrice(p.price) }}</span>
              <span class="stock">Stock: {{ p.stock_quantity ?? 0 }}</span>
            </div>
            <div class="category">{{ (categories.find(c => c.id === p.category_id)?.name) || '-' }}</div>
            <div class="card-actions">
              <button @click="startEdit(p)">Editar</button>
              <button class="danger" @click="removeProduct(p.id)">Eliminar</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.pm { width: 100%; margin: 16px 0; padding: 0 16px; }
.toolbar { display: flex; gap: 8px; margin-bottom: 12px; }
.form { border: 1px solid #ddd; padding: 12px; border-radius: 6px; margin-bottom: 16px; }
.row { display: flex; flex-direction: column; gap: 6px; margin-bottom: 10px; }
.row.two { flex-direction: row; gap: 12px; }
.row.two > div { flex: 1; display: flex; flex-direction: column; gap: 6px; }
label { font-size: 12px; color: #555; }
input, textarea, select { padding: 8px; border: 1px solid #ccc; border-radius: 4px; }
.actions { display: flex; gap: 8px; }
button { padding: 6px 10px; border: 1px solid #aaa; border-radius: 4px; background: #fff; cursor: pointer; }
button:hover { background: #f5f5f5; }
button.danger { border-color: #d33; color: #d33; }
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
.thumb img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; transition: transform .25s ease; }
.card:hover .thumb img { transform: scale(1.02); }
.thumb-placeholder { display: flex; align-items: center; justify-content: center; height: 100%; color: #999; font-size: 12px; }
.info { padding: 10px; display: flex; flex-direction: column; gap: 6px; }
.name { font-size: 14px; margin: 0; }
.meta { display: flex; gap: 8px; align-items: baseline; }
.price { font-weight: 600; }
.stock { color: #666; font-size: 12px; }
.category { color: #777; font-size: 12px; }
.card-actions { display: flex; gap: 8px; margin-top: 8px; }
.error { color: #d33; margin-bottom: 8px; }

/* Packs UI */
.packs { display: flex; flex-direction: column; gap: 8px; border: 1px solid #eee; border-radius: 6px; padding: 8px; }
.packs-head, .packs-row { display: grid; grid-template-columns: 120px 160px 80px 100px; gap: 8px; align-items: center; }
.packs-head { font-size: 12px; color: #666; }
.packs-empty { font-size: 12px; color: #888; padding: 6px 0; }
.packs-actions { display: flex; justify-content: flex-start; }
.hint { color: #777; font-size: 12px; }
</style>
