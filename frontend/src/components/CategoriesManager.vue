<script setup>
import { ref, onMounted, computed } from 'vue'
import { api } from '../services/api'

const categories = ref([])
const loading = ref(false)
const error = ref('')
const showForm = ref(false)

const editingId = ref(null)
const form = ref({
  name: '',
  description: '',
  slug: '',
  parent_id: ''
})

const isEditing = computed(() => !!editingId.value)

async function loadCategories() {
  loading.value = true
  error.value = ''
  try {
    const res = await api.listCategories({ per_page: 100 })
    categories.value = res.data || []
  } catch (e) {
    error.value = e.message || String(e)
  } finally {
    loading.value = false
  }
}

function resetForm() {
  editingId.value = null
  form.value = { name: '', description: '', slug: '', parent_id: '' }
  showForm.value = false
}

async function submitForm() {
  error.value = ''
  try {
    const payload = { ...form.value }
    if (!payload.parent_id) payload.parent_id = null

    if (isEditing.value) {
      await api.updateCategory(editingId.value, payload)
    } else {
      await api.createCategory(payload)
    }
    resetForm()
    await loadCategories()
  } catch (e) {
    error.value = e.message || String(e)
  }
}

function startEdit(c) {
  editingId.value = c.id
  form.value = {
    name: c.name || '',
    description: c.description || '',
    slug: c.slug || '',
    parent_id: c.parent_id || ''
  }
  showForm.value = true
}

async function removeCategory(id) {
  if (!confirm('¿Eliminar esta categoría?')) return
  try {
    await api.deleteCategory(id)
    await loadCategories()
  } catch (e) {
    alert(e.message || String(e))
  }
}

onMounted(loadCategories)
</script>

<template>
  <div class="cm">
    <h1>Categorías</h1>

    <div v-if="error" class="error">{{ error }}</div>

    <div class="toolbar">
      <button v-if="!isEditing" @click="showForm = !showForm" type="button">
        {{ showForm ? 'Cerrar' : 'Crear categoría' }}
      </button>
      <button v-else type="button" @click="resetForm">Salir de edición</button>
    </div>

    <form v-if="showForm || isEditing" class="form" @submit.prevent="submitForm">
      <h2>{{ isEditing ? 'Editar categoría' : 'Crear categoría' }}</h2>
      <div class="row">
        <label>Nombre</label>
        <input v-model="form.name" required />
      </div>
      <div class="row">
        <label>Slug</label>
        <input v-model="form.slug" required />
      </div>
      <div class="row">
        <label>Descripción</label>
        <textarea v-model="form.description" rows="3" />
      </div>
      <div class="row">
        <label>Padre</label>
        <select v-model="form.parent_id">
          <option value="">(sin padre)</option>
          <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.name }}</option>
        </select>
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
            <th>Nombre</th>
            <th>Slug</th>
            <th>Padre</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="c in categories" :key="c.id">
            <td>{{ c.name }}</td>
            <td>{{ c.slug }}</td>
            <td>{{ (categories.find(x => x.id === c.parent_id)?.name) || '-' }}</td>
            <td class="row-actions">
              <button @click="startEdit(c)">Editar</button>
              <button class="danger" @click="removeCategory(c.id)">Eliminar</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.cm { max-width: 960px; margin: 24px auto; padding: 0 12px; }
.toolbar { display: flex; gap: 8px; margin-bottom: 12px; }
.form { border: 1px solid #ddd; padding: 12px; border-radius: 6px; margin-bottom: 16px; }
.row { display: flex; flex-direction: column; gap: 6px; margin-bottom: 10px; }
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
