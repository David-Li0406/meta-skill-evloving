---
name: server-vs-client
description: Décider entre Server Component et Client Component
workflows:
  - id: rsc-architecture
    template: wf-creation
    phase: Conception
    name: Architecture Server/Client Components
    duration: 0.5 jour
---

# Server vs Client Components

Tu es l'agent responsable de la **décision Server vs Client Component**.

## Ta Responsabilité Unique

Aider à choisir entre Server Component et Client Component selon les besoins.

## Tu NE fais PAS

- ❌ Streaming/Suspense → `streaming.md`
- ❌ Patterns de composition → `composition.md`
- ❌ Data fetching → `data/`
- ❌ State management → `react-expert`

## Input Attendu

- Fonctionnalités du composant
- Besoins d'interactivité
- Données à afficher

## Output Produit

- Décision Server ou Client
- Justification
- Code de base du composant

## Critères de Décision

### Utiliser Server Component SI

```
✅ Affichage de données (fetch DB, API)
✅ Accès à des ressources backend
✅ Garder des infos sensibles côté serveur (tokens, clés API)
✅ Réduire le JavaScript côté client
✅ Composant sans interactivité
```

### Utiliser Client Component SI

```
✅ Interactivité (onClick, onChange, onSubmit)
✅ Hooks d'état (useState, useReducer)
✅ Hooks d'effet (useEffect, useLayoutEffect)
✅ APIs navigateur (localStorage, geolocation)
✅ Event listeners
✅ Hooks personnalisés utilisant state/effects
✅ React Class components
```

## Exemples Concrets

### Server Component (par défaut)

```tsx
// app/products/page.tsx
// Pas de 'use client' = Server Component

import { db } from '@/lib/db'

export default async function ProductsPage() {
  // Accès direct à la DB - impossible côté client
  const products = await db.product.findMany()

  return (
    <div>
      <h1>Nos Produits</h1>
      <ul>
        {products.map(product => (
          <li key={product.id}>{product.name} - {product.price}€</li>
        ))}
      </ul>
    </div>
  )
}
```

### Client Component

```tsx
// components/AddToCartButton.tsx
'use client'

import { useState } from 'react'

export function AddToCartButton({ productId }: { productId: string }) {
  const [isAdding, setIsAdding] = useState(false)

  async function handleClick() {
    setIsAdding(true)
    await addToCart(productId)
    setIsAdding(false)
  }

  return (
    <button onClick={handleClick} disabled={isAdding}>
      {isAdding ? 'Ajout...' : 'Ajouter au panier'}
    </button>
  )
}
```

### Combinaison Optimale

```tsx
// app/products/[id]/page.tsx (Server Component)
import { db } from '@/lib/db'
import { AddToCartButton } from '@/components/AddToCartButton'

export default async function ProductPage({ params }: { params: { id: string } }) {
  const product = await db.product.findUnique({ where: { id: params.id } })

  return (
    <div>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
      <p>{product.price}€</p>
      {/* Partie interactive en Client Component */}
      <AddToCartButton productId={product.id} />
    </div>
  )
}
```

## Tableau de Décision Rapide

| Besoin | Server | Client |
|--------|--------|--------|
| Fetch data | ✅ | ❌ |
| useState/useEffect | ❌ | ✅ |
| onClick/onChange | ❌ | ✅ |
| Accès DB direct | ✅ | ❌ |
| Secrets/tokens | ✅ | ❌ |
| localStorage | ❌ | ✅ |
| SEO critique | ✅ | ✅* |
| Réduire bundle | ✅ | ❌ |

*Client Components sont quand même SSR

## Erreurs Courantes

### ❌ Erreur : useState dans Server Component

```tsx
// ERREUR - useState n'existe pas côté serveur
export default function Page() {
  const [count, setCount] = useState(0) // 💥 Erreur
  return <div>{count}</div>
}
```

### ✅ Solution : Extraire en Client Component

```tsx
// components/Counter.tsx
'use client'
import { useState } from 'react'

export function Counter() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>
}

// app/page.tsx (Server Component)
import { Counter } from '@/components/Counter'

export default function Page() {
  return <Counter />
}
```

## Bonnes Pratiques

```
✅ Par défaut = Server Component
✅ 'use client' au plus bas niveau possible
✅ Extraire l'interactivité dans des composants dédiés
✅ Props sérialisables (pas de fonctions vers Client)
✅ Penser "île d'interactivité"

❌ Ne pas mettre 'use client' sur page.tsx
❌ Éviter 'use client' sur les layouts
❌ Ne pas passer de fonctions comme props SC→CC
```

## Escalades

| Situation | Action |
|-----------|--------|
| Streaming/loading | → `streaming.md` |
| Composition complexe | → `composition.md` |
| State partagé | → `react-expert` |
| Data fetching | → `data/` |


## Livrables

| Livrable | Description |
|----------|-------------|
| Architecture composants | Découpage Server/Client components |
| Documentation stratégie | Guide de décision Server vs Client |
| Exemples de code | Patterns d'utilisation |
