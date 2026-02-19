import axios from 'axios';
console.log("ENV VALUE:", import.meta.env.VITE_API_URL);

// Backend base URL from environment
const API_BASE_URL = import.meta.env.VITE_API_URL;

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
  return await apiClient.post('/predict/classification', {
    features,
  });
};

export const predictRegression = async (features) => {
  return await apiClient.post('/predict/regression', {
    features,
  });
};

export const getPredictionHistory = async (limit = 50, offset = 0) => {
  return await apiClient.get('/predictions/history', {
    params: { limit, offset },
  });
};

export const getModelInfo = async () => {
  return await apiClient.get('/models/info');
};

export const checkHealth = async () => {
  return await apiClient.get('/health');
};

export default apiClient;