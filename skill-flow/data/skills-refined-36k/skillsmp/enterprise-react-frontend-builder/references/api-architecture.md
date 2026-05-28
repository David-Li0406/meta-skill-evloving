# API Architecture and Centralized Client

This document details the centralized API client architecture with authentication, error handling, and interceptors.

## Overview

All API communication flows through a single, centralized client with:

- **Request/Response Interceptors** - Auth headers, logging, error handling
- **Token Management** - Automatic token refresh
- **Type Safety** - TypeScript throughout
- **Error Standardization** - Consistent error format
- **Request Cancellation** - AbortController support

## API Client Implementation

### Base Client

```ts
// src/api/client.ts
import axios, { AxiosError, AxiosRequestConfig, AxiosResponse } from 'axios'
import { apiConfig } from './config'
import { getAuthToken, refreshAuthToken, clearAuth } from '@/auth/jwt/tokens'

// Create axios instance
export const apiClient = axios.create({
  baseURL: apiConfig.baseURL,
  timeout: apiConfig.timeout,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor - Add auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = getAuthToken()
    
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    // Log request in development
    if (import.meta.env.DEV) {
      console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`, config.data)
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
      console.log(`[API] Response from ${response.config.url}`, response.data)
    }
    
    return response
  },
  async (error: AxiosError) => {
    const originalRequest = error.config as AxiosRequestConfig & { _retry?: boolean }
    
    // Handle 401 Unauthorized - Token expired
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      
      try {
        // Attempt to refresh token
        const newToken = await refreshAuthToken()
        
        if (newToken && originalRequest.headers) {
          originalRequest.headers.Authorization = `Bearer ${newToken}`
          return apiClient(originalRequest)
        }
      } catch (refreshError) {
        // Refresh failed - Clear auth and redirect to login
        clearAuth()
        window.location.href = '/login'
        return Promise.reject(refreshError)
      }
    }
    
    // Handle other errors
    return Promise.reject(error)
  }
)
```

### API Configuration

```ts
// src/api/config.ts
export const apiConfig = {
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:3000/api',
  timeout: 30000, // 30 seconds
  retryAttempts: 3,
  retryDelay: 1000, // 1 second
}

// API endpoints
export const API_ENDPOINTS = {
  auth: {
    login: '/auth/login',
    logout: '/auth/logout',
    refresh: '/auth/refresh',
    register: '/auth/register',
    forgotPassword: '/auth/forgot-password',
    resetPassword: '/auth/reset-password',
  },
  users: {
    base: '/users',
    byId: (id: string) => `/users/${id}`,
    profile: '/users/profile',
  },
  products: {
    base: '/products',
    byId: (id: string) => `/products/${id}`,
    categories: '/products/categories',
  },
} as const
```

## Type-Safe API Responses

### Response Types

```ts
// src/api/types/responses.ts
export interface ApiResponse<T = unknown> {
  success: boolean
  data: T
  message?: string
  meta?: {
    page?: number
    pageSize?: number
    total?: number
    totalPages?: number
  }
}

export interface ApiError {
  success: false
  error: {
    code: string
    message: string
    details?: Record<string, unknown>
    stack?: string
  }
}

export interface PaginatedResponse<T> {
  items: T[]
  page: number
  pageSize: number
  total: number
  totalPages: number
}
```

### Request Types

```ts
// src/api/types/requests.ts
export interface PaginationParams {
  page?: number
  pageSize?: number
  sortBy?: string
  sortOrder?: 'asc' | 'desc'
}

export interface FilterParams {
  search?: string
  status?: string
  dateFrom?: string
  dateTo?: string
}

export interface CreateUserDto {
  firstName: string
  lastName: string
  email: string
  password: string
  role: 'admin' | 'user'
}

export interface UpdateUserDto {
  firstName?: string
  lastName?: string
  email?: string
  role?: 'admin' | 'user'
}
```

## Endpoint Organization

### Users Endpoint

```ts
// src/api/endpoints/users.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { apiClient } from '../client'
import { API_ENDPOINTS } from '../config'
import type { User } from '@/types/models'
import type { CreateUserDto, UpdateUserDto, PaginationParams } from '../types/requests'
import type { PaginatedResponse } from '../types/responses'

// Raw API functions
export const usersApi = {
  getAll: async (params?: PaginationParams) => {
    const { data } = await apiClient.get<PaginatedResponse<User>>(
      API_ENDPOINTS.users.base,
      { params }
    )
    return data
  },
  
  getById: async (id: string) => {
    const { data } = await apiClient.get<User>(API_ENDPOINTS.users.byId(id))
    return data
  },
  
  create: async (userData: CreateUserDto) => {
    const { data } = await apiClient.post<User>(API_ENDPOINTS.users.base, userData)
    return data
  },
  
  update: async (id: string, userData: UpdateUserDto) => {
    const { data } = await apiClient.put<User>(
      API_ENDPOINTS.users.byId(id),
      userData
    )
    return data
  },
  
  delete: async (id: string) => {
    await apiClient.delete(API_ENDPOINTS.users.byId(id))
  },
  
  search: async (searchTerm: string) => {
    const { data } = await apiClient.get<User[]>(`${API_ENDPOINTS.users.base}/search`, {
      params: { q: searchTerm },
    })
    return data
  },
}

// Query hooks
export const useUsers = (params?: PaginationParams) => {
  return useQuery({
    queryKey: ['users', params],
    queryFn: () => usersApi.getAll(params),
  })
}

export const useUser = (id: string) => {
  return useQuery({
    queryKey: ['users', id],
    queryFn: () => usersApi.getById(id),
    enabled: !!id,
  })
}

export const useSearchUsers = (searchTerm: string) => {
  return useQuery({
    queryKey: ['users', 'search', searchTerm],
    queryFn: () => usersApi.search(searchTerm),
    enabled: searchTerm.length > 2,
  })
}

// Mutation hooks
export const useCreateUser = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: usersApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] })
    },
  })
}

export const useUpdateUser = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: UpdateUserDto }) =>
      usersApi.update(id, data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['users'] })
      queryClient.invalidateQueries({ queryKey: ['users', variables.id] })
    },
  })
}

export const useDeleteUser = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: usersApi.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] })
    },
  })
}
```

## Error Handling

### Error Types

```ts
// src/api/types/errors.ts
export class ApiError extends Error {
  constructor(
    public statusCode: number,
    public code: string,
    message: string,
    public details?: Record<string, unknown>
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

export class NetworkError extends Error {
  constructor(message: string = 'Network error occurred') {
    super(message)
    this.name = 'NetworkError'
  }
}

export class ValidationError extends ApiError {
  constructor(message: string, public errors: Record<string, string[]>) {
    super(422, 'VALIDATION_ERROR', message, errors)
    this.name = 'ValidationError'
  }
}
```

### Error Handler

```ts
// src/api/errorHandler.ts
import { AxiosError } from 'axios'
import { ApiError, NetworkError, ValidationError } from './types/errors'
import toast from 'react-hot-toast' // or your toast library

export function handleApiError(error: unknown): never {
  if (error instanceof AxiosError) {
    const response = error.response
    
    if (!response) {
      // Network error
      toast.error('Network error. Please check your connection.')
      throw new NetworkError()
    }
    
    const { status, data } = response
    
    // Handle specific status codes
    switch (status) {
      case 400:
        toast.error(data?.message || 'Bad request')
        throw new ApiError(status, 'BAD_REQUEST', data?.message)
        
      case 401:
        toast.error('Session expired. Please login again.')
        throw new ApiError(status, 'UNAUTHORIZED', 'Unauthorized')
        
      case 403:
        toast.error('You do not have permission to perform this action')
        throw new ApiError(status, 'FORBIDDEN', 'Forbidden')
        
      case 404:
        toast.error('Resource not found')
        throw new ApiError(status, 'NOT_FOUND', 'Not found')
        
      case 422:
        toast.error('Validation failed. Please check your input.')
        throw new ValidationError(data?.message || 'Validation failed', data?.errors)
        
      case 429:
        toast.error('Too many requests. Please try again later.')
        throw new ApiError(status, 'TOO_MANY_REQUESTS', 'Rate limit exceeded')
        
      case 500:
        toast.error('Server error. Please try again later.')
        throw new ApiError(status, 'INTERNAL_SERVER_ERROR', 'Internal server error')
        
      default:
        toast.error('An unexpected error occurred')
        throw new ApiError(status, 'UNKNOWN_ERROR', data?.message || 'Unknown error')
    }
  }
  
  // Unknown error
  toast.error('An unexpected error occurred')
  throw error
}
```

### Using Error Handler

```tsx
// In components
import { handleApiError } from '@/api/errorHandler'

function UsersList() {
  const { data, error } = useUsers()
  
  useEffect(() => {
    if (error) {
      try {
        handleApiError(error)
      } catch (e) {
        // Error already handled, can log or ignore
      }
    }
  }, [error])
  
  return <div>...</div>
}
```

## Request Retry Logic

```ts
// src/api/retry.ts
import { AxiosError, AxiosRequestConfig } from 'axios'
import { apiClient } from './client'
import { apiConfig } from './config'

export async function retryRequest<T>(
  requestFn: () => Promise<T>,
  maxAttempts: number = apiConfig.retryAttempts,
  delay: number = apiConfig.retryDelay
): Promise<T> {
  let lastError: Error
  
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await requestFn()
    } catch (error) {
      lastError = error as Error
      
      // Don't retry client errors (4xx)
      if (error instanceof AxiosError && error.response?.status && error.response.status < 500) {
        throw error
      }
      
      // Don't retry on last attempt
      if (attempt === maxAttempts) {
        break
      }
      
      // Wait before retrying (exponential backoff)
      const waitTime = delay * Math.pow(2, attempt - 1)
      await new Promise((resolve) => setTimeout(resolve, waitTime))
      
      console.log(`Retrying request (attempt ${attempt + 1}/${maxAttempts})...`)
    }
  }
  
  throw lastError!
}

// Usage
export const usersApiWithRetry = {
  getAll: () => retryRequest(() => usersApi.getAll()),
  getById: (id: string) => retryRequest(() => usersApi.getById(id)),
}
```

## File Upload

```ts
// src/api/endpoints/upload.ts
import { apiClient } from '../client'

export const uploadApi = {
  uploadFile: async (file: File, onProgress?: (progress: number) => void) => {
    const formData = new FormData()
    formData.append('file', file)
    
    const { data } = await apiClient.post<{ url: string }>('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        if (progressEvent.total && onProgress) {
          const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total)
          onProgress(progress)
        }
      },
    })
    
    return data
  },
  
  uploadMultiple: async (files: File[]) => {
    const formData = new FormData()
    
    files.forEach((file, index) => {
      formData.append(`files[${index}]`, file)
    })
    
    const { data } = await apiClient.post<{ urls: string[] }>('/upload/multiple', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    
    return data
  },
}

// Usage with mutation
export const useUploadFile = () => {
  const [progress, setProgress] = useState(0)
  
  const mutation = useMutation({
    mutationFn: (file: File) => uploadApi.uploadFile(file, setProgress),
  })
  
  return { ...mutation, progress }
}
```

## Request Cancellation

```ts
// src/api/endpoints/search.ts
import { useQuery } from '@tanstack/react-query'
import { apiClient } from '../client'

export const useSearchProducts = (searchTerm: string) => {
  return useQuery({
    queryKey: ['products', 'search', searchTerm],
    queryFn: async ({ signal }) => {
      // Pass AbortSignal to axios
      const { data } = await apiClient.get('/products/search', {
        params: { q: searchTerm },
        signal,
      })
      return data
    },
    enabled: searchTerm.length > 2,
  })
}
```

## Rate Limiting

```ts
// src/api/rateLimit.ts
class RateLimiter {
  private requests: number[] = []
  private maxRequests: number
  private windowMs: number
  
  constructor(maxRequests: number = 100, windowMs: number = 60000) {
    this.maxRequests = maxRequests
    this.windowMs = windowMs
  }
  
  async checkLimit(): Promise<void> {
    const now = Date.now()
    
    // Remove old requests outside the window
    this.requests = this.requests.filter((time) => now - time < this.windowMs)
    
    if (this.requests.length >= this.maxRequests) {
      const oldestRequest = this.requests[0]
      const waitTime = this.windowMs - (now - oldestRequest)
      
      throw new Error(`Rate limit exceeded. Please wait ${Math.ceil(waitTime / 1000)} seconds.`)
    }
    
    this.requests.push(now)
  }
}

export const rateLimiter = new RateLimiter(100, 60000) // 100 requests per minute

// Add to request interceptor
apiClient.interceptors.request.use(
  async (config) => {
    await rateLimiter.checkLimit()
    return config
  },
  (error) => Promise.reject(error)
)
```

## API Mocking for Development

```ts
// src/api/mock.ts
import { rest } from 'msw'
import { setupWorker } from 'msw/browser'

const handlers = [
  rest.get('/api/users', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        items: [
          { id: '1', firstName: 'John', lastName: 'Doe', email: 'john@example.com' },
          { id: '2', firstName: 'Jane', lastName: 'Doe', email: 'jane@example.com' },
        ],
        page: 1,
        pageSize: 10,
        total: 2,
        totalPages: 1,
      })
    )
  }),
  
  rest.post('/api/users', async (req, res, ctx) => {
    const body = await req.json()
    
    return res(
      ctx.status(201),
      ctx.json({
        id: '3',
        ...body,
      })
    )
  }),
]

export const worker = setupWorker(...handlers)

// Enable in development
if (import.meta.env.DEV && import.meta.env.VITE_ENABLE_MOCKS === 'true') {
  worker.start()
}
```

## WebSocket Integration

```ts
// src/api/websocket.ts
import { useEffect, useState } from 'react'
import { getAuthToken } from '@/auth/jwt/tokens'

export function useWebSocket<T>(url: string) {
  const [data, setData] = useState<T | null>(null)
  const [isConnected, setIsConnected] = useState(false)
  const [error, setError] = useState<Error | null>(null)
  
  useEffect(() => {
    const token = getAuthToken()
    const ws = new WebSocket(`${url}?token=${token}`)
    
    ws.onopen = () => {
      setIsConnected(true)
      console.log('WebSocket connected')
    }
    
    ws.onmessage = (event) => {
      try {
        const parsedData = JSON.parse(event.data) as T
        setData(parsedData)
      } catch (err) {
        setError(err as Error)
      }
    }
    
    ws.onerror = (event) => {
      setError(new Error('WebSocket error'))
      console.error('WebSocket error:', event)
    }
    
    ws.onclose = () => {
      setIsConnected(false)
      console.log('WebSocket disconnected')
    }
    
    return () => {
      ws.close()
    }
  }, [url])
  
  return { data, isConnected, error }
}

// Usage
function NotificationsWidget() {
  const { data: notification, isConnected } = useWebSocket<Notification>(
    'ws://localhost:3000/notifications'
  )
  
  return (
    <div>
      {isConnected && <span>🟢 Connected</span>}
      {notification && <NotificationItem notification={notification} />}
    </div>
  )
}
```

## Best Practices

1. **Centralize all API calls** - Never use fetch/axios directly in components
2. **Use TanStack Query hooks** - Leverage caching and automatic refetching
3. **Type everything** - Request DTOs, response types, error types
4. **Handle errors globally** - Use interceptors and error boundaries
5. **Implement token refresh** - Seamless auth token renewal
6. **Add request logging** - Debug API issues easily
7. **Use AbortSignal** - Cancel pending requests when component unmounts
8. **Implement rate limiting** - Protect against abuse
9. **Mock API in development** - Test without backend
10. **Monitor API performance** - Track slow endpoints

## Summary

This centralized API architecture provides:

- **Single source of truth** - All API logic in one place
- **Automatic authentication** - Token injection and refresh
- **Consistent error handling** - Standardized error messages
- **Type safety** - TypeScript throughout
- **Performance optimization** - Caching, retries, cancellation
- **Developer experience** - Easy debugging and testing

Follow these patterns for maintainable, scalable API integrations.