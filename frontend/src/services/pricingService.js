import { auth } from './auth'

function getBaseUrl() {
  // Reutiliza la misma convención que otros servicios
  const base = import.meta.env.VITE_API_URL?.replace(/\/$/, '') || ''
  return base
}

export async function fetchResolvedPrices() {
  const token = auth.getAccessToken()
  if (!token) throw new Error('No hay sesión activa')
  const base = getBaseUrl()
  const res = await fetch(`${base}/api/v1/pricing/products`, {
    headers: { Authorization: `Bearer ${token}` },
  })
  const text = await res.text()
  let data = null
  try { data = text ? JSON.parse(text) : null } catch { /* leave as text */ }
  if (!res.ok) {
    const msg = (data && (data.detail || data.message)) || text || res.statusText
    throw new Error(msg)
  }
  // Esperado: array de objetos con product_id y price_resuelto
  return Array.isArray(data) ? data : []
}
