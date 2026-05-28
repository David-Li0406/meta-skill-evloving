---
name: creating-react-utils
description: Create utility functions and helper modules for React applications with TypeScript. Use when creating utilities, helper functions, common logic, or when user mentions utils, helpers, or shared functions.
---

# Create React Utility Functions

Create utility functions and helper modules for React applications with TypeScript. Utils provide reusable logic for formatting, validation, and common operations, organized in the `lib/` directory with full type safety.

## File Structure

Utility functions are organized in the `lib` directory:

```
resources/js/lib/{name}.ts
```

**Examples:**

- `resources/js/lib/utils.ts` (general utilities)
- `resources/js/lib/format.ts` (formatting functions)
- `resources/js/lib/validators.ts` (validation functions)
- `resources/js/lib/api.ts` (API helpers)

## Core Conventions

### 1. Pure Function Structure

Utility functions should be pure and side-effect free:

```ts
export function formatCurrency(
  amount: number,
  currency: string = 'USD'
): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
  }).format(amount)
}
```

**Key Requirements:**

- Use function declarations (NOT arrow functions assigned to const)
- Use named exports (not default exports)
- Always type parameters and return values
- Keep functions pure (no side effects)
- Use descriptive function names
- Group related utilities in the same file

### 2. Function Declaration Style

**Always use function declarations for utility functions:**

```ts
// ✅ Correct: Function declaration
export function formatCurrency(
  amount: number,
  currency: string = 'USD'
): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
  }).format(amount)
}
```

**Even for simple utilities:**

```ts
// ✅ Function declaration
export function capitalize(text: string): string {
  return text.charAt(0).toUpperCase() + text.slice(1).toLowerCase()
}

// ✅ Function declaration for helper functions
function normalizeString(text: string): string {
  return text.trim().toLowerCase()
}

export function slugify(text: string): string {
  const normalized = normalizeString(text)
  return normalized.replace(/\s+/g, '-')
}
```

This pattern makes it clear what is a function versus a variable, improving code readability and maintainability.

### 3. Class Name Utilities

The `cn()` utility from shadcn/ui merges Tailwind classes:

```ts
import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

Usage:

```tsx
import { cn } from '@/lib/utils'

export function Button({ className, variant }: ButtonProps) {
  return (
    <button
      className={cn(
        'rounded-md px-4 py-2',
        {
          'bg-blue-500 text-white': variant === 'primary',
          'bg-gray-200 text-gray-800': variant === 'secondary',
        },
        className
      )}
    />
  )
}
```

### 4. Data Transformation Utilities

Create utilities for common data transformations:

```ts
export function truncate(text: string, length: number): string {
  if (text.length <= length) return text
  return text.slice(0, length) + '...'
}

export function capitalize(text: string): string {
  return text.charAt(0).toUpperCase() + text.slice(1).toLowerCase()
}

export function slugify(text: string): string {
  return text
    .toLowerCase()
    .replace(/[^\w\s-]/g, '')
    .replace(/\s+/g, '-')
    .replace(/--+/g, '-')
    .trim()
}
```

### 5. Type Guards and Validators

Create type-safe validation utilities:

```ts
export function isString(value: unknown): value is string {
  return typeof value === 'string'
}

export function isNotNull<T>(value: T | null): value is T {
  return value !== null
}

export function isDefined<T>(value: T | undefined): value is T {
  return value !== undefined
}

export function isEmpty(value: unknown): boolean {
  if (value === null || value === undefined) return true
  if (typeof value === 'string') return value.trim().length === 0
  if (Array.isArray(value)) return value.length === 0
  if (typeof value === 'object') return Object.keys(value).length === 0
  return false
}
```

## Examples

### Example 1: Date Formatting Utilities

```ts
// resources/js/lib/format.ts

export function formatDate(
  date: string | Date,
  locale: string = 'en-US'
): string {
  const d = typeof date === 'string' ? new Date(date) : date

  return d.toLocaleDateString(locale, {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}

export function formatRelativeTime(date: string | Date): string {
  const d = typeof date === 'string' ? new Date(date) : date
  const now = new Date()
  const diffInSeconds = Math.floor((now.getTime() - d.getTime()) / 1000)

  if (diffInSeconds < 60) return 'just now'
  if (diffInSeconds < 3600)
    return `${Math.floor(diffInSeconds / 60)} minutes ago`
  if (diffInSeconds < 86400)
    return `${Math.floor(diffInSeconds / 3600)} hours ago`
  if (diffInSeconds < 604800)
    return `${Math.floor(diffInSeconds / 86400)} days ago`

  return formatDate(d)
}

export function formatCurrency(
  amount: number,
  currency: string = 'USD',
  locale: string = 'en-US'
): string {
  return new Intl.NumberFormat(locale, {
    style: 'currency',
    currency,
  }).format(amount)
}
```

### Example 2: String Utilities

```ts
// resources/js/lib/string.ts

export function truncate(
  text: string,
  length: number,
  suffix: string = '...'
): string {
  if (text.length <= length) return text
  return text.slice(0, length).trim() + suffix
}

export function capitalize(text: string): string {
  return text.charAt(0).toUpperCase() + text.slice(1).toLowerCase()
}

export function titleCase(text: string): string {
  return text
    .split(' ')
    .map((word) => capitalize(word))
    .join(' ')
}

export function slugify(text: string): string {
  return text
    .toLowerCase()
    .replace(/[^\w\s-]/g, '')
    .replace(/\s+/g, '-')
    .replace(/--+/g, '-')
    .trim()
}

export function initials(name: string): string {
  return name
    .split(' ')
    .map((word) => word.charAt(0).toUpperCase())
    .join('')
    .slice(0, 2)
}
```

### Example 3: Array Utilities

```ts
// resources/js/lib/array.ts

export function unique<T>(array: T[]): T[] {
  return [...new Set(array)]
}

export function groupBy<T>(array: T[], key: keyof T): Record<string, T[]> {
  return array.reduce(
    (groups, item) => {
      const groupKey = String(item[key])
      if (!groups[groupKey]) {
        groups[groupKey] = []
      }
      groups[groupKey].push(item)
      return groups
    },
    {} as Record<string, T[]>
  )
}

export function sortBy<T>(
  array: T[],
  key: keyof T,
  order: 'asc' | 'desc' = 'asc'
): T[] {
  return [...array].sort((a, b) => {
    if (a[key] < b[key]) return order === 'asc' ? -1 : 1
    if (a[key] > b[key]) return order === 'asc' ? 1 : -1
    return 0
  })
}

export function chunk<T>(array: T[], size: number): T[][] {
  const chunks: T[][] = []
  for (let i = 0; i < array.length; i += size) {
    chunks.push(array.slice(i, i + size))
  }
  return chunks
}
```

### Example 4: URL and Query Utilities

```ts
// resources/js/lib/url.ts

export function buildQueryString(
  params: Record<string, string | number | boolean>
): string {
  const searchParams = new URLSearchParams()

  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null) {
      searchParams.append(key, String(value))
    }
  })

  return searchParams.toString()
}

export function parseQueryString(queryString: string): Record<string, string> {
  const params = new URLSearchParams(queryString)
  const result: Record<string, string> = {}

  params.forEach((value, key) => {
    result[key] = value
  })

  return result
}

export function isExternalUrl(url: string): boolean {
  try {
    const parsed = new URL(url)
    return parsed.origin !== window.location.origin
  } catch {
    return false
  }
}
```

## Anti-Patterns

### ❌ Don't Do This

```ts
// Don't use arrow functions assigned to const
export const formatCurrency = (amount: number): string => {
  // ❌ Use function declaration
  return `$${amount}`
}

// Don't use any types
export function format(value: any): any {
  // ❌ No type safety
  return value
}

// Don't use default exports
export default function formatDate() {} // ❌ Use named export

// Don't create impure functions
let counter = 0
export function incrementCounter() {
  counter++ // ❌ Side effect
  return counter
}

// Don't use es-toolkit when native methods exist
import { map } from 'es-toolkit'
export function double(arr: number[]) {
  return map(arr, (n) => n * 2) // ❌ Use native .map()
}

// Don't export unused utilities
export function unusedFunction() {} // ❌ Remove if not used
```

### ✅ Do This Instead

```ts
// Use proper TypeScript types
export function format(value: string): string {
  return value.trim()
}

// Use named exports
export function formatDate() {}

// Create pure functions
export function incrementCounter(current: number): number {
  return current + 1
}

// Use native methods when possible
export function double(arr: number[]): number[] {
  return arr.map((n) => n * 2)
}

// Only export what's needed
// Remove unused functions
```

## Using es-toolkit

Prefer `es-toolkit` over `lodash` for utilities not available natively:

```ts
import { debounce, throttle, groupBy } from 'es-toolkit'

export const debouncedSearch = debounce((query: string) => {
  // Search logic
}, 300)

export function groupUsersByRole<T extends { role: string }>(
  users: T[]
): Record<string, T[]> {
  return groupBy(users, (user) => user.role)
}
```

## Quality Standards

- All utilities must be pure functions (no side effects)
- Use TypeScript for all parameters and return values
- Use named exports (never default exports)
- Prefer native JavaScript methods over libraries
- Use `es-toolkit` for advanced utilities (not lodash)
- Write unit tests for complex utilities
- Document functions with JSDoc comments
- Keep utilities focused and single-purpose
