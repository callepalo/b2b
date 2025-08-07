<template>
  <div class="home">
    <div class="text-center mb-5">
      <h1 class="display-4 mb-3">Bienvenido a Dulpromax</h1>
      <p class="lead text-muted">Sistema de gestión integral para tu negocio</p>
      
      <div class="row justify-content-center mt-5">
        <div class="col-md-8">
          <div class="card">
            <div class="card-body p-4">
              <h2 class="h4 mb-4">Acciones rápidas</h2>
              
              <div class="row g-4">
                <div class="col-md-6">
                  <div class="card h-100 border-0 shadow-sm">
                    <div class="card-body text-center">
                      <div class="bg-primary bg-opacity-10 p-3 rounded-circle d-inline-flex mb-3">
                        <i class="bi bi-box-seam fs-1 text-primary"></i>
                      </div>
                      <h3 class="h5 mb-3">Productos</h3>
                      <p class="text-muted mb-4">Administra tu catálogo de productos y su inventario.</p>
                      <router-link to="/productos" class="btn btn-primary">
                        <i class="bi bi-arrow-right me-1"></i> Gestionar productos
                      </router-link>
                    </div>
                  </div>
                </div>
                
                <div class="col-md-6">
                  <div class="card h-100 border-0 shadow-sm">
                    <div class="card-body text-center">
                      <div class="bg-success bg-opacity-10 p-3 rounded-circle d-inline-flex mb-3">
                        <i class="bi bi-graph-up fs-1 text-success"></i>
                      </div>
                      <h3 class="h5 mb-3">Reportes</h3>
                      <p class="text-muted mb-4">Visualiza informes y estadísticas de tu negocio.</p>
                      <button class="btn btn-outline-secondary" disabled>
                        <i class="bi bi-lock me-1"></i> Próximamente
                      </button>
                    </div>
                  </div>
                </div>
              </div>
              
              <div class="alert alert-info mt-4 mb-0">
                <i class="bi bi-info-circle me-2"></i>
                Selecciona una opción del menú superior para comenzar a gestionar tu negocio.
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="row mt-5">
      <div class="col-12">
        <div class="card border-0 shadow-sm">
          <div class="card-body">
            <h2 class="h4 mb-4">Estado del sistema</h2>
            
            <div class="table-responsive">
              <table class="table table-hover align-middle">
                <thead>
                  <tr>
                    <th>Servicio</th>
                    <th>Estado</th>
                    <th>Versión</th>
                    <th>Detalles</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>API Backend</td>
                    <td>
                      <span class="badge bg-success">
                        <i class="bi bi-check-circle me-1"></i> En línea
                      </span>
                    </td>
                    <td>1.0.0</td>
                    <td>API REST para gestión de datos</td>
                  </tr>
                  <tr>
                    <td>Base de datos</td>
                    <td>
                      <span class="badge bg-success">
                        <i class="bi bi-check-circle me-1"></i> Conectado
                      </span>
                    </td>
                    <td>PostgreSQL 14</td>
                    <td>Almacenamiento seguro de datos</td>
                  </tr>
                  <tr>
                    <td>Frontend</td>
                    <td>
                      <span class="badge bg-success">
                        <i class="bi bi-check-circle me-1"></i> Activo
                      </span>
                    </td>
                    <td>1.0.0</td>
                    <td>Interfaz de usuario moderna</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Lógica del componente
</script>

<style scoped>
.home {
  padding: 1rem 0;
}

.card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 0.5rem 1.5rem rgba(0, 0, 0, 0.05) !important;
}

.bg-opacity-10 {
  background-color: rgba(var(--bs-primary-rgb), 0.1);
}
</style>
