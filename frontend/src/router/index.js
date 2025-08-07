import { createRouter, createWebHistory } from 'vue-router';

// Vistas
import HomeView from '@/views/HomeView.vue';
import ProductosView from '@/views/ProductosView.vue';
import NotFoundView from '@/views/NotFoundView.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: {
      title: 'Inicio | Dulpromax',
      requiresAuth: false
    }
  },
  {
    path: '/productos',
    name: 'productos',
    component: ProductosView,
    meta: {
      title: 'Productos | Dulpromax',
      requiresAuth: true
    }
  },
  // Ruta 404 - debe ir al final
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: NotFoundView,
    meta: {
      title: 'Página no encontrada | Dulpromax',
      requiresAuth: false
    }
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    // Scroll al inicio de la página al cambiar de ruta
    return { top: 0, behavior: 'smooth' };
  }
});

// Configurar título de la página
router.beforeEach((to, from, next) => {
  // Establecer el título de la página
  document.title = to.meta?.title || 'Dulpromax';
  
  // Aquí podríamos agregar lógica de autenticación global si es necesario
  // Por ejemplo, redirigir a login si la ruta requiere autenticación
  
  next();
});

export default router;
