# React + TanStack + TakeOff UI Enterprise Builder Skill

## Overview

This comprehensive skill guides AI assistants in building production-ready, secure React frontend applications using:

- **Vite** - Modern build tooling
- **TanStack Query & Router** - Data fetching and routing
- **TakeOff UI** - Enterprise component library
- **Tailwind CSS** - Utility-first styling
- **TypeScript** - Type safety
- **OAuth 2.0 / JWT** - Authentication
- **Dynamic UI Generation** - Backend-driven forms and tables

## Skill Structure

```
react-tanstack-enterprise-builder/
├── SKILL.md                          # Main skill file (entry point)
├── README.md                         # This file
├── references/                       # Reference documentation
│   ├── file-structure.md             # Project structure guide
│   ├── tanstack-patterns.md          # TanStack Query & Router patterns
│   ├── api-architecture.md           # Centralized API client
│   ├── dynamic-ui-generation.md      # Schema-driven UI patterns
│   ├── auth-patterns.md              # OAuth & JWT implementation
│   └── takeoff-components.md         # TakeOff UI component reference
└── assets/                           # Template files
    ├── vite.config.ts                # Vite configuration
    ├── tailwind.config.ts            # Tailwind configuration
    ├── api-client.ts                 # API client template
    ├── AuthProvider.tsx              # Auth context provider
    ├── DataTable.tsx                 # Generic data table component
    ├── DynamicForm.tsx               # Schema-driven form component
    ├── cn.ts                         # Tailwind class merger utility
    └── .env.example                  # Environment variables template
```

## Key Features

### 1. Clean Architecture
- Strict separation of concerns (API, hooks, components, pages)
- Scalable file structure
- Type-safe throughout

### 2. TakeOff UI Integration
- MCP server for AI-assisted component discovery
- Component approval workflow
- Tailwind-only styling (no CSS files)

### 3. TanStack Ecosystem
- Powerful data fetching with Query
- Type-safe routing with Router
- Automatic caching and refetching

### 4. Centralized API Management
- Single API client with interceptors
- Automatic token refresh
- Consistent error handling

### 5. Authentication
- OAuth 2.0 with PKCE support
- JWT with refresh tokens
- Route guards and role-based access

### 6. Dynamic UI Generation
- Backend-driven forms and tables
- Schema-based validation with Zod
- Reduces frontend boilerplate significantly

## Usage

When creating a new React project:

1. **Trigger the skill** - Mention React, TanStack, TakeOff UI, or enterprise frontend
2. **Follow workflows** - Skill guides through project setup step-by-step
3. **Request component approval** - Before using new TakeOff UI components
4. **Use reference docs** - For detailed patterns and best practices
5. **Copy asset templates** - Use boilerplate files for quick setup

## Workflows Included

### Initial Setup
1. TakeOff UI MCP integration (optional but recommended)
2. Project scaffolding with clean file structure
3. Dependency installation
4. Vite configuration
5. Tailwind configuration with TakeOff UI plugin
6. TanStack Query setup
7. TanStack Router setup
8. Authentication setup (OAuth or JWT)
9. Centralized API client setup

### Development Workflow
1. Define API endpoints
2. Create TanStack Query hooks
3. Build page components
4. Add routes
5. Use TakeOff UI components (with approval)
6. Style with Tailwind only

### Component Approval Workflow
1. Search TakeOff UI docs or MCP
2. Propose component with justification
3. Request user approval
4. Document approval in code comments
5. Implement with Tailwind styling

## Best Practices Enforced

- ✅ Tailwind-only styling (no CSS files)
- ✅ TakeOff UI component approval required
- ✅ Type safety with TypeScript
- ✅ Separation of concerns (API, hooks, components, pages)
- ✅ Centralized API client with auth
- ✅ Dynamic UI generation from backend schemas
- ✅ Route guards for protected routes
- ✅ Error boundaries and loading states
- ✅ Responsive design (mobile-first)
- ✅ Accessibility (WCAG 2.1 AA)

## Reference Documentation

### file-structure.md
Complete project structure guide with:
- Directory organization
- File naming conventions
- Import aliases
- Separation of concerns enforcement
- Anti-patterns to avoid

### tanstack-patterns.md
TanStack Query and Router patterns:
- Query configuration and caching
- Mutation patterns with optimistic updates
- Infinite queries for pagination
- Route guards and protected routes
- Prefetching and lazy loading

### api-architecture.md
Centralized API client architecture:
- Request/response interceptors
- Token management and refresh
- Error handling and retries
- File uploads
- WebSocket integration

### dynamic-ui-generation.md
Schema-driven UI patterns:
- Form schema format
- Dynamic form component
- Dynamic data table component
- Runtime validation with Zod
- Backend-frontend contracts

### auth-patterns.md
Authentication implementations:
- OAuth 2.0 with PKCE
- JWT with refresh tokens
- Route guards
- Token storage strategies
- Security best practices

### takeoff-components.md
TakeOff UI component reference:
- Common components (buttons, inputs, tables, etc.)
- Usage examples
- Tailwind integration
- Component approval workflow
- Responsive design patterns

## Asset Templates

### vite.config.ts
- Path aliases
- Proxy configuration
- Build optimization
- Code splitting

### tailwind.config.ts
- TakeOff UI integration
- Custom theme
- Plugins
- Dark mode support

### api-client.ts
- Axios instance with interceptors
- Token injection
- Token refresh logic
- Error handling

### AuthProvider.tsx
- Auth context provider
- Login/logout functions
- User state management
- Token refresh

### DataTable.tsx
- Generic data table component
- Sorting, filtering, pagination
- Search functionality
- Customizable columns

### DynamicForm.tsx
- Schema-driven form component
- Automatic field rendering
- Zod validation
- Error handling

### cn.ts
- Tailwind class merger utility
- Uses clsx and tailwind-merge

### .env.example
- Environment variables template
- API configuration
- OAuth/JWT settings
- Feature flags

## Installation

This skill is automatically available when loaded into VS Code Copilot or Claude Desktop.

## External Resources

- [TakeOff UI Documentation](https://www.takeoffui.com/docs/Installation)
- [TakeOff UI Components](https://www.takeoffui.com/docs/Components/Overview)
- [TakeOff UI MCP Server](https://www.takeoffui.com/docs/MCP)
- [TanStack Query Docs](https://tanstack.com/query/latest)
- [TanStack Router Docs](https://tanstack.com/router/latest)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)

## License

This skill is provided as-is for use in building React applications.

## Support

For questions or issues, refer to the official documentation of the respective libraries:
- TakeOff UI: https://www.takeoffui.com
- TanStack Query: https://tanstack.com/query
- TanStack Router: https://tanstack.com/router
- Tailwind CSS: https://tailwindcss.com

---

**Created:** 2026-01-21  
**Version:** 1.0.0  
**Skill Type:** Enterprise React Frontend Builder