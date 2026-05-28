# Conventions de Code

Ce document définit les standards de code à respecter dans tous les projets. Ces conventions garantissent la lisibilité, la maintenabilité et la cohérence du code.

---

## Table des Matières

1. [Principes Généraux](#principes-généraux)
2. [Nommage](#nommage)
3. [Structure des Fichiers](#structure-des-fichiers)
4. [TypeScript](#typescript)
5. [React/Vue (Composants)](#composants-frontend)
6. [CSS/Styles](#cssstyles)
7. [Tests](#tests)
8. [Commentaires](#commentaires)
9. [Git](#git)

---

## Principes Généraux

### KISS - Keep It Simple, Stupid
- Privilégier la simplicité à la complexité
- Une fonction = une responsabilité
- Éviter l'over-engineering

### DRY - Don't Repeat Yourself
- Factoriser le code dupliqué (mais pas prématurément)
- Créer des abstractions quand 3+ occurrences

### YAGNI - You Aren't Gonna Need It
- Ne pas coder pour des besoins futurs hypothétiques
- Implémenter uniquement ce qui est demandé

---

## Nommage

### Règles Générales

| Type | Convention | Exemple |
|------|------------|---------|
| Variables | camelCase | `userName`, `isActive` |
| Constantes | UPPER_SNAKE_CASE | `MAX_RETRIES`, `API_URL` |
| Fonctions | camelCase, verbe | `getUserById`, `validateEmail` |
| Classes | PascalCase | `UserService`, `PaymentGateway` |
| Interfaces | PascalCase | `UserData`, `ApiResponse` |
| Types | PascalCase | `UserId`, `Status` |
| Fichiers | kebab-case ou PascalCase | `user-service.ts`, `Button.tsx` |
| Dossiers | kebab-case | `user-management`, `api-clients` |

### Noms Significatifs

```typescript
// ❌ Mauvais
const d = new Date();
const u = users.filter(x => x.active);
function process(data) { }

// ✅ Bon
const currentDate = new Date();
const activeUsers = users.filter(user => user.isActive);
function processPayment(paymentData: PaymentData) { }
```

### Préfixes/Suffixes Standards

| Pattern | Usage | Exemple |
|---------|-------|---------|
| `is`, `has`, `can`, `should` | Booléens | `isVisible`, `hasPermission` |
| `get`, `fetch`, `load` | Récupération de données | `getUser`, `fetchProducts` |
| `set`, `update`, `save` | Modification | `setStatus`, `updateProfile` |
| `create`, `add`, `insert` | Création | `createOrder`, `addItem` |
| `delete`, `remove`, `clear` | Suppression | `deleteUser`, `removeItem` |
| `handle`, `on` | Event handlers | `handleClick`, `onSubmit` |
| `use` | React hooks | `useAuth`, `useLocalStorage` |

---

## Structure des Fichiers

### Organisation d'un Module

```
feature/
├── index.ts              # Export public
├── Feature.tsx           # Composant principal
├── Feature.test.tsx      # Tests
├── Feature.styles.ts     # Styles (si applicable)
├── types.ts              # Types locaux
├── hooks/                # Hooks custom
│   └── useFeature.ts
├── components/           # Sous-composants
│   └── FeatureItem.tsx
└── utils/                # Utilitaires locaux
    └── helpers.ts
```

### Ordre des Imports

```typescript
// 1. Modules externes (node_modules)
import React from 'react';
import { useQuery } from '@tanstack/react-query';

// 2. Alias internes (@/)
import { Button } from '@/components';
import { useAuth } from '@/hooks';

// 3. Imports relatifs (parents)
import { Layout } from '../Layout';

// 4. Imports relatifs (même niveau/enfants)
import { FeatureItem } from './components';
import { useFeature } from './hooks';
import type { FeatureProps } from './types';
```

### Ordre dans un Fichier

```typescript
// 1. Imports
// 2. Types/Interfaces
// 3. Constantes
// 4. Helpers locaux (non exportés)
// 5. Composant/Classe principal(e)
// 6. Exports
```

---

## TypeScript

### Types vs Interfaces

```typescript
// ✅ Interface pour les objets et l'extension
interface User {
  id: string;
  name: string;
}

interface Admin extends User {
  permissions: string[];
}

// ✅ Type pour les unions, intersections, et types primitifs
type Status = 'pending' | 'active' | 'inactive';
type UserId = string;
type UserWithMeta = User & { createdAt: Date };
```

### Éviter `any`

```typescript
// ❌ Mauvais
function processData(data: any) { }

// ✅ Bon - Type explicite
function processData(data: UserData) { }

// ✅ Bon - Generic quand le type est vraiment inconnu
function processData<T>(data: T) { }

// ✅ Acceptable - unknown pour les données externes
function parseJson(json: string): unknown { }
```

### Types Utilitaires

```typescript
// Partial - Tous les champs optionnels
type UpdateUser = Partial<User>;

// Pick - Sélection de champs
type UserPreview = Pick<User, 'id' | 'name'>;

// Omit - Exclusion de champs
type CreateUser = Omit<User, 'id'>;

// Record - Map de types
type UserMap = Record<string, User>;

// ReturnType - Type de retour d'une fonction
type ApiResult = ReturnType<typeof fetchUser>;
```

---

## Composants Frontend

### Structure d'un Composant

```tsx
// 1. Imports
import { useState } from 'react';
import type { ButtonProps } from './types';

// 2. Types
interface Props extends ButtonProps {
  variant?: 'primary' | 'secondary';
}

// 3. Composant
export function Button({ children, variant = 'primary', onClick }: Props) {
  const [isLoading, setIsLoading] = useState(false);

  // Handlers
  const handleClick = () => {
    setIsLoading(true);
    onClick?.();
  };

  // Render
  return (
    <button
      className={`btn btn--${variant}`}
      onClick={handleClick}
      disabled={isLoading}
    >
      {isLoading ? 'Loading...' : children}
    </button>
  );
}
```

### Bonnes Pratiques

```tsx
// ✅ Props destructurées
function Card({ title, children }: CardProps) { }

// ✅ Valeurs par défaut dans la signature
function Button({ size = 'medium' }: ButtonProps) { }

// ✅ Composants petits et focalisés
// Un composant = une responsabilité

// ❌ Éviter les composants géants (> 200 lignes)
// Découper en sous-composants
```

---

## CSS/Styles

### Conventions de Nommage (BEM)

```css
/* Block */
.card { }

/* Element */
.card__header { }
.card__body { }
.card__footer { }

/* Modifier */
.card--featured { }
.card--compact { }
```

### Utility-First (Tailwind)

```tsx
// ✅ Classes utilitaires pour le styling rapide
<button className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
  Click
</button>

// ✅ Extraction en composant si répétition
<Button variant="primary">Click</Button>
```

### CSS-in-JS

```typescript
// ✅ Styles co-localisés avec le composant
const styles = {
  container: css`
    display: flex;
    gap: 1rem;
  `,
};
```

---

## Tests

### Nommage des Tests

```typescript
// ✅ Format: describe what, not how
describe('UserService', () => {
  describe('getById', () => {
    it('returns user when found', () => { });
    it('throws NotFoundError when user does not exist', () => { });
    it('handles database connection errors', () => { });
  });
});
```

### Structure AAA

```typescript
it('calculates total with discount', () => {
  // Arrange
  const cart = createCart([
    { price: 100, quantity: 2 },
  ]);
  const discount = 0.1;

  // Act
  const total = calculateTotal(cart, discount);

  // Assert
  expect(total).toBe(180);
});
```

### Bonnes Pratiques

```typescript
// ✅ Un concept par test
it('validates email format', () => { });
it('rejects empty email', () => { });

// ❌ Plusieurs assertions non liées
it('validates email', () => {
  expect(validate('')).toBe(false);
  expect(validate('invalid')).toBe(false);
  expect(validate('valid@email.com')).toBe(true);
  // Difficile de savoir quel cas échoue
});
```

---

## Commentaires

### Quand Commenter

```typescript
// ✅ Expliquer le POURQUOI, pas le QUOI
// We use a 5 second timeout because the payment provider
// occasionally has latency spikes up to 4 seconds
const PAYMENT_TIMEOUT = 5000;

// ✅ Documenter les edge cases non évidents
// Returns null for anonymous users (not logged in)
function getCurrentUserId(): string | null { }

// ❌ Commentaire inutile (le code est explicite)
// Increment counter
counter++;
```

### JSDoc pour les APIs Publiques

```typescript
/**
 * Fetches a user by their unique identifier.
 *
 * @param id - The user's unique identifier
 * @returns The user object if found
 * @throws {NotFoundError} If no user exists with the given ID
 *
 * @example
 * const user = await getUserById('user_123');
 * console.log(user.name);
 */
export async function getUserById(id: string): Promise<User> {
  // ...
}
```

### TODO/FIXME

```typescript
// TODO: Implement caching (see issue #123)
// FIXME: Race condition when concurrent requests (issue #456)
// HACK: Temporary workaround for library bug (remove after v2.0)
```

---

## Git

### Messages de Commit

```bash
# Format
<type>(<scope>): <description>

[optional body]

[optional footer]

# Exemples
feat(auth): add password reset functionality
fix(cart): resolve race condition on quantity update
docs(api): update authentication examples
refactor(user): extract validation logic to separate module
```

### Types de Commit

| Type | Description |
|------|-------------|
| `feat` | Nouvelle fonctionnalité |
| `fix` | Correction de bug |
| `docs` | Documentation |
| `style` | Formatage (pas de changement de logique) |
| `refactor` | Refactoring |
| `perf` | Amélioration de performance |
| `test` | Ajout/modification de tests |
| `build` | Système de build, dépendances |
| `ci` | Configuration CI/CD |
| `chore` | Maintenance |
| `revert` | Revert un commit |

---

## Checklist Rapide

Avant chaque commit, vérifiez :

- [ ] Noms de variables/fonctions explicites
- [ ] Pas de code dupliqué
- [ ] Types corrects (pas de `any`)
- [ ] Pas de `console.log` oubliés
- [ ] Tests écrits et passent
- [ ] Linter passe
- [ ] Commit message respecte les conventions

---

**Ces conventions sont là pour nous aider, pas pour nous bloquer. En cas de doute, discutez avec l'équipe.**
