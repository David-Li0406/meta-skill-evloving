# Anti-Patterns: What NOT to Do (Next.js 15+)

This document lists forbidden or strongly discouraged patterns.

---

## ❌ Anti-Pattern 1: Bloated `shared/` folder

```txt
shared/
  components/
  hooks/
  utils/
  everything-else/
```

**Problem:**

* Code promoted without real reuse
* Violates Scope Rule
* Makes ownership unclear

**Correct approach:**

* Move code back to the feature
* Promote ONLY after 2+ real usages

---

## ❌ Anti-Pattern 2: Premature abstraction

Creating abstractions before reuse:

```txt
shared/hooks/use-modal.ts
```

Used only in:

* `/dashboard`

**Why this is wrong:**

* Scope Rule violation
* Adds indirection without benefit

---

## ❌ Anti-Pattern 3: Unnecessary Client Components

```ts
'use client';

export function StaticCard() {
  return <div>Static content</div>;
}
```

**Problem:**

* Increases bundle size
* Breaks streaming benefits
* Hurts performance

**Correct:**

* Use Server Components by default

---

## ❌ Anti-Pattern 4: Data fetching in Client Components

```ts
'use client';

useEffect(() => {
  fetch('/api/data');
}, []);
```

**Problem:**

* Waterfalls
* Poor SEO
* Slower TTFB

**Correct:**

* Fetch data in Server Components
* Pass data down as props

---

## ❌ Anti-Pattern 5: Mixing server and client logic

```ts
'use client';
import { db } from '@/lib/db';
```

**Problem:**

* Invalid architecture
* Potential runtime errors
* Security risk

**Correct:**

* Isolate server logic
* Use Server Actions or Server Components

---

## ❌ Anti-Pattern 6: Feature-agnostic root folders

```txt
app/components/
app/hooks/
```

**Problem:**

* Hides business intent
* Breaks Screaming Architecture

**Correct:**

* Feature-based route groups
* Private folders per feature
