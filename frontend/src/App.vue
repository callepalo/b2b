<script setup>
import { ref, computed } from 'vue'
import ProductsManager from './components/ProductsManager.vue'
import CategoriesManager from './components/CategoriesManager.vue'
import CatalogView from './components/CatalogView.vue'
import { auth } from './services/auth'

const tab = ref('catalog')

const isLoggedIn = computed(() => !!auth.state.session)
const isAdmin = computed(() => auth.isAdmin())
const showMobileNav = ref(false)

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
const showLogin = ref(false)

async function doLogin() {
  error.value = ''
  loading.value = true
  try {
    await auth.signIn(email.value, password.value)
    showLogin.value = false
  } catch (e) {
    error.value = String(e?.message || e)
  } finally {
    loading.value = false
  }
}

async function doLogout() {
  await auth.signOut()
  tab.value = 'catalog'
  showLogin.value = false
}
</script>

<template>
  <div class="app">
    <header class="header">
      <div class="gradient-bar" />
      <div class="container header-row">
        <div class="brand-wrap">
          <img class="brand-logo" src="./assets/logo.jpg" alt="Dulpromax" />
          <div class="brand-meta">
            <h1 class="brand">Dulpromax</h1>
            <span class="brand-sub">Panel administrativo</span>
          </div>
        </div>
        <button class="hamburger" aria-label="Abrir menú" @click="showMobileNav = !showMobileNav">
          <span />
          <span />
          <span />
        </button>
        <nav class="tabs" :class="{ open: showMobileNav }">
          <button
            v-for="t in tabs"
            :key="t.key"
            :class="['tab', { active: tab === t.key }]"
            @click="tab = t.key; showMobileNav = false"
          >
            {{ t.label }}
          </button>
        </nav>
        <div class="auth" :class="{ open: showMobileNav }">
          <template v-if="!isLoggedIn">
            <div v-if="!showLogin" class="auth-actions">
              <button class="login-toggle" type="button" @click="showLogin = true">Iniciar sesión</button>
            </div>
            <div v-else class="login-wrap">
              <form class="login" @submit.prevent="doLogin">
                <input v-model="email" type="email" placeholder="Email" required />
                <input v-model="password" type="password" placeholder="Contraseña" required />
                <button type="submit" :disabled="loading">{{ loading ? 'Ingresando…' : 'Ingresar' }}</button>
                <button type="button" class="cancel" @click="showLogin = false">Cancelar</button>
              </form>
              <p v-if="error" class="error">{{ error }}</p>
            </div>
          </template>
          <template v-else>
            <div class="userbox">
              <div class="avatar" aria-hidden="true">{{ (auth.state.profile?.email || 'U')[0].toUpperCase() }}</div>
              <div class="userinfo">
                <span class="user-email">{{ auth.state.profile?.email }}</span>
                <span class="user-role" :class="auth.state.profile?.role">{{ auth.state.profile?.role || 'sin rol' }}</span>
              </div>
              <button class="logout" @click="doLogout">Salir</button>
            </div>
          </template>
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
.header { position: sticky; top: 0; z-index: 50; background: #ffffffcc; backdrop-filter: saturate(180%) blur(8px); border-bottom: 1px solid #eee; }
.gradient-bar { height: 3px; background: linear-gradient(90deg, #f1c40f, #f5deb3, #f1c40f); }
.header-row { display: grid; grid-template-columns: 1fr auto auto; align-items: center; gap: 16px; padding: 10px 0; }
.brand-wrap { display: flex; align-items: center; gap: 12px; min-width: 0; }
.brand-logo { width: 100px; height: 48px; object-fit: cover; border-radius: 10px; box-shadow: 0 2px 6px rgba(0,0,0,0.08); }
.brand-meta { display: flex; flex-direction: column; min-width: 0; }
.brand { font-size: 18px; line-height: 1; margin: 0; }
.brand-sub { font-size: 12px; color: #777; }
.tabs { display: flex; gap: 8px; align-items: center; justify-content: center; }
.tab { padding: 8px 14px; border: 1px solid #ead9a5; background: #fffbea; cursor: pointer; border-radius: 999px; transition: all .2s ease; color: #6b5b2a; }
.tab:hover { transform: translateY(-1px); box-shadow: 0 3px 10px rgba(0,0,0,0.06); }
.tab.active { background: #ffe58a; border-color: #e6c200; font-weight: 700; color: #5a4c22; }
.auth { display: flex; align-items: center; gap: 12px; justify-content: flex-end; }
.auth .login-toggle, .logout, .login button, .cancel { padding: 8px 12px; border: 1px solid #ead9a5; background: #fff; border-radius: 10px; cursor: pointer; transition: all .2s; }
.auth .login-toggle:hover, .logout:hover, .login button:hover, .cancel:hover { background: #fffbea; transform: translateY(-1px); }
.login-wrap { display: flex; flex-direction: column; gap: 6px; }
.login { display: flex; gap: 8px; flex-wrap: wrap; }
.login input { padding: 8px 10px; border: 1px solid #e7e7e7; border-radius: 10px; }
.userbox { display: flex; align-items: center; gap: 10px; }
.avatar { width: 34px; height: 34px; display: grid; place-items: center; background: #ffe58a; border: 1px solid #e6c200; border-radius: 50%; font-weight: 700; color: #5a4c22; }
.userinfo { display: flex; flex-direction: column; line-height: 1.1; }
.user-email { font-size: 12px; color: #555; max-width: 180px; overflow: hidden; text-overflow: ellipsis; }
.user-role { font-size: 11px; color: #5a4c22; background: #fffbea; border: 1px solid #ead9a5; padding: 2px 6px; border-radius: 999px; width: max-content; }
.hamburger { display: none; width: 38px; height: 38px; border: 1px solid #ead9a5; border-radius: 10px; background: #fff; align-items: center; justify-content: center; gap: 3px; flex-direction: column; }
.hamburger span { display: block; width: 18px; height: 2px; background: #6b5b2a; }
.main { flex: 1; padding: 16px 0; }
.footer { border-top: 1px solid #eee; padding: 12px 0; background: #fff; font-size: 12px; color: #666; }

/* Responsive */
@media (max-width: 1024px) {
  .container { padding: 0 12px; }
  .header-row { grid-template-columns: 1fr auto; grid-template-areas:
    'brand actions'
    'nav nav';
  }
  .tabs { order: 3; margin-top: 8px; flex-wrap: wrap; }
  .auth { order: 2; }
  .brand { font-size: 16px; }
  .brand-logo { width: 42px; height: 42px; }
  .user-email { max-width: 140px; }
}

@media (max-width: 720px) {
  .header-row { display: grid; grid-template-columns: 1fr auto; align-items: center; }
  .tabs, .auth { display: none; }
  .tabs.open, .auth.open { display: flex; flex-direction: column; align-items: stretch; gap: 8px; grid-column: 1 / -1; margin-top: 10px; }
  .hamburger { display: inline-flex; }
  .login { flex-direction: column; align-items: stretch; }
  .userbox { align-items: flex-start; }
}
</style>
