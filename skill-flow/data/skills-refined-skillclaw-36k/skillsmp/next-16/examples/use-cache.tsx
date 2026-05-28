import React, { type ReactNode } from 'react'
import { cacheLife, cacheTag } from 'next/cache'

// ============================================
// PASS-THROUGH PATTERN (children, actions)
// ============================================

// ✅ Correct: Accept children, don't introspect them
async function CachedLayout({ children }: { children: ReactNode }) {
  'use cache'
  cacheLife('hours')

  const navigation = await fetchNavigation()

  return (
    <div>
      <nav>{navigation.map(n => <a key={n.href} href={n.href}>{n.label}</a>)}</nav>
      {children} {/* Pass through unchanged */}
    </div>
  )
}

// ✅ Correct: Pass server action through without calling it
async function CachedForm({ action }: { action: (data: FormData) => Promise<void> }) {
  'use cache'
  cacheLife('hours')

  return (
    <form action={action}> {/* Don't call action here */}
      <input name="email" />
      <button>Submit</button>
    </form>
  )
}

// ============================================
// ANTI-PATTERN: Creating JSX inside cache
// ============================================

// ❌ WRONG: Creating JSX and passing to client component
// This causes "Maximum call stack size exceeded" errors
async function BrokenAgent() {
  'use cache'
  const items = await fetchItems()

  // Creating React elements inside cached function
  const itemComponents = items.map(item => (
    <ItemCard key={item.id} item={item} />
  ))

  // Passing JSX to client component - BREAKS SERIALIZATION
  return <ClientWrapper components={itemComponents} />
}

// ✅ CORRECT: Pass data, let client render
async function FixedAgent() {
  'use cache'
  const items = await fetchItems()

  // Pass serializable data only
  return <ClientWrapper items={items} />
}

// ============================================
// COMPOSING CACHED + DYNAMIC
// ============================================

// Outer component reads runtime data, passes to cached inner
async function ProductPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  // cookies() called outside cache
  const currency = (await cookies()).get('currency')?.value ?? 'USD'

  return <CachedProductDetails id={id} currency={currency} />
}

async function CachedProductDetails({ id, currency }: { id: string; currency: string }) {
  'use cache'
  cacheTag(`product-${id}`)
  cacheLife('hours')

  const product = await fetchProduct(id, currency)
  return <div>{product.name}: {product.price}</div>
}

// ============================================
// Placeholder types/functions
// ============================================
declare function fetchNavigation(): Promise<{ href: string; label: string }[]>
declare function fetchItems(): Promise<{ id: string }[]>
declare function fetchProduct(id: string, currency: string): Promise<{ name: string; price: string }>
declare function cookies(): Promise<{ get: (name: string) => { value: string } | undefined }>
declare function ItemCard(props: { item: { id: string } }): React.ReactElement
declare function ClientWrapper(props: { components?: ReactNode[]; items?: { id: string }[] }): React.ReactElement

// Export to avoid unused warnings
export { CachedLayout, CachedForm, BrokenAgent, FixedAgent, ProductPage }
