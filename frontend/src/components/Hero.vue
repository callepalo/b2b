<template>
  <section class="hero">
    <div class="hero-content">
      <h1>Bienvenidos a Dulpromax</h1>
      <p class="hero-subtitle">Los mejores productos de repostería y dulces para tu negocio</p>
      <div class="hero-actions">
        <button class="btn btn-primary" @click="scrollToProducts">Ver Productos</button>
        <button class="btn btn-outline">Contactar</button>
      </div>
    </div>
  </section>
</template>

<script setup>
const scrollToProducts = () => {
  const productsSection = document.getElementById('productos');
  if (productsSection) {
    productsSection.scrollIntoView({ behavior: 'smooth' });
  }
};
</script>

<style scoped>
.hero {
  background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)),
              url('https://images.unsplash.com/photo-1601050690597-df0568f70950?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80');
  background-size: cover;
  background-position: center;
  color: var(--white);
  text-align: center;
  padding: 8rem 1rem;
  margin-bottom: 3rem;
  border-radius: var(--border-radius);
  box-shadow: var(--shadow);
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
}

.hero h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
  color: var(--white);
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.hero-subtitle {
  font-size: 1.5rem;
  margin-bottom: 2rem;
  color: var(--white);
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}

.hero-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.btn {
  padding: 0.75rem 2rem;
  border-radius: 50px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  transition: var(--transition);
  cursor: pointer;
  font-size: 0.9rem;
}

.btn-primary {
  background-color: var(--primary);
  color: var(--text);
  border: 2px solid var(--primary);
}

.btn-primary:hover {
  background-color: transparent;
  color: var(--white);
}

.btn-outline {
  background-color: transparent;
  color: var(--white);
  border: 2px solid var(--white);
}

.btn-outline:hover {
  background-color: var(--white);
  color: var(--text);
}

@media (max-width: 768px) {
  .hero {
    padding: 5rem 1rem;
  }
  
  .hero h1 {
    font-size: 2.2rem;
  }
  
  .hero-subtitle {
    font-size: 1.2rem;
  }
  
  .btn {
    padding: 0.6rem 1.5rem;
    font-size: 0.8rem;
  }
}
</style>
