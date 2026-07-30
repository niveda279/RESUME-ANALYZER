import axios from 'axios';

const API_BASE = '/api';

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor to attach JWT token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('careercast_token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    if (config.data instanceof FormData) {
      delete config.headers['Content-Type'];
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export const authService = {
  login: async (email, password) => {
    const res = await api.post('/login', { email, password });
    return res.data;
  },
  register: async (name, email, password) => {
    const res = await api.post('/register', { name, email, password });
    return res.data;
  },
  getProfile: async () => {
    const res = await api.get('/profile');
    return res.data;
  },
  logout: () => {
    localStorage.removeItem('careercast_token');
    localStorage.removeItem('careercast_user');
  },
};

export const resumeService = {
  uploadResume: async (file, onProgress) => {
    const formData = new FormData();
    formData.append('file', file);
    const res = await api.post('/upload', formData, {
      onUploadProgress: (progressEvent) => {
        if (onProgress && progressEvent.total) {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          onProgress(percentCompleted);
        }
      },
    });
    return res.data;
  },
  getAnalysis: async (id) => {
    const res = await api.get(`/analysis/${id}`);
    return res.data;
  },
  getHistory: async () => {
    const res = await api.get('/history');
    return res.data;
  },
};

export const adminService = {
  getStats: async () => {
    const res = await api.get('/admin/stats');
    return res.data;
  },
  getUsers: async () => {
    const res = await api.get('/admin/users');
    return res.data;
  },
  deleteUser: async (id) => {
    const res = await api.delete(`/admin/user/${id}`);
    return res.data;
  },
  getResumes: async () => {
    const res = await api.get('/admin/resumes');
    return res.data;
  },
  deleteResume: async (id) => {
    const res = await api.delete(`/admin/resume/${id}`);
    return res.data;
  },
};

export default api;
