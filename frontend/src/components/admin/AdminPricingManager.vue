<script setup>
import { ref, onMounted, computed } from 'vue'
import { adminPricing } from '../../services/adminPricingService'
import { api } from '../../services/api'
import { auth } from '../../services/auth'

const loading = ref(false)
const error = ref('')

// Data sources
const products = ref([])
const userTypes = ref([])
const orgs = ref([])

// Segment prices state
const segFilters = ref({ product_id: '', user_type_id: '' })
const segList = ref([])
const segForm = ref({ id: null, product_id: '', user_type_id: '', price: null })

// Overrides state
const ovFilters = ref({ product_id: '', organization_id: '' })
const ovList = ref([])
const ovForm = ref({ id: null, product_id: '', organization_id: '', price: null })

const isAdmin = computed(() => auth.isAdmin())

function currency(val) {
  return new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP' }).format(val || 0)
}

async function loadMeta() {
  loading.value = true
  error.value = ''
  try {
    const [prodRes, ut, og] = await Promise.all([
      api.listProducts({ per_page: 500 }),
      adminPricing.listUserTypes?.() || fetchUserTypesFallback(),
      adminPricing.listOrganizations?.() || fetchOrgsFallback(),
    ])
    products.value = prodRes?.data || []
    userTypes.value = ut || []
    orgs.value = og || []
  } catch (e) {
    error.value = e.message || String(e)
  } finally {
    loading.value = false
  }
}

// In case tree-shaking or missing methods: provide fallbacks hitting the same endpoints
async function fetchUserTypesFallback() {
  return fetch(`${import.meta.env.VITE_API_URL}/api/v1/admin/user-types`, { headers: { Authorization: `Bearer ${auth.getAccessToken()}` } })
    .then(r => r.json())
}
async function fetchOrgsFallback() {
  return fetch(`${import.meta.env.VITE_API_URL}/api/v1/admin/organizations`, { headers: { Authorization: `Bearer ${auth.getAccessToken()}` } })
    .then(r => r.json())
}

async function refreshSegments() {
  segList.value = await adminPricing.listSegmentPrices(segFilters.value)
}
async function refreshOverrides() {
  ovList.value = await adminPricing.listOverrides(ovFilters.value)
}

function editSeg(row) {
  segForm.value = { id: row.id, product_id: row.product_id, user_type_id: row.user_type_id, price: row.price }
}
function clearSegForm() {
  segForm.value = { id: null, product_id: '', user_type_id: '', price: null }
}
async function saveSeg() {
  if (!segForm.value.product_id || !segForm.value.user_type_id || segForm.value.price == null || segForm.value.price < 0) return
  if (segForm.value.id) {
    await adminPricing.updateSegmentPrice(segForm.value.id, {
      product_id: segForm.value.product_id,
      user_type_id: segForm.value.user_type_id,
      price: Number(segForm.value.price),
    })
  } else {
    await adminPricing.createSegmentPrice({
      product_id: segForm.value.product_id,
      user_type_id: segForm.value.user_type_id,
      price: Number(segForm.value.price),
    })
  }
  clearSegForm()
  await refreshSegments()
}
async function delSeg(id) {
  if (!id) return
  await adminPricing.deleteSegmentPrice(id)
  await refreshSegments()
}

function editOv(row) {
  ovForm.value = { id: row.id, product_id: row.product_id, organization_id: row.organization_id, price: row.price }
}
function clearOvForm() {
  ovForm.value = { id: null, product_id: '', organization_id: '', price: null }
}
async function saveOv() {
  if (!ovForm.value.product_id || !ovForm.value.organization_id || ovForm.value.price == null || ovForm.value.price < 0) return
  if (ovForm.value.id) {
    await adminPricing.updateOverride(ovForm.value.id, {
      product_id: ovForm.value.product_id,
      organization_id: ovForm.value.organization_id,
      price: Number(ovForm.value.price),
    })
  } else {
    await adminPricing.createOverride({
      product_id: ovForm.value.product_id,
      organization_id: ovForm.value.organization_id,
      price: Number(ovForm.value.price),
    })
  }
  clearOvForm()
  await refreshOverrides()
}
async function delOv(id) {
  if (!id) return
  await adminPricing.deleteOverride(id)
  await refreshOverrides()
}

onMounted(async () => {
  await loadMeta()
  await Promise.all([refreshSegments(), refreshOverrides()])
})
</script>

<template>
  <div class="admin-pricing">
    <h2>Administración de Precios</h2>
    <div v-if="!isAdmin" class="guard">Se requiere rol administrador.</div>
    <div v-else>
      <div v-if="error" class="error">{{ error }}</div>

      <section class="panel">
        <h3>Precios por Segmento</h3>
        <div class="controls">
          <select v-model="segFilters.product_id" @change="refreshSegments">
            <option value="">Todos los productos</option>
            <option v-for="p in products" :key="p.id" :value="p.id">{{ p.name }}</option>
          </select>
          <select v-model="segFilters.user_type_id" @change="refreshSegments">
            <option value="">Todos los segmentos</option>
            <option v-for="u in userTypes" :key="u.id" :value="u.id">{{ u.name }}</option>
          </select>
        </div>

        <form class="form" @submit.prevent="saveSeg">
          <select v-model="segForm.product_id" required>
            <option value="" disabled>Producto…</option>
            <option v-for="p in products" :key="p.id" :value="p.id">{{ p.name }}</option>
          </select>
          <select v-model="segForm.user_type_id" required>
            <option value="" disabled>Segmento…</option>
            <option v-for="u in userTypes" :key="u.id" :value="u.id">{{ u.name }}</option>
          </select>
          <input v-model.number="segForm.price" type="number" step="0.01" min="0" placeholder="Precio" required />
          <button type="submit">{{ segForm.id ? 'Actualizar' : 'Crear' }}</button>
          <button type="button" class="muted" @click="clearSegForm">Limpiar</button>
        </form>

        <table class="table">
          <thead>
            <tr>
              <th>Producto</th>
              <th>Segmento</th>
              <th>Precio</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in segList" :key="row.id">
              <td>{{ products.find(p => p.id === row.product_id)?.name || row.product_id }}</td>
              <td>{{ userTypes.find(u => u.id === row.user_type_id)?.name || row.user_type_id }}</td>
              <td>{{ currency(row.price) }}</td>
              <td>
                <button @click="editSeg(row)">Editar</button>
                <button class="danger" @click="delSeg(row.id)">Eliminar</button>
              </td>
            </tr>
            <tr v-if="!segList.length">
              <td colspan="4">Sin registros</td>
            </tr>
          </tbody>
        </table>
      </section>

      <section class="panel">
        <h3>Overrides por Cliente</h3>
        <div class="controls">
          <select v-model="ovFilters.product_id" @change="refreshOverrides">
            <option value="">Todos los productos</option>
            <option v-for="p in products" :key="p.id" :value="p.id">{{ p.name }}</option>
          </select>
          <select v-model="ovFilters.organization_id" @change="refreshOverrides">
            <option value="">Todas las organizaciones</option>
            <option v-for="o in orgs" :key="o.id" :value="o.id">{{ o.name }}</option>
          </select>
        </div>

        <form class="form" @submit.prevent="saveOv">
          <select v-model="ovForm.product_id" required>
            <option value="" disabled>Producto…</option>
            <option v-for="p in products" :key="p.id" :value="p.id">{{ p.name }}</option>
          </select>
          <select v-model="ovForm.organization_id" required>
            <option value="" disabled>Organización…</option>
            <option v-for="o in orgs" :key="o.id" :value="o.id">{{ o.name }}</option>
          </select>
          <input v-model.number="ovForm.price" type="number" step="0.01" min="0" placeholder="Precio" required />
          <button type="submit">{{ ovForm.id ? 'Actualizar' : 'Crear' }}</button>
          <button type="button" class="muted" @click="clearOvForm">Limpiar</button>
        </form>

        <table class="table">
          <thead>
            <tr>
              <th>Producto</th>
              <th>Organización</th>
              <th>Precio</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in ovList" :key="row.id">
              <td>{{ products.find(p => p.id === row.product_id)?.name || row.product_id }}</td>
              <td>{{ orgs.find(o => o.id === row.organization_id)?.name || row.organization_id }}</td>
              <td>{{ currency(row.price) }}</td>
              <td>
                <button @click="editOv(row)">Editar</button>
                <button class="danger" @click="delOv(row.id)">Eliminar</button>
              </td>
            </tr>
            <tr v-if="!ovList.length">
              <td colspan="4">Sin registros</td>
            </tr>
          </tbody>
        </table>
      </section>
    </div>
  </div>
</template>

<style scoped>
.admin-pricing { padding: 16px; display: grid; gap: 16px; }
.panel { border: 1px solid #e6e6e6; border-radius: 10px; background: #fff; padding: 12px; }
.controls { display: flex; gap: 8px; margin-bottom: 8px; }
.form { display: flex; gap: 8px; margin-bottom: 8px; flex-wrap: wrap; }
.form input, .form select { padding: 6px 8px; border: 1px solid #ddd; border-radius: 8px; }
.table { width: 100%; border-collapse: collapse; }
.table th, .table td { border-top: 1px solid #eee; padding: 8px; text-align: left; }
button { padding: 6px 10px; border: 1px solid #ead9a5; background: #fffbea; border-radius: 8px; cursor: pointer; }
button:hover { background: #ffe58a; }
button.danger { border-color: #f3b0b0; background: #ffecec; }
button.muted { background: #fff; }
.guard { padding: 12px; border: 1px solid #f0d58a; background: #fff9e6; border-radius: 10px; }
.error { color: #c00; }
</style>
