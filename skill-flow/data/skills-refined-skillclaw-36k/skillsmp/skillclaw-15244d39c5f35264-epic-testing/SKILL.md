---
name: epic-testing
description: Use this skill when you need to write unit and E2E tests for applications using Vitest and Playwright, following best practices for user-centric testing.
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

### Example - Tests that resemble users:
```typescript
// ✅ Good - Tests user workflow
test('User can sign up and create their first note', async ({ page, navigate }) => {
	// User visits signup page
	await navigate('/signup')
	
	// User fills out form like a real person would
	await page.getByRole('textbox', { name: /email/i }).fill('newuser@example.com')
	await page.getByRole('textbox', { name: /username/i }).fill('newuser')
	await page.getByRole('textbox', { name: /^password$/i }).fill('securepassword123')
	await page.getByRole('textbox', { name: /confirm/i }).fill('securepassword123')
	
	// User submits form
	await page.getByRole('button', { name: /sign up/i }).click()
	
	// User is redirected to onboarding
	await expect(page).toHaveURL(/\/onboarding/)
	
	// User creates their first note
	await navigate('/notes/new')
	await page.getByRole('textbox', { name: /title/i }).fill('My First Note')
	await page.getByRole('textbox', { name: /content/i }).fill('This is my first note!')
	await page.getByRole('button', { name: /create/i }).click()
	
	// User sees their note
	await expect(page.getByRole('heading', { name: 'My First Note' })).toBeVisible()
	await expect(page.getByText('This is my first note!')).toBeVisible()
})

// ❌ Avoid - Testing implementation details
test('Signup form calls API endpoint', async ({ page }) => {
	// This tests implementation, not user 
```