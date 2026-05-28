# Story Sizing for Ralph Loops

How to size user stories so they can be completed in 1-3 Ralph iterations.

## The 1-3 Iteration Rule

A well-sized story should be completable in 1-3 Ralph iterations:

- **1 iteration**: Simple, mechanical changes (add a column, create a file)
- **2 iterations**: Moderate complexity (implement an endpoint, add validation)
- **3 iterations**: More complex but still focused (integrate with external service)

If a story consistently takes more than 5 iterations, it's too big and should be broken down.

## Signs a Story is Too Big

### Red Flags

1. **Multiple "and"s in the description**
   - "Create user model AND authentication AND protected routes"
   - Should be 3 separate stories

2. **Vague acceptance criteria**
   - "User can manage their account"
   - What does "manage" mean? View? Edit? Delete? Password reset?

3. **Cross-cutting concerns**
   - "Add logging throughout the application"
   - Better: "Add logging to authentication endpoints"

4. **Undefined scope**
   - "Improve performance"
   - Better: "Reduce API response time for /users endpoint to <200ms"

5. **Multiple verification methods needed**
   - If you need to verify via tests AND manual browser check AND API calls
   - Story might be covering too much

### Story Size Symptoms

| Symptom | Likely Problem |
|---------|----------------|
| Taking 5+ iterations | Story too big |
| Getting blocked repeatedly | Missing dependency, break down differently |
| Forgetting previous work | Story spanning too many context windows |
| Unclear what "done" means | Acceptance criteria too vague |

## Right-Sized Story Examples

### Good: Small, Focused Stories

**Database Layer**
```
US-001: Add users table migration
- Creates users table with id, email, password_hash, created_at
- Migration runs without errors
Verify: Run migration, check table exists

US-002: Add User model with validation
- User model maps to users table
- Email validation (format, uniqueness)
- Password hashing on save
Verify: Unit tests pass
```

**API Endpoints**
```
US-003: Add POST /users endpoint
- Accepts {email, password}
- Returns created user (without password)
- Returns 400 for invalid input
Verify: Integration tests pass

US-004: Add GET /users/:id endpoint
- Returns user by ID
- Returns 404 if not found
Verify: Integration tests pass
```

**Validation**
```
US-005: Add email format validation
- Rejects invalid email formats
- Returns descriptive error message
Verify: curl with invalid email returns 400
```

### Bad: Stories That Are Too Big

**Too big: Entire feature**
```
US-001: Implement user authentication
```
Should be broken into:
- User model and migration
- Registration endpoint
- Login endpoint
- JWT token generation
- Token verification middleware
- Protected route example

**Too big: Multiple concerns**
```
US-001: Add product catalog with search and filtering
```
Should be broken into:
- Product model and migration
- List products endpoint
- Single product endpoint
- Search by name
- Filter by category
- Filter by price range

**Too big: Vague scope**
```
US-001: Set up project infrastructure
```
Should be broken into:
- Initialize package.json and dependencies
- Add TypeScript configuration
- Add ESLint configuration
- Add test framework
- Add development scripts
- Add CI configuration

## Breaking Down Large Stories

### Strategy 1: Vertical Slicing

Break by feature completeness (thin vertical slices through all layers).

**Before**: "Implement todo CRUD"

**After**:
1. Create todo (database + API + validation)
2. Read all todos (API + pagination)
3. Read single todo (API + 404 handling)
4. Update todo (API + validation)
5. Delete todo (API + confirmation)

### Strategy 2: Horizontal Slicing

Break by layer (when dependencies are clear).

**Before**: "Add user authentication"

**After**:
1. User model and migration (data layer)
2. Password hashing utility (service layer)
3. JWT token utilities (service layer)
4. Auth middleware (API layer)
5. Login endpoint (API layer)
6. Register endpoint (API layer)

### Strategy 3: By Acceptance Criterion

Each acceptance criterion becomes a story.

**Before**:
```
US-001: User registration
- Email validation
- Password strength requirements
- Duplicate email prevention
- Confirmation email
- Rate limiting
```

**After**:
```
US-001: Basic registration (email + password)
US-002: Email format validation
US-003: Password strength validation
US-004: Duplicate email prevention
US-005: Confirmation email (if needed)
US-006: Rate limiting (if needed)
```

### Strategy 4: Happy Path First

Start with the simplest success case, then add error handling.

**Before**: "Create order with validation and error handling"

**After**:
1. Create order (happy path only)
2. Validate order items exist
3. Validate quantities available
4. Handle payment failures
5. Handle out-of-stock edge cases

## Dependency Ordering

Stories should be ordered so dependencies come first.

### Correct Order

```
US-001: Create database migration     # No dependencies
US-002: Create model                  # Depends on US-001
US-003: Create repository             # Depends on US-002
US-004: Create service                # Depends on US-003
US-005: Create controller             # Depends on US-004
US-006: Add routes                    # Depends on US-005
US-007: Add integration tests         # Depends on US-006
```

### Incorrect Order (Will Fail)

```
US-001: Create controller             # Needs service!
US-002: Create service                # Needs repository!
US-003: Create routes                 # Needs controller!
```

## Verification Alignment

Each story should have ONE primary verification method.

### Clear Verification

```
US-001: Add health endpoint
Verify: curl localhost:3000/health returns {"status": "ok"}

US-002: Add database connection
Verify: npm run db:test-connection exits with 0

US-003: Add user creation
Verify: npm test -- --testPathPattern=user.create
```

### Unclear Verification (Story Too Big)

```
US-001: Add user management
Verify:
  - Tests pass
  - Manual testing in browser
  - API docs updated
  - Postman collection updated
```

This story should be 4 separate stories with one verification each.

## Iteration Budgeting

When planning stories, assign iteration budgets:

| Story Complexity | Iteration Budget | Example |
|------------------|------------------|---------|
| Simple/mechanical | 1 | Add column, create file |
| Moderate | 2 | Endpoint + tests |
| Complex but focused | 3 | External integration |
| Complex with unknowns | 3 + spike | New technology |

If a story is budgeted for 3+ iterations, consider breaking it down further.

## When to Combine Stories

Sometimes stories are too small:

**Too granular**:
```
US-001: Create users table
US-002: Add id column to users
US-003: Add email column to users
US-004: Add password_hash column to users
```

**Better combined**:
```
US-001: Create users table with id, email, password_hash, created_at
```

**Rule of thumb**: If a story takes <1 iteration consistently, it might be too small. Combine with related work.
