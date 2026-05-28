---
name: epic-testing
description: Use this skill when you need to write unit and E2E tests with Vitest and Playwright for the Epic Stack.
---

# Epic Stack: Testing

## When to use this skill

Use this skill when you need to:
- Write unit tests for utilities and components
- Create E2E tests with Playwright
- Test forms and validation
- Test routes and loaders
- Mock external services with MSW
- Test authentication and permissions
- Configure test database

## Patterns and conventions

### Testing Philosophy

Following Epic Web principles:

**Tests should resemble users** - Write tests that mirror how real users interact with your application. Test user workflows, not implementation details. If a user would click a button, your test should click that button. If a user would see an error message, your test should check for that specific message.

**Make assertions specific** - Be explicit about what you're testing. Instead of vague assertions, use specific, meaningful checks that clearly communicate the expected behavior. This makes tests easier to understand and debug when they fail.

### Two Types of Tests

Epic Stack uses two types of tests:

1. **Unit Tests with Vitest** - Tests for individual components and utilities
2. **E2E Tests with Playwright** - End-to-end tests of the complete flow

### Unit Tests with Vitest

**Basic setup:**
```typescript
// app/utils/my-util.test.ts
import { describe, expect, it } from 'vitest'
import { myUtil } from './my-util.ts'

describe('myUtil', () => {
	it('should do something', () => {
		expect(myUtil('input')).toBe('expected')
	})
})
```

**Testing with DOM:**
```typescript
import { describe, expect, it } from 'vitest'
import { render, screen } from '@testing-library/react'
import { MyComponent } from './my-component.tsx'

describe('MyComponent', () => {
	it('should render correctly', () => {
		render(<MyComponent />)
		expect(screen.getByText('Hello')).toBeInTheDocument()
	})
})
```

### E2E Tests with Playwright

**Basic setup:**
```typescript
// tests/e2e/my-feature.test.ts
import { expect, test } from '#tests/playwright-utils.ts'

test('Users can do something', async ({ page, navigate, login }) => {
	const user = await login()
	await navigate('/my-page')

	// Interact with the page
	await page.getByRole('button', { name: /Submit/i }).click()

	// Verify result
	await expect(page).toHaveURL('/success')
})
```

### Login Fixture

Epic Stack provides a `login` fixture for authenticated tests.

**Use login fixture:**
```typescript
test('Protected route', async ({ page, navigate, login }) => {
	const user = await login() // Creates user and session automatically
	await navigate('/protected')

	// User is authenticated
	await expect(page.getByText(`Welcome ${user.username}`)).toBeVisible()
})
```

### Insert User without Login

To create a user without authentication:

```typescript
test('Public content', async ({ page, navigate, insertNewUser }) => {
	const user = await insertNewUser({
		username: 'publicuser',
		email: 'public@example.com',
	})

	await navigate(`/users/${user.username}`)
	await expect(page.getByText(user.username)).toBeVisible()
})
```

### Navigate Helper

Use the `navigate` helper to navigate with type-safety:

```typescript
// Type-safe navigation
await navigate('/users/:username/notes', { username: user.username })
await navigate('/users/:username/notes/:noteId', {
	username: user.username,
	noteId: note.id,
})

// Also works with routes without parameters
await navigate('/login')
```

### Test Database

Epic Stack uses a separate test database.

**Automatic configuration:**
- The test database is configured automatically
- It's cleaned between tests
- Data created in tests is automatically deleted

### MSW (Mock Service Worker)

Epic Stack uses MSW to mock external services.

**Mock example:**
```typescript
// tests/mocks/github.ts
import { http, HttpResponse } from 'msw'

export const handlers = [
	http.get('https://api.github.com/user', () => {
		return HttpResponse.json({
			id: '123',
			login: 'testuser',
			email: 'test@example.com',
		})
	}),
]
```

**Use in tests:**
Mocks are automatically applied when `MOCKS=true` is configured.

### Testing Forms

**Test form:**
```typescript
test('User can submit form', async ({ page, navigate, login }) => {
	const user = await login()
	await navigate('/notes/new')

	// Fill form
	await page.getByRole('textbox', { name: /title/i }).fill('New Note')
	await page.getByRole('textbox', { name: /content/i }).fill('Note content')

	// Submit
	await page.getByRole('button', { name: /submit/i }).click()

	// Verify redirect
	await expect(page).toHaveURL(new RegExp('/users/.*/notes/.*'))
})
```

### Common examples

#### Example 1: Complete E2E test (resembling user workflow)

```typescript
// tests/e2e/notes.test.ts
import { expect, test } from '#tests/playwright-utils.ts'
import { prisma } from '#app/utils/db.server.ts'
import { faker } from '@faker-js/faker'

test('Users can create, edit, and delete notes', async ({ page, navigate, login }) => {
	const user = await login()
	await navigate('/users/:username/notes', { username: user.username })

	await page.getByRole('link', { name: /new note/i }).click()
	const newNote = {
		title: faker.lorem.words(3),
		content: faker.lorem.paragraphs(2),
	}
	await page.getByRole('textbox', { name: /title/i }).fill(newNote.title)
	await page.getByRole('textbox', { name: /content/i }).fill(newNote.content)
	await page.getByRole('button', { name: /submit/i }).click()

	await expect(page.getByRole('heading', { name: newNote.title })).toBeVisible()
	await expect(page.getByText(newNote.content)).toBeVisible()
	const noteUrl = page.url()
	const noteId = noteUrl.split('/').pop()

	await page.getByRole('link', { name: /edit/i }).click()
	const updatedNote = {
		title: faker.lorem.words(3),
		content: faker.lorem.paragraphs(2),
	}
	await page.getByRole('textbox', { name: /title/i }).fill(updatedNote.title)
	await page.getByRole('textbox', { name: /content/i }).fill(updatedNote.content)
	await page.getByRole('button', { name: /submit/i }).click()

	await expect(page.getByRole('heading', { name: updatedNote.title })).toBeVisible()
	await expect(page.getByText(updatedNote.content)).toBeVisible()

	await page.getByRole('button', { name: /delete/i }).click()
	await expect(page).toHaveURL(`/users/${user.username}/notes`)
	await expect(page.getByText(updatedNote.title)).not.toBeVisible()
})
```

### Common mistakes to avoid

- ❌ **Testing implementation details instead of user workflows**: Write tests that mirror how users actually use your app
- ❌ **Vague assertions**: Use specific, meaningful assertions that clearly communicate expected behavior
- ❌ **Not cleaning data after tests**: Epic Stack cleans automatically, but make sure not to depend on data between tests
- ❌ **Assuming execution order**: Tests must be independent
- ❌ **Not using fixtures**: Use `login`, `insertNewUser`, etc. instead of creating everything manually
- ❌ **Hardcoding data**: Use `faker` to generate unique data
- ❌ **Not waiting for elements**: Use `expect` with `toBeVisible()` instead of assuming it exists
- ❌ **Not using type-safe navigation**: Use `navigate` helper instead of `page.goto()` directly
- ❌ **Forgetting MSW in tests**: External services are automatically mocked when `MOCKS=true`
- ❌ **Not testing error cases**: Test both happy path and errors
- ❌ **Testing internal state instead of user-visible behavior**: Focus on what users see and do

## References

- [Epic Stack Testing Docs](../epic-stack/docs/testing.md)
- [Epic Web Principles](https://www.epicweb.dev/principles)
- [Vitest Documentation](https://vitest.dev/)
- [Playwright Documentation](https://playwright.dev/)
- [Testing Library](https://testing-library.com/)
- [MSW](https://mswjs.io/)
- `tests/playwright-utils.ts` - Playwright fixtures and helpers
- `tests/db-utils.ts` - DB helpers for tests
- `tests/e2e/` - E2E test examples
- `app/utils/*.test.ts` - Unit test examples