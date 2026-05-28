# Example: Task Decomposition for "Add User Registration"

## Original Request
"Add user registration with email verification"

## Decomposed Tasks

### Task 1: Create User Model
- **Depends on:** none
- **Files:** `src/types/user.ts`, `prisma/schema.prisma`
- **Done when:** User type defined, database migration created
- **Complexity:** S

### Task 2: Create Email Service
- **Depends on:** none
- **Files:** `src/services/email.ts`, `src/templates/verify-email.html`
- **Done when:** Email service can send templated emails
- **Complexity:** M

### Task 3: Create Registration API
- **Depends on:** Task 1
- **Files:** `src/app/api/auth/register/route.ts`
- **Done when:** POST /api/auth/register creates user and sends verification email
- **Complexity:** M

### Task 4: Create Email Verification API
- **Depends on:** Task 1
- **Files:** `src/app/api/auth/verify/route.ts`
- **Done when:** GET /api/auth/verify?token=xxx verifies user
- **Complexity:** S

### Task 5: Create Registration Form
- **Depends on:** Task 3
- **Files:** `src/components/auth/RegisterForm.tsx`
- **Done when:** Form submits to API, handles errors, shows success
- **Complexity:** M

### Task 6: Create Verification Page
- **Depends on:** Task 4
- **Files:** `src/app/verify/page.tsx`
- **Done when:** Page handles verification token and shows result
- **Complexity:** S

### Task 7: Write Tests
- **Depends on:** Tasks 1-6
- **Files:** `src/__tests__/auth/registration.test.ts`
- **Done when:** All registration flows tested
- **Complexity:** M

## Execution Strategy

```
Parallel Group 1: [Task 1, Task 2]
  ↓
Parallel Group 2: [Task 3, Task 4] (after Group 1)
  ↓
Parallel Group 3: [Task 5, Task 6] (after Group 2)
  ↓
Sequential: [Task 7] (after all)
```

## Verification Pipeline

1. **Typecheck:** `npm run typecheck`
2. **Lint:** `npm run lint`
3. **Test:** `npm test -- --testPathPattern=registration`
4. **Build:** `npm run build`
