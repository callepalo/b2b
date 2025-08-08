<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const API_URL = 'https://b2b-wa72.onrender.com';
const productos = ref([]);
const categorias = ref([]);
const productoActual = ref({
  id: null,
  nombre: '',
  descripcion: '',
  precio: 0,
  stock: 0,
  categoria_id: ''
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

// Obtener nombre de categoría por ID
const obtenerNombreCategoria = (id) => {
  const categoria = categorias.value.find(cat => cat.id === id);
  return categoria ? categoria.nombre : 'Sin categoría';
};

// Obtener todos los productos
const obtenerProductos = async () => {
  try {
    const { data } = await axios.get(`${API_URL}/productos`);
    productos.value = data;
  } catch (error) {
    console.error('Error al obtener productos:', error);
    alert('Error al cargar los productos');
  }
};

// Obtener un producto por ID
const obtenerProducto = async (id) => {
  try {
    const { data } = await axios.get(`${API_URL}/productos/${id}`);
    productoActual.value = data;
    modoEdicion.value = true;
  } catch (error) {
    console.error('Error al obtener el producto:', error);
    alert('Error al cargar el producto');
  }
};

// Crear un nuevo producto
const crearProducto = async () => {
  try {
    await axios.post(`${API_URL}/productos`, productoActual.value);
    limpiarFormulario();
    await obtenerProductos();
  } catch (error) {
    console.error('Error al crear el producto:', error);
    alert('Error al crear el producto');
  }
};

// Actualizar un producto existente
const actualizarProducto = async () => {
  try {
    await axios.put(`${API_URL}/productos/${productoActual.value.id}`, productoActual.value);
    limpiarFormulario();
    await obtenerProductos();
  } catch (error) {
    console.error('Error al actualizar el producto:', error);
    alert('Error al actualizar el producto');
  }
};

// Eliminar un producto
const eliminarProducto = async (id) => {
  if (!confirm('¿Estás seguro de eliminar este producto?')) return;
  
  try {
    await axios.delete(`${API_URL}/productos/${id}`);
    await obtenerProductos();
  } catch (error) {
    console.error('Error al eliminar el producto:', error);
    alert('Error al eliminar el producto');
  }
};

// Guardar o actualizar producto
const guardarProducto = () => {
  if (modoEdicion.value) {
    actualizarProducto();
  } else {
    crearProducto();
  }
};

// Limpiar formulario
const limpiarFormulario = () => {
  productoActual.value = {
    id: null,
    nombre: '',
    descripcion: '',
    precio: 0,
    stock: 0
  };
  modoEdicion.value = false;
};

// Cargar datos al montar el componente
onMounted(async () => {
  await Promise.all([
    obtenerProductos(),
    obtenerCategorias()
  ]);
});
</script>

<template>
  <div class="productos-container">
    <h2 class="titulo">Gestión de Productos</h2>
    
    <!-- Formulario de Producto -->
    <div class="form-container">
      <h3>{{ modoEdicion ? 'Editar Producto' : 'Nuevo Producto' }}</h3>
      <form @submit.prevent="guardarProducto" class="form-container">
        <div class="form-group">
          <label for="nombre">Nombre:</label>
          <input type="text" id="nombre" v-model="productoActual.nombre" required>
        </div>
        <div class="form-group">
          <label for="descripcion">Descripción:</label>
          <textarea id="descripcion" v-model="productoActual.descripcion"></textarea>
        </div>
        <div class="form-group">
          <label for="precio">Precio:</label>
          <input type="number" id="precio" v-model.number="productoActual.precio" min="0" step="0.01" required>
        </div>
        <div class="form-group">
          <label for="stock">Stock:</label>
          <input type="number" id="stock" v-model.number="productoActual.stock" min="0" required>
        </div>
        <div class="form-group">
          <label for="categoria">Categoría:</label>
          <select id="categoria" v-model="productoActual.categoria_id" required>
            <option value="" disabled>Seleccione una categoría</option>
            <option v-for="categoria in categorias" :key="categoria.id" :value="categoria.id">
              {{ categoria.nombre }}
            </option>
          </select>
        </div>
        <div class="form-actions">
          <button type="submit" class="btn-save">{{ modoEdicion ? 'Actualizar' : 'Guardar' }}</button>
          <button type="button" @click="limpiarFormulario" class="btn-cancel">Cancelar</button>
        </div>
      </form>
    </div>

    <!-- Tabla de Productos -->
    <div class="table-container">
      <h3>Lista de Productos</h3>
      <div v-if="productos.length === 0" class="no-products">
        No hay productos registrados.
      </div>
      <div v-else class="table-wrapper">
        <table class="products-table">
          <thead>
            <tr>
              <th>Nombre</th>
              <th>Descripción</th>
              <th>Precio</th>
              <th>Stock</th>
              <th>Categoría</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="producto in productos" :key="producto.id">
              <td>{{ producto.nombre }}</td>
              <td>{{ producto.descripcion || 'N/A' }}</td>
              <td>${{ producto.precio.toFixed(2) }}</td>
              <td>{{ producto.stock }}</td>
              <td>{{ obtenerNombreCategoria(producto.categoria_id) }}</td>
              <td class="actions">
                <button @click="obtenerProducto(producto.id)" class="btn-edit">
                  Editar
                </button>
                <button @click="eliminarProducto(producto.id)" class="btn-delete">
                  Eliminar
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<style scoped>
.productos-container {
  padding: 20px;
}

.titulo {
  color: var(--secondary);
  margin-bottom: 24px;
  font-size: 1.8rem;
}

/* Estilos del formulario */
.form-container {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 30px;
}

.form-container h3 {
  color: var(--secondary);
  margin-bottom: 20px;
  font-size: 1.4rem;
}

.product-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

label {
  font-weight: 500;
  color: var(--secondary);
}

input, textarea {
  padding: 10px 12px;
  border: 1px solid var(--border);
  border-radius: 4px;
  font-size: 1rem;
  width: 100%;
}

textarea {
  min-height: 80px;
  resize: vertical;
}

.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 10px;
}

button {
  padding: 10px 16px;
  border: none;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-save {
  background-color: var(--primary);
  color: white;
}

.btn-save:hover {
  opacity: 0.9;
}

.btn-cancel {
  background-color: #f0f0f0;
  color: #333;
}

.btn-cancel:hover {
  background-color: #e0e0e0;
}

/* Estilos de la tabla */
.table-container {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.table-container h3 {
  color: var(--secondary);
  margin-bottom: 20px;
  font-size: 1.4rem;
}

.no-products {
  color: #666;
  text-align: center;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 4px;
}

.table-wrapper {
  overflow-x: auto;
}

.products-table {
  width: 100%;
  border-collapse: collapse;
}

.products-table th,
.products-table td {
  padding: 12px 16px;
  text-align: left;
  border-bottom: 1px solid var(--border);
}

.products-table th {
  background-color: #f5f5f5;
  font-weight: 600;
  color: var(--secondary);
}

.products-table tbody tr:hover {
  background-color: #f9f9f9;
}

.actions {
  display: flex;
  gap: 8px;
}

.btn-edit {
  background-color: var(--warning);
  color: white;
  padding: 6px 12px;
  font-size: 0.85rem;
}

.btn-delete {
  background-color: var(--danger);
  color: white;
  padding: 6px 12px;
  font-size: 0.85rem;
}

.btn-edit:hover, .btn-delete:hover {
  opacity: 0.9;
}

/* Responsive */
@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .actions {
    flex-direction: column;
  }
  
  .products-table th,
  .products-table td {
    padding: 8px 12px;
  }
}

.table th, .table td {
  vertical-align: middle;
}

.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
}
</style>
