# Task Examples

Good vs bad task descriptions.

## Example 1: Database Model

### Bad
```
Add user model
```
Why: No location, no fields, no constraints.

### Good
```
Create User model

Location: src/models/user.ts

Fields:
- id: UUID, primary key, auto-generated
- email: string, unique, not null
- passwordHash: string, not null
- createdAt: timestamp, default now()
- updatedAt: timestamp, auto-update

Verify: Model file exists, can import and instantiate User
```

## Example 2: API Endpoint

### Bad
```
Add login endpoint
```
Why: No path, no request/response format, no error cases.

### Good
```
Add POST /api/auth/login endpoint

Location: src/routes/auth.ts

Request body:
- email: string (required)
- password: string (required)

Response:
- 200: { token: string, user: { id, email } }
- 400: { error: "Invalid credentials" }
- 429: { error: "Too many attempts" } (after 5 failures)

Verify: Can login with valid credentials, get 400 on invalid
```

## Example 3: Refactoring

### Bad
```
Refactor auth module
```
Why: No specific changes, no boundaries, no success criteria.

### Good
```
Extract token generation from login handler

Location: src/routes/auth.ts → src/services/token.ts

Changes:
- Create TokenService class in new file
- Move generateToken() and verifyToken() functions
- Update imports in auth.ts
- Keep same function signatures

Verify: All auth tests still pass, no changes to API behavior
```

## Example 4: Bug Fix

### Bad
```
Fix login bug
```
Why: Which bug? What's the expected behavior?

### Good
```
Fix: Login returns 500 when email contains uppercase

Location: src/services/auth.ts:45

Problem: Email comparison is case-sensitive, user "John@example.com"
can register but can't login as "john@example.com"

Fix: Lowercase email before lookup in findUserByEmail()

Verify: Can login with any case variation of registered email
```

## Task Size Guidelines

| Scope | Task count |
|-------|------------|
| Single function change | 1 task |
| New file with 2-3 functions | 1 task |
| New feature touching 3+ files | 2-4 tasks |
| Cross-cutting concern | 1 task per layer |
