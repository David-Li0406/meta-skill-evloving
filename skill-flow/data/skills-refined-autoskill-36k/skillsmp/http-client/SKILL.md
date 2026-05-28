---
name: http-client
description: HTTP client patterns for axios, ky, and native fetch. Detect which client the project uses and follow its patterns. Use for API calls, request/response interceptors, error handling, retries, and TypeScript integration.
---

# HTTP Client Skill

## 1. Client Detection (CRITICAL)

**ALWAYS detect the project's HTTP client before writing any code.**

```bash
# Check package.json for HTTP client
grep -E '"(axios|ky)"' package.json
```

### Decision Tree

1. **Check `package.json` dependencies:**
   - If `axios` is present → Use Axios patterns
   - If `ky` is present → Use Ky patterns
   - If neither → Use native `fetch`

2. **NEVER mix clients in the same project**
   - If project uses Axios, add new API calls with Axios
   - If project uses Ky, add new API calls with Ky
   - Consistency > personal preference

3. **For new projects, recommend based on needs:**
   - Need interceptors + wide browser support → Axios
   - Need small bundle + modern patterns → Ky
   - Need zero dependencies → Native fetch

---

## 2. Quick Comparison Table

| Feature | Axios | Ky | Fetch |
|---------|-------|-----|-------|
| Bundle Size | ~14kb | ~4kb | 0 (native) |
| Interceptors | Yes | Hooks | Manual |
| Auto JSON | Yes | Yes | Manual |
| Retry Built-in | No | Yes | No |
| TypeScript | Good | Excellent | Manual |
| Timeout | Config option | Config option | AbortController |
| Transform Request | Yes | beforeRequest hook | Manual |
| Transform Response | Yes | afterResponse hook | Manual |
| Cancel Request | AbortController | AbortController | AbortController |
| Node.js Support | Yes | Limited | Node 18+ |

---

## 3. Axios Patterns

### Instance Creation with Defaults

```typescript
import axios, { AxiosInstance, AxiosError, InternalAxiosRequestConfig } from 'axios';

// Create configured instance - NEVER use global axios
const api: AxiosInstance = axios.create({
  baseURL: process.env.API_BASE_URL || 'https://api.example.com',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;
```

### Request/Response Interceptors

```typescript
// Request interceptor - inject auth token
api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = getAuthToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error: AxiosError) => Promise.reject(error)
);

// Response interceptor - handle errors globally
api.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      // Handle unauthorized - redirect to login
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
```

### Error Handling (CRITICAL: error.response vs error.request)

```typescript
import { AxiosError } from 'axios';

interface ApiError {
  message: string;
  code: string;
  status: number;
}

async function fetchUser(id: string): Promise<User> {
  try {
    const { data } = await api.get<User>(`/users/${id}`);
    return data;
  } catch (error) {
    if (error instanceof AxiosError) {
      if (error.response) {
        // Server responded with error status (4xx, 5xx)
        const status = error.response.status;
        const message = error.response.data?.message || error.message;
        throw new Error(`API Error ${status}: ${message}`);
      } else if (error.request) {
        // Request made but no response (network error, timeout)
        throw new Error('Network error: No response from server');
      } else {
        // Error setting up request
        throw new Error(`Request error: ${error.message}`);
      }
    }
    throw error;
  }
}
```

### TypeScript Generics

```typescript
// Define response types
interface User {
  id: string;
  name: string;
  email: string;
}

interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  pageSize: number;
}

// Type-safe API calls
async function getUsers(page = 1): Promise<PaginatedResponse<User>> {
  const { data } = await api.get<PaginatedResponse<User>>('/users', {
    params: { page, pageSize: 20 },
  });
  return data;
}

async function createUser(user: Omit<User, 'id'>): Promise<User> {
  const { data } = await api.post<User>('/users', user);
  return data;
}

async function updateUser(id: string, updates: Partial<User>): Promise<User> {
  const { data } = await api.patch<User>(`/users/${id}`, updates);
  return data;
}
```

### Retry with Interceptor

```typescript
import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios';

interface RetryConfig extends InternalAxiosRequestConfig {
  _retryCount?: number;
}

const MAX_RETRIES = 3;
const RETRY_DELAY = 1000;

api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const config = error.config as RetryConfig;
    if (!config) return Promise.reject(error);

    config._retryCount = config._retryCount || 0;

    // Only retry on network errors or 5xx
    const shouldRetry =
      config._retryCount < MAX_RETRIES &&
      (!error.response || error.response.status >= 500);

    if (shouldRetry) {
      config._retryCount += 1;
      await new Promise((r) => setTimeout(r, RETRY_DELAY * config._retryCount!));
      return api(config);
    }

    return Promise.reject(error);
  }
);
```

### Token Refresh Pattern

```typescript
let isRefreshing = false;
let refreshSubscribers: ((token: string) => void)[] = [];

function subscribeTokenRefresh(cb: (token: string) => void) {
  refreshSubscribers.push(cb);
}

function onTokenRefreshed(token: string) {
  refreshSubscribers.forEach((cb) => cb(token));
  refreshSubscribers = [];
}

api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as RetryConfig & { _retry?: boolean };

    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        // Wait for token refresh
        return new Promise((resolve) => {
          subscribeTokenRefresh((token) => {
            originalRequest.headers.Authorization = `Bearer ${token}`;
            resolve(api(originalRequest));
          });
        });
      }

      originalRequest._retry = true;
      isRefreshing = true;

      try {
        const { data } = await axios.post('/auth/refresh', {
          refreshToken: getRefreshToken(),
        });
        const newToken = data.accessToken;
        setAuthToken(newToken);
        onTokenRefreshed(newToken);
        originalRequest.headers.Authorization = `Bearer ${newToken}`;
        return api(originalRequest);
      } catch (refreshError) {
        // Refresh failed - logout user
        logout();
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }

    return Promise.reject(error);
  }
);
```

---

## 4. Ky Patterns

### Instance Creation

```typescript
import ky, { KyInstance } from 'ky';

const api: KyInstance = ky.create({
  prefixUrl: process.env.API_BASE_URL || 'https://api.example.com',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
  retry: {
    limit: 3,
    methods: ['get', 'put', 'delete'],
    statusCodes: [408, 413, 429, 500, 502, 503, 504],
    backoffLimit: 3000,
  },
});

export default api;
```

### Hooks (beforeRequest, afterResponse, beforeRetry, beforeError)

```typescript
import ky from 'ky';

const api = ky.create({
  prefixUrl: 'https://api.example.com',
  hooks: {
    beforeRequest: [
      (request) => {
        const token = getAuthToken();
        if (token) {
          request.headers.set('Authorization', `Bearer ${token}`);
        }
      },
      (request) => {
        // Request logging
        console.log(`[API] ${request.method} ${request.url}`);
      },
    ],
    afterResponse: [
      async (request, options, response) => {
        // Response logging
        console.log(`[API] ${response.status} ${request.url}`);
        return response;
      },
      async (request, options, response) => {
        // Auto-refresh token on 401
        if (response.status === 401) {
          const newToken = await refreshToken();
          if (newToken) {
            request.headers.set('Authorization', `Bearer ${newToken}`);
            return ky(request);
          }
        }
        return response;
      },
    ],
    beforeRetry: [
      async ({ request, options, error, retryCount }) => {
        console.log(`[API] Retry ${retryCount} for ${request.url}`);
        // Modify request before retry if needed
      },
    ],
    beforeError: [
      async (error) => {
        const { response } = error;
        if (response) {
          const body = await response.json();
          error.message = body.message || error.message;
        }
        return error;
      },
    ],
  },
});
```

### Error Handling (HTTPError, TimeoutError)

```typescript
import ky, { HTTPError, TimeoutError } from 'ky';

interface ApiErrorResponse {
  message: string;
  code: string;
  details?: Record<string, string[]>;
}

async function fetchUser(id: string): Promise<User> {
  try {
    return await api.get(`users/${id}`).json<User>();
  } catch (error) {
    if (error instanceof HTTPError) {
      const status = error.response.status;
      try {
        const body = await error.response.json<ApiErrorResponse>();
        throw new Error(`API Error ${status}: ${body.message}`);
      } catch {
        throw new Error(`API Error ${status}: ${error.message}`);
      }
    }
    if (error instanceof TimeoutError) {
      throw new Error('Request timed out');
    }
    throw error;
  }
}
```

### Retry Configuration

```typescript
// Per-request retry override
const data = await api.get('flaky-endpoint', {
  retry: {
    limit: 5,
    methods: ['get'],
    statusCodes: [503],
    backoffLimit: 5000,
  },
}).json();

// Disable retry for specific request
const response = await api.post('idempotent-action', {
  json: { action: 'create' },
  retry: 0,
});
```

### TypeScript Usage

```typescript
import ky from 'ky';

interface User {
  id: string;
  name: string;
  email: string;
}

interface CreateUserRequest {
  name: string;
  email: string;
}

// Type-safe API methods
const userApi = {
  getAll: () => api.get('users').json<User[]>(),
  
  getById: (id: string) => api.get(`users/${id}`).json<User>(),
  
  create: (user: CreateUserRequest) =>
    api.post('users', { json: user }).json<User>(),
  
  update: (id: string, updates: Partial<User>) =>
    api.patch(`users/${id}`, { json: updates }).json<User>(),
  
  delete: (id: string) => api.delete(`users/${id}`),
};

// Usage
const users = await userApi.getAll();
const newUser = await userApi.create({ name: 'John', email: 'john@example.com' });
```

### Search Params

```typescript
// Ky has excellent searchParams support
const users = await api.get('users', {
  searchParams: {
    page: 1,
    limit: 20,
    sort: 'name',
    filter: ['active', 'verified'],
  },
}).json<User[]>();

// Results in: /users?page=1&limit=20&sort=name&filter=active&filter=verified
```

---

## 5. Native Fetch Patterns

### Wrapper Function with Defaults

```typescript
interface FetchOptions extends RequestInit {
  timeout?: number;
  baseURL?: string;
}

interface ApiResponse<T> {
  data: T;
  status: number;
  headers: Headers;
}

const BASE_URL = process.env.API_BASE_URL || 'https://api.example.com';

async function apiFetch<T>(
  endpoint: string,
  options: FetchOptions = {}
): Promise<ApiResponse<T>> {
  const { timeout = 10000, baseURL = BASE_URL, ...fetchOptions } = options;

  const url = endpoint.startsWith('http') ? endpoint : `${baseURL}${endpoint}`;

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);

  try {
    const response = await fetch(url, {
      ...fetchOptions,
      signal: controller.signal,
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeaders(),
        ...fetchOptions.headers,
      },
    });

    if (!response.ok) {
      const errorBody = await response.json().catch(() => ({}));
      throw new ApiError(
        errorBody.message || `HTTP ${response.status}`,
        response.status,
        errorBody
      );
    }

    const data = await response.json();
    return { data, status: response.status, headers: response.headers };
  } finally {
    clearTimeout(timeoutId);
  }
}
```

### Error Handling (check response.ok)

```typescript
class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public body?: unknown
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

async function fetchUser(id: string): Promise<User> {
  try {
    const { data } = await apiFetch<User>(`/users/${id}`);
    return data;
  } catch (error) {
    if (error instanceof ApiError) {
      if (error.status === 404) {
        throw new Error(`User ${id} not found`);
      }
      if (error.status === 401) {
        // Handle unauthorized
        redirectToLogin();
      }
      throw new Error(`API Error: ${error.message}`);
    }
    if (error instanceof DOMException && error.name === 'AbortError') {
      throw new Error('Request timed out');
    }
    throw error;
  }
}
```

### TypeScript Generics

```typescript
// Type-safe fetch helpers
const api = {
  get: <T>(url: string, options?: FetchOptions) =>
    apiFetch<T>(url, { method: 'GET', ...options }),

  post: <T>(url: string, body: unknown, options?: FetchOptions) =>
    apiFetch<T>(url, {
      method: 'POST',
      body: JSON.stringify(body),
      ...options,
    }),

  put: <T>(url: string, body: unknown, options?: FetchOptions) =>
    apiFetch<T>(url, {
      method: 'PUT',
      body: JSON.stringify(body),
      ...options,
    }),

  patch: <T>(url: string, body: unknown, options?: FetchOptions) =>
    apiFetch<T>(url, {
      method: 'PATCH',
      body: JSON.stringify(body),
      ...options,
    }),

  delete: <T>(url: string, options?: FetchOptions) =>
    apiFetch<T>(url, { method: 'DELETE', ...options }),
};

// Usage
const { data: user } = await api.get<User>('/users/123');
const { data: newUser } = await api.post<User>('/users', { name: 'John' });
```

### Retry Helper

```typescript
interface RetryOptions {
  maxRetries?: number;
  delay?: number;
  backoff?: number;
  retryOn?: number[];
}

async function fetchWithRetry<T>(
  url: string,
  options: FetchOptions & RetryOptions = {}
): Promise<ApiResponse<T>> {
  const {
    maxRetries = 3,
    delay = 1000,
    backoff = 2,
    retryOn = [408, 500, 502, 503, 504],
    ...fetchOptions
  } = options;

  let lastError: Error | undefined;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await apiFetch<T>(url, fetchOptions);
    } catch (error) {
      lastError = error as Error;

      const shouldRetry =
        attempt < maxRetries &&
        error instanceof ApiError &&
        retryOn.includes(error.status);

      if (shouldRetry) {
        const waitTime = delay * Math.pow(backoff, attempt);
        await new Promise((r) => setTimeout(r, waitTime));
        continue;
      }

      throw error;
    }
  }

  throw lastError;
}
```

---

## 6. Common Patterns (All Clients)

### Base URL Configuration

```typescript
// Environment-based configuration
const getBaseURL = (): string => {
  if (typeof window === 'undefined') {
    // Server-side
    return process.env.API_BASE_URL || 'http://localhost:3000/api';
  }
  // Client-side
  return process.env.NEXT_PUBLIC_API_URL || '/api';
};

// Use in client creation
const api = createClient({
  baseURL: getBaseURL(),
});
```

### Auth Token Injection

```typescript
// Centralized token management
const tokenManager = {
  getToken: (): string | null => {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem('access_token');
  },
  
  setToken: (token: string): void => {
    localStorage.setItem('access_token', token);
  },
  
  clearToken: (): void => {
    localStorage.removeItem('access_token');
  },
  
  getAuthHeaders: (): Record<string, string> => {
    const token = tokenManager.getToken();
    return token ? { Authorization: `Bearer ${token}` } : {};
  },
};
```

### Request/Response Logging

```typescript
// Development-only logging helper
const isDev = process.env.NODE_ENV === 'development';

function logRequest(method: string, url: string, body?: unknown): void {
  if (!isDev) return;
  console.group(`[API Request] ${method} ${url}`);
  if (body) console.log('Body:', body);
  console.groupEnd();
}

function logResponse(url: string, status: number, data: unknown): void {
  if (!isDev) return;
  console.group(`[API Response] ${status} ${url}`);
  console.log('Data:', data);
  console.groupEnd();
}

function logError(url: string, error: unknown): void {
  console.error(`[API Error] ${url}`, error);
}
```

### Error Normalization

```typescript
// Normalize errors across all HTTP clients
interface NormalizedError {
  message: string;
  status?: number;
  code?: string;
  isNetworkError: boolean;
  isTimeout: boolean;
  isServerError: boolean;
  isClientError: boolean;
  originalError: unknown;
}

function normalizeError(error: unknown): NormalizedError {
  const base: NormalizedError = {
    message: 'An unexpected error occurred',
    isNetworkError: false,
    isTimeout: false,
    isServerError: false,
    isClientError: false,
    originalError: error,
  };

  // Axios
  if (error && typeof error === 'object' && 'isAxiosError' in error) {
    const axiosError = error as AxiosError;
    return {
      ...base,
      message: axiosError.message,
      status: axiosError.response?.status,
      code: axiosError.code,
      isNetworkError: !axiosError.response,
      isTimeout: axiosError.code === 'ECONNABORTED',
      isServerError: (axiosError.response?.status ?? 0) >= 500,
      isClientError:
        (axiosError.response?.status ?? 0) >= 400 &&
        (axiosError.response?.status ?? 0) < 500,
    };
  }

  // Ky HTTPError
  if (error instanceof HTTPError) {
    const status = error.response.status;
    return {
      ...base,
      message: error.message,
      status,
      isServerError: status >= 500,
      isClientError: status >= 400 && status < 500,
    };
  }

  // Ky TimeoutError
  if (error instanceof TimeoutError) {
    return { ...base, message: 'Request timed out', isTimeout: true };
  }

  // Fetch AbortError
  if (error instanceof DOMException && error.name === 'AbortError') {
    return { ...base, message: 'Request timed out', isTimeout: true };
  }

  // Custom ApiError
  if (error instanceof ApiError) {
    return {
      ...base,
      message: error.message,
      status: error.status,
      isServerError: error.status >= 500,
      isClientError: error.status >= 400 && error.status < 500,
    };
  }

  // Generic Error
  if (error instanceof Error) {
    return { ...base, message: error.message };
  }

  return base;
}
```

---

## Quick Reference

### When to Use Each Client

| Scenario | Recommendation |
|----------|----------------|
| Large enterprise app | Axios (mature, well-documented) |
| Modern app, bundle size matters | Ky (small, modern) |
| Zero dependencies needed | Native fetch |
| Node.js backend | Axios or native fetch |
| React Native | Axios |
| Need complex interceptors | Axios |
| Need built-in retry | Ky |

### Common Mistakes to Avoid

1. **Mixing clients** - Pick one and stick with it
2. **Not handling errors** - Always catch and normalize errors
3. **Hardcoding URLs** - Use environment variables
4. **Ignoring timeouts** - Always set reasonable timeouts
5. **Not typing responses** - Use TypeScript generics
6. **Logging in production** - Use dev-only logging
7. **Token in URL** - Always use Authorization header
