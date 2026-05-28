---
name: eridu-authentication-authorization-frontend
description: Provides frontend-specific authentication and authorization implementation patterns for React applications. This skill should be used when implementing login flows, protecting routes, storing tokens securely, managing user context, refreshing tokens, or handling logout.
---

# Eridu Services - Frontend Authentication & Authorization Skill

Provides guidance for implementing frontend authentication and authorization patterns in Eridu Services (React apps: erify_creators, erify_studios, eridu_auth UI).

## Frontend Responsibilities

1. **Collect credentials** - Login form, SSO flow, password input
2. **Store credentials securely** - Token management, session storage
3. **Send credentials with requests** - Attach token to API calls
4. **Manage user context** - Keep track of who is logged in
5. **Protect routes** - Prevent access to pages user shouldn't see
6. **Handle expiration** - Refresh tokens, redirect on logout

## Core Principles

### Secure Token Storage

**Rule**: Don't store sensitive tokens in unsafe locations

**Options by security level**:

1. **Most Secure** - HTTP-only Cookies
   - ✅ Token cannot be accessed by JavaScript
   - ✅ Automatically sent with requests
   - ✅ Protected against XSS attacks
   - Use for: Production environments, sensitive apps

2. **Good** - Secure Session Storage
   - ✅ Token cleared when tab closes
   - ✅ Cannot be accessed by other sites
   - ⚠️ Can be accessed by other tabs/scripts on same site
   - Use for: Medium-security apps, internal tools

3. **Poor** - localStorage
   - ❌ Accessible to any JavaScript on the page
   - ❌ Persists after browser close
   - ❌ Vulnerable to XSS attacks
   - Avoid if: Storing authentication tokens

**Never**:
- ❌ Store tokens in URL
- ❌ Store tokens in plaintext
- ❌ Log tokens to console
- ❌ Display tokens in UI

### Validate on Every Render

**Rule**: Don't assume user is authenticated; check on mount

```typescript
// ✅ CORRECT: Check auth on mount
useEffect(() => {
  const token = authStorage.getToken();
  if (!token) {
    navigate('/login');
  }
}, []);

// ❌ WRONG: Assume auth persists
const user = useAuth(); // Might be null!
```

### Handle Expiration Gracefully

**Rule**: Refresh tokens before expiration; redirect on failure

```typescript
// ✅ Refresh before expiration
const expiresIn = parseJwt(token).exp - Date.now();
const refreshTime = expiresIn - 5 * 60 * 1000; // 5 min before

setTimeout(() => {
  authService.refresh().catch(() => {
    // Refresh failed - log out
    handleLogout();
  });
}, refreshTime);

// ❌ Let it expire
// Don't ignore token expiration - leads to 401 errors
```

### Protect All Sensitive Routes

**Rule**: Require authentication before showing sensitive pages

```typescript
// ✅ CORRECT: Redirect to login if not authenticated
<Route 
  path="/admin"
  element={<ProtectedRoute><AdminPage /></ProtectedRoute>}
/>

// ❌ WRONG: Show page then check auth
<Route path="/admin" element={<AdminPage />} />
// (AdminPage would handle auth check - bad UX)
```

## Implementation Patterns

### Login Flow

```typescript
async function handleLogin(email: string, password: string) {
  try {
    // 1. Call login endpoint
    const response = await apiClient.post('/auth/login', {
      email,
      password,
    });

    const { token, user } = response.data;

    // 2. Store token securely
    authStorage.setToken(token);

    // 3. Update app state
    setUser(user);
    setIsAuthenticated(true);

    // 4. Navigate to authenticated area
    navigate('/dashboard');
  } catch (error) {
    // 5. Show user-friendly error
    setError('Invalid email or password');
  }
}
```

**Checklist**:
- [ ] Login endpoint validates credentials on backend
- [ ] Token is stored securely (not in state only)
- [ ] User context is updated after successful login
- [ ] Errors don't reveal sensitive information
- [ ] Loading state prevents double-submission
- [ ] Redirect happens after state is set

### Protected Routes

```typescript
function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { user, isLoading } = useAuth();

  // Handle loading state (checking auth on mount)
  if (isLoading) {
    return <LoadingSpinner />;
  }

  // Redirect unauthenticated users
  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return children;
}

// Usage
<Routes>
  <Route path="/login" element={<LoginPage />} />
  <Route
    path="/dashboard"
    element={
      <ProtectedRoute>
        <DashboardPage />
      </ProtectedRoute>
    }
  />
</Routes>
```

**Checklist**:
- [ ] Loading state is handled during auth check
- [ ] Unauthenticated users are redirected
- [ ] Redirect uses `replace` to prevent back button issues
- [ ] Protected page is not rendered until auth confirmed
- [ ] Loading spinner shown while checking auth

### User Context Provider

```typescript
// Create context
export const AuthContext = createContext<AuthContextType | null>(null);

// Provider component
export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Check auth on mount
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const token = authStorage.getToken();
        if (token) {
          // Validate token with backend
          const response = await apiClient.get('/auth/me');
          setUser(response.data);
        }
      } catch (error) {
        // Token invalid - clear it
        authStorage.clearToken();
      } finally {
        setIsLoading(false);
      }
    };

    checkAuth();
  }, []);

  return (
    <AuthContext.Provider value={{ user, setUser, isLoading }}>
      {children}
    </AuthContext.Provider>
  );
}

// Hook to use context
export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
```

**Checklist**:
- [ ] Auth is checked on app mount
- [ ] User context is available app-wide
- [ ] Loading state prevents race conditions
- [ ] Invalid tokens are cleared
- [ ] Error during auth check is handled gracefully

### Logout

```typescript
async function handleLogout() {
  try {
    // 1. Notify backend (optional)
    await apiClient.post('/auth/logout');
  } catch (error) {
    // Proceed even if backend fails
    console.warn('Logout notification failed', error);
  } finally {
    // 2. Clear stored token
    authStorage.clearToken();

    // 3. Clear user context
    setUser(null);
    setIsAuthenticated(false);

    // 4. Redirect to login
    navigate('/login', { replace: true });
  }
}
```

**Checklist**:
- [ ] Backend is notified (if implementing logout endpoint)
- [ ] Token is cleared from storage
- [ ] User context is cleared
- [ ] User is redirected to login
- [ ] Logout completes even if backend fails

### Token Refresh

```typescript
function useTokenRefresh() {
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    if (!isAuthenticated) return;

    // Calculate refresh interval (e.g., refresh 5 min before expiry)
    const token = authStorage.getToken();
    const decoded = parseJwt(token);
    const expiresIn = decoded.exp * 1000 - Date.now();
    const refreshTime = expiresIn - 5 * 60 * 1000; // 5 min before expiry

    const timeoutId = setTimeout(async () => {
      try {
        const response = await apiClient.post('/auth/refresh');
        const { token: newToken } = response.data;
        authStorage.setToken(newToken);
      } catch (error) {
        // Refresh failed - log out
        handleLogout();
      }
    }, Math.max(refreshTime, 0));

    return () => clearTimeout(timeoutId);
  }, [isAuthenticated]);
}
```

**Checklist**:
- [ ] Refresh happens before token expiration
- [ ] New token is stored securely
- [ ] Failed refresh logs out user
- [ ] Cleanup prevents memory leaks
- [ ] Refresh is silent (no page reload)

### API Request Interceptor

```typescript
// Attach token to every API request
apiClient.interceptors.request.use((config) => {
  const token = authStorage.getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle 401 responses (token expired or invalid)
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Token is invalid - log out
      handleLogout();
    }
    return Promise.reject(error);
  }
);
```

**Checklist**:
- [ ] Token is attached to all requests
- [ ] 401 responses trigger logout
- [ ] 403 responses don't trigger logout
- [ ] Interceptor doesn't interfere with non-auth requests
- [ ] Errors are properly propagated

## Frontend Implementation Checklist

**Token Management**:
- [ ] Token is stored securely (HTTP-only cookie preferred)
- [ ] Token is not stored in state only
- [ ] Token is not logged or exposed in console
- [ ] Token is sent with every authenticated request
- [ ] Token expiration is handled before it expires
- [ ] Failed refresh redirects to login
- [ ] Logout clears token from all storage

**Route Protection**:
- [ ] Protected routes redirect to login if not authenticated
- [ ] Loading state is shown while checking auth
- [ ] Redirect prevents unauthorized page flash
- [ ] Public routes are not unnecessarily protected
- [ ] Back button doesn't bypass protection

**User Context**:
- [ ] User context is available app-wide
- [ ] Auth is checked on app mount
- [ ] User state is synchronized across tabs (optional but good)
- [ ] Invalid tokens are cleared automatically
- [ ] User is available in protected components

**Logout**:
- [ ] Logout clears all auth data
- [ ] Logout navigates to login page
- [ ] Logout completes even if backend fails
- [ ] User cannot access protected pages after logout
- [ ] Tokens are removed from all storage

**Error Handling**:
- [ ] Login errors don't expose user enumeration
- [ ] Auth errors are user-friendly
- [ ] Failed requests don't expose tokens
- [ ] 401 responses trigger logout
- [ ] 403 responses show permission error

**Security**:
- [ ] No hardcoded credentials
- [ ] No credentials in URLs
- [ ] HTTPS is used for all auth requests
- [ ] Token is validated on backend for every request
- [ ] Session/token lifetime is reasonable

## Related Skills

- **authentication-authorization-backend/SKILL.md** - Backend token validation
- **authentication-authorization/SKILL.md** - General principles
- **controller-pattern/SKILL.md** - Handling authenticated requests
- **data-validation/SKILL.md** - Input validation for login forms

## Common Patterns by Framework

### React + TanStack Query

```typescript
// Fetch user with auth
const { data: user } = useQuery({
  queryKey: ['user'],
  queryFn: async () => {
    const response = await apiClient.get('/auth/me');
    return response.data;
  },
  retry: 1,
  staleTime: 10 * 60 * 1000, // 10 minutes
});
```

### React + Context

```typescript
// See User Context Provider section above
```

### React Router v6

```typescript
// Use ProtectedRoute component for sensitive pages
// See Protected Routes section above
```

## Troubleshooting

**User gets logged out unexpectedly**:
- Check token expiration time
- Verify refresh is happening before expiration
- Check if token is being cleared unexpectedly
- Look for logout being called without user action

**Infinite redirect loop**:
- Check ProtectedRoute doesn't redirect to itself
- Verify loading state prevents premature redirects
- Check auth check doesn't trigger during login

**Token doesn't attach to requests**:
- Verify interceptor is configured
- Check token exists in storage
- Verify endpoint matches interceptor pattern
- Look for request being made before token is loaded

**Other tabs/windows out of sync**:
- Implement cross-tab communication (storage event listener)
- Or use cookie-based auth (shared across tabs automatically)
- Or refresh user context periodically
