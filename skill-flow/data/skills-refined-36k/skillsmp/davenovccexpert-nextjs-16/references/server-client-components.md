<overview>
Server and Client Components in Next.js 16. Server Components are the default. Add `'use client'` only when needed.
</overview>

<decision_tree>
**When to use Server Component (default):**
- Fetch data
- Access backend resources directly
- Keep sensitive information on server (tokens, API keys)
- Reduce client-side JavaScript
- Display static or semi-static content

**When to use Client Component (`'use client'`):**
- Use `useState`, `useEffect`, `useReducer`, `useContext`
- Use browser APIs (`window`, `document`, `localStorage`)
- Add event listeners (`onClick`, `onChange`, `onSubmit`)
- Use custom hooks that depend on state or effects
- Use class components
</decision_tree>

<patterns>
<pattern name="server-fetch-client-interact">
**Pattern: Fetch in Server, Interact in Client**

```tsx
// app/products/page.tsx (Server Component)
import { AddToCartButton } from '@/components/AddToCartButton'

async function getProducts() {
  const res = await fetch('https://api.example.com/products')
  return res.json()
}

export default async function ProductsPage() {
  const products = await getProducts()

  return (
    <ul>
      {products.map(product => (
        <li key={product.id}>
          <h2>{product.name}</h2>
          <p>${product.price}</p>
          {/* Only the button needs to be a Client Component */}
          <AddToCartButton productId={product.id} />
        </li>
      ))}
    </ul>
  )
}

// components/AddToCartButton.tsx (Client Component)
'use client'

import { useState } from 'react'

export function AddToCartButton({ productId }: { productId: string }) {
  const [adding, setAdding] = useState(false)

  async function handleClick() {
    setAdding(true)
    await addToCart(productId)
    setAdding(false)
  }

  return (
    <button onClick={handleClick} disabled={adding}>
      {adding ? 'Adding...' : 'Add to Cart'}
    </button>
  )
}
```
</pattern>

<pattern name="composition">
**Pattern: Composing Server and Client Components**

Server Components can import Client Components.
Client Components can render Server Components passed as children/props.

```tsx
// ServerWrapper.tsx (Server Component)
import ClientComponent from './ClientComponent'
import ServerChild from './ServerChild'

export default function ServerWrapper() {
  return (
    <ClientComponent>
      {/* Server Component passed as children */}
      <ServerChild />
    </ClientComponent>
  )
}

// ClientComponent.tsx (Client Component)
'use client'

export default function ClientComponent({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div onClick={() => console.log('clicked')}>
      {/* Server Component renders here */}
      {children}
    </div>
  )
}
```
</pattern>

<pattern name="client-boundary">
**Pattern: Push Client Boundary Down**

Move `'use client'` as low in the component tree as possible.

```tsx
// BAD - entire page is client
'use client'

export default function Page() {
  const [count, setCount] = useState(0)

  return (
    <div>
      <Header />           {/* Now client, but doesn't need to be */}
      <Sidebar />          {/* Now client, but doesn't need to be */}
      <button onClick={() => setCount(c => c + 1)}>{count}</button>
    </div>
  )
}

// GOOD - only counter is client
export default function Page() {
  return (
    <div>
      <Header />           {/* Server Component */}
      <Sidebar />          {/* Server Component */}
      <Counter />          {/* Client Component - only interactive part */}
    </div>
  )
}

// Counter.tsx
'use client'
export function Counter() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>
}
```
</pattern>

<pattern name="context-provider">
**Pattern: Context Providers**

Create a provider component marked as client, wrap app in layout.

```tsx
// providers/ThemeProvider.tsx
'use client'

import { createContext, useContext, useState } from 'react'

const ThemeContext = createContext<{
  theme: string
  setTheme: (theme: string) => void
} | null>(null)

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState('light')

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
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
          {children}
        </ThemeProvider>
      </body>
    </html>
  )
}
```
</pattern>
</patterns>

<serialization>
**Data passed from Server to Client must be serializable:**

**Allowed:**
- Primitives (string, number, boolean, null, undefined)
- Arrays and objects containing serializable values
- Date (converted to string)
- Map, Set (converted to array)
- Server Actions (special handling)

**NOT allowed:**
- Functions (except Server Actions)
- Classes/instances
- Symbols
- Circular references

```tsx
// BAD - function not serializable
<ClientComponent onSubmit={(data) => saveData(data)} />

// GOOD - pass Server Action
<ClientComponent onSubmit={saveData} />  // Server Action is serializable
```
</serialization>

<anti_patterns>
<anti_pattern name="use-client-everywhere">
**Problem:** Adding `'use client'` to every file

**Why it's bad:**
- Increases client bundle size
- Loses benefits of Server Components
- More JavaScript to download/parse

**Fix:** Only add `'use client'` where interactivity is needed
</anti_pattern>

<anti_pattern name="fetch-in-client">
**Problem:** Fetching data in Client Components

```tsx
'use client'
export function Products() {
  const [products, setProducts] = useState([])

  useEffect(() => {
    fetch('/api/products')
      .then(res => res.json())
      .then(setProducts)
  }, [])

  return <ul>{...}</ul>
}
```

**Why it's bad:**
- Creates waterfall (page loads → JS loads → fetch starts)
- Exposes API to client
- More client-side code

**Fix:** Fetch in Server Component

```tsx
// Server Component
export default async function Products() {
  const products = await getProducts()  // Runs on server
  return <ul>{...}</ul>
}
```
</anti_pattern>

<anti_pattern name="hooks-in-server">
**Problem:** Using hooks in Server Components

```tsx
// Server Component (no 'use client')
export default function Page() {
  const [state, setState] = useState()  // ERROR!
  return <div>...</div>
}
```

**Fix:** Move to Client Component or restructure
</anti_pattern>
</anti_patterns>

<hydration_errors>
**Common causes of hydration mismatch:**

1. **Browser-only values:**
```tsx
// BAD
function Component() {
  return <div>{window.innerWidth}</div>  // undefined on server
}

// GOOD
'use client'
function Component() {
  const [width, setWidth] = useState(0)
  useEffect(() => setWidth(window.innerWidth), [])
  return <div>{width}</div>
}
```

2. **Date/time:**
```tsx
// BAD - different on server vs client
<span>{new Date().toLocaleString()}</span>

// GOOD - suppress warning or use client component
<span suppressHydrationWarning>{new Date().toLocaleString()}</span>
```

3. **Random values:**
```tsx
// BAD
<div key={Math.random()}>...</div>

// GOOD - use stable IDs
<div key={item.id}>...</div>
```

4. **Browser extensions modifying DOM:**
Use `suppressHydrationWarning` on affected elements
</hydration_errors>
