<script setup>
import { ref, onMounted } from 'vue'

const apiUrl = import.meta.env.VITE_API_URL
const status = ref('pending')
const responseText = ref('')

const testApi = async () => {
  status.value = 'loading'
  try {
    if (!apiUrl) throw new Error('VITE_API_URL no está definida')
    const res = await fetch(`${apiUrl}/ping`, {
      headers: { 'Content-Type': 'application/json' }
    })
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    // Intentar parsear JSON, si no, texto plano
    let body
    try {
      body = await res.json()
    } catch (_) {
      body = await res.text()
    }
    responseText.value = typeof body === 'string' ? body : JSON.stringify(body, null, 2)
    status.value = 'ok'
  } catch (err) {
    status.value = `error: ${err.message}`
  }
}

onMounted(() => {
  testApi()
})
</script>

<template>
  <div>
    <h2>Prueba de API</h2>
    <p><strong>VITE_API_URL:</strong> {{ apiUrl || '(no definida)' }}</p>
    <p><strong>Estado:</strong> {{ status }}</p>
    <pre v-if="responseText">{{ responseText }}</pre>
    <button @click="testApi">Probar de nuevo</button>
  </div>
</template>
