<template>
  <div class="categories-section">
    <div class="header">
      <h2>Categorías</h2>
      <button @click="showModal = true" class="btn-add">
        Nueva Categoría
      </button>
    </div>

    <!-- Lista de categorías -->
    <div class="categories-grid">
      <div 
        v-for="category in categories" 
        :key="category.id" 
        class="category-card"
      >
        <div class="card-content">
          <h3>{{ category.name }}</h3>
          <p>{{ category.description || 'Sin descripción' }}</p>
          <div class="card-actions">
            <button @click="editCategory(category)" class="btn-edit">
              Editar
            </button>
            <button @click="deleteCategory(category.id)" class="btn-delete">
              Eliminar
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de formulario -->
    <div v-if="showModal" class="modal" @click.self="closeModal">
      <div class="modal-content">
        <h3>{{ editing ? 'Editar Categoría' : 'Nueva Categoría' }}</h3>
        
        <form @submit.prevent="saveCategory">
          <div class="form-group">
            <label>Nombre *</label>
            <input 
              v-model="form.name" 
              type="text" 
              required 
              maxlength="100"
            />
          </div>
          
          <div class="form-group">
            <label>Descripción</label>
            <textarea 
              v-model="form.description" 
              maxlength="500"
            ></textarea>
          </div>
          
          <div class="form-actions">
            <button type="button" @click="closeModal" class="btn-cancel">
              Cancelar
            </button>
            <button type="submit" :disabled="loading" class="btn-save">
              {{ loading ? 'Guardando...' : 'Guardar' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { categoriesService } from '@/services/api'

// Estado
const categories = ref([])
const showModal = ref(false)
const loading = ref(false)
const editing = ref(false)
const currentCategoryId = ref(null)

// Formulario
const form = reactive({
  name: '',
  description: '',
})

// Cargar categorías
const loadCategories = async () => {
  try {
    const response = await categoriesService.getAll()
    categories.value = response.data || response
  } catch (error) {
    console.error('Error loading categories:', error)
  }
}

// Guardar categoría
const saveCategory = async () => {
  try {
    loading.value = true
    
    const categoryData = {
      name: form.name,
      description: form.description,
    }
    
    if (editing.value && currentCategoryId.value) {
      await categoriesService.update(currentCategoryId.value, categoryData)
    } else {
      await categoriesService.create(categoryData)
    }
    
    closeModal()
    await loadCategories()
  } catch (error) {
    console.error('Error saving category:', error)
  } finally {
    loading.value = false
  }
}

// Editar categoría
const editCategory = (category) => {
  form.name = category.name
  form.description = category.description
  currentCategoryId.value = category.id
  editing.value = true
  showModal.value = true
}

// Eliminar categoría
const deleteCategory = async (id) => {
  if (confirm('¿Estás seguro de eliminar esta categoría?')) {
    try {
      await categoriesService.delete(id)
      await loadCategories()
    } catch (error) {
      console.error('Error deleting category:', error)
    }
  }
}

// Cerrar modal
const closeModal = () => {
  showModal.value = false
  editing.value = false
  currentCategoryId.value = null
  form.name = ''
  form.description = ''
}

// Lifecycle
onMounted(() => {
  loadCategories()
})
</script>

<style scoped>
.categories-section {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.header h2 {
  margin: 0;
}

.btn-add {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.categories-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.category-card {
  padding: 1.5rem;
}

.category-card h3 {
  margin: 0 0 0.5rem 0;
}

.category-card p {
  margin: 0 0 1rem 0;
}

.card-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-edit, .btn-delete {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.875rem;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  max-width: 500px;
  width: 90%;
}

.modal-content h3 {
  margin: 0 0 1.5rem 0;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 1.5rem;
}

.btn-save,
.btn-cancel {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
</style>
