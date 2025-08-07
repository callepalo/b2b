<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

// Configuración del router
const router = useRouter();

// Estado de la aplicación
const apiStatus = ref('');
const loading = ref(true);
const error = ref(null);

// Verificar estado de la API al cargar el componente
onMounted(async () => {
  try {
    const response = await $http.get('/health');
    if (response.data) {
      apiStatus.value = response.data.status;
    }
  } catch (err) {
    console.error('Error al conectar con la API:', err);
    error.value = 'No se pudo conectar con el servidor';
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <!-- Barra de navegación -->
  <nav class="navbar navbar-expand-lg navbar-dark bg-primary mb-4">
    <div class="container">
      <router-link class="navbar-brand" to="/">
        <i class="bi bi-shop me-2"></i>Dulpromax
      </router-link>
      
      <button 
        class="navbar-toggler" 
        type="button" 
        data-bs-toggle="collapse" 
        data-bs-target="#navbarNav"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto">
          <li class="nav-item">
            <router-link class="nav-link" to="/" exact-active-class="active">
              <i class="bi bi-house-door me-1"></i> Inicio
            </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/productos" active-class="active">
              <i class="bi bi-box-seam me-1"></i> Productos
            </router-link>
          </li>
        </ul>
        
        <div class="d-flex align-items-center">
          <span 
            class="badge me-3" 
            :class="apiStatus === 'OK' ? 'bg-success' : 'bg-danger'"
            v-if="!loading && apiStatus"
          >
            <i class="bi bi-circle-fill me-1"></i>
            {{ apiStatus === 'OK' ? 'Conectado' : 'Desconectado' }}
          </span>
        </div>
      </div>
    </div>
  </nav>

  <!-- Contenido principal -->
  <main class="container">
    <!-- Mensajes de carga y error -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Cargando...</span>
      </div>
      <p class="mt-2 mb-0">Cargando aplicación...</p>
    </div>
    
    <div v-else-if="error" class="alert alert-danger">
      <i class="bi bi-exclamation-triangle me-2"></i>
      {{ error }}
    </div>
    
    <!-- Router view para el contenido dinámico -->
    <router-view v-else />
  </main>
  
  <!-- Footer -->
  <footer class="bg-light mt-5 py-3">
    <div class="container text-center">
      <p class="mb-0">
        &copy; {{ new Date().getFullYear() }} Dulpromax - Todos los derechos reservados
      </p>
    </div>
  </footer>
</template>

<style scoped>
.navbar {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.navbar-brand {
  font-weight: 600;
  font-size: 1.4rem;
}

.nav-link {
  font-weight: 500;
  transition: all 0.2s;
  padding: 0.5rem 1rem;
  border-radius: 4px;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.nav-link.active {
  background-color: rgba(255, 255, 255, 0.2);
  font-weight: 600;
}

footer {
  border-top: 1px solid #e9ecef;
  color: #6c757d;
  font-size: 0.9rem;
}
</style>
