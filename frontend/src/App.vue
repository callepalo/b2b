<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const API_URL = 'https://b2b-wa72.onrender.com';
const productos = ref([]);

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

// Cargar productos al montar el componente
onMounted(() => {
  obtenerProductos();
});
</script>

<template>
  <div class="container mt-5">
    <h1 class="mb-4">Lista de Productos</h1>
    
    <div v-if="productos.length === 0" class="alert alert-info">
      Cargando productos...
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
          </tr>
        </thead>
        <tbody>
          <tr v-for="producto in productos" :key="producto.id">
            <td>{{ producto.id }}</td>
            <td>{{ producto.nombre }}</td>
            <td>{{ producto.descripcion }}</td>
            <td>${{ producto.precio }}</td>
            <td>{{ producto.stock }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style>
/* Estilos básicos */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 15px;
}

.table {
  width: 100%;
  margin-bottom: 1rem;
  color: #212529;
}

.table th,
.table td {
  padding: 0.75rem;
  vertical-align: top;
  border-top: 1px solid #dee2e6;
}

.table thead th {
  vertical-align: bottom;
  border-bottom: 2px solid #dee2e6;
}

.table-striped tbody tr:nth-of-type(odd) {
  background-color: rgba(0, 0, 0, 0.05);
}

.alert {
  position: relative;
  padding: 0.75rem 1.25rem;
  margin-bottom: 1rem;
  border: 1px solid transparent;
  border-radius: 0.25rem;
}

.alert-info {
  color: #0c5460;
  background-color: #d1ecf1;
  border-color: #bee5eb;
}
</style>
