# VeloxTS Troubleshooting Guide

## MCP Server vs CLI

VeloxTS provides two ways to run generators and commands:

### CLI (Terminal)

Use directly in your terminal:

```bash
pnpm velox make resource Post --crud
pnpm velox migrate status
pnpm velox db seed
```

### MCP Server (AI Assistants)

For Claude Desktop or other MCP-compatible assistants, the `@veloxts/mcp` server provides the same functionality through a protocol interface.

**Setup** (Claude Desktop config):
```json
{
  "mcpServers": {
    "veloxts": {
      "command": "npx",
      "args": ["@veloxts/mcp"],
      "cwd": "/path/to/your/project"
    }
  }
}
```

**Key difference**: MCP needs the `cwd` path to find your project. The CLI auto-detects it.

**If MCP says "Not in a VeloxTS project"**:
1. Check that `cwd` points to your project root (where `package.json` is)
2. Ensure the project has VeloxTS dependencies installed
3. Fallback: Use CLI directly via terminal

---

## Procedure Errors

### "useQuery is not a function"

**Cause**: Procedure name doesn't follow query naming conventions.

```typescript
// BAD - "fetchUsers" is not recognized as a query
const { data } = api.users.fetchUsers.useQuery({});

// GOOD - Use standard prefixes
const { data } = api.users.listUsers.useQuery({});
const { data } = api.users.getUser.useQuery({ id });
const { data } = api.users.findUsers.useQuery({ search });
```

**Query prefixes**: `get*`, `list*`, `find*`

**Mutation prefixes**: `create*`, `add*`, `update*`, `edit*`, `patch*`, `delete*`, `remove*`

### "procedure.input is not a function"

**Cause**: Missing parentheses after `procedure`.

```typescript
// BAD
getUser: procedure.input(z.object({ id: z.string() }))

// GOOD
getUser: procedure().input(z.object({ id: z.string() }))
```

### "Cannot read property 'query' of undefined"

**Cause**: Procedure not registered in router.

**Fix**: Add procedure to `createRouter()` in `src/router.ts`:

```typescript
// src/router.ts
import { createRouter, extractRoutes } from '@veloxts/velox';

import { healthProcedures } from './procedures/health.js';
import { userProcedures } from './procedures/users.js';
import { postProcedures } from './procedures/posts.js';  // Add import

export const { collections, router } = createRouter(
  healthProcedures,
  userProcedures,
  postProcedures  // Add here
);

export type AppRouter = typeof router;
export const routes = extractRoutes(collections);
```

### "Input validation failed"

**Cause**: Request data doesn't match Zod schema.

**Debug**:
```typescript
// Temporarily log input to see what's being sent
createUser: procedure()
  .input(CreateUserSchema)
  .mutation(async ({ input }) => {
    console.log('Received input:', input);
    // ...
  }),
```

**Common issues**:
- Missing required fields
- Wrong field types (string vs number)
- Invalid format (email, uuid, date)

---

## Prisma Errors

### "Unknown property datasourceUrl"

**Cause**: Using Prisma 7 with deprecated connection syntax.

**Fix**: Use driver adapters in `apps/api/src/config/database.ts`:

```typescript
// BAD - Prisma 7 removed this
const db = new PrismaClient({
  datasourceUrl: process.env.DATABASE_URL,  // Error!
});

// GOOD - Use driver adapter
import { PrismaBetterSqlite3 } from '@prisma/adapter-better-sqlite3';

const adapter = new PrismaBetterSqlite3({ url: process.env.DATABASE_URL });
const db = new PrismaClient({ adapter });
```

### Prisma Decimal validation fails

**Cause**: Prisma returns `Decimal` objects, not numbers.

**Fix**: Use transforms in Zod schemas:

```typescript
// Input - coerce string/number to number
price: z.coerce.number().positive()

// Output - transform Decimal to number
price: z.any().transform((val) => Number(val))
```

### "Cannot find module '.prisma/client'"

**Cause**: Prisma client not generated.

**Fix**:
```bash
pnpm db:generate
# or
npx prisma generate
```

### Database URL not found

**Cause**: Environment variable not loaded.

**Fix**: Check `.env` file exists and has `DATABASE_URL`:

```env
# .env
DATABASE_URL="file:./dev.db"
```

For Prisma 7, database URL goes in `prisma.config.ts`, NOT in `schema.prisma`.

---

## REST Route Errors

### "Route not found" (404)

**Check**:
1. Procedure is registered in collections
2. Procedure name follows naming conventions
3. Correct HTTP method is being used

```bash
# Check registered routes
curl http://localhost:3030/api/health
```

### Double `/api/api/` in URL

**Cause**: Including `/api` prefix in `.rest()` override.

```typescript
// BAD - Results in /api/api/posts/:id/publish
.rest({ method: 'POST', path: '/api/posts/:id/publish' })

// GOOD - Prefix is auto-added
.rest({ method: 'POST', path: '/posts/:id/publish' })
```

### Path parameter not in input

**Cause**: REST path params (`:id`) are NOT auto-extracted.

```typescript
// The :id in the path is informational only
// You must pass id in the request body
.rest({ method: 'POST', path: '/posts/:id/publish' })
.input(z.object({ id: z.string().uuid() }))  // Required!
```

---

## Authentication Errors

### "Unauthorized" (401)

**Cause**: Request missing or invalid auth token.

**Check**:
1. Token is being sent in Authorization header
2. Token format: `Authorization: Bearer <token>`
3. Token hasn't expired

```typescript
// Frontend
const response = await fetch('/api/users/me', {
  headers: {
    Authorization: `Bearer ${token}`,
  },
});
```

### "Forbidden" (403)

**Cause**: User authenticated but lacks permission.

**Check**:
1. User has required role/permission
2. Guard logic is correct

```typescript
// Debug: log user info
.guard(hasRole('admin'))
.query(({ ctx }) => {
  console.log('User:', ctx.user);
  console.log('Roles:', ctx.user?.roles);
  // ...
}),
```

### Session not persisting

**Cause**: Cookie not being set or sent.

**Check**:
1. Cookie settings match your domain
2. `credentials: 'include'` in fetch requests
3. CORS allows credentials

```typescript
// Frontend fetch
const response = await fetch('/api/auth/login', {
  method: 'POST',
  credentials: 'include',  // Required for cookies
  body: JSON.stringify(data),
});
```

---

## Generator Errors

### "Not in a VeloxTS project"

**Cause**: CLI can't find project root.

**Fix**:
1. Run from project root directory
2. Ensure `package.json` exists with VeloxTS dependencies
3. For MCP: set `cwd` in config

```bash
# Run from correct directory
cd /path/to/your-velox-project
pnpm velox make resource Post
```

### "File already exists"

**Cause**: Generator won't overwrite existing files.

**Fix**: Use `--force` flag:

```bash
pnpm velox make resource Post --force
```

### "Model already exists in schema"

**Cause**: Prisma model with same name already defined.

**Options**:
1. Use a different name
2. Use `namespace` generator (doesn't inject Prisma)
3. Manually remove existing model first

---

## Build Errors

### TypeScript errors in generated code

**Cause**: Generated code doesn't match your types.

**Fix**:
1. Regenerate Prisma client: `pnpm db:generate`
2. Check schema matches Prisma model
3. Ensure imports are correct

### "Cannot find module '@veloxts/velox'"

**Cause**: Dependencies not installed.

**Fix**:
```bash
pnpm install
```

### Module resolution errors

**Cause**: Missing `.js` extension in imports.

**Fix**: Use `.js` extension for local imports:

```typescript
// BAD
import { userProcedures } from './procedures/users';

// GOOD
import { userProcedures } from './procedures/users.js';
```

---

## Development Server Errors

### Port already in use

**Cause**: Another process using port 3030.

**Fix**:
```bash
# Find process
lsof -i :3030

# Kill it
kill -9 <PID>

# Or use different port
pnpm velox dev --port 4000
```

### HMR not working

**Check**:
1. `hot-hook` is installed
2. `hotHook` config in `package.json`
3. Try `--no-hmr` to diagnose

```bash
# Disable HMR to compare
pnpm velox dev --no-hmr
```

### Slow startup

**Try**:
```bash
# Enable verbose timing
pnpm velox dev --verbose
```

Look for which phase is slow (dependency loading, Prisma, etc.)

---

## Quick Fixes Checklist

When something doesn't work:

1. **Regenerate Prisma**: `pnpm db:generate`
2. **Restart dev server**: `Ctrl+C` then `pnpm dev`
3. **Clear node_modules**: `rm -rf node_modules && pnpm install`
4. **Check imports**: Ensure `.js` extensions
5. **Check registration**: Procedure in `index.ts` exports and collections
6. **Check naming**: Procedure names follow conventions
7. **Check env**: `.env` file has required variables

---

## Getting Help

1. **Check this guide** for common issues
2. **Read error codes**: VeloxTS uses structured error codes (E1xxx, E2xxx, etc.)
3. **Use `--verbose`**: Most commands support verbose output
4. **Use `--dry-run`**: Preview changes before applying

```bash
# Verbose output
pnpm velox migrate status --verbose

# Dry run
pnpm velox make resource Post --dry-run
```
