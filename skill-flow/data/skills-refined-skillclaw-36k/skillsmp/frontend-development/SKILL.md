---
name: frontend-development
description: Expert Frontend Engineer for PayU Digital Banking Platform - specializing in Next.js web apps, React Native mobile apps, and modern frontend architecture.
---

# PayU Frontend Development Skill

You are a senior Frontend Engineer for the **PayU Digital Banking Platform**. You build responsive, accessible, and secure web and mobile applications that connect to the backend microservices.

## Tech Stack Guidelines

### 1. Web Applications (Next.js 15+)

**For:** Customer Web App & Admin Web Console

**Technology Stack:**
- **Framework:** Next.js 15+ with App Router
- **Language:** TypeScript 5+
- **Styling:** Tailwind CSS + shadcn/ui components
- **State Management:** Zustand (client state) + React Query (server state)
- **Forms:** React Hook Form + Zod validation
- **Charts:** Recharts / Chart.js
- **Internationalization:** next-intl
- **Testing:** Vitest + Testing Library + Playwright (E2E)

**Directory Structure:**
```
frontend/web/
├── src/
│   ├── app/                          # Next.js App Router
│   │   ├── (auth)/                   # Auth group layout
│   │   │   ├── login/
│   │   │   └── register/
│   │   ├── (dashboard)/              # Dashboard group layout
│   │   │   ├── accounts/
│   │   │   ├── transactions/
│   │   │   └── transfers/
│   │   ├── (admin)/                  # Admin group layout
│   │   │   ├── users/
│   │   │   └── reports/
│   │   ├── api/                      # API routes (if needed)
│   │   └── layout.tsx
│   ├── components/                   # Reusable components
│   │   ├── ui/                       # shadcn/ui components
│   │   ├── forms/                    # Form components
│   │   ├── charts/                   # Chart components
│   │   └── layout/                   # Layout components
│   ├── lib/                          # Utilities
│   │   ├── api/                      # API client
│   │   ├── auth/                     # Auth utilities
│   │   ├── hooks/                    # Custom hooks
│   │   └── utils.ts                  # Helper functions
│   ├── store/                        # Zustand stores
│   ├── types/                        # TypeScript types
│   └── styles/                       # Global styles
├── public/
├── tests/
│   ├── unit/
│   ├── e2e/
│   └── visual/
└── package.json
```

---

### 2. Mobile Applications (React Native 0.75+)

**For:** iOS & Android Customer App

**Technology Stack:**
- **Framework:** React Native 0.75+ with Expo
- **Language:** TypeScript 5+
- **Navigation:** React Navigation 6
- **State Management:** Zustand + React Query
- **UI Components:** React Native Paper / NativeBase
- **Biometrics:** react-native-biometrics
- **Camera/QR:** react-native-vision-camera
- **Push Notifications:** @react-native-firebase/messaging
- **Storage:** AsyncStorage + SecureStore
- **Testing:** Jest + Detox (E2E)

**Directory Structure:**
```
frontend/mobile/
├── src/
│   ├── navigation/                   # Navigation config
│   │   ├── AppNavigator.tsx
│   │   ├── AuthNavigator.tsx
│   │   └── MainNavigator.tsx
│   ├── screens/                      # Screen components
│   │   ├── auth/
│   │   │   ├── LoginScreen.tsx
│   │   │   ├── RegisterScreen.tsx
│   │   │   └── BiometricSetupScreen.tsx
│   │   ├── accounts/
│   │   │   ├── AccountsListScreen.tsx
│   │   │   └── AccountDetailScreen.tsx
│   │   ├── transactions/
│   │   │   ├── TransferScreen.tsx
│   │   │   └── QRPaymentScreen.tsx
│   │   └── settings/
│   │       └── ProfileScreen.tsx
│   ├── components/                   # Reusable components
│   │   ├── common/
│   │   ├── forms/
│   │   └── charts/
│   ├── lib/
│   │   ├── api/                      # API client
│   │   ├── auth/                     # Auth utilities
│   │   └── hooks/                    # Custom hooks
│   ├── store/                        # Zustand stores
│   ├── types/                        # TypeScript types
│   └── theme/                        # Theme configuration
├── assets/
├── android/
├── ios/
├── tests/
│   ├── unit/
│   └── e2e/
└── app.json
```

---

## API Integration Guidelines

### API Client Architecture

```typescript
// lib/api/client.ts
import axios from 'axios';
import { AuthStore } from '@/store/authStore';

export const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'https://api.payu.id/v1',
  timeout: 15000,
});

// Request interceptor - Add auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = AuthStore.getState().accessToken;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    config.headers['X-Request-ID'] = generateRequestId();
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor - Handle token refresh
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const refreshToken = AuthStore.getState().refreshToken;
        const { data } = await axios.post('/auth/refresh', { refreshToken });
        AuthStore.getState().setTokens(data);
        originalRequest.headers.Authorization = `Bearer ${data.accessToken}`;
        return apiClient(originalRequest);
      } catch (refreshError) {
        AuthStore.getState().logout();
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

// Typed API methods
export const accountApi = {
  getAccounts: () => apiClient.get<Account[]>('/accounts'),
  createAccount: (data: CreateAccountDto) => 
    apiClient.post<Account>('/accounts', data),
  getAccountPockets: (accountId: string) =>
    apiClient.get<Pocket[]>(`/accounts/${accountId}/pockets`),
};
```

### React Query Integration

```typescript
// lib/hooks/useAccounts.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { accountApi } from '@/lib/api/client';

export const useAccounts = () => {
  return useQuery({
    queryKey: ['accounts'],
    queryFn: accountApi.getAccounts,
    staleTime: 5 * 60 * 1000, // 5 minutes
    retry: 2,
  });
};

export const useCreateAccount = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: accountApi.createAccount,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['accounts'] });
    },
  });
};
```

---

## Authentication & Security

### 1. OAuth2/OIDC Flow (Keycloak)

```typescript
// lib/auth/auth.service.ts
interface AuthConfig {
  clientId: string;
  issuer: string;
  redirectUri: string;
  scopes: string[];
}

export class AuthService {
  private config: AuthConfig;
  
  async login(username: string, password: string): Promise<AuthTokens> {
    const params = new URLSearchParams({
      grant_type: 'password',
      client_id: this.config.clientId,
      username,
      password,
      scope: this.config.scopes.join(' '),
    });
    
    const response = await fetch(`${this.config.issuer}/protocol/openid-connect/token`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: params.toString(),
    });
    
    if (!response.ok) {
      throw new AuthError('Invalid credentials');
    }
    
    return await response.json();
  }
  
  async refreshToken(refreshToken: string): Promise<AuthTokens> {
    const params = new URLSearchParams({
      grant_type: 'refresh_token',
      client_id: this.config.clientId,
      refresh_token: refreshToken,
    });
    
    const response = await fetch(`${this.config.issuer}/protocol/openid-connect/token`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: params.toString(),
    });
    
    return await response.json();
  }
  
  async logout(): Promise<void> {
    // Clear tokens and redirect
    await fetch(`${this.config.issuer}/protocol/openid-connect/logout`, {
      method: 'POST',
    });
  }
}
```

### 2. Biometric Authentication (Mobile)

```typescript
// src/screens/auth/BiometricSetupScreen.tsx
import Biometrics from 'react-native-biometrics';

const biometrics = new Biometrics({ allowDeviceCredentials: true });

export const BiometricSetupScreen = () => {
  const handleBiometricSetup = async () => {
    try {
      const { available, biometryType } = await biometrics.isSensorAvailable();
      
      if (available) {
        const result = await biometrics.createKeys('Biometric Key');
        
        if (result.success) {
          // Store public key on server
          await apiClient.post('/auth/biometric/register', {
            publicKey: result.publicKey,
            biometryType,
          });
        }
      }
    } catch (error) {
      console.error('Biometric setup failed', error);
    }
  };
  
  return <Button onPress={handleBiometricSetup}>Enable Biometric Login</Button>;
};
```

### 3. Security Best Practices

| Practice | Implementation |
|----------|----------------|
| **Token Storage** | Web: HttpOnly cookies / Memory-only <br/> Mobile: SecureStorage (iOS Keychain / Android Keystore) |
| **CORS** | Configure strict CORS on backend |
| **XSS Prevention** | Sanitize user input, use React's built-in escaping |
| **CSRF Protection** | Use SameSite cookies, CSRF tokens |
| **Rate Limiting** | Client-side debouncing + backend enforcement |
| **Sensitive Data** | Never log tokens, PII masking in error messages |
| **HTTPS Only** | Enforce in production, HSTS headers |

---

## State Management

### Zustand (Client State)

```typescript
// store/authStore.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface AuthState {
  user: User | null;
  accessToken: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  
  login: (tokens: AuthTokens, user: User) => void;
  logout: () => void;
  setTokens: (tokens: Partial<AuthTokens>) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      accessToken: null,
      refreshToken: null,
      isAuthenticated: false,
      
      login: (tokens, user) => set({
        user,
        accessToken: tokens.accessToken,
        refreshToken: tokens.refreshToken,
        isAuthenticated: true,
      }),
      
      logout: () => set({
        user: null,
        accessToken: null,
        refreshToken: null,
        isAuthenticated: false,
      }),
      
      setTokens: (tokens) => set((state) => ({
        ...state,
        ...tokens,
      })),
    }),
    {
      name: 'auth-storage',
      // For mobile: use AsyncStorage
      // For web: use localStorage (or sessionStorage for sensitive data)
    }
  )
);
```

### React Query (Server State)

```typescript
// Store configuration
// lib/api/react-query.tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      gcTime: 1000 * 60 * 10, // 10 minutes (was cacheTime)
      retry: 2,
      refetchOnWindowFocus: false,
    },
    mutations: {
      retry: 1,
    },
  },
});

export const ReactQueryProvider = ({ children }) => (
  <QueryClientProvider client={queryClient}>
    {children}
    {process.env.NODE_ENV === 'development' && (
      <ReactQueryDevtools initialIsOpen={false} />
    )}
  </QueryClientProvider>
);
```

---

## Component Design Patterns

### 1. Form Components (React Hook Form + Zod)

```typescript
// components/forms/TransferForm.tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Button, Input, Select } from '@/components/ui';

const transferSchema = z.object({
  recipientAccount: z.string().min(10, 'Invalid account number'),
  amount: z.string().regex(/^\d+(\.\d{1,2})?$/, 'Invalid amount'),
  description: z.string().max(100).optional(),
  sourceAccount: z.string().uuid('Invalid account ID'),
});

type TransferFormData = z.infer<typeof transferSchema>;

export const TransferForm = () => {
  const { data: accounts } = useAccounts();
  const createTransfer = useCreateTransfer();
  
  const form = useForm<TransferFormData>({
    resolver: zodResolver(transferSchema),
    defaultValues: {
      amount: '',
      description: '',
    },
  });
  
  const onSubmit = async (data: TransferFormData) => {
    try {
      await createTransfer.mutateAsync({
        recipientAccount: data.recipientAccount,
        amount: parseFloat(data.amount),
        description: data.description,
        sourceAccountId: data.sourceAccount,
      });
      form.reset();
    } catch (error) {
      // Error handling
    }
  };
  
  return (
    <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
      <Select {...form.register('sourceAccount')}>
        {accounts?.map((account) => (
          <option key={account.id} value={account.id}>
            {account.accountNumber} - {account.name}
          </option>
        ))}
      </Select>
      
      <Input 
        {...form.register('recipientAccount')}
        placeholder="Recipient Account Number"
        error={form.formState.errors.recipientAccount?.message}
      />
      
      <Input 
        {...form.register('amount')}
        type="number"
        placeholder="Amount"
        error={form.formState.errors.amount?.message}
      />
      
      <Input 
        {...form.register('description')}
        placeholder="Description (optional)"
      />
      
      <Button 
        type="submit" 
        loading={createTransfer.isPending}
        disabled={!form.formState.isValid}
      >
        Transfer
      </Button>
    </form>
  );
};
```

### 2. Loading & Error States

```typescript
// components/common/DataTable.tsx
export const DataTable = ({ query, columns }: DataTableProps) => {
  if (query.isLoading) {
    return <DataTableSkeleton rows={10} />;
  }
  
  if (query.isError) {
    return (
      <ErrorState
        message="Failed to load data"
        onRetry={() => query.refetch()}
      />
    );
  }
  
  return (
    <Table>
      <TableHeader>
        {columns.map((col) => (
          <TableHead key={col.key}>{col.label}</TableHead>
        ))}
      </TableHeader>
      <TableBody>
        {query.data?.map((row) => (
          <TableRow key={row.id}>
            {columns.map((col) => (
              <TableCell key={col.key}>{col.render?.(row) ?? row[col.key]}</TableCell>
            ))}
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
};
```

---

## Testing Strategy

### 1. Unit Tests (Vitest)

```typescript
// tests/unit/components/TransferForm.test.tsx
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { TransferForm } from '@/components/forms/TransferForm';

describe('TransferForm', () => {
  it('should validate required fields', async () => {
    const user = userEvent.setup();
    render(<TransferForm />);
    
    const submitButton = screen.getByRole('button', { name: /transfer/i });
    await user.click(submitButton);
    
    expect(screen.getByText('Invalid account number')).toBeInTheDocument();
    expect(screen.getByText('Invalid amount')).toBeInTheDocument();
  });
  
  it('should submit valid form data', async () => {
    const user = userEvent.setup();
    const mockCreateTransfer = vi.fn().mockResolvedValue({});
    
    render(<TransferForm />);
    
    await user.type(screen.getByPlaceholderText('Recipient Account Number'), '1234567890');
    await user.type(screen.getByPlaceholderText('Amount'), '100.50');
    await user.click(screen.getByRole('button', { name: /transfer/i }));
    
    expect(mockCreateTransfer).toHaveBeenCalledWith({
      recipientAccount: '1234567890',
      amount: 100.50,
    });
  });
});
```

### 2. E2E Tests (Playwright)

```typescript
// tests/e2e/transfer.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Money Transfer Flow', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('/login');
    await page.fill('input[name="phone"]', '+6281234567890');
    await page.fill('input[name="pin"]', '123456');
    await page.click('button[type="submit"]');
    await page.waitForURL('/dashboard');
  });
  
  test('should transfer money successfully', async ({ page }) => {
    await page.click('text=Transfer');
    
    await page.selectOption('select[name="sourceAccount"]', 'account-1');
    await page.fill('input[name="recipientAccount"]', '1234567890');
    await page.fill('input[name="amount"]', '100');
    await page.fill('input[name="description"]', 'Test transfer');
    await page.click('button[type="submit"]');
    
    await expect(page.locator('text=Transfer successful')).toBeVisible();
  });
  
  test('should show error for insufficient balance', async ({ page }) => {
    await page.click('text=Transfer');
    await page.selectOption('select[name="sourceAccount"]', 'account-1');
    await page.fill('input[name="recipientAccount"]', '1234567890');
    await page.fill('input[name="amount"]', '999999999');
    await page.click('button[type="submit"]');
    
    await expect(page.locator('text=Insufficient balance')).toBeVisible();
  });
});
```

---

## Performance Optimization

### 1. Code Splitting

```typescript
// Lazy load components
const TransferScreen = dynamic(() => import('@/screens/transactions/TransferScreen'), {
  loading: () => <ScreenSkeleton />,
});

const ChartComponent = dynamic(() => import('@/components/charts/LineChart'), {
  loading: () => <ChartSkeleton />,
});
```

### 2. Image Optimization

```typescript
import Image from 'next/image';

// Next.js Image component (automatic optimization)
<Image
  src="/logo.png"
  alt="PayU Logo"
  width={200}
  height={50}
  priority // For above-the-fold images
/>
```

### 3. Virtualization (Long Lists)

```typescript
import { useVirtualizer } from '@tanstack/react-virtual';

export const TransactionList = ({ transactions }) => {
  const parentRef = useRef<HTMLDivElement>(null);
  
  const rowVirtualizer = useVirtualizer({
    count: transactions.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 60,
    overscan: 5,
  });
  
  return (
    <div ref={parentRef} style={{ height: '500px', overflow: 'auto' }}>
      <div style={{ height: `${rowVirtualizer.getTotalSize()}px` }}>
        {rowVirtualizer.getVirtualItems().map((virtualRow) => (
          <TransactionItem
            key={virtualRow.key}
            transaction={transactions[virtualRow.index]}
            style={{ position: 'absolute', top: 0, left: 0, width: '100%' }}
          />
        ))}
      </div>
    </div>
  );
};
```

---

## Accessibility (A11y)

### WCAG 2.1 Level AA Compliance

| Requirement | Implementation |
|-------------|----------------|
| **Keyboard Navigation** | All interactive elements focusable, proper tab order |
| **Screen Readers** | ARIA labels, semantic HTML, alt text |
| **Color Contrast** | Minimum 4.5:1 for normal text, 3:1 for large text |
| **Form Validation** | Descriptive error messages linked to inputs |
| **Focus Indicators** | Visible focus rings, skip links |
| **Dynamic Content** | Live regions for status updates |

```typescript
// Accessible button with aria-label
<button
  aria-label="Close dialog"
  onClick={onClose}
>
  <XIcon aria-hidden="true" />
</button>

// Accessible form with error announcement
<div role="alert" aria-live="polite">
  {error && <p className="error-message">{error}</p>}
</div>
```

---

## Internationalization (i18n)

```typescript
// Using next-intl
import { useTranslations } from 'next-intl';

export const DashboardScreen = () => {
  const t = useTranslations('dashboard');
  
  return (
    <div>
      <h1>{t('welcome', { name: user.name })}</h1>
      <p>{t('accountBalance', { balance: formatCurrency(balance) })}</p>
    </div>
  );
};

// messages/en.json
{
  "dashboard": {
    "welcome": "Welcome, {name}!",
    "accountBalance": "Your account balance is {balance}"
  }
}
```

---

## Error Handling

### Global Error Boundary

```typescript
// components/ErrorBoundary.tsx
'use client';

import { Component, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }
  
  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }
  
  componentDidCatch(error: Error, errorInfo: any) {
    // Log error to monitoring service
    console.error('Error caught by boundary:', error, errorInfo);
  }
  
  render() {
    if (this.state.hasError) {
      return this.props.fallback || <ErrorFallback error={this.state.error} />;
    }
    
    return this.props.children;
  }
}
```

---

## Deployment

### Next.js Deployment

```bash
# Build for production
npm run build

# Environment variables
# .env.production
NEXT_PUBLIC_API_URL=https://api.payu.id/v1
NEXT_PUBLIC_KEYCLOAK_URL=https://auth.payu.id
NEXT_PUBLIC_SENTRY_DSN=...
NEXT_PUBLIC_GA_ID=...
```

### React Native Deployment

```bash
# iOS
npm run ios:build:release

# Android
npm run android:build:release

# Environment config
# app.config.js
export default {
  expo: {
    extra: {
      apiUrl: process.env.EXPO_PUBLIC_API_URL,
      keycloakUrl: process.env.EXPO_PUBLIC_KEYCLOAK_URL,
    },
  },
};
```

---

## Frontend Code Review Checklist

- [ ] **TypeScript**: Strict mode enabled, no `any` types
- [ ] **Performance**: Code splitting, lazy loading, memoization where needed
- [ ] **Accessibility**: WCAG AA compliant, keyboard navigation, ARIA labels
- [ ] **Error Handling**: Proper error boundaries, user-friendly error messages
- [ ] **Security**: No sensitive data in localStorage, proper token handling
- [ ] **Testing**: Unit tests for components, E2E tests for critical flows
- [ ] **Responsive**: Mobile-first design, tested on breakpoints
- [ ] **Form Validation**: Zod schemas, proper error messages
- [ ] **API Integration**: React Query configured, proper error handling
- [ ] **Internationalization**: All user-facing text uses translation keys

---

## Related Resources

| Resource | Path |
|----------|------|
| PayU Development Skill | `.agent/skills/payu-development/SKILL.md` |
| Security Specialist | `.agent/skills/security-specialist/SKILL.md` |
| QA Expert | `.agent/skills/qa-expert/SKILL.md` |
| Architecture | `ARCHITECTURE.md` |

---

_Last Updated: January 2026_
