// Servicio base para consumir la API
const API_BASE_URL = 'https://b2b-wa72.onrender.com/api/v1';

class ApiService {
  async get(endpoint, params = {}) {
    const url = new URL(`${API_BASE_URL}${endpoint}`);
    Object.keys(params).forEach(key => {
      if (params[key] !== undefined && params[key] !== null) {
        url.searchParams.append(key, params[key]);
      }
    });

    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  }

  async post(endpoint, data) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  }

  async put(endpoint, data) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  }

  async delete(endpoint) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  }
}

// Servicios específicos
class CategoriesService extends ApiService {
  constructor() {
    super();
    this.endpoint = '/categories';
  }

  async getAll() {
    return this.get(this.endpoint);
  }

  async getById(id) {
    return this.get(`${this.endpoint}/${id}`);
  }

  async create(data) {
    return this.post(this.endpoint, data);
  }

  async update(id, data) {
    return this.put(`${this.endpoint}/${id}`, data);
  }

  async delete(id) {
    return this.delete(`${this.endpoint}/${id}`);
  }
}

class ProductsService extends ApiService {
  async getAll(params = {}) {
    const response = await this.get('/products', params);
    return response.data || response; // Handle both direct response and wrapped response
  }

  async getById(id) {
    return this.get(`/products/${id}`);
  }

  async create(data) {
    return this.post('/products', data);
  }

  async search(query, params = {}) {
    return this.get('/products', { ...params, search: query });
  }
}

class PingService extends ApiService {
  async ping() {
    return this.get('/ping');
  }

  async health() {
    return this.get('/health');
  }
}

export const categoriesService = new CategoriesService();
export const productsService = new ProductsService();
export const pingService = new PingService();
