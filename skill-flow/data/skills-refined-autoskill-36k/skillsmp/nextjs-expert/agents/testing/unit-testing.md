---
name: unit-testing
description: Tests unitaires avec Vitest/Jest
workflows:
  - id: unit-testing-nextjs
    template: wf-creation
    phase: Production
    name: Setup tests unitaires
    duration: 0.5 jour
---

# Unit Testing

Tu es l'agent responsable des **tests unitaires** dans Next.js.

## Ta Responsabilité Unique

Configurer et écrire des tests unitaires avec Vitest ou Jest.

## Tu NE fais PAS

- ❌ Tests composants → `integration-testing.md`
- ❌ Tests E2E → `e2e-testing.md`
- ❌ Mocking avancé → `mocking.md`
- ❌ CI/CD → `deployment/ci-cd`

## Input Attendu

- Code à tester (utils, hooks, logique)
- Cas de test
- Couverture souhaitée

## Output Produit

- Configuration Vitest/Jest
- Tests unitaires
- Scripts npm

## Configuration Vitest

### Installation

```bash
npm install -D vitest @vitejs/plugin-react
```

### vitest.config.ts

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./vitest.setup.ts'],
    include: ['**/*.{test,spec}.{js,ts,jsx,tsx}'],
    exclude: ['node_modules', '.next', 'e2e'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html'],
      exclude: ['node_modules', '.next'],
    },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './'),
    },
  },
})
```

### vitest.setup.ts

```typescript
// vitest.setup.ts
import '@testing-library/jest-dom'
import { vi } from 'vitest'

// Mock next/navigation
vi.mock('next/navigation', () => ({
  useRouter: () => ({
    push: vi.fn(),
    replace: vi.fn(),
    back: vi.fn(),
    forward: vi.fn(),
    refresh: vi.fn(),
    prefetch: vi.fn(),
  }),
  usePathname: () => '/',
  useSearchParams: () => new URLSearchParams(),
}))

// Mock next/image
vi.mock('next/image', () => ({
  default: (props: any) => <img {...props} />,
}))
```

## Scripts package.json

```json
{
  "scripts": {
    "test": "vitest",
    "test:run": "vitest run",
    "test:watch": "vitest watch",
    "test:coverage": "vitest run --coverage",
    "test:ui": "vitest --ui"
  }
}
```

## Tests Fonctions Utilitaires

### Utils Basiques

```typescript
// lib/utils.ts
export function formatPrice(price: number): string {
  return new Intl.NumberFormat('fr-FR', {
    style: 'currency',
    currency: 'EUR',
  }).format(price)
}

export function slugify(text: string): string {
  return text
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '')
}

// lib/utils.test.ts
import { describe, it, expect } from 'vitest'
import { formatPrice, slugify } from './utils'

describe('formatPrice', () => {
  it('formate un prix en euros', () => {
    expect(formatPrice(1234.56)).toBe('1 234,56 €')
  })

  it('gère les prix à zéro', () => {
    expect(formatPrice(0)).toBe('0,00 €')
  })
})

describe('slugify', () => {
  it('convertit en slug', () => {
    expect(slugify('Hello World')).toBe('hello-world')
  })

  it('gère les accents', () => {
    expect(slugify('Café Crème')).toBe('cafe-creme')
  })

  it('supprime les caractères spéciaux', () => {
    expect(slugify('Hello! @World#')).toBe('hello-world')
  })
})
```

### Fonctions Async

```typescript
// lib/api.ts
export async function fetchUser(id: string) {
  const res = await fetch(`/api/users/${id}`)
  if (!res.ok) throw new Error('User not found')
  return res.json()
}

// lib/api.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { fetchUser } from './api'

describe('fetchUser', () => {
  beforeEach(() => {
    vi.resetAllMocks()
  })

  it('retourne les données utilisateur', async () => {
    const mockUser = { id: '1', name: 'John' }

    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockUser),
    })

    const user = await fetchUser('1')

    expect(fetch).toHaveBeenCalledWith('/api/users/1')
    expect(user).toEqual(mockUser)
  })

  it('throw si utilisateur non trouvé', async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: false,
    })

    await expect(fetchUser('999')).rejects.toThrow('User not found')
  })
})
```

## Tests Custom Hooks

```typescript
// hooks/useCounter.ts
import { useState, useCallback } from 'react'

export function useCounter(initial = 0) {
  const [count, setCount] = useState(initial)

  const increment = useCallback(() => setCount(c => c + 1), [])
  const decrement = useCallback(() => setCount(c => c - 1), [])
  const reset = useCallback(() => setCount(initial), [initial])

  return { count, increment, decrement, reset }
}

// hooks/useCounter.test.ts
import { describe, it, expect } from 'vitest'
import { renderHook, act } from '@testing-library/react'
import { useCounter } from './useCounter'

describe('useCounter', () => {
  it('initialise avec la valeur par défaut', () => {
    const { result } = renderHook(() => useCounter())
    expect(result.current.count).toBe(0)
  })

  it('initialise avec une valeur custom', () => {
    const { result } = renderHook(() => useCounter(10))
    expect(result.current.count).toBe(10)
  })

  it('incrémente le compteur', () => {
    const { result } = renderHook(() => useCounter())

    act(() => {
      result.current.increment()
    })

    expect(result.current.count).toBe(1)
  })

  it('décrémente le compteur', () => {
    const { result } = renderHook(() => useCounter(5))

    act(() => {
      result.current.decrement()
    })

    expect(result.current.count).toBe(4)
  })

  it('reset le compteur', () => {
    const { result } = renderHook(() => useCounter(5))

    act(() => {
      result.current.increment()
      result.current.increment()
      result.current.reset()
    })

    expect(result.current.count).toBe(5)
  })
})
```

## Tests Validation

```typescript
// lib/validation.ts
import { z } from 'zod'

export const userSchema = z.object({
  name: z.string().min(2, 'Nom trop court'),
  email: z.string().email('Email invalide'),
  age: z.number().min(18, 'Doit être majeur'),
})

export function validateUser(data: unknown) {
  return userSchema.safeParse(data)
}

// lib/validation.test.ts
import { describe, it, expect } from 'vitest'
import { validateUser } from './validation'

describe('validateUser', () => {
  it('valide un utilisateur correct', () => {
    const result = validateUser({
      name: 'John Doe',
      email: 'john@example.com',
      age: 25,
    })

    expect(result.success).toBe(true)
  })

  it('rejette un email invalide', () => {
    const result = validateUser({
      name: 'John',
      email: 'not-an-email',
      age: 25,
    })

    expect(result.success).toBe(false)
    if (!result.success) {
      expect(result.error.issues[0].message).toBe('Email invalide')
    }
  })

  it('rejette un mineur', () => {
    const result = validateUser({
      name: 'John',
      email: 'john@example.com',
      age: 16,
    })

    expect(result.success).toBe(false)
  })
})
```

## Patterns de Test

### Table-Driven Tests

```typescript
describe('slugify', () => {
  const cases = [
    ['Hello World', 'hello-world'],
    ['Café Crème', 'cafe-creme'],
    ['  Spaced  ', 'spaced'],
    ['123 Numbers', '123-numbers'],
  ]

  it.each(cases)('slugify("%s") === "%s"', (input, expected) => {
    expect(slugify(input)).toBe(expected)
  })
})
```

### Snapshot Testing

```typescript
import { describe, it, expect } from 'vitest'

describe('generateConfig', () => {
  it('génère une config valide', () => {
    const config = generateConfig({ env: 'production' })
    expect(config).toMatchSnapshot()
  })
})
```

## Bonnes Pratiques

```
✅ Un test = un comportement
✅ Noms descriptifs (should... when...)
✅ Arrange-Act-Assert pattern
✅ Tester les edge cases
✅ Isolation des tests (pas d'état partagé)

❌ Ne pas tester l'implémentation
❌ Éviter les tests trop couplés
❌ Ne pas ignorer les tests qui échouent
❌ Éviter les mocks excessifs
```

## Escalades

| Situation | Action |
|-----------|--------|
| Tests composants | → `integration-testing.md` |
| Tests E2E | → `e2e-testing.md` |
| Mocking complexe | → `mocking.md` |
| CI/CD | → `deployment/ci-cd` |


## Livrables

| Livrable | Description |
|----------|-------------|
| Configuration tests unitaires | Setup Jest/Vitest pour Next.js |
| Suite de tests | Tests des composants et utils |
| Documentation testing | Guide des tests unitaires |
