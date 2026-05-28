# Task Decomposition Patterns

Common patterns for breaking down different types of features.

## Pattern 1: CRUD Feature

**Example:** "Add user management"

```
Group 1 (Parallel - Data Layer):
├── Task 1: Create User type/model
├── Task 2: Create User database schema
└── Task 3: Create User validation schema

Group 2 (Parallel - API Layer):
├── Task 4: Create GET /users endpoint (depends: 1, 2)
├── Task 5: Create POST /users endpoint (depends: 1, 2, 3)
├── Task 6: Create PUT /users/:id endpoint (depends: 1, 2, 3)
└── Task 7: Create DELETE /users/:id endpoint (depends: 1, 2)

Group 3 (Parallel - UI Layer):
├── Task 8: Create UserList component (depends: 4)
├── Task 9: Create UserForm component (depends: 5, 6)
└── Task 10: Create UserCard component (depends: 4)

Group 4 (Sequential - Integration):
└── Task 11: Create UsersPage with all components (depends: 8, 9, 10)

Group 5 (Parallel - Tests):
├── Task 12: Unit tests for User model
├── Task 13: API integration tests
└── Task 14: Component tests
```

## Pattern 2: Authentication Feature

**Example:** "Add login/logout"

```
Group 1 (Sequential - Core):
├── Task 1: Design auth flow and token strategy
└── Task 2: Set up auth provider/context

Group 2 (Parallel - Backend):
├── Task 3: Create POST /auth/login endpoint
├── Task 4: Create POST /auth/logout endpoint
├── Task 5: Create GET /auth/me endpoint
└── Task 6: Create auth middleware

Group 3 (Parallel - Frontend):
├── Task 7: Create LoginForm component
├── Task 8: Create useAuth hook
└── Task 9: Create ProtectedRoute component

Group 4 (Sequential - Integration):
├── Task 10: Integrate auth with API client
└── Task 11: Add auth to app layout

Group 5 (Tests):
└── Task 12: Auth flow integration tests
```

## Pattern 3: Data Visualization Feature

**Example:** "Add analytics dashboard"

```
Group 1 (Parallel - Data):
├── Task 1: Define analytics data types
├── Task 2: Create data aggregation utilities
└── Task 3: Create mock data generators

Group 2 (Parallel - API):
├── Task 4: Create GET /analytics/overview endpoint
├── Task 5: Create GET /analytics/trends endpoint
└── Task 6: Create GET /analytics/breakdown endpoint

Group 3 (Parallel - Components):
├── Task 7: Create Chart wrapper component
├── Task 8: Create StatCard component
├── Task 9: Create DataTable component
└── Task 10: Create DateRangePicker component

Group 4 (Sequential - Dashboard):
├── Task 11: Create DashboardLayout
└── Task 12: Compose AnalyticsDashboard page

Group 5 (Polish):
├── Task 13: Add loading states
├── Task 14: Add error boundaries
└── Task 15: Add responsive design
```

## Pattern 4: Integration Feature

**Example:** "Add Stripe payments"

```
Group 1 (Setup):
├── Task 1: Install and configure Stripe SDK
└── Task 2: Set up webhook endpoint

Group 2 (Parallel - Backend):
├── Task 3: Create payment intent service
├── Task 4: Create subscription service
├── Task 5: Create webhook handlers
└── Task 6: Create payment status utilities

Group 3 (Parallel - Frontend):
├── Task 7: Create PaymentForm component
├── Task 8: Create SubscriptionSelector component
└── Task 9: Create PaymentHistory component

Group 4 (Integration):
├── Task 10: Create checkout flow
└── Task 11: Handle payment callbacks

Group 5 (Testing):
├── Task 12: Unit tests with Stripe mocks
└── Task 13: Webhook integration tests
```

## Complexity Estimation Guidelines

### Small (S) - ~15 minutes
- Single file modification
- Simple logic (CRUD, basic validation)
- No external dependencies
- Examples: Add a type, create a simple component, write a utility function

### Medium (M) - ~30-45 minutes
- 2-4 file modifications
- Moderate logic (state management, API integration)
- May have external dependencies
- Examples: Create an API endpoint with validation, build a form with validation

### Large (L) - ~1+ hours
- 5+ file modifications
- Complex logic (workflows, algorithms)
- Multiple external dependencies
- **Consider breaking down further**
- Examples: Complete auth flow, complex dashboard

## Anti-Patterns to Avoid

### ❌ Vague Tasks
```
Task: "Implement user feature"
```

### ✅ Specific Tasks
```
Task 1: Create User TypeScript interface in types/user.ts
Task 2: Create users table migration
Task 3: Create GET /api/users endpoint
```

### ❌ Missing Dependencies
```
Task 1: Create UserList component
Task 2: Create User type
```

### ✅ Correct Order
```
Task 1: Create User type
Task 2: Create UserList component (depends: Task 1)
```

### ❌ Too Large
```
Task: "Build complete checkout system"
```

### ✅ Properly Decomposed
```
Task 1: Create CartContext
Task 2: Create CartItem component
Task 3: Create CheckoutForm component
Task 4: Create payment service
Task 5: Integrate and test
```
