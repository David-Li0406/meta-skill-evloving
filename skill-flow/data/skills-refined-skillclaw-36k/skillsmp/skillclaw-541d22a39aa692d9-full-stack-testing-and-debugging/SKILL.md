---
name: full-stack-testing-and-debugging
description: Use this skill when you need to write tests, debug errors, or validate behaviors across the full stack of the Faiston NEXO project, including Frontend, Backend, and Agents.
---

# Skill body

## Overview

This skill combines full-stack testing and debugging expertise for the Faiston NEXO project, covering all layers from Frontend to Backend and Agents.

## Allowed Tools

- Read
- Write
- Edit
- Bash
- Grep
- Glob
- WebFetch

## Testing Stack

### Frontend

- **Unit/Integration Testing**: Vitest
- **Component Testing**: React Testing Library
- **API Mocking**: MSW (Mock Service Worker)
- **Assertions**: Vitest matchers + jest-dom
- **Accessibility**: jest-axe
- **Coverage**: Vitest coverage

### Backend

- **Framework**: pytest + pytest-asyncio
- **API Testing**: httpx (async client for FastAPI)
- **Mocking**: unittest.mock, pytest-mock
- **Fixtures**: conftest.py patterns
- **Coverage**: pytest-cov

### Agents

- **ADK Mocking**: Mock Runner and Agent responses
- **AgentCore Testing**: Mock HTTP invocations
- **LLM Mocking**: Deterministic response fixtures

## Debugging Process

### Step 1: Capture the Error

**Collect Information:**
1. Error message (exact text)
2. Stack trace (full output)
3. Browser console logs
4. Network tab (if API-related)
5. Component tree (React DevTools)

**Quick Commands:**
```bash
# Check for TypeScript errors
pnpm typecheck

# Check build errors
pnpm build

# Run tests
pnpm test
```

### Step 2: Categorize the Issue

#### React/Component Errors

**Hook Rules Violation:**
```typescript
// ❌ Problem: Conditional hook call
function Component({ show }) {
  if (show) {
    const [state, setState] = useState() // Error!
  }
}

// ✅ Fix: Always call hooks at top level
function Component({ show }) {
  const [state, setState] = useState()
  if (!show) return null
  // ...
}
```

**Stale Closure:**
```typescript
// ❌ Problem: Stale value in callback
const handleClick = () => {
  console.log(count) // Always logs initial value
}

// ✅ Fix: Use ref or dependency
const handleClick = useCallback(() => {
  console.log(count) // Correctly logs updated value
}, [count]);
```

## Testing Philosophy

### Testing Pyramid

```
      /\
     /E2E\       ← Few: Full user flows (login → dashboard)
    /──────\
   /Integr.\     ← Some: Component + API interactions
  /──────────\
 / Unit Tests \  ← Many: Individual functions, hooks
```

**Priority:**
1. **Unit Tests**: Utility functions, hooks, pure logic
2. **Integration Tests**: Components with API calls
3. **Component Tests**: User interactions, rendering
4. **E2E Tests**: Critical user journeys

## File Structure

```
client/
├── components/
│   ├── PostCard.tsx
│   └── PostCard.test.tsx      # Co-located test
├── hooks/
│   ├── useAuth.ts
│   └── useAuth.test.ts
├── lib/
│   ├── utils.ts
│   └── utils.test.ts
└── __tests__/                  # Integration tests
    └── Community.test.tsx
```