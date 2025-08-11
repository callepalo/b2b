<script setup>
import { ref, computed } from 'vue'
import ProductsManager from './components/ProductsManager.vue'
import CategoriesManager from './components/CategoriesManager.vue'
import CatalogView from './components/CatalogView.vue'
import { auth } from './services/auth'

const tab = ref('catalog')

const isLoggedIn = computed(() => !!auth.state.session)
const isAdmin = computed(() => auth.isAdmin())

const tabs = computed(() => {
  const base = [{ key: 'catalog', label: 'Catálogo' }]
  if (isAdmin.value) {
    base.push({ key: 'products', label: 'Productos' })
    base.push({ key: 'categories', label: 'Categorías' })
  }
  return base
})

// Simple login form state
const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

async function doLogin() {
  error.value = ''
  loading.value = true
  try {
    await auth.signIn(email.value, password.value)
  } catch (e) {
    error.value = String(e?.message || e)
  } finally {
    loading.value = false
  }
}

async function doLogout() {
  await auth.signOut()
  tab.value = 'catalog'
}
</script>

<template>
  <div class="app">
    <header class="header">
      <div class="container">
        <h1 class="brand">Dulpromax Admin</h1>
        <img src="./assets/logo.jpg" alt="Logo" width="350" height="200"/>
        <div class="topbar">
          <nav class="tabs">
            <button
              v-for="t in tabs"
              :key="t.key"
              :class="['tab', { active: tab === t.key }]"
              @click="tab = t.key"
            >
              {{ t.label }}
            </button>
          </nav>
          <div class="auth">
            <template v-if="!isLoggedIn">
              <form class="login" @submit.prevent="doLogin">
                <input v-model="email" type="email" placeholder="Email" required />
                <input v-model="password" type="password" placeholder="Contraseña" required />
                <button type="submit" :disabled="loading">{{ loading ? 'Ingresando…' : 'Ingresar' }}</button>
              </form>
              <p v-if="error" class="error">{{ error }}</p>
            </template>
            <template v-else>
              <span class="user">{{ auth.state.profile?.email || 'Usuario' }} ({{ auth.state.profile?.role || 'sin rol' }})</span>
              <button class="logout" @click="doLogout">Salir</button>
            </template>
          </div>
        </div>
      </div>
    </header>

    <main class="main">
      <CatalogView v-if="tab === 'catalog'" />
      <template v-else>
        <div v-if="!isAdmin" class="guard">Se requiere rol administrador para acceder.</div>
        <ProductsManager v-else-if="tab === 'products'" />
        <CategoriesManager v-else />
      </template>
    </main>

    <footer class="footer">
      <div class="container">© {{ new Date().getFullYear() }} Dulpromax — Panel de gestión</div>
    </footer>
  </div>
</template>

<style scoped>
.app { min-height: 100vh; display: flex; flex-direction: column; }
.container { max-width: 1880px; margin: 0 auto; padding: 0 16px; }
.header { border-bottom: 1px solid #eee; background: #fff; }
.brand { font-size: 18px; margin: 0; padding: 12px 0; }
.topbar { display: flex; gap: 16px; align-items: center; justify-content: space-between; padding-bottom: 12px; flex-wrap: wrap; }
.tabs { display: flex; gap: 8px; }
.tab { padding: 8px 12px; border: 1px solid #ddd; background: #f9f9f9; cursor: pointer; border-radius: 6px; }
.tab.active { background: #fff; border-color: #bbb; font-weight: 600; }
.auth { display: flex; align-items: center; gap: 12px; }
.login { display: flex; gap: 8px; }
.login input { padding: 6px 8px; border: 1px solid #ddd; border-radius: 6px; }
.login button, .logout { padding: 8px 12px; border: 1px solid #ddd; background: #fff; border-radius: 6px; cursor: pointer; }
.user { font-size: 12px; color: #555; }
.error { color: #b00020; font-size: 12px; margin: 0; }
.guard { padding: 16px; border: 1px dashed #f0c; background: #fff8f8; }
.main { flex: 1; padding: 16px 0; }
.footer { border-top: 1px solid #eee; padding: 12px 0; background: #fff; font-size: 12px; color: #666; }
</style>
