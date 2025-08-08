<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';

const API_URL = 'https://b2b-wa72.onrender.com/api/v1';
const productos = ref([]);
const productosFiltrados = ref([]);
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
const mostrarFormulario = ref(false);
const busqueda = ref('');

// Imágenes de ejemplo para las categorías
const imagenesCategorias = {
  'cereales': 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=880&q=80',
  'caramelos': 'https://images.unsplash.com/photo-1575224526795-35d2411f9b4e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=880&q=80',
  'panaderia': 'https://images.unsplash.com/photo-1509440159596-0249088772ff?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1472&q=80',
  'default': 'https://images.unsplash.com/photo-1542838132-92c53300491e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80'
};

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
    productosFiltrados.value = [...data];
  } catch (error) {
    console.error('Error al obtener productos:', error);
    alert('Error al cargar los productos');
  }
};

// Obtener un producto por ID
const obtenerProducto = async (id) => {
  try {
    console.log(`Obteniendo producto con ID: ${id}`);
    const { data } = await axios.get(`${API_URL}/productos/${id}`);
    
    if (!data) {
      throw new Error('No se recibieron datos del producto');
    }
    
    console.log('Datos del producto recibidos:', data);
    
    // Asegurarse de que los campos numéricos sean números
    productoActual.value = {
      ...data,
      precio: parseFloat(data.precio) || 0,
      stock: parseInt(data.stock) || 0
    };
    
    modoEdicion.value = true;
    mostrarFormulario.value = true;
    
  } catch (error) {
    console.error('Error al obtener el producto:', error);
    alert(`Error al cargar el producto: ${error.response?.data?.detail || error.message}`);
  }
};

// Crear un nuevo producto
const crearProducto = async () => {
  try {
    console.log('Creando producto con datos:', JSON.stringify(productoActual.value, null, 2));
    
    // Asegurarse de que los campos numéricos sean números
    const datosProducto = {
      ...productoActual.value,
      precio: parseFloat(productoActual.value.precio),
      stock: parseInt(productoActual.value.stock, 10)
    };
    
    console.log('Datos del producto a enviar:', JSON.stringify(datosProducto, null, 2));
    
    const response = await axios.post(`${API_URL}/productos`, datosProducto);
    console.log('Respuesta del servidor:', response.data);
    console.log('Status de respuesta:', response.status);
    // Si no se lanza excepción, consideramos la creación exitosa
    await obtenerProductos();
    cerrarFormulario();
    alert('Producto creado exitosamente');
  } catch (error) {
    console.error('Error al crear el producto:', error);
    
    let errorMessage = 'Error al crear el producto';
    
    if (error.response) {
      console.error('Detalles del error del servidor:', error.response.data);
      
      if (error.response.status === 400) {
        errorMessage = error.response.data?.detail || 'Datos de entrada inválidos';
      } else if (error.response.data?.message) {
        errorMessage = error.response.data.message;
      } else if (error.response.data?.detail) {
        errorMessage = error.response.data.detail;
      }
    } else if (error.request) {
      errorMessage = 'No se pudo conectar con el servidor. Verifica tu conexión a internet.';
    }
    
    alert(errorMessage);
  }
};

// Actualizar un producto existente
const actualizarProducto = async () => {
  try {
    console.log('Actualizando producto con ID:', productoActual.value.id);
    console.log('Datos a enviar:', productoActual.value);
    
    const response = await axios.put(
      `${API_URL}/productos/${productoActual.value.id}`, 
      productoActual.value
    );
    
    console.log('Respuesta del servidor:', response.data);
    console.log('Status de respuesta:', response.status);
    
    // Verificar que la respuesta sea exitosa (status 200 para actualización)
    if (response.status === 200 && response.data) {
      alert('Producto actualizado correctamente');
      await obtenerProductos();
      cerrarFormulario();
    } else {
      throw new Error(`Error en la respuesta del servidor. Status: ${response.status}`);
    }
  } catch (error) {
    console.error('Error al actualizar el producto:', error);
    
    let errorMessage = 'Error al actualizar el producto';
    
    if (error.response) {
      if (error.response.status === 400) {
        errorMessage = error.response.data?.detail || 'Datos de entrada inválidos';
      } else if (error.response.status === 404) {
        errorMessage = 'El producto no fue encontrado';
      } else if (error.response.status === 500) {
        errorMessage = 'Error en el servidor al actualizar el producto';
      } else if (error.response.data?.detail) {
        errorMessage = error.response.data.detail;
      }
    } else if (error.request) {
      errorMessage = 'No se pudo conectar con el servidor. Verifica tu conexión a internet.';
    }
    
    alert(errorMessage);
  }
};

// Eliminar un producto
const confirmarEliminar = (id) => {
  if (confirm('¿Estás seguro de eliminar este producto?')) {
    eliminarProducto(id);
  }
};

const eliminarProducto = async (id) => {
  try {
    console.log(`Eliminando producto con ID: ${id}`);
    const response = await axios.delete(`${API_URL}/productos/${id}`);
    
    if (response.status === 200 || response.status === 204) {
      console.log('Producto eliminado exitosamente');
      alert('Producto eliminado correctamente');
      await obtenerProductos();
    } else {
      throw new Error(`Respuesta inesperada del servidor: ${response.status}`);
    }
  } catch (error) {
    console.error('Error al eliminar el producto:', error);
    let errorMessage = 'Error al eliminar el producto';
    
    if (error.response) {
      // El servidor respondió con un código de estado fuera del rango 2xx
      if (error.response.status === 404) {
        errorMessage = 'El producto no fue encontrado o ya fue eliminado';
      } else if (error.response.status === 500) {
        errorMessage = 'Error en el servidor al intentar eliminar el producto';
      } else if (error.response.data?.detail) {
        errorMessage = error.response.data.detail;
      }
    } else if (error.request) {
      // La petición fue hecha pero no se recibió respuesta
      errorMessage = 'No se pudo conectar con el servidor. Por favor, verifica tu conexión a internet.';
    }
    
    alert(errorMessage);
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

// Manejo del formulario
const abrirFormulario = () => {
  mostrarFormulario.value = true;
};

const cerrarFormulario = () => {
  mostrarFormulario.value = false;
  limpiarFormulario();
};

// Limpiar formulario
const limpiarFormulario = () => {
  productoActual.value = {
    id: null,
    nombre: '',
    descripcion: '',
    precio: 0,
    stock: 0,
    categoria_id: '',
    // Incluir todos los campos que espera el backend, incluso si son opcionales
    imagen_url: null,
    // Agregar cualquier otro campo que pueda ser necesario
  };
  modoEdicion.value = false;
  // Limpiar cualquier mensaje de error previo
  errorMensaje.value = '';
};

// Obtener imagen del producto basada en la categoría
const obtenerImagenProducto = (producto) => {
  const categoria = categorias.value.find(cat => cat.id === producto.categoria_id);
  if (categoria) {
    const nombreCategoria = categoria.nombre.toLowerCase();
    return imagenesCategorias[nombreCategoria] || imagenesCategorias.default;
  }
  return imagenesCategorias.default;
};

// Filtrar productos por búsqueda
const filtrarProductos = () => {
  if (!busqueda.value.trim()) {
    productosFiltrados.value = [...productos.value];
    return;
  }
  
  const busquedaLower = busqueda.value.toLowerCase();
  productosFiltrados.value = productos.value.filter(producto => {
    return (
      producto.nombre.toLowerCase().includes(busquedaLower) ||
      (producto.descripcion && producto.descripcion.toLowerCase().includes(busquedaLower)) ||
      obtenerNombreCategoria(producto.categoria_id).toLowerCase().includes(busquedaLower)
    );
  });
};

// Alias para editar producto
const editarProducto = (id) => {
  obtenerProducto(id);
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
    <!-- Botón flotante para agregar producto -->
    <button class="add-product-btn" @click="abrirFormulario">
      <i class="fas fa-plus"></i>
    </button>

    <!-- Formulario flotante -->
    <div class="form-overlay" v-if="mostrarFormulario" @click.self="cerrarFormulario">
      <div class="form-container">
        <div class="form-header">
          <h3>{{ modoEdicion ? 'Editar Producto' : 'Nuevo Producto' }}</h3>
          <button class="close-btn" @click="cerrarFormulario">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <form @submit.prevent="guardarProducto" class="product-form">
          <div class="form-group">
            <label for="nombre">Nombre</label>
            <input type="text" id="nombre" v-model="productoActual.nombre" required>
          </div>
          <div class="form-group">
            <label for="descripcion">Descripción</label>
            <textarea id="descripcion" v-model="productoActual.descripcion" rows="3"></textarea>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label for="precio">Precio ($)</label>
              <input type="number" id="precio" v-model.number="productoActual.precio" min="0" step="0.01" required>
            </div>
            <div class="form-group">
              <label for="stock">Stock</label>
              <input type="number" id="stock" v-model.number="productoActual.stock" min="0" required>
            </div>
          </div>
          <div class="form-group">
            <label for="categoria">Categoría</label>
            <select id="categoria" v-model="productoActual.categoria_id" required>
              <option value="" disabled>Seleccione una categoría</option>
              <option v-for="categoria in categorias" :key="categoria.id" :value="categoria.id">
                {{ categoria.nombre }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label for="imagen_url">URL de la Imagen (opcional)</label>
            <input type="url" id="imagen_url" v-model="productoActual.imagen_url" placeholder="https://ejemplo.com/imagen.jpg">
          </div>
          <div class="form-actions">
            <button type="button" @click="cerrarFormulario" class="btn btn-outline">
              Cancelar
            </button>
            <button type="submit" class="btn btn-primary">
              {{ modoEdicion ? 'Actualizar' : 'Guardar' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Filtros y búsqueda -->
    <div class="filters-container">
      <div class="search-box">
        <i class="fas fa-search"></i>
        <input 
          type="text" 
          v-model="busqueda" 
          placeholder="Buscar productos..."
          @input="filtrarProductos"
        >
      </div>
      <div class="filter-actions">
        <button class="btn btn-outline" @click="abrirFormulario">
          <i class="fas fa-plus"></i> Nuevo Producto
        </button>
      </div>
    </div>

    <!-- Listado de productos en tarjetas -->
    <div class="products-grid">
      <div v-if="productosFiltrados.length === 0" class="no-products">
        <i class="fas fa-box-open"></i>
        <p>No se encontraron productos</p>
        <button class="btn btn-primary" @click="abrirFormulario">
          Agregar Producto
        </button>
      </div>

      <div v-else class="product-cards">
        <div v-for="producto in productosFiltrados" :key="producto.id" class="product-card">
          <div class="product-image">
            <img :src="obtenerImagenProducto(producto)" :alt="producto.nombre">
            <div class="product-badge" :class="{'in-stock': producto.stock > 0, 'out-of-stock': producto.stock <= 0}">
              {{ producto.stock > 0 ? 'En stock' : 'Agotado' }}
            </div>
          </div>
          <div class="product-info">
            <div class="product-category">
              {{ obtenerNombreCategoria(producto.categoria_id) }}
            </div>
            <h3 class="product-name">{{ producto.nombre }}</h3>
            <p class="product-description" v-if="producto.descripcion">
              {{ producto.descripcion }}
            </p>
            <div class="product-footer">
              <span class="product-price">${{ producto.precio.toFixed(2) }}</span>
              <div class="product-actions">
                <button class="action-btn edit" @click="editarProducto(producto.id)" title="Editar">
                  <i class="fas fa-edit"></i>
                </button>
                <button class="action-btn delete" @click="confirmarEliminar(producto.id)" title="Eliminar">
                  <i class="fas fa-trash"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Base Styles */
.productos-container {
  padding: 2rem 1.5rem;
  max-width: 1400px;
  margin: 0 auto;
  position: relative;
}

/* Floating Action Button */
.add-product-btn {
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
  transition: all 0.3s ease;
}

.add-product-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.3);
}

/* Form Overlay */
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

/* Form Container */
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

/* Form Header */
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
}

.close-btn:hover {
  color: var(--danger);
}

/* Form Styles */
.product-form {
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

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1.25rem;
}

/* Form Buttons */
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border);
}

.btn {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  border: 2px solid transparent;
}

.btn i {
  font-size: 1rem;
}

.btn-primary {
  background-color: var(--primary);
  color: var(--text);
  border-color: var(--primary);
}

.btn-primary:hover {
  background-color: #e6c200;
  border-color: #e6c200;
  transform: translateY(-1px);
}

.btn-outline {
  background-color: transparent;
  border-color: var(--border);
  color: var(--text);
}

.btn-outline:hover {
  background-color: #f8f8f8;
  border-color: #ddd;
}

/* Search and Filter */
.filters-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
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

/* Products Grid */
.products-grid {
  margin-top: 2rem;
}

.products-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.products-title {
  font-size: 1.75rem;
  color: var(--text);
  margin: 0;
  font-weight: 700;
}

.products-count {
  color: var(--text-muted);
  font-size: 0.95rem;
}

.product-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

/* Product Card */
.product-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  display: flex;
  flex-direction: column;
  height: 100%;
  border: 1px solid var(--border);
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.product-image {
  position: relative;
  height: 180px;
  overflow: hidden;
  background-color: #f8f9fa;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.product-card:hover .product-image img {
  transform: scale(1.05);
}

.product-badge {
  position: absolute;
  top: 1rem;
  right: 1rem;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  z-index: 1;
}

.in-stock {
  background-color: rgba(76, 175, 80, 0.9);
  color: white;
}

.out-of-stock {
  background-color: rgba(244, 67, 54, 0.9);
  color: white;
}

.product-info {
  padding: 1.5rem;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.product-category {
  font-size: 0.85rem;
  color: var(--primary);
  font-weight: 600;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.product-name {
  font-size: 1.25rem;
  font-weight: 700;
  margin: 0 0 0.75rem 0;
  color: var(--text);
  line-height: 1.3;
}

.product-description {
  color: var(--text-muted);
  font-size: 0.95rem;
  line-height: 1.5;
  margin-bottom: 1.25rem;
  flex: 1;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.product-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border);
}

.product-price {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text);
}

.product-stock {
  font-size: 0.9rem;
  color: var(--text-muted);
}

.product-actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: 1px solid var(--border);
  color: var(--text-muted);
  cursor: pointer;
  transition: all 0.2s;
  font-size: 1rem;
}

.action-btn:hover {
  background: #f8f9fa;
  transform: translateY(-2px);
}

.action-btn.edit {
  color: var(--primary);
  border-color: var(--primary);
}

.action-btn.edit:hover {
  background-color: rgba(255, 193, 7, 0.1);
  color: var(--primary);
}

.action-btn.delete {
  color: var(--danger);
  border-color: var(--danger);
}

.action-btn.delete:hover {
  background-color: rgba(244, 67, 54, 0.1);
  color: var(--danger);
}

/* No Products Message */
.no-products {
  grid-column: 1 / -1;
  text-align: center;
  padding: 3rem 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  margin-top: 1.5rem;
}

.no-products h3 {
  color: var(--text);
  margin-bottom: 0.5rem;
}

.no-products p {
  color: var(--text-muted);
  margin-bottom: 1.5rem;
}

/* Responsive Styles */
@media (max-width: 1200px) {
  .product-cards {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  }
}

@media (max-width: 992px) {
  .products-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .search-box {
    max-width: 100%;
    width: 100%;
  }
}

@media (max-width: 768px) {
  .productos-container {
    padding: 1.5rem 1rem;
  }
  
  .form-row {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }
  
  .form-actions {
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .btn {
    width: 100%;
  }
  
  .product-cards {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1.25rem;
  }
  
  .product-footer {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
  
  .product-actions {
    width: 100%;
    justify-content: flex-end;
  }
}

@media (max-width: 480px) {
  .product-cards {
    grid-template-columns: 1fr;
  }
  
  .form-container {
    margin: 1rem;
    max-height: 90vh;
  }
  
  .product-card {
    max-width: 100%;
  }
  
  .btn-icon {
    width: 32px;
    height: 32px;
  }
}
</style>
