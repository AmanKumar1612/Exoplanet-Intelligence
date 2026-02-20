import axios from 'axios';

// Use relative URL so Vercel proxy handles routing (eliminates CORS)
// In dev, Vite proxy (vite.config.js) routes /api → localhost:8000
// In production, vercel.json rewrites /api/* → Render backend
const API_BASE_URL = '';

// Create axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});


// Response interceptor (clean error handling)
apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const message =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      error.message ||
      'Something went wrong';

    return Promise.reject(new Error(message));
  }
);

// -------------------- API CALLS --------------------

export const predictClassification = async (features) => {
  return await apiClient.post('/api/predict/classification', {
    features,
  });
};

export const predictRegression = async (features) => {
  return await apiClient.post('/api/predict/regression', {
    features,
  });
};

export const getPredictionHistory = async (limit = 50, offset = 0) => {
  return await apiClient.get('/api/predictions/history', {
    params: { limit, offset },
  });
};

export const getModelInfo = async () => {
  return await apiClient.get('/api/models/info');
};

export const checkHealth = async () => {
  return await apiClient.get('/api/health');
};

export default apiClient;
