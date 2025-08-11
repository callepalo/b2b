const BASE_URL = import.meta.env.VITE_API_URL?.replace(/\/$/, '') || '';

async function http(method, path, body) {
  const res = await fetch(`${BASE_URL}${path}`, {
    method,
    headers: {
      'Content-Type': 'application/json',
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  const text = await res.text();
  let data;
  try { data = text ? JSON.parse(text) : null; } catch { data = text; }
  if (!res.ok) {
    const msg = (data && (data.detail || data.message)) || res.statusText;
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
    return fetch(`${BASE_URL}/api/v1/products/${id}/image`, {
      method: 'POST',
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
