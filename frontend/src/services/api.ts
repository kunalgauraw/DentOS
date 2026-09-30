import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth
export const login = async (username: string, password: string) => {
  const response = await api.post('/auth/login', { username, password });
  return response.data;
};

export const getCurrentUser = async () => {
  const response = await api.get('/auth/me');
  return response.data;
};

// Patients
export const getPatients = async (search?: string) => {
  const response = await api.get('/patients', { params: { search } });
  return response.data;
};

export const getPatient = async (id: number) => {
  const response = await api.get(`/patients/${id}`);
  return response.data;
};

export const createPatient = async (data: any) => {
  const response = await api.post('/patients', data);
  return response.data;
};

export const updatePatient = async (id: number, data: any) => {
  const response = await api.put(`/patients/${id}`, data);
  return response.data;
};

export const deletePatient = async (id: number) => {
  const response = await api.delete(`/patients/${id}`);
  return response.data;
};

// Visits
export const getVisits = async (patientId?: number) => {
  const response = await api.get('/visits', { params: { patient_id: patientId } });
  return response.data;
};

export const getVisit = async (id: number) => {
  const response = await api.get(`/visits/${id}`);
  return response.data;
};

export const createVisit = async (data: any) => {
  const response = await api.post('/visits', data);
  return response.data;
};

export const updateVisit = async (id: number, data: any) => {
  const response = await api.put(`/visits/${id}`, data);
  return response.data;
};

// Prescriptions
export const getPrescriptions = async (patientId?: number, visitId?: number) => {
  const response = await api.get('/prescriptions', { params: { patient_id: patientId, visit_id: visitId } });
  return response.data;
};

export const createPrescription = async (data: any) => {
  const response = await api.post('/prescriptions', data);
  return response.data;
};

// Invoices
export const getInvoices = async (patientId?: number, status?: string) => {
  const response = await api.get('/invoices', { params: { patient_id: patientId, status } });
  return response.data;
};

export const getInvoice = async (id: number) => {
  const response = await api.get(`/invoices/${id}`);
  return response.data;
};

export const createInvoice = async (data: any) => {
  const response = await api.post('/invoices', data);
  return response.data;
};

// Payments
export const getPayments = async (invoiceId?: number) => {
  const response = await api.get('/payments', { params: { invoice_id: invoiceId } });
  return response.data;
};

export const createPayment = async (data: any) => {
  const response = await api.post('/payments', data);
  return response.data;
};

export const getTodayCollection = async () => {
  const response = await api.get('/payments/today-collection');
  return response.data;
};

// Dashboard
export const getDashboardStats = async () => {
  const response = await api.get('/dashboard/stats');
  return response.data;
};

export const getRecentPatients = async () => {
  const response = await api.get('/dashboard/recent-patients');
  return response.data;
};

export const getPendingPayments = async () => {
  const response = await api.get('/dashboard/pending-payments');
  return response.data;
};

export default api;
