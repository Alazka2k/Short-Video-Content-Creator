const API_BASE_URL = '/api'; // Adjust this if your API has a different base URL

export const api = {
  async get(endpoint) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  },

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
  },

  // Add more methods (PUT, DELETE, etc.) as needed
};

export const createContent = (formData) => api.post('/create-content', formData);
export const getContentProgress = (id) => api.get(`/content-progress/${id}`);
export const getContent = (id) => api.get(`/get-content/${id}`);