import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL ||
  (import.meta.env.MODE === 'production' ? '/api/v1' : 'http://localhost:8000/api/v1');

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      console.error('API Error:', error.response.data);
    } else if (error.request) {
      console.error('Network Error:', error.message);
    } else {
      console.error('Error:', error.message);
    }
    return Promise.reject(error);
  }
);

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

// AI Intelligence Features
export const getAIInsights = async (userId) => {
  try {
    const response = await apiClient.get(`/ai/insights/${userId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching AI insights:', error);
    return {
      insights: [],
      summary: 'Unable to generate insights at this time.',
      motivation: 'Keep up the great work!',
      success: false
    };
  }
};

export const predictGoals = async (userId, goalId = null) => {
  try {
    const response = await apiClient.get(`/ai/predict-goals/${userId}`, {
      params: goalId ? { goal_id: goalId } : {}
    });
    return response.data;
  } catch (error) {
    console.error('Error predicting goals:', error);
    return { predictions: [], count: 0, success: false };
  }
};

export const getWorkoutRecommendation = async (userId) => {
  try {
    const response = await apiClient.get(`/ai/recommend-workout/${userId}`);
    return response.data;
  } catch (error) {
    console.error('Error getting workout recommendation:', error);
    return {
      workout_type: 'Moderate Cardio',
      duration: 30,
      intensity: 'moderate',
      reasoning: 'A balanced workout to maintain fitness.',
      tips: ['Warm up first', 'Stay hydrated', 'Cool down after'],
      alternatives: ['Walking', 'Cycling'],
      success: false
    };
  }
};

export const getUsers = async (skip = 0, limit = 100) => {
  try {
    const response = await apiClient.get('/users/', {
      params: { skip, limit }
    });
    return Array.isArray(response.data) ? response.data : [];
  } catch (error) {
    console.error('Error fetching users:', error);
    return [];
  }
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

export const getWorkouts = async (filters = {}) => {
  const { user_id, date_from, date_to, skip = 0, limit = 100 } = filters;

  try {
    const response = await apiClient.get('/workouts/', {
      params: { user_id, date_from, date_to, skip, limit }
    });
    return Array.isArray(response.data) ? response.data : [];
  } catch (error) {
    console.error('Error fetching workouts:', error);
    return [];
  }
};

export const getWorkout = async (workoutId) => {
  const response = await apiClient.get(`/workouts/${workoutId}`);
  return response.data;
};

export const createWorkout = async (workoutData) => {
  const response = await apiClient.post('/workouts/', workoutData);
  return response.data;
};

export const updateWorkout = async (workoutId, workoutData) => {
  const response = await apiClient.put(`/workouts/${workoutId}/`, workoutData);
  return response.data;
};

export const deleteWorkout = async (workoutId) => {
  await apiClient.delete(`/workouts/${workoutId}/`);
};

export const getGoals = async (filters = {}) => {
  const { user_id, status, skip = 0, limit = 100 } = filters;

  try {
    const response = await apiClient.get('/goals/', {
      params: { user_id, status, skip, limit }
    });
    return Array.isArray(response.data) ? response.data : [];
  } catch (error) {
    console.error('Error fetching goals:', error);
    return [];
  }
};

export const getGoal = async (goalId) => {
  const response = await apiClient.get(`/goals/${goalId}`);
  return response.data;
};

export const createGoal = async (goalData) => {
  const response = await apiClient.post('/goals/', goalData);
  return response.data;
};

export const updateGoal = async (goalId, goalData) => {
  const response = await apiClient.put(`/goals/${goalId}/`, goalData);
  return response.data;
};

export const deleteGoal = async (goalId) => {
  await apiClient.delete(`/goals/${goalId}/`);
};

export const getProgressMetrics = async (filters = {}) => {
  const { user_id, metric, date_from, date_to, skip = 0, limit = 100 } = filters;

  const response = await apiClient.get('/progress', {
    params: { user_id, metric, date_from, date_to, skip, limit }
  });
  return response.data;
};

export const getProgressMetric = async (progressId) => {
  const response = await apiClient.get(`/progress/${progressId}`);
  return response.data;
};

export const createProgressMetric = async (progressData) => {
  const response = await apiClient.post('/progress', progressData);
  return response.data;
};

export const updateProgressMetric = async (progressId, progressData) => {
  const response = await apiClient.put(`/progress/${progressId}`, progressData);
  return response.data;
};

export const deleteProgressMetric = async (progressId) => {
  await apiClient.delete(`/progress/${progressId}`);
};

export const getUserAnalytics = async (userId, days = 30) => {
  const response = await apiClient.get(`/analytics/analytics/${userId}`, {
    params: { days }
  });
  return response.data;
};

export const getWorkoutStreak = async (userId) => {
  const response = await apiClient.get(`/analytics/streak/${userId}`);
  return response.data;
};

export const exportUserData = async (userId) => {
  const response = await apiClient.get(`/analytics/export/${userId}`);
  return response.data;
};

export default apiClient;
