# Server Components vs Client Components

## Overview

React Server Components (RSC) are the default in Next.js App Router. Understanding when to use Server vs Client Components is crucial for performance and proper data flow.

## Default Behavior

| Location | Default |
|----------|---------|
| `app/**/*.tsx` | Server Component |
| `features/**/components/*.tsx` | Server Component |
| Files with `"use client"` | Client Component |

## When to Use Each

### Server Components (Default)

Use for:
- Data fetching
- Direct database access
- Accessing backend resources
- Heavy computations that shouldn't ship to client
- Components that don't need interactivity

```typescript
// app/dashboard/page.tsx - Server Component (default)
import { auth } from "@clerk/nextjs/server";
import { getBudgets } from "~/features/budget/server/db/budgets";

export default async function DashboardPage() {
  const { userId } = await auth();
  const [, budgets] = await getBudgets(userId!);

  return (
    <div>
      <h1>Dashboard</h1>
      <BudgetList budgets={budgets} />  {/* Can be Server or Client */}
    </div>
  );
}
```

### Client Components

Use for:
- Event handlers (onClick, onChange, etc.)
- State (useState, useReducer)
- Effects (useEffect, useLayoutEffect)
- Browser APIs (window, document)
- Custom hooks with state
- Form interactivity

```typescript
// features/budget/components/budget-form.tsx
"use client";  // Required for interactivity

import { useState } from "react";
import { useFormStatus } from "react-dom";

export function BudgetForm({ onSubmit }: Props) {
  const [amount, setAmount] = useState("");

  return (
    <form action={onSubmit}>
      <input
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
      />
      <SubmitButton />
    </form>
  );
}

function SubmitButton() {
  const { pending } = useFormStatus();
  return <button disabled={pending}>Save</button>;
}
```

## Composition Patterns

### Server Component with Client Children

```typescript
// app/budgets/page.tsx - Server Component
import { getBudgets } from "~/features/budget/server/db/budgets";
import { BudgetFilters } from "~/features/budget/components/budget-filters";

export default async function BudgetsPage() {
  const budgets = await getBudgets();

  return (
    <div>
      {/* Client Component for interactivity */}
      <BudgetFilters />

      {/* Server-rendered list */}
      <ul>
        {budgets.map(b => <li key={b.id}>{b.name}</li>)}
      </ul>
    </div>
  );
}
```

### Client Component with Server Data

```typescript
// features/budget/components/budget-card.tsx
"use client";

import { useState } from "react";
import type { Budget } from "~/features/budget/types/budget";

interface Props {
  budget: Budget;  // Passed from Server Component
  onDelete: (id: string) => Promise<void>;  // Server Action
}

export function BudgetCard({ budget, onDelete }: Props) {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div>
      <h3>{budget.name}</h3>
      <button onClick={() => setIsExpanded(!isExpanded)}>
        {isExpanded ? "Hide" : "Show"} Details
      </button>
      {isExpanded && <p>{budget.description}</p>}
      <button onClick={() => onDelete(budget.id)}>Delete</button>
    </div>
  );
}
```

### Server Actions in Client Components

```typescript
// features/budget/components/quick-add-budget.tsx
"use client";

import { useActionState } from "react";
import { quickAddBudget } from "~/features/budget/server/actions/quick-add";

export function QuickAddBudget() {
  const [state, formAction, isPending] = useActionState(
    quickAddBudget,
    null
  );

  return (
    <form action={formAction}>
      <input name="name" placeholder="Budget name" />
      <input name="amount" type="number" placeholder="Amount" />
      <button disabled={isPending}>
        {isPending ? "Adding..." : "Quick Add"}
      </button>
    </form>
  );
}
```

## Data Flow Patterns

### Pattern 1: Server Fetch, Client Display

```typescript
// app/products/page.tsx (Server)
async function ProductsPage() {
  const products = await fetchProducts();  // Server-side fetch

  return <ProductGrid products={products} />;
}

// features/products/components/product-grid.tsx (Client)
"use client";

export function ProductGrid({ products }: { products: Product[] }) {
  const [filter, setFilter] = useState("");

  const filtered = products.filter(p =>
    p.name.toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <div>
      <input
        placeholder="Filter..."
        value={filter}
        onChange={e => setFilter(e.target.value)}
      />
      <div className="grid">
        {filtered.map(p => <ProductCard key={p.id} product={p} />)}
      </div>
    </div>
  );
}
```

### Pattern 2: Server Action for Mutations

```typescript
// features/budget/server/actions/update-budget.ts
"use server";

import { auth } from "@clerk/nextjs/server";
import { revalidatePath } from "next/cache";

export async function updateBudget(
  budgetId: string,
  data: UpdateBudgetDto
): ActionResponse<Budget> {
  const { userId } = await auth();
  if (!userId) {
    return { success: false, error: "Unauthorized" };
  }

  const [error, budget] = await updateBudgetInDb(budgetId, data);
  if (error) {
    return { success: false, error: error.message };
  }

  revalidatePath("/budgets");
  return { success: true, data: budget };
}

// features/budget/components/edit-budget-form.tsx (Client)
"use client";

import { updateBudget } from "../server/actions/update-budget";

export function EditBudgetForm({ budget }: { budget: Budget }) {
  const [state, formAction, isPending] = useActionState(
    async (prev, formData: FormData) => {
      return updateBudget(budget.id, {
        name: formData.get("name") as string,
        amount: Number(formData.get("amount"))
      });
    },
    null
  );

  return (
    <form action={formAction}>
      <input name="name" defaultValue={budget.name} />
      <input name="amount" type="number" defaultValue={budget.amount} />
      <button disabled={isPending}>Save</button>
    </form>
  );
}
```

## Common Mistakes

### Mistake 1: Using Hooks in Server Components

```typescript
// ❌ WRONG - Hooks don't work in Server Components
async function ServerPage() {
  const [count, setCount] = useState(0);  // Error!
  return <div>{count}</div>;
}

// ✅ CORRECT - Move to Client Component
"use client";
function ClientCounter() {
  const [count, setCount] = useState(0);
  return <div>{count}</div>;
}
```

### Mistake 2: Fetching in Client Components

```typescript
// ❌ Inefficient - Fetching on client
"use client";
function ProductList() {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    fetch("/api/products")
      .then(r => r.json())
      .then(setProducts);
  }, []);

  return <List items={products} />;
}

// ✅ Better - Fetch on server, render on client
// app/products/page.tsx (Server)
async function ProductsPage() {
  const products = await getProducts();
  return <ProductList products={products} />;
}

// components/product-list.tsx (Client)
"use client";
function ProductList({ products }: { products: Product[] }) {
  return <List items={products} />;
}
```

### Mistake 3: Passing Functions to Client Components

```typescript
// ❌ WRONG - Can't pass functions as props from Server to Client
async function ServerPage() {
  const handleClick = () => console.log("clicked");  // Not serializable
  return <ClientButton onClick={handleClick} />;
}

// ✅ CORRECT - Use Server Actions
async function ServerPage() {
  async function handleClick() {
    "use server";
    // Server-side logic
  }
  return <ClientButton onClick={handleClick} />;
}
```

## Boundaries

### Creating Client Boundaries

When you add `"use client"`, all imports become client-side:

```typescript
// features/dashboard/components/dashboard-widgets.tsx
"use client";

// All of these are now Client Components
import { ChartWidget } from "./chart-widget";
import { StatsWidget } from "./stats-widget";
import { ActivityWidget } from "./activity-widget";

export function DashboardWidgets({ data }: Props) {
  return (
    <div>
      <ChartWidget data={data.chart} />
      <StatsWidget data={data.stats} />
      <ActivityWidget data={data.activity} />
    </div>
  );
}
```

### Minimizing Client Boundaries

Keep client boundary as small as possible:

```typescript
// ✅ Good - Only interactive part is client
async function ProductPage({ id }: Props) {
  const product = await getProduct(id);  // Server

  return (
    <div>
      <h1>{product.name}</h1>           {/* Server */}
      <p>{product.description}</p>       {/* Server */}
      <AddToCartButton product={product} /> {/* Client */}
    </div>
  );
}

// features/cart/components/add-to-cart-button.tsx
"use client";
function AddToCartButton({ product }: Props) {
  const [isPending, startTransition] = useTransition();
  // ...
}
```

## Summary

| Aspect | Server Component | Client Component |
|--------|------------------|------------------|
| Directive | None (default) | `"use client"` |
| Data fetching | Direct DB/API | Via props or fetch |
| State | ❌ No | ✅ Yes |
| Events | ❌ No | ✅ Yes |
| Browser APIs | ❌ No | ✅ Yes |
| Bundle size | Not in JS bundle | In JS bundle |
| Rendering | Server only | Server + Client |
