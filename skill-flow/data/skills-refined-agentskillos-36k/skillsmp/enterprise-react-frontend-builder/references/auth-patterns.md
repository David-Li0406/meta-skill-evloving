# Authentication Patterns (OAuth 2.0 & JWT)

This document covers comprehensive authentication patterns for enterprise React applications, including OAuth 2.0 and JWT implementations.

## Overview

Authentication strategies:

- **OAuth 2.0** - For enterprise SSO (Azure AD, Auth0, Okta, Google)
- **JWT** - For traditional token-based authentication
- **Refresh tokens** - Seamless token renewal
- **Route guards** - Protected routes with TanStack Router
- **Token storage** - Secure storage strategies

## OAuth 2.0 Implementation

### OAuth Configuration

```ts
// src/auth/oauth/config.ts
export interface OAuthConfig {
  clientId: string
  authorizeUrl: string
  tokenUrl: string
  redirectUri: string
  scopes: string[]
  usesPKCE: boolean
}

export const oauthConfig: OAuthConfig = {
  clientId: import.meta.env.VITE_OAUTH_CLIENT_ID,
  authorizeUrl: import.meta.env.VITE_OAUTH_AUTHORIZE_URL,
  tokenUrl: import.meta.env.VITE_OAUTH_TOKEN_URL,
  redirectUri: import.meta.env.VITE_OAUTH_REDIRECT_URI || window.location.origin + '/auth/callback',
  scopes: ['openid', 'profile', 'email'],
  usesPKCE: true, // Recommended for SPA
}

// Example for Azure AD
export const azureADConfig: OAuthConfig = {
  clientId: import.meta.env.VITE_AZURE_CLIENT_ID,
  authorizeUrl: `https://login.microsoftonline.com/${import.meta.env.VITE_AZURE_TENANT_ID}/oauth2/v2.0/authorize`,
  tokenUrl: `https://login.microsoftonline.com/${import.meta.env.VITE_AZURE_TENANT_ID}/oauth2/v2.0/token`,
  redirectUri: window.location.origin + '/auth/callback',
  scopes: ['openid', 'profile', 'email', 'User.Read'],
  usesPKCE: true,
}
```

### PKCE Helper Functions

```ts
// src/auth/oauth/pkce.ts
export async function generateCodeVerifier(): Promise<string> {
  const array = new Uint8Array(32)
  crypto.getRandomValues(array)
  return base64URLEncode(array)
}

export async function generateCodeChallenge(verifier: string): Promise<string> {
  const encoder = new TextEncoder()
  const data = encoder.encode(verifier)
  const hash = await crypto.subtle.digest('SHA-256', data)
  return base64URLEncode(new Uint8Array(hash))
}

function base64URLEncode(buffer: Uint8Array): string {
  const base64 = btoa(String.fromCharCode(...buffer))
  return base64
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=/g, '')
}
```

### OAuth Flow Implementation

```ts
// src/auth/oauth/flows.ts
import { oauthConfig } from './config'
import { generateCodeVerifier, generateCodeChallenge } from './pkce'

export async function initiateOAuthLogin(): Promise<void> {
  const state = generateRandomState()
  
  // Store state in sessionStorage for validation
  sessionStorage.setItem('oauth_state', state)
  
  let authorizeUrl = new URL(oauthConfig.authorizeUrl)
  authorizeUrl.searchParams.append('client_id', oauthConfig.clientId)
  authorizeUrl.searchParams.append('redirect_uri', oauthConfig.redirectUri)
  authorizeUrl.searchParams.append('response_type', 'code')
  authorizeUrl.searchParams.append('scope', oauthConfig.scopes.join(' '))
  authorizeUrl.searchParams.append('state', state)
  
  // PKCE (Recommended for SPAs)
  if (oauthConfig.usesPKCE) {
    const codeVerifier = await generateCodeVerifier()
    const codeChallenge = await generateCodeChallenge(codeVerifier)
    
    sessionStorage.setItem('pkce_verifier', codeVerifier)
    authorizeUrl.searchParams.append('code_challenge', codeChallenge)
    authorizeUrl.searchParams.append('code_challenge_method', 'S256')
  }
  
  // Redirect to authorization server
  window.location.href = authorizeUrl.toString()
}

export async function handleOAuthCallback(
  code: string,
  state: string
): Promise<{ accessToken: string; refreshToken?: string }> {
  // Validate state
  const savedState = sessionStorage.getItem('oauth_state')
  if (state !== savedState) {
    throw new Error('Invalid state parameter')
  }
  
  // Exchange code for tokens
  const body: Record<string, string> = {
    grant_type: 'authorization_code',
    code,
    redirect_uri: oauthConfig.redirectUri,
    client_id: oauthConfig.clientId,
  }
  
  // Include PKCE verifier
  if (oauthConfig.usesPKCE) {
    const codeVerifier = sessionStorage.getItem('pkce_verifier')
    if (!codeVerifier) {
      throw new Error('PKCE verifier not found')
    }
    body.code_verifier = codeVerifier
  }
  
  const response = await fetch(oauthConfig.tokenUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: new URLSearchParams(body),
  })
  
  if (!response.ok) {
    throw new Error('Token exchange failed')
  }
  
  const data = await response.json()
  
  // Cleanup
  sessionStorage.removeItem('oauth_state')
  sessionStorage.removeItem('pkce_verifier')
  
  return {
    accessToken: data.access_token,
    refreshToken: data.refresh_token,
  }
}

function generateRandomState(): string {
  const array = new Uint8Array(32)
  crypto.getRandomValues(array)
  return Array.from(array, (byte) => byte.toString(16).padStart(2, '0')).join('')
}
```

### OAuth Provider Component

```tsx
// src/auth/oauth/OAuthProvider.tsx
import { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import { initiateOAuthLogin, handleOAuthCallback } from './flows'
import { useNavigate } from '@tanstack/react-router'

interface OAuthContextValue {
  isAuthenticated: boolean
  user: User | null
  login: () => void
  logout: () => void
  isLoading: boolean
}

const OAuthContext = createContext<OAuthContextValue | undefined>(undefined)

export function OAuthProvider({ children }: { children: ReactNode }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const navigate = useNavigate()
  
  useEffect(() => {
    // Check for existing token
    const token = localStorage.getItem('access_token')
    if (token) {
      // Validate and fetch user
      fetchUser(token)
    } else {
      setIsLoading(false)
    }
  }, [])
  
  const login = () => {
    initiateOAuthLogin()
  }
  
  const logout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    setIsAuthenticated(false)
    setUser(null)
    navigate({ to: '/login' })
  }
  
  const fetchUser = async (token: string) => {
    try {
      // Fetch user profile from OAuth provider or your API
      const response = await fetch('/api/auth/me', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      
      if (response.ok) {
        const userData = await response.json()
        setUser(userData)
        setIsAuthenticated(true)
      } else {
        logout()
      }
    } catch (error) {
      console.error('Failed to fetch user:', error)
      logout()
    } finally {
      setIsLoading(false)
    }
  }
  
  return (
    <OAuthContext.Provider value={{ isAuthenticated, user, login, logout, isLoading }}>
      {children}
    </OAuthContext.Provider>
  )
}

export function useOAuth() {
  const context = useContext(OAuthContext)
  if (!context) {
    throw new Error('useOAuth must be used within OAuthProvider')
  }
  return context
}
```

### OAuth Callback Page

```tsx
// src/pages/Auth/OAuthCallbackPage.tsx
import { useEffect } from 'react'
import { useNavigate, useSearch } from '@tanstack/react-router'
import { handleOAuthCallback } from '@/auth/oauth/flows'

export default function OAuthCallbackPage() {
  const navigate = useNavigate()
  const search = useSearch({ from: '/auth/callback' })
  
  useEffect(() => {
    const processCallback = async () => {
      try {
        const { code, state } = search as { code: string; state: string }
        
        if (!code || !state) {
          throw new Error('Invalid callback parameters')
        }
        
        const { accessToken, refreshToken } = await handleOAuthCallback(code, state)
        
        // Store tokens
        localStorage.setItem('access_token', accessToken)
        if (refreshToken) {
          localStorage.setItem('refresh_token', refreshToken)
        }
        
        // Redirect to app
        navigate({ to: '/dashboard' })
      } catch (error) {
        console.error('OAuth callback error:', error)
        navigate({ to: '/login', search: { error: 'auth_failed' } })
      }
    }
    
    processCallback()
  }, [search, navigate])
  
  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="text-center">
        <Spinner />
        <p className="mt-4 text-gray-600">Completing login...</p>
      </div>
    </div>
  )
}
```

## JWT Authentication Implementation

### JWT Token Management

```ts
// src/auth/jwt/tokens.ts
const ACCESS_TOKEN_KEY = 'access_token'
const REFRESH_TOKEN_KEY = 'refresh_token'

export function getAuthToken(): string | null {
  return localStorage.getItem(ACCESS_TOKEN_KEY)
}

export function setAuthToken(token: string): void {
  localStorage.setItem(ACCESS_TOKEN_KEY, token)
}

export function getRefreshToken(): string | null {
  return localStorage.getItem(REFRESH_TOKEN_KEY)
}

export function setRefreshToken(token: string): void {
  localStorage.setItem(REFRESH_TOKEN_KEY, token)
}

export function clearAuth(): void {
  localStorage.removeItem(ACCESS_TOKEN_KEY)
  localStorage.removeItem(REFRESH_TOKEN_KEY)
}

// Decode JWT (without verification - for client-side use only)
export function decodeToken<T = Record<string, unknown>>(token: string): T | null {
  try {
    const base64Url = token.split('.')[1]
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/')
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    )
    return JSON.parse(jsonPayload)
  } catch (error) {
    console.error('Failed to decode token:', error)
    return null
  }
}

// Check if token is expired
export function isTokenExpired(token: string): boolean {
  const decoded = decodeToken<{ exp: number }>(token)
  if (!decoded || !decoded.exp) return true
  
  return decoded.exp * 1000 < Date.now()
}

// Refresh access token
export async function refreshAuthToken(): Promise<string | null> {
  const refreshToken = getRefreshToken()
  
  if (!refreshToken) {
    return null
  }
  
  try {
    const response = await fetch('/api/auth/refresh', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ refreshToken }),
    })
    
    if (!response.ok) {
      clearAuth()
      return null
    }
    
    const data = await response.json()
    setAuthToken(data.accessToken)
    
    if (data.refreshToken) {
      setRefreshToken(data.refreshToken)
    }
    
    return data.accessToken
  } catch (error) {
    console.error('Token refresh failed:', error)
    clearAuth()
    return null
  }
}
```

### JWT Auth Provider

```tsx
// src/auth/jwt/JWTProvider.tsx
import { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import { getAuthToken, setAuthToken, setRefreshToken, clearAuth, decodeToken } from './tokens'
import { apiClient } from '@/api/client'

interface JWTContextValue {
  isAuthenticated: boolean
  user: User | null
  login: (email: string, password: string) => Promise<void>
  logout: () => void
  isLoading: boolean
}

const JWTContext = createContext<JWTContextValue | undefined>(undefined)

export function JWTProvider({ children }: { children: ReactNode }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  
  useEffect(() => {
    const initAuth = async () => {
      const token = getAuthToken()
      
      if (token) {
        try {
          // Fetch user profile
          const response = await apiClient.get('/auth/me')
          setUser(response.data)
          setIsAuthenticated(true)
        } catch (error) {
          clearAuth()
        }
      }
      
      setIsLoading(false)
    }
    
    initAuth()
  }, [])
  
  const login = async (email: string, password: string) => {
    const response = await apiClient.post('/auth/login', { email, password })
    
    const { accessToken, refreshToken, user: userData } = response.data
    
    setAuthToken(accessToken)
    setRefreshToken(refreshToken)
    setUser(userData)
    setIsAuthenticated(true)
  }
  
  const logout = () => {
    clearAuth()
    setUser(null)
    setIsAuthenticated(false)
  }
  
  return (
    <JWTContext.Provider value={{ isAuthenticated, user, login, logout, isLoading }}>
      {children}
    </JWTContext.Provider>
  )
}

export function useJWT() {
  const context = useContext(JWTContext)
  if (!context) {
    throw new Error('useJWT must be used within JWTProvider')
  }
  return context
}
```

### Login Page

```tsx
// src/pages/Auth/LoginPage.tsx
import { useState } from 'react'
import { useNavigate } from '@tanstack/react-router'
import { useAuth } from '@/auth/useAuth'
import { TkButton, TkInput } from '@takeoff-ui/react'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const { login, isLoading } = useAuth()
  const navigate = useNavigate()
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    
    try {
      await login(email, password)
      navigate({ to: '/dashboard' })
    } catch (err) {
      setError('Invalid email or password')
    }
  }
  
  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-50">
      <div className="w-full max-w-md p-8 bg-white rounded-lg shadow-md">
        <h1 className="text-2xl font-bold text-center mb-6">Login</h1>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Email</label>
            <TkInput
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your email"
              required
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-1">Password</label>
            <TkInput
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              required
            />
          </div>
          
          {error && (
            <p className="text-sm text-red-500">{error}</p>
          )}
          
          <TkButton
            label="Login"
            type="submit"
            loading={isLoading}
            className="w-full"
          />
        </form>
      </div>
    </div>
  )
}
```

## Route Guards with TanStack Router

### Protected Route Guard

```tsx
// src/auth/guards/ProtectedRoute.tsx
import { useEffect } from 'react'
import { useNavigate } from '@tanstack/react-router'
import { useAuth } from '../useAuth'
import { Outlet } from '@tanstack/react-router'

export function ProtectedRoute() {
  const { isAuthenticated, isLoading } = useAuth()
  const navigate = useNavigate()
  
  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      navigate({ to: '/login' })
    }
  }, [isAuthenticated, isLoading, navigate])
  
  if (isLoading) {
    return <div className="flex items-center justify-center min-h-screen">Loading...</div>
  }
  
  if (!isAuthenticated) {
    return null
  }
  
  return <Outlet />
}
```

### Role-Based Guard

```tsx
// src/auth/guards/RoleGuard.tsx
import { useAuth } from '../useAuth'
import { Navigate } from '@tanstack/react-router'

interface RoleGuardProps {
  allowedRoles: string[]
  children: React.ReactNode
}

export function RoleGuard({ allowedRoles, children }: RoleGuardProps) {
  const { user } = useAuth()
  
  if (!user || !allowedRoles.includes(user.role)) {
    return <Navigate to="/unauthorized" />
  }
  
  return <>{children}</>
}

// Usage
<RoleGuard allowedRoles={['admin']}>
  <AdminPanel />
</RoleGuard>
```

### Router Configuration with Guards

```tsx
// src/routes/index.tsx
import { createRouter, createRoute, createRootRoute } from '@tanstack/react-router'
import { ProtectedRoute } from '@/auth/guards/ProtectedRoute'
import DashboardPage from '@/pages/Dashboard'
import LoginPage from '@/pages/Auth/LoginPage'

const rootRoute = createRootRoute()

// Public routes
const loginRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/login',
  component: LoginPage,
})

// Protected routes
const protectedRoute = createRoute({
  getParentRoute: () => rootRoute,
  id: 'protected',
  component: ProtectedRoute,
})

const dashboardRoute = createRoute({
  getParentRoute: () => protectedRoute,
  path: '/dashboard',
  component: DashboardPage,
})

const routeTree = rootRoute.addChildren([
  loginRoute,
  protectedRoute.addChildren([dashboardRoute]),
])

export const router = createRouter({ routeTree })
```

## Token Refresh Interceptor

Already implemented in [references/api-architecture.md](references/api-architecture.md), but here's the key part:

```ts
// src/api/client.ts
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      
      const newToken = await refreshAuthToken()
      
      if (newToken && originalRequest.headers) {
        originalRequest.headers.Authorization = `Bearer ${newToken}`
        return apiClient(originalRequest)
      }
    }
    
    return Promise.reject(error)
  }
)
```

## Secure Token Storage

### Option 1: httpOnly Cookies (Most Secure)

```ts
// Backend sets httpOnly cookies
// Frontend automatically sends cookies with requests
// Immune to XSS attacks

// Axios configuration
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true, // Send cookies with requests
})
```

### Option 2: Memory + sessionStorage (Good)

```ts
// Store in memory for access, sessionStorage for refresh
let accessToken: string | null = null

export function getAuthToken(): string | null {
  return accessToken
}

export function setAuthToken(token: string): void {
  accessToken = token
  // Only store refresh token in sessionStorage
  // Access token stays in memory
}
```

### Option 3: localStorage (Least Secure, but Simple)

```ts
// Already shown above
// Vulnerable to XSS, but acceptable for low-risk applications
```

## Best Practices

1. **Use PKCE for OAuth** - Protects against authorization code interception
2. **Rotate refresh tokens** - Issue new refresh token with each refresh
3. **Short-lived access tokens** - 15-30 minutes max
4. **httpOnly cookies** - Most secure storage for tokens
5. **CSRF protection** - Use anti-CSRF tokens for state-changing operations
6. **Token validation** - Verify tokens on backend
7. **Logout on token refresh failure** - Clear all auth state
8. **Redirect after login** - Return to originally requested page
9. **Secure redirect URIs** - Whitelist allowed redirect URIs
10. **Monitor failed attempts** - Implement rate limiting on auth endpoints

## Summary

This authentication architecture provides:

- **Flexible auth strategies** - OAuth 2.0 and JWT support
- **Secure token management** - Refresh, storage, validation
- **Route protection** - Guards for authenticated and role-based access
- **Seamless UX** - Automatic token refresh, redirect handling
- **Enterprise-ready** - SSO integration, PKCE, security best practices

Choose OAuth 2.0 for enterprise SSO, JWT for traditional auth, or support both for maximum flexibility.