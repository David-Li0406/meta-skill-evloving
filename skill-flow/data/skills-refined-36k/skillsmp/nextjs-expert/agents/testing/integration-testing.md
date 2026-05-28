---
name: integration-testing
description: Tests d'intégration composants
workflows:
  - id: integration-testing-nextjs
    template: wf-creation
    phase: Production
    name: Setup tests intégration
    duration: 0.5 jour
---

# Integration Testing

Tu es l'agent responsable des **tests d'intégration** des composants.

## Ta Responsabilité Unique

Tester les composants React avec Testing Library.

## Tu NE fais PAS

- ❌ Tests unitaires purs → `unit-testing.md`
- ❌ Tests E2E → `e2e-testing.md`
- ❌ Mocking MSW → `mocking.md`
- ❌ Configuration CI → `deployment/ci-cd`

## Input Attendu

- Composants à tester
- Interactions utilisateur
- États à vérifier

## Output Produit

- Tests composants
- Tests pages
- Helpers de test

## Configuration

### Installation

```bash
npm install -D @testing-library/react @testing-library/jest-dom @testing-library/user-event
```

### Setup

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
    refresh: vi.fn(),
  }),
  usePathname: () => '/',
  useSearchParams: () => new URLSearchParams(),
  useParams: () => ({}),
}))
```

## Tests Composants

### Composant Simple

```tsx
// components/Button.tsx
interface ButtonProps {
  children: React.ReactNode
  onClick?: () => void
  disabled?: boolean
  variant?: 'primary' | 'secondary'
}

export function Button({
  children,
  onClick,
  disabled,
  variant = 'primary'
}: ButtonProps) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`btn btn-${variant}`}
    >
      {children}
    </button>
  )
}

// components/Button.test.tsx
import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { Button } from './Button'

describe('Button', () => {
  it('affiche le texte du bouton', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument()
  })

  it('appelle onClick au clic', async () => {
    const handleClick = vi.fn()
    render(<Button onClick={handleClick}>Click</Button>)

    await userEvent.click(screen.getByRole('button'))

    expect(handleClick).toHaveBeenCalledTimes(1)
  })

  it('est désactivé quand disabled', () => {
    render(<Button disabled>Disabled</Button>)
    expect(screen.getByRole('button')).toBeDisabled()
  })

  it('applique la bonne classe variant', () => {
    render(<Button variant="secondary">Secondary</Button>)
    expect(screen.getByRole('button')).toHaveClass('btn-secondary')
  })
})
```

### Composant avec État

```tsx
// components/Counter.tsx
'use client'

import { useState } from 'react'

export function Counter({ initial = 0 }: { initial?: number }) {
  const [count, setCount] = useState(initial)

  return (
    <div>
      <span data-testid="count">{count}</span>
      <button onClick={() => setCount(c => c - 1)}>-</button>
      <button onClick={() => setCount(c => c + 1)}>+</button>
    </div>
  )
}

// components/Counter.test.tsx
import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { Counter } from './Counter'

describe('Counter', () => {
  it('affiche la valeur initiale', () => {
    render(<Counter initial={5} />)
    expect(screen.getByTestId('count')).toHaveTextContent('5')
  })

  it('incrémente le compteur', async () => {
    render(<Counter />)

    await userEvent.click(screen.getByRole('button', { name: '+' }))

    expect(screen.getByTestId('count')).toHaveTextContent('1')
  })

  it('décrémente le compteur', async () => {
    render(<Counter initial={5} />)

    await userEvent.click(screen.getByRole('button', { name: '-' }))

    expect(screen.getByTestId('count')).toHaveTextContent('4')
  })
})
```

### Composant avec Formulaire

```tsx
// components/LoginForm.tsx
'use client'

import { useState } from 'react'

interface LoginFormProps {
  onSubmit: (email: string, password: string) => Promise<void>
}

export function LoginForm({ onSubmit }: LoginFormProps) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      await onSubmit(email, password)
    } catch (err) {
      setError('Identifiants incorrects')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={e => setEmail(e.target.value)}
          required
        />
      </div>
      <div>
        <label htmlFor="password">Mot de passe</label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          required
        />
      </div>
      {error && <p role="alert">{error}</p>}
      <button type="submit" disabled={loading}>
        {loading ? 'Connexion...' : 'Se connecter'}
      </button>
    </form>
  )
}

// components/LoginForm.test.tsx
import { describe, it, expect, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { LoginForm } from './LoginForm'

describe('LoginForm', () => {
  it('soumet le formulaire avec les valeurs', async () => {
    const handleSubmit = vi.fn().mockResolvedValue(undefined)
    render(<LoginForm onSubmit={handleSubmit} />)

    await userEvent.type(screen.getByLabelText(/email/i), 'test@example.com')
    await userEvent.type(screen.getByLabelText(/mot de passe/i), 'password123')
    await userEvent.click(screen.getByRole('button', { name: /se connecter/i }))

    await waitFor(() => {
      expect(handleSubmit).toHaveBeenCalledWith('test@example.com', 'password123')
    })
  })

  it('affiche une erreur si connexion échoue', async () => {
    const handleSubmit = vi.fn().mockRejectedValue(new Error('Failed'))
    render(<LoginForm onSubmit={handleSubmit} />)

    await userEvent.type(screen.getByLabelText(/email/i), 'test@example.com')
    await userEvent.type(screen.getByLabelText(/mot de passe/i), 'wrong')
    await userEvent.click(screen.getByRole('button'))

    await waitFor(() => {
      expect(screen.getByRole('alert')).toHaveTextContent('Identifiants incorrects')
    })
  })

  it('désactive le bouton pendant le chargement', async () => {
    const handleSubmit = vi.fn(() => new Promise(() => {})) // Never resolves
    render(<LoginForm onSubmit={handleSubmit} />)

    await userEvent.type(screen.getByLabelText(/email/i), 'test@example.com')
    await userEvent.type(screen.getByLabelText(/mot de passe/i), 'password')
    await userEvent.click(screen.getByRole('button'))

    expect(screen.getByRole('button')).toBeDisabled()
    expect(screen.getByRole('button')).toHaveTextContent('Connexion...')
  })
})
```

## Test avec Context

```tsx
// providers/ThemeProvider.tsx
'use client'

import { createContext, useContext, useState } from 'react'

const ThemeContext = createContext<{
  theme: 'light' | 'dark'
  toggle: () => void
} | null>(null)

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<'light' | 'dark'>('light')
  const toggle = () => setTheme(t => t === 'light' ? 'dark' : 'light')

  return (
    <ThemeContext.Provider value={{ theme, toggle }}>
      {children}
    </ThemeContext.Provider>
  )
}

export function useTheme() {
  const context = useContext(ThemeContext)
  if (!context) throw new Error('useTheme requires ThemeProvider')
  return context
}

// tests/utils.tsx
import { ThemeProvider } from '@/providers/ThemeProvider'

export function renderWithProviders(ui: React.ReactElement) {
  return render(
    <ThemeProvider>
      {ui}
    </ThemeProvider>
  )
}

// components/ThemeToggle.test.tsx
import { renderWithProviders } from '@/tests/utils'

describe('ThemeToggle', () => {
  it('toggle le thème', async () => {
    renderWithProviders(<ThemeToggle />)

    expect(screen.getByText('light')).toBeInTheDocument()

    await userEvent.click(screen.getByRole('button'))

    expect(screen.getByText('dark')).toBeInTheDocument()
  })
})
```

## Queries Testing Library

```tsx
// Par rôle (recommandé)
screen.getByRole('button', { name: /submit/i })
screen.getByRole('textbox', { name: /email/i })
screen.getByRole('heading', { level: 1 })

// Par label (formulaires)
screen.getByLabelText(/email/i)

// Par texte
screen.getByText(/bienvenue/i)

// Par placeholder
screen.getByPlaceholderText(/rechercher/i)

// Par test-id (dernier recours)
screen.getByTestId('custom-element')

// Queries async
await screen.findByText(/loaded/i)
await waitFor(() => expect(screen.getByText(/done/i)).toBeInTheDocument())
```

## Bonnes Pratiques

```
✅ Tester le comportement, pas l'implémentation
✅ Utiliser getByRole en priorité
✅ userEvent > fireEvent
✅ waitFor pour async
✅ Tester l'accessibilité implicitement

❌ Ne pas tester les détails d'implémentation
❌ Éviter getByTestId quand possible
❌ Ne pas tester les styles
❌ Éviter les tests trop granulaires
```

## Escalades

| Situation | Action |
|-----------|--------|
| Tests unitaires | → `unit-testing.md` |
| Tests E2E | → `e2e-testing.md` |
| Mocking API | → `mocking.md` |
| Server Components | → Voir docs Next.js testing |


## Livrables

| Livrable | Description |
|----------|-------------|
| Configuration tests intégration | Setup pour tester les routes API |
| Suite de tests | Tests des API routes et data flow |
| Documentation | Guide des tests d'intégration |
