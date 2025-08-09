<script setup>
import { ref, onMounted, computed } from 'vue'
import { api } from '../services/api'

const products = ref([])
const categories = ref([])
const loading = ref(false)
const error = ref('')

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

function imageUrl(val) {
  if (!val) return ''
  if (typeof val === 'string') return val
  if (typeof val === 'object') {
    return val.publicUrl || (val.data && val.data.publicUrl) || val.signedUrl || ''
  }
  return ''
}

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
}

async function submitForm() {
  error.value = ''
  try {
    const payload = { ...form.value }
    // Convert empty category to null
    if (!payload.category_id) payload.category_id = null

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
    resetForm()
    await loadProducts()
  } catch (e) {
    error.value = e.message || String(e)
  }
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

    <form class="form" @submit.prevent="submitForm">
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
        <div>
          <label>Precio</label>
          <input v-model.number="form.price" type="number" step="0.01" min="0" required />
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
        <input type="file" accept="image/*" @change="e => imageFile.value = e.target.files?.[0] || null" />
      </div>
      <div class="actions">
        <button type="submit">{{ isEditing ? 'Guardar cambios' : 'Crear' }}</button>
        <button type="button" v-if="isEditing" @click="resetForm">Cancelar</button>
      </div>
    </form>

    <div class="list">
      <h2>Listado</h2>
      <div v-if="loading">Cargando...</div>
      <table v-else>
        <thead>
          <tr>
            <th>Imagen</th>
            <th>Nombre</th>
            <th>Precio</th>
            <th>Stock</th>
            <th>Categoría</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in products" :key="p.id">
            <td>
              <img v-if="p.images && p.images.length" :src="imageUrl(p.images[0])" alt="img" style="width:48px;height:48px;object-fit:cover;border-radius:4px;border:1px solid #eee;" />
            </td>
            <td>{{ p.name }}</td>
            <td>{{ new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP' }).format(p.price || 0) }}</td>
            <td>{{ p.stock_quantity }}</td>
            <td>{{ (categories.find(c => c.id === p.category_id)?.name) || '-' }}</td>
            <td class="row-actions">
              <button @click="startEdit(p)">Editar</button>
              <button class="danger" @click="removeProduct(p.id)">Eliminar</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.pm { max-width: 960px; margin: 24px auto; padding: 0 12px; }
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
.list table { width: 100%; border-collapse: collapse; }
.list th, .list td { border-bottom: 1px solid #eee; padding: 8px; text-align: left; }
.error { color: #d33; margin-bottom: 8px; }
</style>
