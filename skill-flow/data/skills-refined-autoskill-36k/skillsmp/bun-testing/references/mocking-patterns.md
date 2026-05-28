# Mocking Patterns Reference

Detailed patterns for ModuleMocker and mock setup in bun:test.

## Table of Contents

1. [Variable Declaration Order](#variable-declaration-order)
2. [Initial Mock Setup in beforeEach](#initial-mock-setup-in-beforeeach)
3. [Module Mocking Rules](#module-mocking-rules)
4. [Updating Mock Behavior](#updating-mock-behavior)
5. [Complete Example](#complete-example)

## Variable Declaration Order

Group variables by module/domain with blank lines between groups. Order groups to match their initialization in `beforeEach`:

```typescript
const moduleMocker = new ModuleMocker(import.meta.url)

let mockSignupParams: any                    // Test data group

let mockNewUser: any                         // @/data module group
let mockUserRepo: any
let mockAuthRepo: any
let mockTransaction: any

let mockToken: string                        // @/security/token module group
let mockExpiresAt: Date
let mockGenerateToken: any

let mockEmailAgent: any                      // @/lib/email-agent module group
```

## Initial Mock Setup in beforeEach

**Core principle**: Use `const` for static test data that never changes, use `let` + `beforeEach` for mocks needing re-initialization.

**Pattern**: Follow small → large dependency chain within each module group.

Setup sequence:

1. Initialize test data and primitive constants
2. Initialize base data objects used by mocks
3. Initialize mock objects depending on the data
4. Call `moduleMocker.mock()` immediately after defining related mocks
5. Repeat for each module: primitives → mock objects → `moduleMocker.mock()`

```typescript
describe('Signup', () => {
  const moduleMocker = new ModuleMocker(import.meta.url)

  // Static test data - never changes across tests
  const VALID_EMAIL = 'test@example.com'
  const VALID_PASSWORD = 'SecurePass123!'
  const HASHED_PASSWORD = '$2b$10$hash123'

  // Mocks that need re-initialization
  let mockSignupParams: any
  let mockNewUser: any
  let mockUserRepo: any
  let mockHashPassword: any

  beforeEach(async () => {
    // Test data
    mockSignupParams = { firstName: 'John', email: VALID_EMAIL, ... }

    // @/data module group
    mockNewUser = { id: 1, email: VALID_EMAIL, ... }
    mockUserRepo = { findByEmail: mock(() => ...) }

    await moduleMocker.mock('@/data', () => ({
      userRepo: mockUserRepo,
    }))

    // @/crypto module group
    mockHashPassword = mock(async () => HASHED_PASSWORD)

    await moduleMocker.mock('@/crypto', () => ({
      hashPassword: mockHashPassword,
    }))
  })
})
```

## Module Mocking Rules

1. Use `moduleMocker.mock()` ONLY in `beforeEach` for initial module mocking
2. Never use `moduleMocker.mock()` in individual test cases
3. Always define mock object variable before calling `moduleMocker.mock()` with it
4. Call `moduleMocker.mock()` immediately after defining all related mock objects
5. **Don't mock encapsulated dependencies**: Only mock the public API/wrapper, not underlying implementation
   - Example: If `@/net/http/cookie` wraps `hono/cookie`, only mock the wrapper
   - Prevents tight coupling to implementation details

## Updating Mock Behavior

Use `mockImplementation()` to update mock behavior in individual tests:

```typescript
it('should handle user not found', async () => {
  // Override default mock behavior for this test only
  mockUserRepo.findByEmail.mockImplementation(async () => null)

  // Act & Assert
  await expect(service.login(email)).rejects.toThrow('User not found')
})
```

Other mock utilities: `mockReturnValue`, `mockResolvedValue`, `mockRejectedValue`

## Complete Example

Dependency chain from small to large:

```typescript
// Good: Clear dependency chain
mockUser = { id: 1, email: 'test@example.com' }
mockUserRepo = { findByEmail: mock(async () => mockUser) }
await moduleMocker.mock('@/data', () => ({ userRepo: mockUserRepo }))

mockJwtToken = 'token-123'
mockJwt = { default: { sign: mock(async () => mockJwtToken) } }
await moduleMocker.mock('@/lib/jwt', () => mockJwt)
```

```typescript
describe('AuthService', () => {
  const moduleMocker = new ModuleMocker(import.meta.url)

  // Static constants
  const TEST_EMAIL = 'user@example.com'
  const TEST_PASSWORD = 'Password123!'
  const JWT_TOKEN = 'jwt-token-abc'

  // Mock variables
  let mockUser: any
  let mockUserRepo: any
  let mockAuthRepo: any

  let mockVerifyPassword: any
  let mockSignToken: any

  beforeEach(async () => {
    // Data layer mocks
    mockUser = { id: 1, email: TEST_EMAIL, role: 'user' }
    mockUserRepo = {
      findByEmail: mock(async () => mockUser),
      update: mock(async () => mockUser),
    }
    mockAuthRepo = {
      findByUserId: mock(async () => ({ passwordHash: 'hash' })),
    }

    await moduleMocker.mock('@/data', () => ({
      userRepo: mockUserRepo,
      authRepo: mockAuthRepo,
    }))

    // Security mocks
    mockVerifyPassword = mock(async () => true)
    mockSignToken = mock(async () => JWT_TOKEN)

    await moduleMocker.mock('@/security/password', () => ({
      verifyPassword: mockVerifyPassword,
    }))

    await moduleMocker.mock('@/security/jwt', () => ({
      signToken: mockSignToken,
    }))
  })

  afterEach(() => {
    mockUserRepo.findByEmail.mockClear()
    mockUserRepo.update.mockClear()
    mockAuthRepo.findByUserId.mockClear()
    mockVerifyPassword.mockClear()
    mockSignToken.mockClear()
  })

  it('should login successfully with valid credentials', async () => {
    const { login } = await import('./auth-service')

    const result = await login(TEST_EMAIL, TEST_PASSWORD)

    expect(result.token).toBe(JWT_TOKEN)
    expect(mockUserRepo.findByEmail).toHaveBeenCalledWith(TEST_EMAIL)
    expect(mockVerifyPassword).toHaveBeenCalled()
  })

  it('should reject invalid password', async () => {
    mockVerifyPassword.mockImplementation(async () => false)

    const { login } = await import('./auth-service')

    await expect(login(TEST_EMAIL, 'wrong')).rejects.toThrow('Invalid credentials')
  })
})
```
