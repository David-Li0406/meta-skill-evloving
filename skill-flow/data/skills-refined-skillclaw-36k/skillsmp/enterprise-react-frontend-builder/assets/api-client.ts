import axios, { AxiosError } from 'axios'

// API Configuration
export const API_CONFIG = {
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:3000/api',
  timeout: 30000, // 30 seconds
}

// Create Axios instance
export const apiClient = axios.create({
  baseURL: API_CONFIG.baseURL,
  timeout: API_CONFIG.timeout,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Send cookies with requests
})

// Request interceptor - Add auth token
apiClient.interceptors.request.use(
  (config) => {
    // Get token from localStorage (or use your auth method)
    const token = localStorage.getItem('access_token')
    
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    // Log request in development
    if (import.meta.env.DEV) {
      console.log(`[API Request] ${config.method?.toUpperCase()} ${config.url}`, config.data)
    }
    
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor - Handle errors and token refresh
apiClient.interceptors.response.use(
  (response) => {
    // Log response in development
    if (import.meta.env.DEV) {
      console.log(`[API Response] ${response.config.url}`, response.data)
    }
    
    return response
  },
  async (error: AxiosError) => {
    const originalRequest = error.config as typeof error.config & { _retry?: boolean }
    
    // Handle 401 Unauthorized - Token expired
    if (error.response?.status === 401 && !originalRequest?._retry) {
      originalRequest._retry = true
      
      try {
        // Attempt to refresh token
        const refreshToken = localStorage.getItem('refresh_token')
        
        if (!refreshToken) {
          throw new Error('No refresh token available')
        }
        
        const { data } = await axios.post(`${API_CONFIG.baseURL}/auth/refresh`, {
          refreshToken,
        })
        
        // Store new token
        localStorage.setItem('access_token', data.accessToken)
        
        if (data.refreshToken) {
          localStorage.setItem('refresh_token', data.refreshToken)
        }
        
        // Retry original request with new token
        if (originalRequest.headers) {
          originalRequest.headers.Authorization = `Bearer ${data.accessToken}`
        }
        
        return apiClient(originalRequest)
      } catch (refreshError) {
        // Refresh failed - Clear auth and redirect to login
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        window.location.href = '/login'
        return Promise.reject(refreshError)
      }
    }
    
    // Handle other errors
    if (error.response) {
      const { status, data } = error.response
      
      switch (status) {
        case 400:
          console.error('Bad Request:', data)
          break
        case 403:
          console.error('Forbidden:', data)
          break
        case 404:
          console.error('Not Found:', data)
          break
        case 422:
          console.error('Validation Error:', data)
          break
        case 500:
          console.error('Server Error:', data)
          break
        default:
          console.error('API Error:', data)
      }
    } else if (error.request) {
      console.error('Network Error: No response received')
    } else {
      console.error('Error:', error.message)
    }
    
    return Promise.reject(error)
  }
)

// Export typed API client
export default apiClient