---
name: vitest-feature-protector
description: Generate Vitest unit tests for new features/components to prevent regressions
---

# Vitest Feature Protector

Automatically creates Vitest test templates when new features or components are added.

## When to use this skill

- A new React/Vue component is created
- A new feature module is added
- Existing code needs test coverage
- User explicitly asks to "generate tests" or "create unit tests"

## How to use it

1. **Identify the target**
   - Get the feature/component name and file path
   - Determine type: component, utility function, or feature logic

2. **Generate test template**
```typescript
   // For React components
   import { describe, it, expect } from 'vitest'
   import { render, screen } from '@testing-library/react'
   import { ComponentName } from './ComponentName'

   describe('ComponentName', () => {
     it('should render without errors', () => {
       render(<ComponentName />)
       expect(screen.getByRole('...').toBeInTheDocument()
     })
     
     it('should handle props correctly', () => {
       // TODO: Test props
     })
   })
```

3. **File placement**
   - Components → `tests/components/ComponentName.test.tsx`
   - Features → `tests/features/FeatureName.test.ts`
   - Utils → `tests/utils/UtilName.test.ts`

4. **Follow conventions**
   - Use `describe()` for grouping
   - Use `it('should...')` for test cases
   - Include at least: render test, props test, interaction test
   - Add TODO comments for edge cases

5. **Remind user to**
   - Run `npm test` before committing
   - Check test coverage with `npm run test:coverage`

## Examples

**User request:** "Create a Button component"

**Agent response:**
```typescript
// src/components/Button.tsx
export function Button({ label, onClick }) { ... }

// tests/components/Button.test.tsx
import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { Button } from '@/components/Button'

describe('Button', () => {
  it('should render with label', () => {
    render(<Button label="Click me" onClick={() => {}} />)
    expect(screen.getByText('Click me')).toBeInTheDocument()
  })

  it('should call onClick when clicked', () => {
    const handleClick = vi.fn()
    render(<Button label="Click" onClick={handleClick} />)
    fireEvent.click(screen.getByText('Click'))
    expect(handleClick).toHaveBeenCalledOnce()
  })
})
```

## Notes

- Don't generate tests for third-party libraries
- Skip tests if user explicitly says "no tests needed"
- Prefer Testing Library queries in this order: `getByRole` > `getByLabelText` > `getByText`