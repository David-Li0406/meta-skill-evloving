# Prompt Examples

Real-world prompt examples from simple to complex.

## Simple Tasks

### Fix a Bug

**Vague (Bad):**
```
The login is broken, fix it.
```

**Effective:**
```
Fix the login bug where users get "Invalid credentials" even with correct password.

@src/api/auth/login.ts
@src/services/auth.ts

Reproduction:
1. Register new user with email: test@example.com
2. Try to login with same credentials
3. Error: "Invalid credentials"

The password hash comparison might be the issue.
```

### Add a Simple Feature

**Vague (Bad):**
```
Add dark mode.
```

**Effective:**
```
Add a dark mode toggle to the settings page.

@src/components/Settings.tsx
@src/context/ThemeContext.tsx
@src/styles/globals.css

Requirements:
- Toggle switch in settings
- Persist preference to localStorage
- Apply .dark class to <html> element
- Use existing CSS variables (--bg-primary, --text-primary)

Done when: Toggle switches theme and persists across page reload.
```

### Update a Dependency

**Vague (Bad):**
```
Update React.
```

**Effective:**
```
Update React from 17 to 18.

@package.json

Steps:
1. Update react and react-dom to ^18.2.0
2. Update @types/react and @types/react-dom
3. Replace ReactDOM.render with createRoot
4. Fix any TypeScript errors
5. Run tests to verify nothing broke

Stop if: Major breaking changes require architectural decisions.
```

## Complex Tasks

### Implement a Feature Module

```
Implement user notification preferences.

## Context
@src/types/user.ts
@src/api/users/
@prisma/schema.prisma

## Database Changes
Add to User model:
- emailNotifications: boolean (default true)
- pushNotifications: boolean (default true)
- notificationFrequency: enum (instant, daily, weekly)

## API Endpoints
- GET /api/users/:id/preferences
- PATCH /api/users/:id/preferences

## Frontend
- Add Preferences section to Settings page
- Toggle switches for each preference
- Dropdown for frequency
- Save button with loading state

## Success Criteria
- [ ] Database migration runs cleanly
- [ ] API endpoints work (test with curl examples)
- [ ] Frontend renders and saves preferences
- [ ] Existing user tests still pass
- [ ] New tests cover preference CRUD

ultrathink about edge cases like:
- What happens to existing users (migration defaults)
- Race conditions on concurrent updates
```

### Refactor a Module

```
Refactor the payment processing module for better testability.

## Current State
@src/services/payment.ts (monolithic 800 line file)
@src/api/payments/

## Problems
- Direct Stripe SDK calls make testing hard
- Mixed concerns (validation, processing, logging)
- No dependency injection
- Difficult to add new payment providers

## Target Architecture
```
src/services/payment/
  index.ts         # Public exports
  types.ts         # Interfaces
  processor.ts     # PaymentProcessor class
  providers/
    stripe.ts      # StripeProvider implements PaymentProvider
    mock.ts        # MockProvider for testing
  validators/
    card.ts        # Card validation
    amount.ts      # Amount validation
```

## Requirements
- PaymentProvider interface for multiple providers
- Dependency injection for provider
- Separate validation layer
- All existing tests must pass
- Add unit tests for each new module

## Constraints
- No changes to public API consumed by other modules
- Keep Stripe as default provider
- Don't change database schema

ultrathink about the migration path to avoid breaking changes.
```

### Debug a Complex Issue

```
ultrathink about this memory leak in production.

## Symptom
Server memory grows from 512MB to 4GB over 24 hours, then OOM kills process.

## Evidence
@logs/memory-profile.json
@src/services/cache.ts
@src/middleware/session.ts

## Environment
- Node.js 18.17.0
- Express 4.18
- Redis for sessions
- In-memory LRU cache for API responses

## Monitoring Data
- Memory grows linearly (~150MB/hour)
- No correlation with request volume
- Happens on all server instances
- Started after deploy on 2024-01-15

## Changes in That Deploy
@git:log --since="2024-01-14" --until="2024-01-16"

## Already Investigated
- Redis connections: stable at 10
- Event listeners: removed known leak patterns
- Heap snapshots: show growing cache entries

Consider:
- Cache eviction not working
- Closure references holding objects
- Stream not being properly closed
- Timer/interval accumulation
```

## Multi-File Operations

### Rename and Reorganize

```
Rename the "widgets" module to "components" throughout the codebase.

## Scope
@src/widgets/ -> @src/components/
@tests/widgets/ -> @tests/components/

## Changes Needed
1. Rename directories
2. Update all imports
3. Update path aliases in tsconfig.json
4. Update any documentation references
5. Update test configurations

## Verification
- [ ] TypeScript compiles
- [ ] All tests pass
- [ ] No broken imports (grep for 'widgets')
- [ ] Build succeeds
```

### Cross-Cutting Concern

```
Add request logging to all API endpoints.

## Current API Structure
@src/api/
  users/
  products/
  orders/
  auth/

## Requirements
- Log: timestamp, method, path, status, duration, user ID
- Don't log sensitive data (passwords, tokens)
- Log level: info for success, warn for 4xx, error for 5xx
- Include request ID for tracing

## Implementation
1. Create logging middleware @src/middleware/requestLogger.ts
2. Add to Express app before routes
3. Use existing logger @src/utils/logger.ts
4. Add request ID middleware if not exists

## Don't Change
- Individual route handlers
- Response format
- Existing middleware order (auth must come first)

Example log output:
{"timestamp":"...","requestId":"abc123","method":"GET","path":"/api/users","userId":"user_1","status":200,"duration":45}
```

## Context-Heavy Tasks

### Working with External APIs

```
Integrate with the Acme API for order fulfillment.

## API Documentation
@https://docs.acme.com/api/v2/fulfillment

## Our Types
@src/types/order.ts
@src/types/shipping.ts

## Requirements
1. Create Acme API client @src/services/acme/client.ts
   - Use their OAuth2 flow
   - Handle rate limiting (100 req/min)
   - Retry on 5xx with exponential backoff

2. Map our Order type to their fulfillment format

3. Implement methods:
   - createFulfillment(order: Order): Promise<FulfillmentResponse>
   - getFulfillmentStatus(id: string): Promise<Status>
   - cancelFulfillment(id: string): Promise<void>

4. Add webhook handler for status updates
   @src/api/webhooks/acme.ts

## Credentials
Store in environment variables:
- ACME_CLIENT_ID
- ACME_CLIENT_SECRET
- ACME_WEBHOOK_SECRET

## Testing
- Mock the API for unit tests
- Integration tests against sandbox environment
```

### Legacy Code Integration

```
Integrate new React dashboard with legacy jQuery admin panel.

## Legacy System
@public/admin/js/main.js (jQuery)
@public/admin/css/admin.css

## New Dashboard
@src/dashboard/ (React)

## Integration Points
1. Embed React component in legacy page
   - Mount point: #react-dashboard-root
   - Pass legacy session data to React

2. Communication between systems
   - React emits events for legacy to handle
   - Legacy calls exposed React methods

3. Shared styling
   - React components use legacy CSS variables
   - No style conflicts (namespace React styles)

## Constraints
- Can't rewrite legacy system
- Must work with jQuery 2.x
- IE11 not required (finally!)
- Both systems share same session

## Build
- React builds to /public/admin/js/dashboard.bundle.js
- Legacy loads bundle after jQuery

ultrathink about potential conflicts and race conditions.
```

## Iterative Refinement Examples

### Building a Feature Incrementally

**Round 1: Foundation**
```
Create the data model for a task management feature.

@prisma/schema.prisma
@src/types/

Add:
- Task model (title, description, status, dueDate, assignee)
- TaskStatus enum (TODO, IN_PROGRESS, DONE)
- Relation to User model

Run migration, verify schema.
```

**Round 2: API**
```
Good, schema looks correct.

Now add the API endpoints for tasks:

@src/api/tasks/

- GET /tasks (list with pagination and filters)
- GET /tasks/:id
- POST /tasks
- PATCH /tasks/:id
- DELETE /tasks/:id

Use the patterns from @src/api/users/ for consistency.
Include validation with zod.
```

**Round 3: Tests**
```
API endpoints work.

Now add comprehensive tests:

@tests/api/tasks.test.ts

Cover:
- CRUD operations
- Validation errors
- Authorization (users can only see their tasks)
- Pagination edge cases
- Filter combinations

Use test fixtures from @tests/fixtures/
```

**Round 4: Frontend**
```
Backend is solid.

Now build the frontend task list:

@src/pages/tasks/index.tsx

Requirements:
- Fetch tasks with React Query
- Display in table with sorting
- Filter by status dropdown
- Pagination controls
- Loading and error states

Use components from @src/components/ui/
```

**Round 5: Polish**
```
Almost done!

Add final polish:
- Optimistic updates on status change
- Bulk selection and actions
- Keyboard shortcuts (j/k to navigate, x to toggle)
- Empty state illustration

Then run the full test suite and fix any issues.
```

### Debugging Iteratively

**Round 1: Identify**
```
Users report slow page loads on the product list.

@src/pages/products/index.tsx
@src/api/products/

First, identify the bottleneck:
- Check API response time
- Check component render time
- Check network waterfall
```

**Round 2: Investigate**
```
API takes 3 seconds. That's the problem.

@src/services/products.ts
@prisma/schema.prisma

Investigate:
- What queries are being made?
- Are there N+1 problems?
- Is pagination implemented?
```

**Round 3: Fix**
```
Found N+1 on product images. Fix it.

Current: Fetches images in loop
Target: Single query with include

Also add:
- Cursor-based pagination
- Index on products.categoryId
```

**Round 4: Verify**
```
Faster! Down to 200ms.

Now verify:
- Run existing tests (should still pass)
- Add performance test asserting < 500ms
- Test with 10,000 products in staging DB
```

## Session Management Examples

### Compact and Continue

```
/compact

## Context for continuation:
Building user authentication system.

## Completed:
- User model with email/password
- Password hashing with bcrypt
- Login endpoint returning JWT
- Registration endpoint with validation

## Next steps:
- JWT middleware for protected routes
- Refresh token flow
- Password reset functionality

## Key decisions made:
- Using RS256 for JWT signing
- Access tokens expire in 15 minutes
- Refresh tokens stored in Redis

Continue with JWT middleware implementation.
```

### Fresh Start with Context

```
Let's restart the caching implementation.

Ignore the previous attempts that used Redis Cluster -
it's overkill for our scale.

New approach:
- Simple single-node Redis
- Cache only: product listings, user sessions
- TTL: 5 min for products, 24h for sessions
- No distributed locking

@src/services/cache.ts (delete and recreate)
@src/config/redis.ts

Keep it simple.
```
