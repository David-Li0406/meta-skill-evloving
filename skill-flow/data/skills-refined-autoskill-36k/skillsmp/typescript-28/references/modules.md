# TypeScript Modules Reference

## Contents
- Import Patterns
- Path Aliases
- Module Structure
- Re-exports and Barrel Files

## Import Patterns

### Standard Import Order

This codebase follows a consistent import order:

```typescript
'use client' // 1. Directive (if needed)

import { useState, useEffect } from 'react' // 2. React
import Link from 'next/link' // 3. Next.js
import Image from 'next/image'
import Navigation from '@/app/components/Navigation' // 4. Local components
import Footer from '@/app/components/Footer'
import { ChevronRight, X } from 'lucide-react' // 5. Third-party
```

### Path Aliases

The `@/` alias maps to the project root:

```json
// tsconfig.json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./*"]
    }
  }
}
```

```typescript
// GOOD - use path alias
import Navigation from '@/app/components/Navigation'
import Footer from '@/app/components/Footer'

// BAD - relative imports for deeply nested components
import Navigation from '../../../components/Navigation'
```

## Module Structure

### Page Component Pattern

```typescript
// app/[page]/page.tsx
'use client'

import Navigation from '@/app/components/Navigation'
import Footer from '@/app/components/Footer'
import { useState } from 'react'

export default function PageName() {
  const [state, setState] = useState(initialValue)

  return (
    <div className="min-h-screen bg-black text-white">
      <Navigation />
      {/* Page content */}
      <Footer />
    </div>
  )
}
```

### API Route Pattern

```typescript
// app/api/[endpoint]/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { Resend } from 'resend'

const resend = new Resend(process.env.RESEND_API_KEY)

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    // validation and processing
    return NextResponse.json({ success: true }, { status: 200 })
  } catch (error) {
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}
```

### Component File Pattern

```typescript
// app/components/[ComponentName].tsx
'use client'

import { useState } from 'react'
import Link from 'next/link'
import { IconName } from 'lucide-react'

export default function ComponentName() {
  const [internalState, setInternalState] = useState(false)

  return (
    <div>
      {/* Component JSX */}
    </div>
  )
}
```

## Type-Only Imports

### When to Use `import type`

```typescript
// GOOD - import type for type-only usage
import type { Metadata } from 'next'
import type { ReactNode } from 'react'

// Only used in type positions
export const metadata: Metadata = { /* ... */ }

function Layout({ children }: { children: ReactNode }) {
  return <div>{children}</div>
}
```

```typescript
// Also fine - regular import if value is also used
import { NextRequest, NextResponse } from 'next/server'

// These are used as values (constructors/functions)
export async function POST(request: NextRequest) {
  return NextResponse.json({ success: true })
}
```

## Module Resolution

### Bundler Resolution Mode

```json
// tsconfig.json
{
  "compilerOptions": {
    "moduleResolution": "bundler"
  }
}
```

This enables:
- Importing without extensions: `import './module'` (not `'./module.ts'`)
- Support for package.json `exports` field
- Better compatibility with Next.js and modern bundlers

### isolatedModules

```json
// tsconfig.json
{
  "compilerOptions": {
    "isolatedModules": true
  }
}
```

Required for:
- Babel transpilation
- SWC (used by Next.js)
- esbuild

**Constraints:**
- Can't use `const enum` (use regular `enum` or union types)
- Can't use `export =` syntax
- All files must be modules (have imports/exports)

## WARNING: Circular Dependencies

**The Problem:**

```typescript
// components/A.tsx
import { B } from './B'
export const A = () => <B />

// components/B.tsx
import { A } from './A' // Circular!
export const B = () => <A />
```

**Why This Breaks:**
1. Runtime errors or undefined imports
2. Bundler may fail silently
3. Hot reload breaks unpredictably

**The Fix:**

```typescript
// Extract shared dependency or restructure
// components/shared.tsx
export const SharedComponent = () => { /* ... */ }

// components/A.tsx
import { SharedComponent } from './shared'