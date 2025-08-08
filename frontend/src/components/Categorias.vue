<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';

const API_URL = 'https://b2b-wa72.onrender.com/api/v1';
const categorias = ref([]);
const categoriasFiltradas = ref([]);
const busqueda = ref('');
const mostrarFormulario = ref(false);
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
    categoriasFiltradas.value = [...data];
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
    mostrarFormulario.value = true;
  } catch (error) {
    console.error('Error al obtener la categoría:', error);
    alert('Error al cargar la categoría');
  }
};

// Crear una nueva categoría
const crearCategoria = async () => {
  // Validación básica del formulario
  if (!categoriaActual.value.nombre || categoriaActual.value.nombre.trim() === '') {
    alert('El nombre de la categoría es obligatorio');
    return;
  }

  try {
    // Limpiar el nombre de espacios en blanco al inicio/fin
    const categoriaData = {
      ...categoriaActual.value,
      nombre: categoriaActual.value.nombre.trim(),
      descripcion: categoriaActual.value.descripcion ? categoriaActual.value.descripcion.trim() : ''
    };

    const { data } = await axios.post(`${API_URL}/categorias`, categoriaData);
    
    // Mostrar mensaje de éxito
    alert('Categoría creada exitosamente');
    
    // Actualizar la lista de categorías
    await obtenerCategorias();
    cerrarFormulario();
  } catch (error) {
    console.error('Error al crear la categoría:', error);
    
    // Manejo de errores específicos
    if (error.response) {
      // Error de validación del servidor
      if (error.response.status === 400) {
        alert(error.response.data.detail || 'Error de validación: ' + JSON.stringify(error.response.data));
      } else if (error.response.status === 500) {
        alert('Error en el servidor al crear la categoría');
      } else {
        alert(`Error ${error.response.status}: ${error.response.data?.detail || 'Error desconocido'}`);
      }
    } else if (error.request) {
      // La petición fue hecha pero no hubo respuesta
      alert('No se pudo conectar con el servidor. Por favor, verifica tu conexión a internet.');
    } else {
      // Error al configurar la petición
      alert('Error al configurar la petición: ' + error.message);
    }
  }
};

// Actualizar una categoría existente
const actualizarCategoria = async () => {
  try {
    await axios.put(
      `${API_URL}/categorias/${categoriaActual.value.id}`,
      categoriaActual.value
    );
    await obtenerCategorias();
    cerrarFormulario();
  } catch (error) {
    console.error('Error al actualizar la categoría:', error);
    alert('Error al actualizar la categoría');
  }
};

// Confirmar eliminación
const confirmarEliminar = (id) => {
  if (confirm('¿Está seguro de eliminar esta categoría? Esto no afectará los productos existentes.')) {
    eliminarCategoria(id);
  }
};

// Eliminar una categoría
const eliminarCategoria = async (id) => {
  try {
    await axios.delete(`${API_URL}/categorias/${id}`);
    await obtenerCategorias();
  } catch (error) {
    console.error('Error al eliminar la categoría:', error);
    alert('No se pudo eliminar la categoría. Asegúrese de que no tenga productos asociados.');
  }
};

// Estado de carga
const isLoading = ref(false);

// Guardar o actualizar categoría
const guardarCategoria = async () => {
  // No hacer nada si ya hay una operación en curso
  if (isLoading.value) return;
  
  try {
    isLoading.value = true;
    
    if (modoEdicion.value) {
      await actualizarCategoria();
    } else {
      await crearCategoria();
    }
  } catch (error) {
    console.error('Error al guardar la categoría:', error);
    // El manejo de errores específicos ya está en las funciones individuales
  } finally {
    isLoading.value = false;
  }
};

// Abrir formulario para nueva categoría
const abrirFormulario = () => {
  mostrarFormulario.value = true;
  modoEdicion.value = false;
  limpiarFormulario();
};

// Cerrar formulario
const cerrarFormulario = () => {
  mostrarFormulario.value = false;
  limpiarFormulario();
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

// Filtrar categorías por búsqueda
const filtrarCategorias = () => {
  if (!busqueda.value.trim()) {
    categoriasFiltradas.value = [...categorias.value];
    return;
  }
  
  const busquedaLower = busqueda.value.toLowerCase();
  categoriasFiltradas.value = categorias.value.filter(categoria => 
    categoria.nombre.toLowerCase().includes(busquedaLower) ||
    (categoria.descripcion && categoria.descripcion.toLowerCase().includes(busquedaLower))
  );
};

// Contador de productos por categoría (simulado - en una implementación real, esto vendría del backend)
const contarProductosPorCategoria = (categoriaId) => {
  // En una implementación real, esto debería venir del backend
  return Math.floor(Math.random() * 20); // Número aleatorio para demostración
};

// Cargar categorías al montar el componente
onMounted(() => {
  obtenerCategorias();
});
</script>

<template>
  <div class="categorias-container">
    <!-- Botón flotante para agregar categoría -->
    <button class="add-category-btn" @click="abrirFormulario">
      <i class="fas fa-plus"></i>
    </button>

    <!-- Filtros y búsqueda -->
    <div class="filters-container">
      <h1 class="categories-title">Gestión de Categorías</h1>
      <div class="search-box">
        <i class="fas fa-search"></i>
        <input 
          type="text" 
          v-model="busqueda" 
          @input="filtrarCategorias"
          placeholder="Buscar categorías..."
        >
      </div>
    </div>

    <!-- Overlay del formulario -->
    <div v-if="mostrarFormulario" class="form-overlay" @click.self="cerrarFormulario">
      <div class="form-container">
        <div class="form-header">
          <h3>{{ modoEdicion ? 'Editar Categoría' : 'Nueva Categoría' }}</h3>
          <button class="close-btn" @click="cerrarFormulario">&times;</button>
        </div>
        
        <form @submit.prevent="guardarCategoria" class="category-form">
          <div class="form-group">
            <label for="nombre">Nombre</label>
            <input 
              type="text" 
              id="nombre" 
              v-model="categoriaActual.nombre" 
              required
              maxlength="50"
              placeholder="Ej: Panadería"
            >
          </div>
          
          <div class="form-group">
            <label for="descripcion">Descripción</label>
            <textarea 
              id="descripcion" 
              v-model="categoriaActual.descripcion"
              maxlength="500"
              placeholder="Agrega una descripción para la categoría..."
              rows="4"
            ></textarea>
          </div>
          
          <div class="form-actions">
            <button type="button" class="btn btn-outline" @click="cerrarFormulario">
              <i class="fas fa-times"></i> Cancelar
            </button>
            <button type="submit" class="btn btn-primary" :disabled="isLoading">
              <span v-if="isLoading" class="btn-loader"></span>
              <i v-else class="fas fa-save"></i> 
              {{ isLoading ? 'Procesando...' : (modoEdicion ? 'Actualizar' : 'Guardar') }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Lista de Categorías -->
    <div class="categories-grid">
      <div class="categories-header">
        <h2 class="categories-count">{{ categoriasFiltradas.length }} Categorías</h2>
      </div>
      
      <div v-if="categoriasFiltradas.length === 0" class="no-categories">
        <h3>No se encontraron categorías</h3>
        <p>Intenta con otros términos de búsqueda o crea una nueva categoría.</p>
        <button class="btn btn-primary" @click="abrirFormulario">
          <i class="fas fa-plus"></i> Crear Categoría
        </button>
      </div>
      
      <div v-else class="category-cards">
        <div v-for="categoria in categoriasFiltradas" :key="categoria.id" class="category-card">
          <div class="category-info">
            <h3 class="category-name">{{ categoria.nombre }}</h3>
            <p class="category-description" v-if="categoria.descripcion">{{ categoria.descripcion }}</p>
            <p class="category-description empty" v-else>Sin descripción</p>
            <div class="category-stats">
              <span class="product-count">
                <i class="fas fa-box"></i> {{ contarProductosPorCategoria(categoria.id) }} productos
              </span>
            </div>
          </div>
          
          <div class="category-actions">
            <button class="btn-icon" @click="obtenerCategoria(categoria.id)" title="Editar">
              <i class="fas fa-edit"></i>
            </button>
            <button 
              class="btn-icon delete" 
              @click="confirmarEliminar(categoria.id)" 
              title="Eliminar"
            >
              <i class="fas fa-trash"></i>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Variables de colores */
:root {
  --primary: #FFD700;
  --primary-dark: #e6c200;
  --secondary: #2c3e50;
  --light: #f8f9fa;
  --dark: #343a40;
  --success: #28a745;
  --danger: #dc3545;
  --warning: #ffc107;
  --info: #17a2b8;
  --gray: #6c757d;
  --light-gray: #e9ecef;
  --border: #dee2e6;
  --text: #333;
  --text-muted: #6c757d;
  --white: #fff;
  --box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  --transition: all 0.3s ease;
}

/* Estilos generales */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  line-height: 1.6;
  color: var(--text);
  background-color: #f5f5f5;
}

h1, h2, h3, h4, h5, h6 {
  font-weight: 600;
  line-height: 1.2;
  margin-bottom: 1rem;
}

/* Contenedor principal */
.categorias-container {
  padding: 2rem 1.5rem;
  max-width: 1400px;
  margin: 0 auto;
  position: relative;
}

/* Botón flotante para agregar categoría */
.add-category-btn {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background-color: var(--primary);
  color: var(--text);
  border: none;
  font-size: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  cursor: pointer;
  z-index: 100;
  transition: var(--transition);
}

.add-category-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.3);
}

/* Títulos y encabezados */
.categories-title {
  font-size: 1.8rem;
  color: var(--text);
  margin: 0;
  font-weight: 700;
}

.categories-count {
  font-size: 1.2rem;
  color: var(--text-muted);
  font-weight: 500;
  margin: 0;
}

/* Filtros y búsqueda */
.filters-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1.5rem;
}

.search-box {
  position: relative;
  flex: 1;
  max-width: 400px;
  min-width: 250px;
}

.search-box i {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-muted);
}

.search-box input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  border: 1px solid var(--border);
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.2s;
  background-color: #fff;
}

.search-box input:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.2);
  outline: none;
}

/* Grid de categorías */
.categories-grid {
  margin-top: 2rem;
}

.categories-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

/* Tarjetas de categorías */
.category-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.category-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  display: flex;
  flex-direction: column;
  border: 1px solid var(--border);
  height: 100%;
}

.category-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.category-info {
  padding: 1.5rem;
  flex: 1;
}

.category-name {
  font-size: 1.25rem;
  font-weight: 700;
  margin: 0 0 0.75rem 0;
  color: var(--text);
  line-height: 1.3;
}

.category-description {
  color: var(--text-muted);
  font-size: 0.95rem;
  line-height: 1.5;
  margin-bottom: 1.25rem;
}

.category-description.empty {
  color: #aaa;
  font-style: italic;
}

.category-stats {
  display: flex;
  align-items: center;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border);
  font-size: 0.9rem;
  color: var(--text-muted);
}

.product-count {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.product-count i {
  color: var(--primary);
}

.category-actions {
  display: flex;
  justify-content: flex-end;
  padding: 1rem 1.5rem;
  border-top: 1px solid var(--border);
  gap: 0.5rem;
}

/* Botones */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-weight: 500;
  font-size: 0.95rem;
  cursor: pointer;
  transition: var(--transition);
  border: 1px solid transparent;
  gap: 0.5rem;
}

.btn i {
  font-size: 0.9em;
}

.btn-primary {
  background-color: var(--primary);
  color: var(--text);
  border-color: var(--primary);
}

.btn-primary:hover {
  background-color: var(--primary-dark);
  border-color: var(--primary-dark);
  transform: translateY(-1px);
}

.btn-outline {
  background-color: transparent;
  color: var(--text);
  border: 1px solid var(--border);
}

.btn-outline:hover {
  background-color: var(--light-gray);
  border-color: var(--gray);
}

.btn-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: 1px solid var(--border);
  color: var(--text);
  cursor: pointer;
  transition: var(--transition);
}

.btn-icon:hover {
  background-color: var(--light-gray);
  color: var(--primary);
}

.btn-icon.delete:hover {
  color: var(--danger);
  border-color: #f5c6cb;
  background-color: #f8d7da;
}

/* Loading spinner */
.btn-loader {
  display: inline-block;
  width: 1rem;
  height: 1rem;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: #fff;
  animation: spin 0.8s ease-in-out infinite;
  margin-right: 0.5rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Disabled button state */
.btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none !important;
}

/* Formulario */
.form-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
  backdrop-filter: blur(3px);
}

.form-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid var(--border);
}

.form-header h3 {
  margin: 0;
  font-size: 1.5rem;
  color: var(--text);
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: var(--text-muted);
  transition: color 0.2s;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.close-btn:hover {
  color: var(--danger);
  background-color: #f8d7da;
}

.category-form {
  padding: 1.5rem;
}

.form-group {
  margin-bottom: 1.25rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--text);
  font-size: 0.95rem;
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid var(--border);
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.2s, box-shadow 0.2s;
  background-color: #fff;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.2);
  outline: none;
}

.form-group textarea {
  min-height: 100px;
  resize: vertical;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border);
}

/* Estado vacío */
.no-categories {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  margin-top: 1.5rem;
}

.no-categories h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: var(--text);
}

.no-categories p {
  color: var(--text-muted);
  margin-bottom: 1.5rem;
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
}

/* Responsive */
@media (max-width: 768px) {
  .filters-container {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-box {
    max-width: 100%;
  }
  
  .category-cards {
    grid-template-columns: 1fr;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .btn {
    width: 100%;
  }
}

/* Animaciones */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.category-card {
  animation: fadeIn 0.3s ease-out forwards;
}

/* No additional styles needed - all styles have been consolidated above */

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
