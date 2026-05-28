---
name: typescript
description: TypeScript patterns for Node.js backends, testing, and type-safe development. Use when writing TypeScript/Node.js code.
---

# TypeScript

## Type Patterns

```typescript
// Utility types
type Partial<T> = { [P in keyof T]?: T[P] }
type Required<T> = { [P in keyof T]-?: T[P] }
type Pick<T, K extends keyof T> = { [P in K]: T[P] }
type Omit<T, K extends keyof T> = Pick<T, Exclude<keyof T, K>>

// Discriminated unions
type Result<T, E> = { ok: true; value: T } | { ok: false; error: E }

// Generic constraints
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K]

// Infer in conditionals
type ReturnType<T> = T extends (...args: any[]) => infer R ? R : never
```

## Backend Patterns (Express/Fastify)

```typescript
// Middleware pattern
const asyncHandler = (fn: RequestHandler) => (req, res, next) =>
  Promise.resolve(fn(req, res, next)).catch(next)

// Error class hierarchy
class AppError extends Error {
  constructor(public statusCode: number, message: string) {
    super(message)
  }
}
class NotFoundError extends AppError { constructor(msg: string) { super(404, msg) } }
class ValidationError extends AppError { constructor(msg: string) { super(400, msg) } }

// Zod validation
const userSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1)
})
type User = z.infer<typeof userSchema>
```

## Testing (Jest/Vitest)

```typescript
// AAA pattern
describe('UserService', () => {
  it('creates user with valid data', async () => {
    // Arrange
    const mockRepo = { save: vi.fn().mockResolvedValue({ id: '1' }) }
    const service = new UserService(mockRepo)

    // Act
    const result = await service.create({ name: 'Test' })

    // Assert
    expect(result.id).toBe('1')
    expect(mockRepo.save).toHaveBeenCalledOnce()
  })
})

// Mocking modules
vi.mock('./database', () => ({ query: vi.fn() }))
```

## Error Handling

```typescript
// Result pattern over exceptions
async function fetchUser(id: string): Promise<Result<User, Error>> {
  try {
    const user = await db.users.findUnique({ where: { id } })
    if (!user) return { ok: false, error: new Error('Not found') }
    return { ok: true, value: user }
  } catch (e) {
    return { ok: false, error: e as Error }
  }
}

// Global error handler
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  const status = err instanceof AppError ? err.statusCode : 500
  res.status(status).json({ error: err.message })
})
```

## Best Practices

- Enable strict mode in tsconfig
- Use `unknown` over `any`, narrow with type guards
- Prefer interfaces for objects, types for unions/intersections
- Use `as const` for literal types
- Validate external data at boundaries (Zod/io-ts)
- Return `Result<T,E>` for operations that can fail
