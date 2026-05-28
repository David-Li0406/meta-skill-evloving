# Convex Testing with convex-test

`convex-test` provides a mock Convex backend for fast, isolated testing without network calls.

## Setup

```bash
pnpm add -D convex-test @edge-runtime/vm
```

Requires `edge-runtime` environment in vitest config.

## Basic Pattern

```typescript
import { convexTest } from 'convex-test'
import { describe, it, expect, vi } from 'vitest'
import { api } from './_generated/api'
import schema from './schema'

describe('messages', () => {
  it('creates and lists messages', async () => {
    const t = convexTest(schema)

    await t.mutation(api.messages.send, { body: 'Hello', author: 'Sarah' })
    await t.mutation(api.messages.send, { body: 'World', author: 'Tom' })

    const messages = await t.query(api.messages.list)

    expect(messages).toMatchObject([
      { body: 'Hello', author: 'Sarah' },
      { body: 'World', author: 'Tom' },
    ])
  })
})
```

## Authentication Testing

```typescript
describe('tasks with auth', () => {
  it('user can only see their own tasks', async () => {
    const t = convexTest(schema)

    // Create authenticated contexts
    const asSarah = t.withIdentity({
      name: 'Sarah',
      email: 'sarah@test.com',
      subject: 'user_sarah_123',
    })
    const asLee = t.withIdentity({
      name: 'Lee',
      email: 'lee@test.com',
      subject: 'user_lee_456',
    })

    // Each user creates a task
    await asSarah.mutation(api.tasks.create, { text: 'Sarah task' })
    await asLee.mutation(api.tasks.create, { text: 'Lee task' })

    // Each user can only see their own task
    const sarahTasks = await asSarah.query(api.tasks.list)
    const leeTasks = await asLee.query(api.tasks.list)

    expect(sarahTasks).toHaveLength(1)
    expect(sarahTasks[0].text).toBe('Sarah task')
    expect(leeTasks).toHaveLength(1)
    expect(leeTasks[0].text).toBe('Lee task')
  })
})
```

## Scheduled Functions

```typescript
describe('scheduled functions', () => {
  it('executes reminder after delay', async () => {
    vi.useFakeTimers()
    const t = convexTest(schema)

    await t.mutation(api.scheduler.scheduleReminder, { delayMs: 10000 })

    // Advance time past the scheduled delay
    vi.advanceTimersByTime(11000)
    await t.finishInProgressScheduledFunctions()

    // Verify the scheduled function ran
    const reminder = await t.run(async (ctx) =>
      ctx.db.query('reminders').first()
    )
    expect(reminder).toMatchObject({ status: 'sent' })

    vi.useRealTimers()
  })
})
```

## Direct Database Access

```typescript
describe('database operations', () => {
  it('seeds and queries data directly', async () => {
    const t = convexTest(schema)

    // Seed data directly
    await t.run(async (ctx) => {
      await ctx.db.insert('users', {
        name: 'Admin User',
        role: 'admin',
        createdAt: Date.now(),
      })
    })

    // Query data directly
    const user = await t.run(async (ctx) =>
      ctx.db.query('users').filter(q => q.eq(q.field('role'), 'admin')).first()
    )

    expect(user?.name).toBe('Admin User')
  })
})
```

## Test Factories

```typescript
// convex/__tests__/factories.ts
import { faker } from '@faker-js/faker'
import type { Doc } from '../_generated/dataModel'

export const createUser = (overrides?: Partial<Doc<'users'>>): Omit<Doc<'users'>, '_id' | '_creationTime'> => ({
  name: faker.person.fullName(),
  email: faker.internet.email(),
  role: 'user',
  createdAt: Date.now(),
  ...overrides,
})

export const createTask = (overrides?: Partial<Doc<'tasks'>>): Omit<Doc<'tasks'>, '_id' | '_creationTime'> => ({
  text: faker.lorem.sentence(),
  completed: false,
  userId: 'user_test_123',
  createdAt: Date.now(),
  ...overrides,
})
```

Usage:
```typescript
import { createUser, createTask } from './factories'

it('uses factories for test data', async () => {
  const t = convexTest(schema)

  await t.run(async (ctx) => {
    await ctx.db.insert('users', createUser({ name: 'Test User' }))
    await ctx.db.insert('tasks', createTask({ completed: true }))
  })

  // ...assertions
})
```

## HTTP Actions Testing

```typescript
describe('HTTP actions', () => {
  it('handles webhook payload', async () => {
    const t = convexTest(schema)

    const response = await t.fetch('/webhook', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ event: 'user.created', data: { id: '123' } }),
    })

    expect(response.status).toBe(200)
    const body = await response.json()
    expect(body.success).toBe(true)
  })
})
```

## Best Practices

1. **Always import schema**: `convexTest(schema)` ensures type safety
2. **Use `withIdentity` for auth tests**: Don't test unauthenticated paths with authenticated functions
3. **Clean state per test**: Each `convexTest()` call starts fresh
4. **Use `t.run()` for setup/verification**: Direct DB access for seeding and assertions
5. **Test edge cases**: Empty results, permissions, validation errors

## Common Issues

### Timeout Errors
Increase timeout in vitest config:
```typescript
testTimeout: 30000,
hookTimeout: 30000,
```

### Module Resolution
Ensure convex-test and convex are inlined:
```typescript
server: {
  deps: {
    inline: ['convex-test', 'convex'],
  },
},
```

### Isolation Issues
Use forks pool with single fork:
```typescript
pool: 'forks',
poolOptions: {
  forks: {
    singleFork: true,
  },
},
```
