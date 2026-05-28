# Decision Tree: Component and Code Placement (Next.js 15+)

Use this decision tree whenever you need to place, move, or refactor code.

---

## Step 1: Identify execution environment

**Does this code require browser-only APIs?**

* `window`, `document`, `localStorage`
* DOM events
* Client-side state (`useState`, `useEffect`)

✔ YES → Client Component (`"use client"`)
✖ NO → Server Component (default)

---

## Step 2: Identify responsibility

**What is the primary role of this code?**

* Data fetching → Server Component or Server Action
* Mutation / form submission → Server Action
* UI interactivity → Client Component
* Pure UI (no state) → Server Component
* Utility / helper → Utility module

---

## Step 3: Count feature usage (Scope Rule)

**How many route groups or features use this code?**

* 1 feature → Keep it local
* 2+ features → Move to `shared/`

⚠️ Never promote code to `shared/` preemptively.

---

## Step 4: Choose the correct location

### If used by one feature only

```txt
app/(feature)/_components/
app/(feature)/_hooks/
app/(feature)/_actions/
app/(feature)/_utils/
```

### If used by multiple features

```txt
shared/components/
shared/hooks/
shared/actions/
shared/utils/
```

---

## Step 5: Validate Server / Client boundary

**Is any server-only code imported by a Client Component?**

✔ YES → INVALID (must refactor)
✖ NO → OK

**Rules:**

* Server Actions MUST use `server-only`
* Database access is server-only
* Environment secrets never reach client bundles

---

## Step 6: Performance validation

Before finalizing placement, ensure:

* Client Components are minimal
* No unnecessary `"use client"`
* Server Components control data flow
* Bundle splitting is preserved

---

## Final Check (Must all be YES)

* Scope Rule respected?
* Server-first architecture preserved?
* Folder structure screams business intent?
* No duplication or premature sharing?

If any answer is NO → refactor before proceeding.
