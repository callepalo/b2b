import { auth } from './auth'

const BASE_URL = import.meta.env.VITE_API_URL?.replace(/\/$/, '') || ''

async function http(method, path, body) {
  const headers = { 'Content-Type': 'application/json' }
  const token = auth.getAccessToken?.() || null
  if (token) headers['Authorization'] = `Bearer ${token}`
  const res = await fetch(`${BASE_URL}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  })
  const text = await res.text()
  let data
  try { data = text ? JSON.parse(text) : null } catch { data = text }
  if (!res.ok) {
    const msg = (data && (data.detail || data.message)) || res.statusText
    throw new Error(`HTTP ${res.status}: ${msg}`)
  }
  return data
}

export const adminPricing = {
  // Segment prices
  listSegmentPrices({ product_id, user_type_id } = {}) {
    const q = new URLSearchParams()
    if (product_id) q.set('product_id', product_id)
    if (user_type_id) q.set('user_type_id', user_type_id)
    const qs = q.toString()
    return http('GET', `/api/v1/admin/pricing/segments${qs ? `?${qs}` : ''}`)
  },
  createSegmentPrice(payload) {
    return http('POST', '/api/v1/admin/pricing/segments', payload)
  },
  updateSegmentPrice(id, payload) {
    return http('PUT', `/api/v1/admin/pricing/segments/${id}`, payload)
  },
  deleteSegmentPrice(id) {
    return http('DELETE', `/api/v1/admin/pricing/segments/${id}`)
  },

  // Overrides
  listOverrides({ product_id, organization_id } = {}) {
    const q = new URLSearchParams()
    if (product_id) q.set('product_id', product_id)
    if (organization_id) q.set('organization_id', organization_id)
    const qs = q.toString()
    return http('GET', `/api/v1/admin/pricing/overrides${qs ? `?${qs}` : ''}`)
  },
  createOverride(payload) {
    return http('POST', '/api/v1/admin/pricing/overrides', payload)
  },
  updateOverride(id, payload) {
    return http('PUT', `/api/v1/admin/pricing/overrides/${id}`, payload)
  },
  deleteOverride(id) {
    return http('DELETE', `/api/v1/admin/pricing/overrides/${id}`)
  },

  // Metadata
  listUserTypes() {
    return http('GET', '/api/v1/admin/user-types')
  },
  listOrganizations() {
    return http('GET', '/api/v1/admin/organizations')
  },
}
