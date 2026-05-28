# Example: Component Placement Decisions

## Case 1: Component used by one route only

Used only in `/dashboard`.

**Correct placement:**

```txt
app/(dashboard)/dashboard/_components/stats-card.tsx
```

**Incorrect placement:**

```txt
shared/components/stats-card.tsx
```

**Reason:**

* Usage count = 1 feature
* Scope Rule forbids promotion to shared

---

## Case 2: Component used by multiple features

Used in:

* `/shop`
* `/cart`
* `/wishlist`

**Correct placement:**

```txt
shared/components/product-card.tsx
```

**Incorrect placement:**

```txt
app/(shop)/shop/_components/product-card.tsx
```

**Reason:**

* Usage count ≥ 2
* Duplication is forbidden

---

# Example: Server vs Client Component Boundaries

## Server Component (Default)

```ts
import { getUser } from '@/lib/auth';

export default async function ProfilePage() {
  const user = await getUser();

  return <ProfileView user={user} />;
}
```

**Why:**

* Data fetching
* No interactivity
* Optimal for SEO and performance

---

## Client Component (Only when required)

```ts
'use client';

import { useState } from 'react';

export function ProfileView({ user }) {
  const [open, setOpen] = useState(false);

  return (
    <>
      <button onClick={() => setOpen(true)}>Edit</button>
    </>
  );
}
```

**Why:**

* Requires browser state
* Explicit `"use client"`
* UI-only logic

---

# Example: Refactoring a Scope Violation

## Initial (Incorrect)

A utility duplicated across features:

```txt
app/(shop)/shop/_utils/format-price.ts
app/(cart)/cart/_utils/format-price.ts
```

**Problem:**

* Same logic duplicated
* Violates Scope Rule

---

## Correct Refactor

```txt
shared/utils/format-price.ts
```

Then imported by both features.

**Why:**

* Usage count = 2
* Shared location is mandatory
* Single source of truth
