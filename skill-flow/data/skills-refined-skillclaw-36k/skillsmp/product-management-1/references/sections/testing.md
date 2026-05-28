# Testing Strategy

Define test approach per capability and phase.

## Test Pyramid

```
        /\
       /E2E\         (few, slow, high confidence)
      /------\
     / Integ  \      (some, medium speed)
    /----------\
   /   Unit     \    (many, fast, low cost)
  /--------------\
```

## Testing by Phase

```
## Test Strategy

### Phase 1: Foundation
- Unit tests for utilities
- Integration tests for database connection
- No E2E (nothing to test yet)

### Phase 2: Core Features
- Unit tests for all business logic
- Integration tests for API endpoints
- Component tests for UI

### Phase 3: Integration
- E2E tests for critical paths
- Load testing for performance
- Security testing

### Phase 4: Polish
- Regression test suite
- Edge case coverage
- Accessibility testing
```

## Test Coverage by Capability

```
| Capability | Unit | Integration | E2E |
|------------|------|-------------|-----|
| Auth       | 90%  | Yes         | Yes |
| Users      | 80%  | Yes         | Yes |
| Reports    | 70%  | Optional    | No  |
```

## Critical Test Scenarios

```
## Must-Test Scenarios

### Authentication
1. Valid login → success
2. Invalid password → error message
3. Locked account → appropriate response
4. Session expiry → redirect to login

### User Management
1. Create user → user exists
2. Update profile → changes persist
3. Delete user → cascade handled
```

## Test File Mapping

```
| Source File | Test File |
|-------------|-----------|
| auth.service.ts | auth.service.spec.ts |
| user.model.ts | user.model.spec.ts |
| LoginForm.tsx | LoginForm.test.tsx |
```

## Acceptance Criteria Format

For each task, include testable acceptance:

```
Task 2.1: Implement Login
Acceptance:
- [ ] POST /auth/login returns 200 with valid credentials
- [ ] POST /auth/login returns 401 with invalid credentials
- [ ] Session token set in response
- [ ] Rate limiting after 5 failed attempts
```
