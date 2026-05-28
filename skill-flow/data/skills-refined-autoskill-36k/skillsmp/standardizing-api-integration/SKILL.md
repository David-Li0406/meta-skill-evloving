---
name: standardizing-api-integration
description: Standardize API communication, error handling, and authentication. Use when building new API services or debugging network issues.
---

# API Integration Standards

## When to use this skill
- When creating new API services or endpoints.
- When setting up authentication flows.
- When debugging network errors or timeout issues.
- When configuring the HTTP client (Axios, Dio, Fetch).

## API Client Setup
- **Library**: Use a robust HTTP client like **Axios** (JS/TS) or **Dio** (Flutter). Avoid raw `fetch` for complex apps.
- **Configuration**:
    - **Base URL**: Always load from environment variables (`process.env.API_URL` or `Config.apiUrl`).
    - **Timeouts**: Set reasonable connection and receive timeouts (e.g., 10s/30s).
    - **Interceptors**: Use interceptors for:
        - Attaching Auth headers (`Authorization: Bearer ...`).
        - Logging requests/responses (in debug mode).
        - Global error handling.

## Request Handling
- **Service Layer**: Centralize all API calls in `/services` (e.g., `AuthService.ts`, `UserService.ts`). UI components should never call the API client directly.
- **Typed Responses**: Define strict TypeScript interfaces for all API response payloads. Do not use `any`.
- **Retry Logic**: Implement retry mechanisms for transient network errors (e.g., 503 Service Unavailable, timeout).
- **Cancellation**: Support request cancellation (AbortController) to prevent race conditions on unmount.

## Error Handling
Define a standardized error interface to handle exceptions consistently across the app.

```typescript
interface ApiError {
  message: string;
  status: number;
  code: string; // e.g., 'USER_NOT_FOUND'
  details?: any;
}

// Example Generic Handler
const handleApiError = (error: any): ApiError => {
  if (isAxiosError(error)) {
    // Map HTTP error to domain error
    return {
       message: error.response?.data?.message || 'Unknown error',
       status: error.response?.status || 500,
       code: error.response?.data?.code || 'SERVER_ERROR'
    };
  }
  return { message: error.message, status: 0, code: 'UNKNOWN' };
};
```

## Authentication
- **Storage**: Store tokens securely.
    - **Mobile**: Use OS keychain (Expo SecureStore / Flutter SecureStorage).
    - **Web**: Use HttpOnly cookies (preferred) or Secure LocalStorage.
- **lifecycle**:
    - **Auto-Refresh**: Intercept 401 responses to refresh the access token transparently.
    - **Logout**: Clear all local tokens and state on logout.
