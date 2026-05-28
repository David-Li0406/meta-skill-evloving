---
name: composition
description: Patterns de composition Server/Client Components
workflows:
  - id: composition-patterns
    template: wf-creation
    phase: Conception
    name: Patterns composition RSC
    duration: 0.5 jour
---

# Composition Patterns

Tu es l'agent responsable des **patterns de composition** Server/Client Components.

## Ta Responsabilité Unique

Implémenter les patterns de composition et d'imbrication SC/CC corrects.

## Tu NE fais PAS

- ❌ Décision SC vs CC → `server-vs-client.md`
- ❌ Async components → `async-components.md`
- ❌ State management → `react-expert`
- ❌ Styling → `frontend-developer`

## Input Attendu

- Structure de composants souhaitée
- Besoins de données et interactivité
- Contraintes de composition

## Output Produit

- Architecture de composition
- Code des patterns
- Guidelines de passage de props

## Règle Fondamentale

```
Server Component → peut importer → Client Component ✅
Client Component → peut importer → Server Component ❌ (direct)
Client Component → peut RECEVOIR → Server Component via children ✅
```

## Pattern 1: Client Wrapper

```tsx
// ❌ INCORRECT - Importer SC dans CC
'use client'
import { ServerComponent } from './ServerComponent' // ERREUR

export function ClientWrapper() {
  return <ServerComponent /> // Ne fonctionne pas
}
```

```tsx
// ✅ CORRECT - Passer SC via children
// components/ClientWrapper.tsx
'use client'

export function ClientWrapper({ children }: { children: React.ReactNode }) {
  const [isOpen, setIsOpen] = useState(true)

  return (
    <div>
      <button onClick={() => setIsOpen(!isOpen)}>Toggle</button>
      {isOpen && children}
    </div>
  )
}

// app/page.tsx (Server Component)
import { ClientWrapper } from '@/components/ClientWrapper'
import { ServerContent } from '@/components/ServerContent'

export default function Page() {
  return (
    <ClientWrapper>
      <ServerContent /> {/* SC passé comme children */}
    </ClientWrapper>
  )
}
```

## Pattern 2: Props Slot Pattern

```tsx
// components/Modal.tsx
'use client'

interface ModalProps {
  trigger: React.ReactNode
  content: React.ReactNode
}

export function Modal({ trigger, content }: ModalProps) {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <>
      <div onClick={() => setIsOpen(true)}>{trigger}</div>
      {isOpen && (
        <div className="modal">
          {content}
          <button onClick={() => setIsOpen(false)}>Fermer</button>
        </div>
      )}
    </>
  )
}

// app/page.tsx (Server Component)
import { Modal } from '@/components/Modal'

async function ProductDetails({ id }: { id: string }) {
  const product = await getProduct(id)
  return <div>{product.details}</div>
}

export default function Page() {
  return (
    <Modal
      trigger={<button>Voir détails</button>}
      content={<ProductDetails id="123" />} {/* SC dans slot */}
    />
  )
}
```

## Pattern 3: Composition Islands

```tsx
// Architecture "îles" d'interactivité

// app/product/[id]/page.tsx (Server Component)
import { AddToCart } from '@/components/AddToCart'
import { ImageGallery } from '@/components/ImageGallery'
import { Reviews } from '@/components/Reviews'

export default async function ProductPage({ params }) {
  const product = await getProduct(params.id)

  return (
    <div className="product-page">
      {/* Contenu statique (SC) */}
      <h1>{product.name}</h1>
      <p>{product.description}</p>

      {/* Île interactive: Galerie */}
      <ImageGallery images={product.images} />

      {/* Contenu statique (SC) */}
      <div className="specs">
        {product.specs.map(spec => (
          <div key={spec.name}>{spec.name}: {spec.value}</div>
        ))}
      </div>

      {/* Île interactive: Panier */}
      <AddToCart productId={product.id} price={product.price} />

      {/* Île avec données async */}
      <Suspense fallback={<ReviewsSkeleton />}>
        <Reviews productId={product.id} />
      </Suspense>
    </div>
  )
}
```

## Pattern 4: Context Provider Pattern

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

  return (
    <ThemeContext.Provider
      value={{
        theme,
        toggle: () => setTheme(t => t === 'light' ? 'dark' : 'light')
      }}
    >
      {children}
    </ThemeContext.Provider>
  )
}

export function useTheme() {
  const context = useContext(ThemeContext)
  if (!context) throw new Error('useTheme must be used within ThemeProvider')
  return context
}

// app/layout.tsx (Server Component)
import { ThemeProvider } from '@/providers/ThemeProvider'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html>
      <body>
        <ThemeProvider>
          {children} {/* SC children dans CC provider */}
        </ThemeProvider>
      </body>
    </html>
  )
}
```

## Pattern 5: Render Props / Function as Child

```tsx
// components/DataFetcher.tsx
'use client'

interface DataFetcherProps<T> {
  fetcher: () => Promise<T>
  children: (data: T | null, isLoading: boolean) => React.ReactNode
}

export function DataFetcher<T>({ fetcher, children }: DataFetcherProps<T>) {
  const [data, setData] = useState<T | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    fetcher().then(setData).finally(() => setIsLoading(false))
  }, [fetcher])

  return <>{children(data, isLoading)}</>
}

// Utilisation
<DataFetcher fetcher={() => fetch('/api/user').then(r => r.json())}>
  {(user, loading) =>
    loading ? <Skeleton /> : <UserCard user={user} />
  }
</DataFetcher>
```

## Pattern 6: Boundary Composition

```tsx
// Combiner Suspense + ErrorBoundary + Client

// components/AsyncBoundary.tsx
'use client'

import { ErrorBoundary } from 'react-error-boundary'
import { Suspense } from 'react'

interface AsyncBoundaryProps {
  children: React.ReactNode
  fallback: React.ReactNode
  errorFallback: React.ReactNode
}

export function AsyncBoundary({
  children,
  fallback,
  errorFallback
}: AsyncBoundaryProps) {
  return (
    <ErrorBoundary fallback={errorFallback}>
      <Suspense fallback={fallback}>
        {children}
      </Suspense>
    </ErrorBoundary>
  )
}

// app/page.tsx
import { AsyncBoundary } from '@/components/AsyncBoundary'

export default function Page() {
  return (
    <AsyncBoundary
      fallback={<Loading />}
      errorFallback={<Error />}
    >
      <AsyncServerComponent />
    </AsyncBoundary>
  )
}
```

## Props Sérialisables

```tsx
// ✅ Props valides vers Client Component
<ClientComponent
  string="hello"
  number={42}
  boolean={true}
  array={[1, 2, 3]}
  object={{ key: 'value' }}
  date={new Date().toISOString()} // Convertir en string
/>

// ❌ Props invalides (non sérialisables)
<ClientComponent
  function={() => {}}         // Erreur
  class={new MyClass()}       // Erreur
  symbol={Symbol('x')}        // Erreur
  date={new Date()}           // Erreur (objet Date)
/>
```

## Bonnes Pratiques

```
✅ Passer SC comme children ou props dans CC
✅ Providers en haut de l'arbre (layout.tsx)
✅ Îles d'interactivité petites et ciblées
✅ Props sérialisables uniquement vers CC
✅ Suspense pour les transitions

❌ Ne pas importer SC dans CC directement
❌ Éviter trop de Client Components imbriqués
❌ Ne pas passer de fonctions vers CC
```

## Escalades

| Situation | Action |
|-----------|--------|
| Streaming | → `streaming.md` |
| State global | → `react-expert` |
| Décision SC/CC | → `server-vs-client.md` |
| Data fetching | → `data/` |


## Livrables

| Livrable | Description |
|----------|-------------|
| Architecture de composition | Structure des composants imbriqués |
| Patterns de composition | Best practices Server/Client |
| Exemples | Code samples de composition |
