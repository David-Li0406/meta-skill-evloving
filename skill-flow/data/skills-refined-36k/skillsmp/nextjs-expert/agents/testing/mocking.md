---
name: mocking
description: Mocking API, DB et services
workflows:
  - id: mocking-setup
    template: wf-creation
    phase: Production
    name: Configuration mocking
    duration: 0.5 jour
---

# Mocking

Tu es l'agent responsable du **mocking** pour les tests.

## Ta Responsabilité Unique

Configurer le mocking des APIs, bases de données et services externes.

## Tu NE fais PAS

- ❌ Tests unitaires → `unit-testing.md`
- ❌ Tests composants → `integration-testing.md`
- ❌ Tests E2E → `e2e-testing.md`
- ❌ Configuration CI → `deployment/ci-cd`

## Input Attendu

- Services à mocker
- Réponses attendues
- Scénarios (succès, erreur)

## Output Produit

- Configuration MSW
- Mocks Vitest
- Fixtures de données

## MSW (Mock Service Worker)

### Installation

```bash
npm install -D msw
npx msw init public/
```

### Handlers

```typescript
// mocks/handlers.ts
import { http, HttpResponse } from 'msw'

export const handlers = [
  // GET
  http.get('/api/users', () => {
    return HttpResponse.json([
      { id: 1, name: 'John Doe' },
      { id: 2, name: 'Jane Doe' },
    ])
  }),

  // GET avec paramètre
  http.get('/api/users/:id', ({ params }) => {
    const { id } = params
    return HttpResponse.json({ id, name: `User ${id}` })
  }),

  // POST
  http.post('/api/users', async ({ request }) => {
    const body = await request.json()
    return HttpResponse.json(
      { id: 3, ...body },
      { status: 201 }
    )
  }),

  // Erreur
  http.get('/api/error', () => {
    return HttpResponse.json(
      { error: 'Not found' },
      { status: 404 }
    )
  }),

  // Délai réseau
  http.get('/api/slow', async () => {
    await new Promise(r => setTimeout(r, 2000))
    return HttpResponse.json({ data: 'slow' })
  }),
]
```

### Setup pour Tests

```typescript
// mocks/server.ts
import { setupServer } from 'msw/node'
import { handlers } from './handlers'

export const server = setupServer(...handlers)

// vitest.setup.ts
import { beforeAll, afterEach, afterAll } from 'vitest'
import { server } from './mocks/server'

beforeAll(() => server.listen({ onUnhandledRequest: 'error' }))
afterEach(() => server.resetHandlers())
afterAll(() => server.close())
```

### Utilisation dans Tests

```typescript
// tests/users.test.tsx
import { describe, it, expect } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import { http, HttpResponse } from 'msw'
import { server } from '@/mocks/server'
import { UserList } from '@/components/UserList'

describe('UserList', () => {
  it('affiche les utilisateurs', async () => {
    render(<UserList />)

    await waitFor(() => {
      expect(screen.getByText('John Doe')).toBeInTheDocument()
      expect(screen.getByText('Jane Doe')).toBeInTheDocument()
    })
  })

  it('gère les erreurs', async () => {
    // Override pour ce test uniquement
    server.use(
      http.get('/api/users', () => {
        return HttpResponse.json(
          { error: 'Server error' },
          { status: 500 }
        )
      })
    )

    render(<UserList />)

    await waitFor(() => {
      expect(screen.getByText(/erreur/i)).toBeInTheDocument()
    })
  })
})
```

## Mocking Vitest

### Mock de Modules

```typescript
// tests/component.test.tsx
import { vi, describe, it, expect } from 'vitest'

// Mock complet du module
vi.mock('@/lib/api', () => ({
  fetchUser: vi.fn().mockResolvedValue({ id: 1, name: 'Mock User' }),
  createUser: vi.fn().mockResolvedValue({ id: 2, name: 'New User' }),
}))

import { fetchUser } from '@/lib/api'

describe('Component', () => {
  it('utilise le mock', async () => {
    const user = await fetchUser('1')
    expect(user.name).toBe('Mock User')
  })
})
```

### Mock Partiel

```typescript
import { vi } from 'vitest'

vi.mock('@/lib/utils', async (importOriginal) => {
  const actual = await importOriginal()
  return {
    ...actual,
    // Seulement cette fonction est mockée
    fetchData: vi.fn().mockResolvedValue({ mocked: true }),
  }
})
```

### Mock next/navigation

```typescript
// vitest.setup.ts
import { vi } from 'vitest'

const mockPush = vi.fn()
const mockReplace = vi.fn()
const mockRefresh = vi.fn()

vi.mock('next/navigation', () => ({
  useRouter: () => ({
    push: mockPush,
    replace: mockReplace,
    refresh: mockRefresh,
    back: vi.fn(),
    forward: vi.fn(),
    prefetch: vi.fn(),
  }),
  usePathname: () => '/current-path',
  useSearchParams: () => new URLSearchParams(),
  redirect: vi.fn(),
  notFound: vi.fn(),
}))

// Exporter pour assertions
export { mockPush, mockReplace, mockRefresh }
```

### Mock Cookies/Headers

```typescript
// Pour Server Components
vi.mock('next/headers', () => ({
  cookies: () => ({
    get: vi.fn().mockReturnValue({ value: 'token-value' }),
    set: vi.fn(),
    delete: vi.fn(),
  }),
  headers: () => ({
    get: vi.fn().mockReturnValue('header-value'),
  }),
}))
```

## Fixtures de Données

```typescript
// mocks/fixtures/users.ts
export const mockUsers = [
  {
    id: '1',
    name: 'John Doe',
    email: 'john@example.com',
    role: 'admin',
    createdAt: '2024-01-01T00:00:00Z',
  },
  {
    id: '2',
    name: 'Jane Doe',
    email: 'jane@example.com',
    role: 'user',
    createdAt: '2024-01-02T00:00:00Z',
  },
]

export const mockUser = mockUsers[0]

// Factory function
export function createMockUser(overrides = {}) {
  return {
    id: Math.random().toString(36).substr(2, 9),
    name: 'Test User',
    email: 'test@example.com',
    role: 'user',
    createdAt: new Date().toISOString(),
    ...overrides,
  }
}
```

### Utilisation des Fixtures

```typescript
// handlers.ts
import { mockUsers } from './fixtures/users'

export const handlers = [
  http.get('/api/users', () => {
    return HttpResponse.json(mockUsers)
  }),
]

// tests/users.test.tsx
import { mockUsers, createMockUser } from '@/mocks/fixtures/users'

describe('UserList', () => {
  it('affiche le bon nombre d\'utilisateurs', async () => {
    render(<UserList />)

    await waitFor(() => {
      expect(screen.getAllByRole('listitem')).toHaveLength(mockUsers.length)
    })
  })
})
```

## Mock Database (Prisma)

```typescript
// mocks/prisma.ts
import { PrismaClient } from '@prisma/client'
import { mockDeep, DeepMockProxy } from 'vitest-mock-extended'

export const prismaMock = mockDeep<PrismaClient>()

vi.mock('@/lib/db', () => ({
  db: prismaMock,
}))

// tests/users.test.ts
import { prismaMock } from '@/mocks/prisma'
import { createUser } from '@/lib/users'

describe('createUser', () => {
  it('crée un utilisateur', async () => {
    const mockUser = { id: '1', name: 'Test', email: 'test@test.com' }

    prismaMock.user.create.mockResolvedValue(mockUser)

    const result = await createUser({ name: 'Test', email: 'test@test.com' })

    expect(result).toEqual(mockUser)
    expect(prismaMock.user.create).toHaveBeenCalledWith({
      data: { name: 'Test', email: 'test@test.com' },
    })
  })
})
```

## Mock Environment Variables

```typescript
// vitest.setup.ts
vi.stubEnv('DATABASE_URL', 'postgresql://test:test@localhost:5432/test')
vi.stubEnv('NEXT_PUBLIC_API_URL', 'http://localhost:3000')

// Ou dans un test spécifique
describe('Config', () => {
  it('utilise les variables d\'env', () => {
    vi.stubEnv('API_KEY', 'test-key')
    expect(process.env.API_KEY).toBe('test-key')
  })
})
```

## Bonnes Pratiques

```
✅ MSW pour mocking réseau
✅ Fixtures réutilisables
✅ Reset des mocks entre tests
✅ Factory functions pour données dynamiques
✅ Mock au plus bas niveau possible

❌ Ne pas over-mocker (perd la valeur du test)
❌ Éviter les mocks dans les tests E2E
❌ Ne pas oublier de reset les mocks
❌ Éviter les mocks trop couplés à l'implémentation
```

## Escalades

| Situation | Action |
|-----------|--------|
| Tests unitaires | → `unit-testing.md` |
| Tests composants | → `integration-testing.md` |
| Tests E2E | → `e2e-testing.md` |
| CI/CD | → `deployment/ci-cd` |


## Livrables

| Livrable | Description |
|----------|-------------|
| Configuration mocking | Setup MSW et mocks pour Next.js |
| Mocks réutilisables | Mocks d'API et composants |
| Documentation | Guide du mocking |
