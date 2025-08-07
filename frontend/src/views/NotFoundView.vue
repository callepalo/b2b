<template>
  <div class="not-found text-center py-5">
    <div class="container">
      <h1 class="display-1 text-primary">404</h1>
      <h2 class="h3 mb-4">Página no encontrada</h2>
      <p class="lead text-muted mb-4">
        Lo sentimos, la página que estás buscando no existe o ha sido movida.
      </p>
      <router-link to="/" class="btn btn-primary">
        <i class="bi bi-house-door me-2"></i> Volver al inicio
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NotFoundView',
  mounted() {
    // Establecer el título de la página
    document.title = 'Página no encontrada | Dulpromax';
  }
};
</script>

<style scoped>
.not-found {
  min-height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.display-1 {
  font-weight: 700;
  margin-bottom: 1.5rem;
}

.btn {
  padding: 0.5rem 1.5rem;
  font-weight: 500;
}
</style>
