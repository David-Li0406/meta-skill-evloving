# Locator Strategy Reference

Choosing the right locator for reliable tests.

## Priority Order

| Priority | Method | When to Use |
|----------|--------|-------------|
| 1 | `getByTestId()` | When test IDs are available |
| 2 | `getByRole()` | Semantic elements (buttons, headings, links) |
| 3 | `getByLabel()` | Form inputs with labels |
| 4 | `getByPlaceholder()` | Inputs with placeholder text |
| 5 | `getByText()` | Visible text content |
| 6 | `locator()` | CSS/XPath as last resort |

## Examples

### Test ID (Most Reliable)

```typescript
page.getByTestId('submit-btn')
page.getByTestId('user-menu')
page.getByTestId('welcome-message')
```

### Role with Name (Semantic)

```typescript
page.getByRole('button', { name: 'Submit' })
page.getByRole('heading', { level: 1 })
page.getByRole('link', { name: 'Dashboard' })
page.getByRole('alert')
page.getByRole('navigation')
```

### Label (Form Fields)

```typescript
page.getByLabel('Email address')
page.getByLabel('Password')
page.getByLabel('Remember me')
```

### Placeholder

```typescript
page.getByPlaceholder('Enter your email')
page.getByPlaceholder('Search...')
```

### Text (Exact or Partial)

```typescript
page.getByText('Welcome back')
page.getByText(/welcome/i)  // case-insensitive
page.getByText('Submit', { exact: true })
```

### CSS (Last Resort)

```typescript
page.locator('.submit-button')
page.locator('[data-cy="submit"]')
page.locator('#login-form')
```

## Chaining Locators

```typescript
// Within a container
page.getByRole('navigation').getByRole('link', { name: 'Home' })

// Filter by text
page.getByRole('listitem').filter({ hasText: 'Product 1' })

// Nth element
page.getByRole('listitem').nth(0)
```
