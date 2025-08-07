<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const API_URL = 'https://b2b-wa72.onrender.com';
const productos = ref([]);
const productoActual = ref({
  id: null,
  nombre: '',
  descripcion: '',
  precio: 0,
  stock: 0
});
const modoEdicion = ref(false);

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

// Cargar productos al montar el componente
onMounted(() => {
  obtenerProductos();
});
</script>

<template>
  <div class="container mt-4">
    <h2>Gestión de Productos</h2>
    
    <!-- Formulario de Producto -->
    <div class="card mb-4">
      <div class="card-header">
        {{ modoEdicion ? 'Editar Producto' : 'Nuevo Producto' }}
      </div>
      <div class="card-body">
        <form @submit.prevent="guardarProducto">
          <div class="mb-3">
            <label class="form-label">Nombre</label>
            <input v-model="productoActual.nombre" type="text" class="form-control" required>
          </div>
          <div class="mb-3">
            <label class="form-label">Descripción</label>
            <textarea v-model="productoActual.descripcion" class="form-control"></textarea>
          </div>
          <div class="row">
            <div class="col-md-6 mb-3">
              <label class="form-label">Precio</label>
              <input v-model.number="productoActual.precio" type="number" step="0.01" class="form-control" required>
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label">Stock</label>
              <input v-model.number="productoActual.stock" type="number" class="form-control" required>
            </div>
          </div>
          <div class="d-flex gap-2">
            <button type="submit" class="btn btn-primary">
              {{ modoEdicion ? 'Actualizar' : 'Guardar' }}
            </button>
            <button v-if="modoEdicion" type="button" class="btn btn-secondary" @click="limpiarFormulario">
              Cancelar
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Tabla de Productos -->
    <div class="card">
      <div class="card-header">
        Lista de Productos
      </div>
      <div class="card-body">
        <div v-if="productos.length === 0" class="alert alert-info">
          No hay productos registrados.
        </div>
        <div v-else class="table-responsive">
          <table class="table table-striped">
            <thead>
              <tr>
                <th>ID</th>
                <th>Nombre</th>
                <th>Descripción</th>
                <th>Precio</th>
                <th>Stock</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="producto in productos" :key="producto.id">
                <td>{{ producto.id }}</td>
                <td>{{ producto.nombre }}</td>
                <td>{{ producto.descripcion }}</td>
                <td>${{ producto.precio.toFixed(2) }}</td>
                <td>{{ producto.stock }}</td>
                <td>
                  <button @click="obtenerProducto(producto.id)" class="btn btn-sm btn-warning me-2">
                    Editar
                  </button>
                  <button @click="eliminarProducto(producto.id)" class="btn btn-sm btn-danger">
                    Eliminar
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.table th, .table td {
  vertical-align: middle;
}

.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
}
</style>
