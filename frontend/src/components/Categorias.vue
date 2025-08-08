<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const API_URL = 'https://b2b-wa72.onrender.com';
const categorias = ref([]);
const categoriaActual = ref({
  id: null,
  nombre: '',
  descripcion: ''
});
const modoEdicion = ref(false);

// Obtener todas las categorías
const obtenerCategorias = async () => {
  try {
    const { data } = await axios.get(`${API_URL}/categorias`);
    categorias.value = data;
  } catch (error) {
    console.error('Error al obtener categorías:', error);
    alert('Error al cargar las categorías');
  }
};

// Obtener una categoría por ID
const obtenerCategoria = async (id) => {
  try {
    const { data } = await axios.get(`${API_URL}/categorias/${id}`);
    categoriaActual.value = data;
    modoEdicion.value = true;
  } catch (error) {
    console.error('Error al obtener la categoría:', error);
    alert('Error al cargar la categoría');
  }
};

// Crear una nueva categoría
const crearCategoria = async () => {
  try {
    await axios.post(`${API_URL}/categorias`, categoriaActual.value);
    limpiarFormulario();
    await obtenerCategorias();
  } catch (error) {
    console.error('Error al crear la categoría:', error);
    alert('Error al crear la categoría');
  }
};

// Actualizar una categoría existente
const actualizarCategoria = async () => {
  try {
    await axios.put(
      `${API_URL}/categorias/${categoriaActual.value.id}`,
      categoriaActual.value
    );
    limpiarFormulario();
    await obtenerCategorias();
  } catch (error) {
    console.error('Error al actualizar la categoría:', error);
    alert('Error al actualizar la categoría');
  }
};

// Eliminar una categoría
const eliminarCategoria = async (id) => {
  if (!confirm('¿Está seguro de eliminar esta categoría? Esto no afectará los productos existentes.')) {
    return;
  }
  
  try {
    await axios.delete(`${API_URL}/categorias/${id}`);
    await obtenerCategorias();
  } catch (error) {
    console.error('Error al eliminar la categoría:', error);
    alert('No se pudo eliminar la categoría. Asegúrese de que no tenga productos asociados.');
  }
};

// Guardar o actualizar categoría
const guardarCategoria = () => {
  if (modoEdicion.value) {
    actualizarCategoria();
  } else {
    crearCategoria();
  }
};

// Limpiar el formulario
const limpiarFormulario = () => {
  categoriaActual.value = {
    id: null,
    nombre: '',
    descripcion: ''
  };
  modoEdicion.value = false;
};

// Cargar categorías al montar el componente
onMounted(() => {
  obtenerCategorias();
});
</script>

<template>
  <div class="categorias-container">
    <h2>Gestión de Categorías</h2>
    
    <!-- Formulario de Categoría -->
    <div class="form-container">
      <h3>{{ modoEdicion ? 'Editar Categoría' : 'Nueva Categoría' }}</h3>
      <form @submit.prevent="guardarCategoria" class="categoria-form">
        <div class="form-group">
          <label for="nombre">Nombre:</label>
          <input 
            type="text" 
            id="nombre" 
            v-model="categoriaActual.nombre" 
            required
            maxlength="50"
          >
        </div>
        <div class="form-group">
          <label for="descripcion">Descripción:</label>
          <textarea 
            id="descripcion" 
            v-model="categoriaActual.descripcion"
            maxlength="500"
          ></textarea>
        </div>
        <div class="form-actions">
          <button type="submit" class="btn-save">
            {{ modoEdicion ? 'Actualizar' : 'Guardar' }}
          </button>
          <button 
            v-if="modoEdicion" 
            type="button" 
            @click="limpiarFormulario" 
            class="btn-cancel"
          >
            Cancelar
          </button>
        </div>
      </form>
    </div>

    <!-- Lista de Categorías -->
    <div class="categorias-list">
      <h3>Lista de Categorías</h3>
      <table class="categorias-table">
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Descripción</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="categoria in categorias" :key="categoria.id">
            <td>{{ categoria.nombre }}</td>
            <td>{{ categoria.descripcion || 'Sin descripción' }}</td>
            <td class="actions">
              <button 
                @click="obtenerCategoria(categoria.id)" 
                class="btn-edit"
              >
                Editar
              </button>
              <button 
                @click="eliminarCategoria(categoria.id)" 
                class="btn-delete"
              >
                Eliminar
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.categorias-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

h2, h3 {
  color: #2c3e50;
  margin-bottom: 20px;
}

.form-container {
  background: #f9f9f9;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 30px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.categoria-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

label {
  font-weight: 600;
  color: #555;
}

input[type="text"],
textarea {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

textarea {
  min-height: 80px;
  resize: vertical;
}

.form-actions {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.categorias-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 15px;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.categorias-table th,
.categorias-table td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.categorias-table th {
  background-color: #f5f5f5;
  font-weight: 600;
  color: #333;
}

.categorias-table tbody tr:hover {
  background-color: #f9f9f9;
}

.actions {
  display: flex;
  gap: 8px;
  justify-content: flex-start;
}

.btn-save,
.btn-edit,
.btn-delete,
.btn-cancel {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s ease;
}

.btn-save {
  background-color: #4CAF50;
  color: white;
}

.btn-save:hover {
  background-color: #45a049;
}

.btn-edit {
  background-color: #2196F3;
  color: white;
}

.btn-edit:hover {
  background-color: #0b7dda;
}

.btn-delete {
  background-color: #f44336;
  color: white;
}

.btn-delete:hover {
  background-color: #da190b;
}

.btn-cancel {
  background-color: #9e9e9e;
  color: white;
}

.btn-cancel:hover {
  background-color: #757575;
}

@media (max-width: 768px) {
  .categorias-container {
    padding: 10px;
  }
  
  .categorias-table {
    display: block;
    overflow-x: auto;
  }
  
  .actions {
    flex-direction: column;
    gap: 5px;
  }
  
  .btn-save,
  .btn-edit,
  .btn-delete,
  .btn-cancel {
    width: 100%;
    margin-bottom: 5px;
  }
}
</style>
