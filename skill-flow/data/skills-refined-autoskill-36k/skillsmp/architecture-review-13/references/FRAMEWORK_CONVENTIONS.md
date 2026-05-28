# Framework Conventions Reference

This reference documents expected conventions for common JavaScript/TypeScript frameworks. Use this to identify deviations from standard patterns.

---

## Next.js

### App Router (Next.js 13+)

**Directory Structure:**
```
app/
  layout.tsx          # Root layout
  page.tsx            # Home page
  loading.tsx         # Loading UI
  error.tsx           # Error boundary
  not-found.tsx       # 404 page
  (group)/            # Route groups (no URL impact)
  @modal/             # Parallel routes
  [...slug]/          # Catch-all segments
  [[...slug]]/        # Optional catch-all
  api/
    route.ts          # API route handler
```

**Key Conventions:**
- `page.tsx` - Defines a route's UI
- `layout.tsx` - Shared UI for segments
- `route.ts` - API endpoints (GET, POST, etc. as named exports)
- Server Components by default
- `'use client'` directive for Client Components
- `generateMetadata()` for SEO
- `generateStaticParams()` for static generation

**API Route Pattern (App Router):**
```typescript
export async function GET(request: Request) {}
export async function POST(request: Request) {}
```

### Pages Router (Legacy)

**Directory Structure:**
```
pages/
  _app.tsx            # App wrapper
  _document.tsx       # HTML document
  index.tsx           # Home page
  api/
    users.ts          # API route
  posts/
    [id].tsx          # Dynamic route
    [...slug].tsx     # Catch-all route
```

**Key Conventions:**
- File name = route path
- `getServerSideProps` - Server-side rendering
- `getStaticProps` + `getStaticPaths` - Static generation
- API routes export default handler function

**API Route Pattern (Pages Router):**
```typescript
export default function handler(req, res) {
  if (req.method === 'GET') {}
}
```

---

## React Native / Expo

### Standard React Native

**Directory Structure:**
```
src/
  components/         # Reusable UI components
  screens/            # Screen components
  navigation/         # Navigation configuration
  hooks/              # Custom hooks
  services/           # API clients, storage
  utils/              # Utility functions
  types/              # TypeScript types
  assets/             # Images, fonts
```

**Key Files:**
- `App.tsx` - Root component
- `app.json` - App configuration
- `metro.config.js` - Bundler config
- `babel.config.js` - Babel configuration

### Expo

**Directory Structure (Expo Router):**
```
app/
  _layout.tsx         # Root layout
  index.tsx           # Home screen
  (tabs)/             # Tab navigation group
    _layout.tsx       # Tab layout
    home.tsx
    settings.tsx
  [id].tsx            # Dynamic route
```

**Key Conventions:**
- Expo Router uses file-based routing (like Next.js)
- `_layout.tsx` defines navigation structure
- `expo-router` for navigation
- `app.json` / `app.config.js` for configuration

---

## Express.js

**Directory Structure:**
```
src/
  routes/             # Route definitions
  controllers/        # Request handlers
  middleware/         # Custom middleware
  models/             # Data models
  services/           # Business logic
  utils/              # Utilities
  config/             # Configuration
  types/              # TypeScript types
```

**Key Conventions:**
- `app.js` / `server.js` - Entry point
- Router pattern: `express.Router()`
- Middleware chain: `app.use()`
- Error handling middleware at the end

**Standard Patterns:**
```javascript
// Route definition
router.get('/users', controller.getUsers);

// Controller
const getUsers = async (req, res, next) => {
  try {
    const users = await userService.findAll();
    res.json(users);
  } catch (error) {
    next(error);
  }
};
```

---

## NestJS

**Directory Structure:**
```
src/
  app.module.ts       # Root module
  main.ts             # Entry point
  users/
    users.module.ts   # Feature module
    users.controller.ts
    users.service.ts
    dto/
      create-user.dto.ts
    entities/
      user.entity.ts
  common/
    decorators/
    filters/
    guards/
    interceptors/
    pipes/
```

**Key Conventions:**
- Decorator-based (`@Controller`, `@Injectable`, `@Module`)
- Dependency injection
- DTOs for validation
- Entities for database models
- Guards for authentication
- Interceptors for transformation

**Standard Patterns:**
```typescript
@Controller('users')
export class UsersController {
  @Get()
  findAll() {}

  @Post()
  create(@Body() dto: CreateUserDto) {}
}
```

---

## Fastify

**Directory Structure:**
```
src/
  routes/             # Route definitions
  plugins/            # Fastify plugins
  schemas/            # JSON schemas
  services/           # Business logic
  utils/              # Utilities
```

**Key Conventions:**
- Plugin-based architecture
- JSON Schema validation
- Hooks for lifecycle events
- Decorators for extending request/reply

**Standard Patterns:**
```javascript
fastify.register(async function (fastify) {
  fastify.get('/users', async (request, reply) => {
    return { users: [] };
  });
});
```

---

## Hono

**Directory Structure:**
```
src/
  routes/             # Route modules
  middleware/         # Custom middleware
  utils/              # Utilities
  index.ts            # Entry point
```

**Key Conventions:**
- Minimal, Web Standard API
- Works on edge runtimes
- Middleware via `app.use()`
- Route grouping

**Standard Patterns:**
```typescript
const app = new Hono();

app.get('/users', (c) => c.json({ users: [] }));
app.post('/users', async (c) => {
  const body = await c.req.json();
  return c.json(body, 201);
});
```

---

## Monorepo Patterns

### Turborepo

**Directory Structure:**
```
apps/
  web/                # Next.js app
  mobile/             # React Native app
  api/                # Backend
packages/
  ui/                 # Shared UI components
  config/             # Shared configuration
  types/              # Shared TypeScript types
turbo.json            # Pipeline configuration
```

### pnpm Workspaces

**Directory Structure:**
```
packages/
  app/
  shared/
pnpm-workspace.yaml
```

### Nx

**Directory Structure:**
```
apps/
  web/
  api/
libs/
  shared/
  ui/
nx.json
```

---

## Common Configuration Files

| File | Purpose |
|------|---------|
| `tsconfig.json` | TypeScript configuration |
| `next.config.js` | Next.js configuration |
| `vite.config.ts` | Vite configuration |
| `.env` / `.env.local` | Environment variables |
| `tailwind.config.js` | Tailwind CSS |
| `jest.config.js` | Jest testing |
| `vitest.config.ts` | Vitest testing |
| `.eslintrc.js` | ESLint rules |
| `.prettierrc` | Prettier formatting |
| `docker-compose.yml` | Docker services |

---

## Deviation Detection

When reviewing architecture, flag these deviations:

1. **Non-standard directories** - Using `screens/` in Next.js (React Native convention)
2. **Mixed patterns** - Some pages using App Router, some using Pages Router
3. **Wrong entry points** - API logic in page components
4. **Missing conventions** - No `loading.tsx` in App Router routes
5. **Outdated patterns** - Using `getInitialProps` instead of modern data fetching
6. **Configuration drift** - Multiple conflicting config files
