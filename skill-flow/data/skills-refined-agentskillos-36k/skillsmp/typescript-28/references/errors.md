# TypeScript Errors Reference

## Contents
- Common Type Errors
- Strict Mode Errors
- React-Specific Errors
- API Route Errors
- Troubleshooting Workflow

## Common Type Errors

### TS2322: Type 'X' is not assignable to type 'Y'

**Example from this codebase:**

```typescript
// Error: Type 'string | undefined' is not assignable to type 'string'
const email: string = process.env.EMAIL_ADDRESS

// Fix: Handle undefined case
const email = process.env.EMAIL_ADDRESS ?? 'default@example.com'

// Or: Use type assertion only if you're certain
const email = process.env.EMAIL_ADDRESS! // Use sparingly
```

### TS2345: Argument of type 'X' is not assignable to parameter of type 'Y'

```typescript
// Error: Argument of type 'string | null' is not assignable
const value: string | null = getValue()
processString(value) // Error!

// Fix: Narrow the type first
if (value !== null) {
  processString(value) // OK
}
```

### TS7006: Parameter 'x' implicitly has an 'any' type

With `strict: true`, you must type function parameters:

```typescript
// Error
const handleChange = (e) => { /* ... */ }

// Fix
const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
  setFormData({ ...formData, [e.target.name]: e.target.value })
}
```

### TS2339: Property 'x' does not exist on type 'Y'

```typescript
// Error: Property 'Calendly' does not exist on type 'Window'
window.Calendly.initPopupWidget({ url: '...' })

// Fix: Augment the Window interface (pattern from app/page.tsx)
declare global {
  interface Window {
    Calendly: {
      initPopupWidget: (options: { url: string }) => void
    }
  }
}
```

## Strict Mode Errors

### strictNullChecks Errors

```typescript
// With strictNullChecks: true

// Error: Object is possibly 'null'
const element = document.querySelector('.widget')
element.innerHTML = 'content' // Error!

// Fix: Null check
const element = document.querySelector('.widget')
if (element) {
  element.innerHTML = 'content'
}

// Or: Optional chaining
document.querySelector('.widget')?.classList.add('active')
```

### strictPropertyInitialization Errors

```typescript
// Error: Property 'name' has no initializer
class User {
  name: string // Error in strict mode
}

// Fix 1: Initialize in constructor
class User {
  name: string
  constructor(name: string) {
    this.name = name
  }
}

// Fix 2: Use definite assignment assertion (if set elsewhere)
class User {
  name!: string
}
```

## React-Specific Errors

### TS2786: Component type is not assignable

```typescript
// Error: 'Component' cannot be used as a JSX component
// Usually means the component returns wrong type

// Fix: Ensure return type is valid JSX
export default function Component(): JSX.Element | null {
  if (!mounted) return null
  return <div>Content</div>
}
```

### Event Handler Type Errors

```typescript
// Error: Type 'MouseEvent' is not assignable to 'ChangeEvent'
const handleChange = (e: React.MouseEvent) => {
  setFormData({ ...formData, [e.target.name]: e.target.value }) // Error!
}

// Fix: Use correct event type
const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
  setFormData({ ...formData, [e.target.name]: e.target.value })
}
```

### Children Prop Errors

```typescript
// Error: Property 'children' does not exist
function Layout({ children }) { /* ... */ }

// Fix: Type the children prop
function Layout({ children }: { children: React.ReactNode }) {
  return <div>{children}</div>
}
```

## API Route Errors

### Request Body Type Errors

```typescript
// Pattern from app/api/contact/route.ts
export async function POST(request: NextRequest) {
  const body = await request.json() // body is 'any'
  
  // Validate required fields explicitly
  const { firstName, lastName, email } = body
  if (!firstName || !lastName || !email) {
    return NextResponse.json(
      { error: 'All fields are required' },
      { status: 400 }
    )
  }
  // After validation, you know fields exist
}
```

### Response Type Safety

```typescript
// Type the API response shape
interface ApiResponse {
  success: boolean
  message?: string
  error?: string
}

return NextResponse.json<ApiResponse>(
  { success: true, message: 'Email sent' },
  { status: 200 }
)
```

## Troubleshooting Workflow

Copy this checklist and track progress:
- [ ] Check the exact error location (file:line)
- [ ] Read the full error message including expected vs actual types
- [ ] Hover over the problematic expression to see inferred type
- [ ] Check if the issue is strictNullChecks (null/undefined)
- [ ] Verify all function parameters are typed
- [ ] Run `npm run build` to surface all type errors

### Validation Loop

1. Make type changes
2. Run `npm run lint` or check IDE errors
3. If errors remain, analyze the type mismatch
4. Repeat until no errors

### Common Quick Fixes

| Error Pattern | Quick Fix |
|--------------|-----------|
| "possibly null" | Add null check or optional chaining `?.` |
| "implicitly has any" | Add explicit type annotation |
| "not assignable to" | Check source and target types match |
| "property does not exist" | Add to interface or use type guard |
| "missing properties" | Add required properties to object |

### When to Use Type Assertions

Only use type assertions when:
1. You have runtime validation ensuring the type
2. You're working with external data you can't control
3. TypeScript's inference is genuinely wrong (rare)

```typescript
// OK - after runtime validation
const data = await response.json()
if (isValidResponse(data)) {
  return data as ValidResponse
}

// AVOID - no runtime validation
return data as ValidResponse // Dangerous!