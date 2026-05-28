---
name: enterprise-react-frontend-builder
description: Expert skill for building secure, scalable, enterprise-grade React frontend applications using Vite, TanStack Query & Router, TakeOff UI components, and Tailwind CSS. Use this skill when creating new React projects, building API-driven dynamic UIs, implementing centralized auth/API management, setting up OAuth/JWT authentication, generating forms/tables from backend schemas, or refactoring existing React apps to follow enterprise patterns. This skill enforces clean architecture with strict separation of concerns (services, hooks, components, pages), Tailwind-only styling (no CSS files), dynamic UI generation from API contracts, and TakeOff UI component approval workflows.
---

# React + TanStack + TakeOff UI Enterprise Builder

## Overview

This skill guides you through building production-ready, secure React frontends with:

- **Vite** - Modern build tool for fast development
- **TanStack Query** - Powerful data synchronization and caching
- **TanStack Router** - Type-safe file-based routing
- **TakeOff UI** - Enterprise component library with Tailwind integration
- **Tailwind CSS** - Utility-first styling (NO custom CSS files)
- **TypeScript** - Type safety throughout
- **Centralized Auth** - OAuth 2.0 or JWT-based authentication
- **Dynamic UI Generation** - Forms and tables from backend schemas
- **Clean Architecture** - Strict separation of concerns

### When to Use This Skill

- Starting a new React frontend project
- Building API-driven applications with dynamic UIs
- Implementing secure authentication (OAuth/JWT)
- Creating enterprise applications with TakeOff UI
- Migrating React apps to scalable architecture
- Setting up backend-frontend schema contracts

## Core Principles

1. **Tailwind-Only Styling** - Never create CSS files or custom classes
2. **API-First Design** - UI components driven by backend schemas
3. **Separation of Concerns** - Services ≠ Hooks ≠ Components ≠ Pages
4. **Component Approval** - Always request approval before using new TakeOff UI components
5. **Type Safety** - TypeScript everywhere, no `any` types
6. **Security First** - Centralized auth, token management, API interceptors

## Initial Setup Workflow

### Step 1: TakeOff UI MCP Integration (Recommended)

Before starting development, set up the TakeOff UI MCP server for AI-assisted component discovery and code generation.

**Option A: Remote (Recommended - No Installation)**

```bash
# VS Code Copilot - Add to settings.json
{
  "mcp": {
    "servers": {
      "takeoff-ui-mcp": {
        "command": "npx",
        "args": ["-y", "mcp-remote", "https://takeoffui.turkishtechlab.com/mcp"]
      }
    }
  }
}
```

**Option B: Local Installation**

```bash
git clone https://github.com/turkishtechnology/takeoff-ui-mcp.git
cd takeoff-ui-mcp
npm install
npm run build
npm start  # STDIO mode
# or
npm run start:stream  # HTTP mode (http://127.0.0.1:3845/mcp)
```

Then configure your editor:

```json
// VS Code Copilot - STDIO
{
  "mcp": {
    "servers": {
      "takeoff-ui-mcp": {
        "type": "stdio",
        "command": "node",
        "args": ["/absolute/path/to/takeoff-ui-mcp/dist/index.js"]
      }
    }
  }
}

// VS Code Copilot - HTTP
{
  "mcp": {
    "servers": {
      "takeoff-ui-mcp": {
        "type": "streamable-http",
        "url": "http://127.0.0.1:3845/mcp"
      }
    }
  }
}
```

**MCP Capabilities:**
- `get_components_list` - Browse all TakeOff UI components
- `get_component_info` - Detailed docs and examples
- `get_tailwind_integration` - Tailwind setup guidance
- `get_framework_integration` - React/Vue/Angular integration
- `refactor_takeoff_ui_code` - Code refactoring prompts
- `figma_to_code` - Convert Figma designs to TakeOff UI code

**Usage Tip:** In your prompts, add "use takeoff-ui-mcp" to leverage MCP tools.

### Step 2: Project Scaffolding

Generate the clean file structure (see [references/file-structure.md](references/file-structure.md) for details):

```
project-root/
├── src/
│   ├── api/              # API services and clients
│   │   ├── client.ts     # Axios/Fetch instance with interceptors
│   │   ├── endpoints/    # API endpoint definitions
│   │   └── types/        # API request/response types
│   ├── auth/             # Authentication logic
│   │   ├── AuthProvider.tsx
│   │   ├── useAuth.ts
│   │   ├── oauth.ts      # OAuth 2.0 flows
│   │   └── jwt.ts        # JWT handling
│   ├── hooks/            # Custom React hooks (non-API)
│   │   ├── useLocalStorage.ts
│   │   └── useDebounce.ts
│   ├── components/       # Reusable UI components
│   │   ├── DataTable/    # Generic data table
│   │   ├── DynamicForm/  # Schema-driven form
│   │   └── Layout/       # Layout components
│   ├── pages/            # Page components (routes)
│   │   ├── Dashboard/
│   │   ├── Users/
│   │   └── Settings/
│   ├── routes/           # TanStack Router configuration
│   │   └── index.tsx
│   ├── lib/              # Utilities and helpers
│   │   ├── cn.ts         # Tailwind class merger
│   │   └── validators.ts
│   ├── types/            # Shared TypeScript types
│   └── main.tsx          # Entry point
├── vite.config.ts
├── tailwind.config.ts
└── tsconfig.json
```

**Create this structure:**

```bash
mkdir -p src/{api/{endpoints,types},auth,hooks,components/{DataTable,DynamicForm,Layout},pages,routes,lib,types}
```

### Step 3: Install Dependencies

```bash
# Core packages
npm install @takeoff-ui/core @takeoff-ui/react

# TanStack ecosystem
npm install @tanstack/react-query @tanstack/react-router @tanstack/router-devtools @tanstack/react-query-devtools

# Utilities
npm install axios zod clsx tailwind-merge

# Dev dependencies
npm install -D @types/react @types/react-dom vite @vitejs/plugin-react typescript tailwindcss postcss autoprefixer
```

### Step 4: Configure Vite

See [assets/vite.config.ts](assets/vite.config.ts) for template.

### Step 5: Configure Tailwind with TakeOff UI

See [assets/tailwind.config.ts](assets/tailwind.config.ts) for template with TakeOff UI plugin integration.

### Step 6: Setup TakeOff UI

```tsx
// src/main.tsx
import '@takeoff-ui/core/dist/core/core.css'
import { createRoot } from 'react-dom/client'
import App from './App'

createRoot(document.getElementById('root')!).render(<App />)
```

### Step 7: Configure TanStack Query

See [references/tanstack-patterns.md](references/tanstack-patterns.md) for setup and usage patterns.

### Step 8: Configure TanStack Router

See [references/tanstack-patterns.md](references/tanstack-patterns.md) for router setup.

### Step 9: Setup Authentication

Choose auth strategy and implement (see [references/auth-patterns.md](references/auth-patterns.md)):

- **OAuth 2.0** - For enterprise SSO (Azure AD, Auth0, Okta)
- **JWT** - For traditional token-based auth

### Step 10: Setup Centralized API Client

See [references/api-architecture.md](references/api-architecture.md) for implementation.

## Development Workflow

### Creating a New Page

1. **Define the API endpoint** in `src/api/endpoints/`
2. **Create TanStack Query hooks** for data fetching
3. **Build the page component** in `src/pages/`
4. **Add the route** in TanStack Router
5. **Use TakeOff UI components** from approved list

**Example:**

```tsx
// 1. API endpoint
// src/api/endpoints/users.ts
export const usersApi = {
  getAll: () => apiClient.get('/users'),
  getById: (id: string) => apiClient.get(`/users/${id}`),
  create: (data: CreateUserDto) => apiClient.post('/users', data),
}

// 2. Query hooks
// src/api/endpoints/users.ts
export const useUsers = () => {
  return useQuery({
    queryKey: ['users'],
    queryFn: usersApi.getAll,
  })
}

// 3. Page component
// src/pages/Users/UsersPage.tsx
import { DataTable } from '@/components/DataTable'
import { useUsers } from '@/api/endpoints/users'

export default function UsersPage() {
  const { data, isLoading } = useUsers()
  
  return (
    <DataTable
      data={data}
      endpoint="/users"
      columns={['name', 'email', 'role']}
      enableFilters
      enablePagination
    />
  )
}
```

### Dynamic UI Generation

See [references/dynamic-ui-generation.md](references/dynamic-ui-generation.md) for:

- **Schema-driven forms** - Backend defines fields, frontend renders
- **Dynamic tables** - API metadata controls columns, filters, badges
- **Auto-validation** - Backend schemas → frontend validators

**Quick Example:**

```tsx
// Backend sends schema with API response
const schema = {
  fields: [
    { name: 'firstName', type: 'text', required: true },
    { name: 'email', type: 'email', required: true },
    { name: 'role', type: 'select', options: ['admin', 'user'] }
  ]
}

// Frontend automatically renders
<DynamicForm schema={schema} onSubmit={handleSubmit} />
```

### Component Usage Guidelines

**Before Using a New TakeOff UI Component:**

1. Check the [TakeOff UI docs](https://www.takeoffui.com/docs/Components/Overview) or use MCP:
   ```
   Use takeoff-ui-mcp: Show me DataTable component with examples
   ```

2. **Request approval** with justification:
   - "I need `TkDataGrid` because it has built-in filtering that reduces 50 lines of custom code"
   - "Should I use `TkModal` or `TkDialog` for this use case?"

3. **Wait for confirmation** before implementing

4. **Document usage** in component file:
   ```tsx
   /**
    * Uses TkButton from TakeOff UI
    * Approved: 2026-01-21
    * Reason: Standard button with built-in loading states
    */
   ```

### Styling with Tailwind

**CRITICAL: NO CSS FILES**

```tsx
// ✅ CORRECT - Tailwind utilities
<div className="flex items-center justify-between p-4 bg-gray-100 rounded-lg">
  <TkButton label="Submit" className="px-6 py-2 bg-blue-600 hover:bg-blue-700" />
</div>

// ❌ WRONG - Custom CSS
// Never create styles.css or use <style> tags

// ✅ CORRECT - Dynamic classes
const buttonClass = cn(
  'px-4 py-2 rounded-md',
  isPrimary && 'bg-blue-600 text-white',
  isDisabled && 'opacity-50 cursor-not-allowed'
)
```

**Use the `cn()` utility** (see [assets/lib/cn.ts](assets/lib/cn.ts)) to merge Tailwind classes:

```tsx
import { cn } from '@/lib/cn'

const className = cn(
  'base-classes',
  condition && 'conditional-classes',
  props.className  // Allow parent overrides
)
```

## Advanced Patterns

### API Integration with TanStack Query

See [references/tanstack-patterns.md](references/tanstack-patterns.md) for:
- Query configuration and caching strategies
- Mutation patterns with optimistic updates
- Infinite queries for pagination
- Dependent queries
- Query invalidation strategies

### Authentication Flows

See [references/auth-patterns.md](references/auth-patterns.md) for:
- OAuth 2.0 Authorization Code Flow
- JWT refresh token rotation
- Protected routes with TanStack Router
- Token storage and security
- API interceptors for auth headers

### Backend-Frontend Contracts

See [references/dynamic-ui-generation.md](references/dynamic-ui-generation.md) for:
- OpenAPI/Swagger schema integration
- JSON Schema validation
- Automatic form field generation
- Type generation from backend schemas
- Runtime validation with Zod

### Error Handling

```tsx
// Centralized error handling in API client
apiClient.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      // Redirect to login
      router.navigate({ to: '/login' })
    }
    // Show toast notification
    toast.error(error.response?.data?.message || 'An error occurred')
    return Promise.reject(error)
  }
)

// Component-level error handling
const { data, error, isError } = useUsers()

if (isError) {
  return <ErrorBoundary error={error} />
}
```

### Performance Optimization

1. **Code splitting** with TanStack Router lazy loading
2. **Query prefetching** on route navigation
3. **Optimistic updates** for instant UI feedback
4. **Virtual scrolling** for large lists (TakeOff UI DataGrid)
5. **Debounced search** inputs

## Component Reference Workflow

When you need to match a design reference:

1. **Analyze the design** - Identify UI patterns (table, form, modal, etc.)
2. **Search TakeOff UI** - Use MCP or docs to find matching components
3. **Propose mapping** - "Design shows a data grid → I recommend `TkDataGrid` with filters"
4. **Request approval** - Get confirmation before implementing
5. **Implement with Tailwind** - Use only TakeOff UI + Tailwind utilities
6. **If no match exists** - Propose creating a composite component OR request new TakeOff component

**Example Workflow:**

```
User: "Build this design: [image of user management table]"

You: 
1. Analyzing design... I see:
   - Data table with sortable columns
   - Filter dropdowns for role/status
   - Action buttons (edit, delete)
   - Pagination

2. TakeOff UI component search...
   "use takeoff-ui-mcp: Show me data table components"
   
3. Recommendation:
   - TkDataGrid for the main table (has built-in sorting, filtering)
   - TkButton for actions
   - TkBadge for status indicators
   
4. Approval request:
   "I recommend using TkDataGrid, TkButton, and TkBadge. 
   This approach eliminates ~200 lines of custom table logic. Approved?"

5. After approval → Implement with Tailwind styling
```

## Security Best Practices

1. **Never store tokens in localStorage** - Use httpOnly cookies or secure storage
2. **Validate all API responses** - Use Zod schemas
3. **Sanitize user inputs** - Especially in dynamic forms
4. **Implement CSRF protection** - For state-changing operations
5. **Use HTTPS only** - Enforce in production
6. **Implement rate limiting** - On auth endpoints
7. **Audit dependencies** - Regular `npm audit`

## Quality Checklist

Before considering a page/feature complete:

- [ ] No custom CSS files created
- [ ] All TakeOff UI components approved
- [ ] TypeScript strict mode passing
- [ ] API calls use centralized client
- [ ] Auth tokens managed securely
- [ ] Error states handled gracefully
- [ ] Loading states implemented
- [ ] Responsive design (Tailwind breakpoints)
- [ ] Accessibility tested (keyboard navigation, screen readers)
- [ ] Form validation working (client + server)
- [ ] Query invalidation on mutations
- [ ] Route guards for protected pages
- [ ] No hardcoded API URLs (use env variables)
- [ ] Dynamic UI uses backend schemas where applicable

## Troubleshooting

### TakeOff UI Not Rendering

```tsx
// Ensure core CSS is imported in main.tsx
import '@takeoff-ui/core/dist/core/core.css'

// For Next.js, add to app/layout.tsx or page.tsx
import '@takeoff-ui/core/dist/core/core.css'
```

### TanStack Router Type Errors

```bash
# Generate route types
npx tsx ./src/routes/index.tsx
```

### Auth Token Refresh Issues

See [references/auth-patterns.md](references/auth-patterns.md) for token refresh interceptor implementation.

### TakeOff UI MCP Not Connecting

```bash
# Check MCP server status
curl http://127.0.0.1:3845/health
curl http://127.0.0.1:3845/info

# Debug logs
# In .env: LOG_LEVEL=0

# Verify absolute paths in config
# WRONG: "args": ["./dist/index.js"]
# RIGHT: "args": ["/full/path/to/takeoff-ui-mcp/dist/index.js"]
```

## Quick Reference

### Common Commands

```bash
# Development
npm run dev

# Build
npm run build

# Type check
npm run type-check

# Lint
npm run lint

# TakeOff UI MCP (local)
npm start  # STDIO mode
npm run start:stream  # HTTP mode
```

### File Templates

- [assets/vite.config.ts](assets/vite.config.ts) - Vite configuration
- [assets/tailwind.config.ts](assets/tailwind.config.ts) - Tailwind + TakeOff plugin
- [assets/api-client.ts](assets/api-client.ts) - Centralized API client
- [assets/AuthProvider.tsx](assets/AuthProvider.tsx) - Auth context provider
- [assets/DataTable.tsx](assets/DataTable.tsx) - Generic data table component
- [assets/DynamicForm.tsx](assets/DynamicForm.tsx) - Schema-driven form

### Reference Documentation

- [references/file-structure.md](references/file-structure.md) - Complete project structure guide
- [references/tanstack-patterns.md](references/tanstack-patterns.md) - Query & Router patterns
- [references/api-architecture.md](references/api-architecture.md) - API client design
- [references/dynamic-ui-generation.md](references/dynamic-ui-generation.md) - Schema-based UI patterns
- [references/auth-patterns.md](references/auth-patterns.md) - OAuth & JWT implementations
- [references/takeoff-components.md](references/takeoff-components.md) - Common component usage

## External Resources

- [TakeOff UI Documentation](https://www.takeoffui.com/docs/Installation)
- [TakeOff UI Components](https://www.takeoffui.com/docs/Components/Overview)
- [TakeOff UI Tailwind Plugin](https://www.takeoffui.com/docs/Tailwind)
- [TakeOff UI MCP Server](https://www.takeoffui.com/docs/MCP)
- [TanStack Query Docs](https://tanstack.com/query/latest)
- [TanStack Router Docs](https://tanstack.com/router/latest)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)

## Summary

This skill enforces a clean, scalable architecture for React frontends with:

1. **TakeOff UI components** - Enterprise-grade, Tailwind-integrated
2. **TanStack Query & Router** - Modern data fetching and routing
3. **Centralized API & Auth** - Secure, maintainable integrations
4. **Dynamic UI generation** - Backend schemas drive frontend
5. **Tailwind-only styling** - No custom CSS complexity
6. **Strict separation** - Services, hooks, components, pages isolated
7. **Type safety** - TypeScript throughout
8. **MCP assistance** - AI-powered component discovery

Follow the workflows, request component approval, and maintain clean architecture. The result: production-ready, secure, maintainable React applications.