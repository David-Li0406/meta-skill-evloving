# Storybook Testing Best Practices (CSF Next)

## CSF Next Format Best Practices

### 1. Always Import Preview

```typescript
// GOOD - Import preview for type-safe factory functions
import preview from "~/.storybook/preview";

const meta = preview.meta({
  component: MyComponent
});

export const Default = meta.story({});
```

### 2. No Default Export Needed

```typescript
// CSF 3.0 (old)

// CSF Next (new) - No default export required
const meta = preview.meta({ ... });
```

### 3. Let Types Be Inferred

```typescript
// BAD - Unnecessary type annotations
import preview from "~/.storybook/preview";
export const Default: Story = { };

// GOOD - Types inferred automatically
const meta = preview.meta({ component: MyComponent });
export const Default = meta.story({ });
```

## Testing Best Practices

### 1. Use Semantic Queries

```typescript
// GOOD - Accessible queries
canvas.getByRole("button", { name: /submit/i });
canvas.getByLabelText(/email/i);

// AVOID - Implementation-dependent queries
canvas.getByTestId("submit-btn");
canvas.querySelector(".btn-primary");
```

### 2. Await Async Operations

```typescript
// BAD
userEvent.click(button);
expect(args.onSubmit).toHaveBeenCalled();

// GOOD
await userEvent.click(button);
await expect(args.onSubmit).toHaveBeenCalled();
```

### 3. Use waitFor for Dynamic Content

```typescript
// BAD
const message = canvas.getByText(/success/i);

// GOOD
await waitFor(async () => {
  const message = canvas.getByText(/success/i);
  await expect(message).toBeVisible();
});

// ALSO GOOD - findBy* waits automatically
const message = await canvas.findByText(/success/i);
```

### 4. Test User-Visible Behavior

```typescript
// BAD - Testing implementation details
await expect(component.state.isLoading).toBe(true);

// GOOD - Testing visible outcomes
await expect(canvas.getByRole("button")).toBeDisabled();
await expect(canvas.getByText(/loading/i)).toBeVisible();
```

### 5. Mock Functions with fn()

```typescript
// BAD - Not trackable
args: { onSubmit: async () => {} }

// GOOD - Trackable with fn()
args: { onSubmit: fn(async () => ({ success: true })) }
```

### 6. Organize with Steps

```typescript
// GOOD - Clear test organization
play: async ({ canvas, userEvent, step }) => {
  await step("Fill in credentials", async () => {
    await userEvent.type(canvas.getByLabelText(/email/i), "user@example.com");
    await userEvent.type(canvas.getByLabelText(/password/i), "secret");
  });

  await step("Submit and verify", async () => {
    await userEvent.click(canvas.getByRole("button", { name: /submit/i }));
    await expect(canvas.getByText(/success/i)).toBeVisible();
  });
}
```

### 7. Handle Portals Correctly

```typescript
import { screen } from "storybook/test";

// BAD - Won't find portal content (portals render outside canvas)
const option = canvas.getByRole("option");

// GOOD - Use screen for portals
const option = await screen.findByRole("option");
```

**Portal query strategy:**
- **Use `screen`** for portal content (modals, tooltips, dropdowns)
- Portals render to document.body, so `screen` is the natural choice
- Simpler and more readable than `within(canvasElement.parentElement)`

### 8. Use queryBy* for Negative Assertions

```typescript
// BAD - Throws error if not found
const error = canvas.getByText(/error/i);
await expect(error).toBeNull();

// GOOD - Returns null if not found
const error = canvas.queryByText(/error/i);
await expect(error).toBeNull();
```

### 9. Keep Stories Focused

```typescript
// BAD - Too many concerns in one story
export const EverythingTest = meta.story({
  play: async ({ canvas }) => {
    // Tests initial state, validation, submission, error handling...
  }
});

// GOOD - One scenario per story
export const InitialState = meta.story({ ... });
export const ValidationErrors = meta.story({ ... });
export const SuccessfulSubmission = meta.story({ ... });
export const ServerError = meta.story({ ... });
```

### 10. Use Test-Only Tag for Hidden Tests

```typescript
// Stories that should run in tests but not appear in Storybook UI
export const InternalTest = meta.story({
  tags: ["test-only"],
  play: async ({ canvas }) => {
    // Implementation tests hidden from docs
  }
});
```

## Common Pitfalls

### 1. Not Awaiting userEvent

```typescript
// BAD - Race condition
userEvent.click(button);
expect(args.onClick).toHaveBeenCalled();

// GOOD
await userEvent.click(button);
await expect(args.onClick).toHaveBeenCalled();
```

### 2. Using getBy* for Elements That May Not Exist

```typescript
// BAD - Throws immediately if not found
const error = canvas.getByText(/error/i);

// GOOD - Returns null, doesn't throw
const error = canvas.queryByText(/error/i);
await expect(error).toBeNull();
```

### 3. Not Handling Async State Changes

```typescript
// BAD - May fail due to timing
await userEvent.click(submitButton);
const success = canvas.getByText(/success/i);

// GOOD - Wait for state change
await userEvent.click(submitButton);
await waitFor(async () => {
  const success = canvas.getByText(/success/i);
  await expect(success).toBeVisible();
});
```

### 4. Forgetting Portal Queries

```typescript
import { screen } from "storybook/test";

// BAD - Portal content not in canvas
const tooltip = canvas.getByRole("tooltip");

// GOOD - Use screen for portals
const tooltip = await screen.findByRole("tooltip");
```

**Why use `screen` for portals:**
- Portals (modals, tooltips, dropdowns) render outside the story canvas (usually to document.body)
- `canvas` won't find them (they're not children of the story)
- `screen` is the standard Testing Library pattern for querying document
- Simpler and more readable than `within(canvasElement.parentElement)`

**When to use `within(canvasElement.parentElement)` instead:**
- Only if you experience test isolation issues in your specific setup
- If you need more explicit scoping for complex scenarios

### 5. Hardcoding Test Data

```typescript
// BAD - Inline mock data
args: {
  user: { id: "1", name: "John", email: "john@example.com" }
}

// GOOD - Use test builders
import { userBuilder } from "~/features/users/test/builders";

args: {
  user: userBuilder.one()
}
```

## Story Categories Checklist

For each component, consider:

- [ ] Initial/Default State
- [ ] Prefilled State
- [ ] Loading State
- [ ] Error State (validation, server)
- [ ] Success State
- [ ] Edge Cases (empty, max values)
- [ ] User Interactions
- [ ] Complete User Flows
- [ ] Keyboard Navigation
- [ ] Accessibility (screen reader, focus)
