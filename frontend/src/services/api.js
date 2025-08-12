import { auth } from './auth'
const BASE_URL = import.meta.env.VITE_API_URL?.replace(/\/$/, '') || '';

async function http(method, path, body) {
  const headers = {
    'Content-Type': 'application/json',
  }
  const token = auth.getAccessToken?.() || null
  if (token) headers['Authorization'] = `Bearer ${token}`
  const res = await fetch(`${BASE_URL}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });
  const text = await res.text();
  let data;
  try { data = text ? JSON.parse(text) : null; } catch { data = text; }
  if (!res.ok) {
    let msg = res.statusText;
    if (data) {
      if (typeof data === 'string') msg = data;
      else if (data.detail) {
        // FastAPI may return detail as string or list of validation errors
        if (Array.isArray(data.detail)) {
          msg = data.detail.map(e => `${e.loc?.join('.')}: ${e.msg}`).join('; ');
        } else if (typeof data.detail === 'object') {
          msg = JSON.stringify(data.detail);
        } else {
          msg = String(data.detail);
        }
      } else if (data.message) {
        msg = String(data.message);
      } else {
        msg = JSON.stringify(data);
      }
    }
    throw new Error(`HTTP ${res.status}: ${msg}`);
  }
  return data;
}

export const api = {
  // Products
  listProducts(params = {}) {
    const q = new URLSearchParams();
    if (params.page) q.set('page', params.page);
    if (params.per_page) q.set('per_page', params.per_page);
    if (params.search) q.set('search', params.search);
    if (params.category_id) q.set('category_id', params.category_id);
    if (params.mode) q.set('mode', params.mode);
    if (params.expand) q.set('expand', params.expand);
    const qs = q.toString();
    return http('GET', `/api/v1/products${qs ? `?${qs}` : ''}`);
  },
  getProduct(id) {
    return http('GET', `/api/v1/products/${id}`);
  },
  createProduct(payload) {
    return http('POST', '/api/v1/products', payload);
  },
  updateProduct(id, payload) {
    return http('PUT', `/api/v1/products/${id}`, payload);
  },
  deleteProduct(id) {
    return http('DELETE', `/api/v1/products/${id}`);
  },
  uploadProductImage(id, file) {
    const form = new FormData();
    form.append('file', file);
    const headers = {}
    const token = auth.getAccessToken?.() || null
    if (token) headers['Authorization'] = `Bearer ${token}`
    return fetch(`${BASE_URL}/api/v1/products/${id}/image`, {
      method: 'POST',
      headers,
      body: form,
    }).then(async (res) => {
      const text = await res.text();
      let data; try { data = text ? JSON.parse(text) : null; } catch { data = text; }
      if (!res.ok) {
        const msg = (data && (data.detail || data.message)) || res.statusText;
        throw new Error(`HTTP ${res.status}: ${msg}`);
      }
      return data;
    });
  },
  // Product Packs
  listProductPacks(productId) {
    return http('GET', `/api/v1/products/${productId}/packs`);
  },
  createProductPack(productId, payload) {
    return http('POST', `/api/v1/products/${productId}/packs`, payload);
  },
  updateProductPack(productId, packId, payload) {
    return http('PUT', `/api/v1/products/${productId}/packs/${packId}`, payload);
  },
  deleteProductPack(productId, packId) {
    return http('DELETE', `/api/v1/products/${productId}/packs/${packId}`);
  },
  // Categories
  listCategories(params = {}) {
    const q = new URLSearchParams();
    if (params.page) q.set('page', params.page);
    if (params.per_page) q.set('per_page', params.per_page);
    if (params.search) q.set('search', params.search);
    const qs = q.toString();
    return http('GET', `/api/v1/categories${qs ? `?${qs}` : ''}`);
  },
  getCategory(id) {
    return http('GET', `/api/v1/categories/${id}`);
  },
  createCategory(payload) {
    return http('POST', '/api/v1/categories', payload);
  },
  updateCategory(id, payload) {
    return http('PUT', `/api/v1/categories/${id}`, payload);
  },
  deleteCategory(id) {
    return http('DELETE', `/api/v1/categories/${id}`);
  },
};
