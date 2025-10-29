/**
 * API Service Layer
 *
 * Centralized axios-based API client for all backend communication.
 * Handles authentication, error handling, and request/response formatting.
 */

import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds
});

// Request interceptor (can add auth tokens here)
apiClient.interceptors.request.use(
  (config) => {
    // Add authentication token if available
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Server responded with error status
      console.error('API Error:', error.response.data);
    } else if (error.request) {
      // Request made but no response received
      console.error('Network Error:', error.message);
    } else {
      // Something else happened
      console.error('Error:', error.message);
    }
    return Promise.reject(error);
  }
);

// ============================================================================
// AI Agent Endpoints
// ============================================================================

export const chatWithAgent = async (message, options = {}) => {
  const { use_memory = true, use_rag = true } = options;

  const response = await apiClient.post('/ai/chat', {
    message,
    use_memory,
    use_rag,
  });

  return response.data;
};

export const getAgentInfo = async () => {
  const response = await apiClient.get('/ai/agent');
  return response.data;
};

export const getTools = async () => {
  const response = await apiClient.get('/ai/tools');
  return response.data;
};

export const getHealthStatus = async () => {
  const response = await apiClient.get('/ai/health');
  return response.data;
};

export const clearMemory = async () => {
  const response = await apiClient.post('/ai/clear-memory');
  return response.data;
};

// ============================================================================
// User Endpoints
// ============================================================================

export const getUsers = async (skip = 0, limit = 100) => {
  const response = await apiClient.get('/users', {
    params: { skip, limit }
  });
  return response.data;
};

export const getUser = async (userId) => {
  const response = await apiClient.get(`/users/${userId}`);
  return response.data;
};

export const createUser = async (userData) => {
  const response = await apiClient.post('/users', userData);
  return response.data;
};

export const updateUser = async (userId, userData) => {
  const response = await apiClient.put(`/users/${userId}`, userData);
  return response.data;
};

export const deleteUser = async (userId) => {
  await apiClient.delete(`/users/${userId}`);
};

// ============================================================================
// Workout Endpoints
// ============================================================================

export const getWorkouts = async (filters = {}) => {
  const { user_id, date_from, date_to, skip = 0, limit = 100 } = filters;

  const response = await apiClient.get('/workout-sessions', {
    params: { user_id, date_from, date_to, skip, limit }
  });
  return response.data;
};

export const getWorkout = async (workoutId) => {
  const response = await apiClient.get(`/workout-sessions/${workoutId}`);
  return response.data;
};

export const createWorkout = async (workoutData) => {
  const response = await apiClient.post('/workout-sessions', workoutData);
  return response.data;
};

export const updateWorkout = async (workoutId, workoutData) => {
  const response = await apiClient.put(`/workout-sessions/${workoutId}`, workoutData);
  return response.data;
};

export const deleteWorkout = async (workoutId) => {
  await apiClient.delete(`/workout-sessions/${workoutId}`);
};

// ============================================================================
// Goal Endpoints
// ============================================================================

export const getGoals = async (filters = {}) => {
  const { user_id, status, skip = 0, limit = 100 } = filters;

  const response = await apiClient.get('/fitness-goals', {
    params: { user_id, status, skip, limit }
  });
  return response.data;
};

export const getGoal = async (goalId) => {
  const response = await apiClient.get(`/fitness-goals/${goalId}`);
  return response.data;
};

export const createGoal = async (goalData) => {
  const response = await apiClient.post('/fitness-goals', goalData);
  return response.data;
};

export const updateGoal = async (goalId, goalData) => {
  const response = await apiClient.put(`/fitness-goals/${goalId}`, goalData);
  return response.data;
};

export const deleteGoal = async (goalId) => {
  await apiClient.delete(`/fitness-goals/${goalId}`);
};

// ============================================================================
// Progress Endpoints
// ============================================================================

export const getProgressMetrics = async (filters = {}) => {
  const { user_id, metric, date_from, date_to, skip = 0, limit = 100 } = filters;

  const response = await apiClient.get('/progress-metrics', {
    params: { user_id, metric, date_from, date_to, skip, limit }
  });
  return response.data;
};

export const getProgressMetric = async (progressId) => {
  const response = await apiClient.get(`/progress-metrics/${progressId}`);
  return response.data;
};

export const createProgressMetric = async (progressData) => {
  const response = await apiClient.post('/progress-metrics', progressData);
  return response.data;
};

export const updateProgressMetric = async (progressId, progressData) => {
  const response = await apiClient.put(`/progress-metrics/${progressId}`, progressData);
  return response.data;
};

export const deleteProgressMetric = async (progressId) => {
  await apiClient.delete(`/progress-metrics/${progressId}`);
};

export default apiClient;
