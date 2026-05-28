---
name: full-stack-testing-and-debugging
description: Use this skill when writing tests, fixing test failures, or debugging errors across the full stack of the Faiston NEXO project, including Frontend, Backend, Agents, AWS, and Terraform.
---

# Full Stack Testing and Debugging Skill

This skill covers both testing and debugging for the Faiston NEXO project across all layers.

## Testing Stack

### Frontend

- **Unit/Integration**: Vitest
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

- **Hook Rules Violation**: Ensure hooks are called at the top level.
- **Stale Closure**: Use `useCallback` to avoid stale values in callbacks.
- **Infinite Re-render**: Memoize objects created in render.

#### TypeScript Errors

- **Type Mismatch**: Add type annotations to avoid `any`.
- **Null/Undefined**: Use optional chaining to handle potential undefined values.

#### Tailwind CSS Issues

- **Classes Not Applying**: Use complete class names instead of dynamic ones.

#### Vite/Build Issues

- **HMR Not Working**: Clear Vite cache and restart the dev server.

#### TanStack Query Issues

- **Stale Data**: Invalidate queries after mutations to refresh data.

#### MSW Mock API Issues

- **Mocks Not Working**: Ensure MSW is started in development.

### Step 3: Backend Debugging (FastAPI/Lambda)

- **Pydantic Validation Error**: Use proper coercion or validators.
- **CORS Issues**: Configure CORS in Terraform, not FastAPI.
- **Lambda Cold Start**: Import heavy libraries at the module level.

### Step 4: Agent Debugging (Google ADK/AgentCore)

- **Agent Not Responding**: Handle empty responses properly.
- **Session Service Issues**: Use AgentCore Memory for persistence.

### Step 5: AWS Debugging

- **S3 Presigned URL Issues**: Use regional endpoints with s3v4 signature.
- **Cognito Errors**: Check token expiration and user existence.

### Step 6: Terraform Debugging

- **State Lock Error**: Use `terraform force-unlock` with caution.
- **State Drift**: Use `terraform refresh` to update state from actual.

## Running Tests

### Frontend

```bash
# Run all frontend tests
pnpm test

# Run tests in watch mode
pnpm test --watch

# Run specific test file
pnpm test PostCard.test.tsx

# Run with coverage
pnpm test --coverage
```

### Backend

```bash
# Run all backend tests
cd server && pytest

# Run with verbose output
cd server && pytest -v

# Run specific test file
cd server && pytest tests/test_main.py

# Run with coverage
cd server && pytest --cov=. --cov-report=html
```

### Full Stack

```bash
# Run all tests (frontend + backend)
pnpm test && cd server && pytest
```

## Debugging Checklist

Before declaring a bug fixed:

- [ ] Error no longer appears in console
- [ ] TypeScript compiles without errors
- [ ] Build succeeds (`pnpm build`)
- [ ] Tests pass (`pnpm test`)
- [ ] Works on mobile viewport
- [ ] Works with slow network (DevTools throttle)
- [ ] No memory leaks (long usage)

## Common Quick Fixes

```bash
# Reset everything
rm -rf node_modules && pnpm install

# Clear Vite cache
rm -rf node_modules/.vite

# TypeScript issues
pnpm typecheck
```

## Response Format

When debugging:

1. **Acknowledge the issue**
   - "I see the error: [exact message]"
   - "Let me investigate systematically"

2. **Gather information**
   - Check console logs
   - Read relevant code
   - Test reproduction steps

3. **Identify root cause**
   - "The issue is caused by [explanation]"
   - "This happens because [technical reason]"

4. **Provide the fix**
   - Show exact code changes
   - Explain why this fixes it

5. **Verify the fix**
   - Run typecheck
   - Test in browser
   - Check edge cases

Remember: Most React bugs are about timing, state, or missing dependencies!