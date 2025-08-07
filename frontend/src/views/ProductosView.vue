<template>
  <div class="productos">
    <!-- Encabezado -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1 class="h3 mb-0">Listado de Productos</h1>
    </div>

    <!-- Estado de carga -->
    <div v-if="cargando" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Cargando...</span>
      </div>
      <p class="mt-2 mb-0">Cargando productos...</p>
    </div>

    <!-- Mensaje de error -->
    <div v-else-if="error" class="alert alert-danger">
      <i class="bi bi-exclamation-triangle me-2"></i>
      {{ error }}
    </div>

    <!-- Lista de productos -->
    <div v-else>
      <div v-if="productos.length === 0" class="text-center py-5">
        <div class="text-muted mb-3">
          <i class="bi bi-inbox" style="font-size: 3rem; opacity: 0.5;"></i>
          <p class="mt-3 mb-0">No hay productos registrados</p>
        </div>
      </div>

      <div v-else class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
        <div v-for="producto in productos" :key="producto.id" class="col">
          <div class="card h-100">
            <div class="position-relative">
              <img 
                :src="producto.imagen_url || 'https://via.placeholder.com/300x200?text=Sin+imagen'" 
                class="card-img-top" 
                :alt="producto.nombre"
                style="height: 180px; object-fit: cover;"
              >
              <span 
                class="position-absolute top-0 end-0 m-2 badge" 
                :class="producto.stock > 0 ? 'bg-success' : 'bg-danger'"
              >
                {{ producto.stock > 0 ? 'En stock' : 'Agotado' }}
              </span>
            </div>
            
            <div class="card-body">
              <h5 class="card-title">{{ producto.nombre }}</h5>
              <p class="card-text text-muted small">
                {{ producto.descripcion || 'Sin descripción' }}
              </p>
              
              <div class="d-flex justify-content-between align-items-center mt-3">
                <div>
                  <span class="h5 text-primary">${{ parseFloat(producto.precio).toFixed(2) }}</span>
                  <span class="text-muted ms-2">/unidad</span>
                </div>
                <div>
                  <span class="badge bg-secondary">{{ producto.categoria || 'Sin categoría' }}</span>
                </div>
              </div>
              
              <div class="d-flex justify-content-between align-items-center mt-3">
                <span class="text-muted small">
                  Stock: {{ producto.stock }}
                </span>
                <button 
                  class="btn btn-sm btn-outline-primary"
                  @click="verDetalle(producto.id)"
                >
                  <i class="bi bi-eye me-1"></i> Ver
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProductosView',
  data() {
    return {
      productos: [],
      cargando: true,
      error: null
    };
  },
  async created() {
    await this.cargarProductos();
  },
  methods: {
    async cargarProductos() {
      this.cargando = true;
      this.error = null;
      
      try {
        const response = await this.$http.get('/productos');
        this.productos = response.data || [];
      } catch (error) {
        console.error('Error al cargar productos:', error);
        this.error = 'No se pudieron cargar los productos. Intente de nuevo más tarde.';
      } finally {
        this.cargando = false;
      }
    },
    verDetalle(id) {
      // Esta función se implementará en la siguiente iteración
      console.log('Ver detalle del producto:', id);
    }
  }
};
</script>

<style scoped>
.card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 0.5rem 1.5rem rgba(0, 0, 0, 0.05) !important;
}
</style>
