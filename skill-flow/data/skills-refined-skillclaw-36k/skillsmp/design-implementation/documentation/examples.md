# Design Implementation Examples

## Basic Usage

### Implement from Verbal Description

```
User: "implement a hero section with a large heading, subtext, and a CTA button"

Agent:
1. Starts dev server (auto-detected port)
2. Creates src/components/Hero.tsx
3. Styles with Tailwind
4. Verifies: no errors, looks right
5. Reports completion
```

### Implement from Figma Link

```
User: "implement the hero section from this Figma: https://figma.com/file/abc123/Design?node-id=1:100"

Agent:
1. Fetches design from Figma API
2. Saves reference to history/hero-section/figma-reference.png
3. Implements matching the design
4. Compares screenshot to Figma
5. Iterates until match (max 5)
```

### Implement from Spec File

```
User: "implement the feature in thoughts/features/pricing-table.md"

Agent:
1. Reads spec file
2. Extracts requirements and Figma links
3. Implements each component
4. Verifies against spec criteria
```

## React Examples

### Simple Component

```tsx
// src/components/Hero.tsx
export function Hero() {
  return (
    <section className="min-h-screen flex items-center justify-center bg-gradient-to-b from-slate-900 to-slate-800">
      <div className="text-center max-w-4xl px-4">
        <h1 className="text-5xl md:text-7xl font-bold text-white mb-6">
          Build Faster
        </h1>
        <p className="text-xl text-slate-300 mb-8">
          Ship production-ready features in minutes, not hours.
        </p>
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-lg text-lg font-semibold transition-colors">
          Get Started
        </button>
      </div>
    </section>
  );
}
```

### With State

```tsx
// src/components/Counter.tsx
import { useState } from 'react';

export function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div className="flex items-center gap-4">
      <button
        onClick={() => setCount(c => c - 1)}
        className="w-10 h-10 rounded-full bg-slate-200 hover:bg-slate-300"
      >
        -
      </button>
      <span className="text-2xl font-mono">{count}</span>
      <button
        onClick={() => setCount(c => c + 1)}
        className="w-10 h-10 rounded-full bg-slate-200 hover:bg-slate-300"
      >
        +
      </button>
    </div>
  );
}
```

## Svelte Examples

### Simple Component

```svelte
<!-- src/lib/components/Hero.svelte -->
<section class="min-h-screen flex items-center justify-center bg-gradient-to-b from-slate-900 to-slate-800">
  <div class="text-center max-w-4xl px-4">
    <h1 class="text-5xl md:text-7xl font-bold text-white mb-6">
      Build Faster
    </h1>
    <p class="text-xl text-slate-300 mb-8">
      Ship production-ready features in minutes, not hours.
    </p>
    <button class="bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-lg text-lg font-semibold transition-colors">
      Get Started
    </button>
  </div>
</section>
```

### With Reactivity

```svelte
<!-- src/lib/components/Counter.svelte -->
<script lang="ts">
  let count = 0;
</script>

<div class="flex items-center gap-4">
  <button
    on:click={() => count--}
    class="w-10 h-10 rounded-full bg-slate-200 hover:bg-slate-300"
  >
    -
  </button>
  <span class="text-2xl font-mono">{count}</span>
  <button
    on:click={() => count++}
    class="w-10 h-10 rounded-full bg-slate-200 hover:bg-slate-300"
  >
    +
  </button>
</div>
```

## Common Patterns

### Feature Spec Format

```markdown
# Feature: Pricing Table

## Overview
Three-tier pricing table with monthly/annual toggle.

## Design Reference
Figma: https://figma.com/file/abc123/Design?node-id=2:200

## Components
- PricingToggle (monthly/annual switch)
- PricingCard (individual tier)
- PricingTable (container)

## Acceptance Criteria
- [ ] Three tiers: Basic, Pro, Enterprise
- [ ] Toggle switches prices
- [ ] Annual shows 20% savings badge
- [ ] CTA buttons link to /checkout
- [ ] Responsive on mobile (stack vertically)
```

### Error Fixing Examples

**Console Error:**
```
Error: Cannot find module './components/Hero'
Fix: Check file exists at expected path, fix import
```

**TypeScript Error:**
```
Error: Property 'title' is missing in type '{}' but required in type 'HeroProps'
Fix: Add required prop or make optional in interface
```

**Visual Issue:**
```
Issue: Button appears on wrong side
Fix: Change flex direction or adjust order
```

## CLI Flags

```bash
# Headless mode (no visible browser)
"implement next feature --headless"

# Custom port
"start server --port 3000"

# Verbose output
"verify implementation --verbose"
```

## Integration with Other Skills

### Delegate to frontend-design

For complex components:
```
"implement this complex dashboard"
→ Delegates to frontend-design skill
→ Returns to design-implementation for verification
```

### Escalate to engineer

For bugs beyond visual:
```
"fix the state management issue"
→ Escalates to engineer agent
→ Returns with technical fix
```

### Use design-iterator

For refinement loops:
```
"iterate on this hero section 5 times"
→ Uses design-iterator agent
→ Each iteration improves design
```
