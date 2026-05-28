# Storybook Testing Patterns (CSF Next)

Reference patterns for different testing scenarios using CSF Next format.

## Basic Story Structure

```typescript
import { expect, fn, waitFor, within } from "storybook/test";

import preview from "~/.storybook/preview";

import { MyComponent } from "./my-component";

const meta = preview.meta({
  title: "Features/MyFeature/MyComponent",
  component: MyComponent,
  args: {
    onSubmit: fn()
  }
});

// Stories defined using meta.story()
export const Default = meta.story({});
```

## Initial State Testing

```typescript
export const InitialForm = meta.story({
  play: async ({ canvas, step }) => {
    await step("Verify initial field visibility", async () => {
      const input = canvas.getByLabelText(/email/i);
      await expect(input).toBeVisible();
      await expect(input).toHaveValue("");
    });

    await step("Verify default button state", async () => {
      const button = canvas.getByRole("button", { name: /submit/i });
      await expect(button).toBeEnabled();
    });
  }
});
```

## Prefilled Values Testing

```typescript
export const Prefilled = meta.story({
  args: {
    defaultValues: {
      email: "user@example.com",
      name: "John Doe"
    }
  },
  play: async ({ canvas, args }) => {
    const emailInput = canvas.getByLabelText(/email/i);
    await expect(emailInput).toHaveValue(args.defaultValues?.email);
  }
});
```

## Validation Error Testing

```typescript
export const ValidationEmptyForm = meta.story({
  args: { onSubmit: fn() },
  play: async ({ canvas, userEvent, args }) => {
    const submitButton = canvas.getByRole("button", { name: /submit/i });
    await userEvent.click(submitButton);

    await waitFor(async () => {
      const errorMessage = canvas.getByText(/required/i);
      await expect(errorMessage).toBeInTheDocument();
    });

    await expect(args.onSubmit).not.toHaveBeenCalled();
  }
});
```

## User Interaction Flow Testing

```typescript
export const Interaction = meta.story({
  args: { onSubmit: fn() },
  play: async ({ canvas, userEvent, args }) => {
    await userEvent.type(canvas.getByLabelText(/email/i), "user@example.com");
    await userEvent.type(canvas.getByLabelText(/password/i), "password123");
    await userEvent.click(canvas.getByRole("button", { name: /submit/i }));

    await waitFor(async () => {
      await expect(args.onSubmit).toHaveBeenCalledWith({
        email: "user@example.com",
        password: "password123"
      });
    });
  }
});
```

## Loading State Testing

```typescript
export const LoadingState = meta.story({
  args: {
    onSubmit: async () => new Promise((resolve) => setTimeout(resolve, 2000))
  },
  play: async ({ canvas, userEvent }) => {
    const submitButton = canvas.getByRole("button", { name: /submit/i });
    await userEvent.click(submitButton);

    await expect(submitButton).toBeDisabled();
    await expect(submitButton).toHaveAttribute("data-state", "loading");
  }
});
```

## Portal/Dropdown Testing

For elements rendered in portals (outside the story canvas), use `screen`:

```typescript
import { screen } from "storybook/test";

export const DropdownInteraction = meta.story({
  play: async ({ canvas, userEvent }) => {
    const trigger = canvas.getByLabelText("Select option");
    await userEvent.click(trigger);

    // For portal content (modals, dropdowns, tooltips), use screen
    // Portals typically render to document.body

    await waitFor(async () => {
      const option = screen.getByRole("option", { name: /option 1/i });
      await expect(option).toBeVisible();
      await userEvent.click(option);
    });

    await expect(trigger).toHaveTextContent("Option 1");
  }
});
```

## Tooltip Testing

```typescript
export const TooltipInteraction = meta.story({
  play: async ({ canvas, userEvent, step }) => {
    await step("Hover to show tooltip", async () => {
      const trigger = canvas.getByRole("button", { name: /info/i });
      await userEvent.hover(trigger);
    });

    await step("Verify tooltip content", async () => {
      const tooltip = await screen.findByRole("tooltip");
      await expect(tooltip).toHaveTextContent(/helpful information/i);
    });

    await step("Unhover to hide tooltip", async () => {
      const trigger = canvas.getByRole("button", { name: /info/i });
      await userEvent.unhover(trigger);
    });
  }
});
```

## Navigation/Callback Testing

```typescript
export const BackNavigation = meta.story({
  args: { onBack: fn() },
  play: async ({ canvas, userEvent, args }) => {
    await userEvent.click(canvas.getByRole("button", { name: /back/i }));
    await expect(args.onBack).toHaveBeenCalledOnce();
  }
});
```

## Server Error Handling Testing

```typescript
export const ServerErrorHandling = meta.story({
  args: {
    onSubmit: fn(async () => ({
      success: false as const,
      error: "Failed to save. Please try again."
    }))
  },
  play: async ({ canvas, userEvent, args }) => {
    await userEvent.click(canvas.getByRole("button", { name: /submit/i }));

    await waitFor(async () => {
      await expect(args.onSubmit).toHaveBeenCalled();
    });
  }
});
```

## Using Steps for Organization

```typescript
export const CompleteFlow = meta.story({
  play: async ({ canvas, userEvent, step }) => {
    await step("Fill in user information", async () => {
      await userEvent.type(canvas.getByLabelText(/name/i), "John Doe");
    });

    await step("Select preferences", async () => {
      await userEvent.click(canvas.getByRole("checkbox", { name: /newsletter/i }));
    });

    await step("Submit form", async () => {
      await userEvent.click(canvas.getByRole("button", { name: /submit/i }));
    });
  }
});
```

## Complete User Flow Testing

```typescript
export const CompleteUserFlow = meta.story({
  args: { onSubmit: fn() },
  play: async ({ canvas, userEvent, args }) => {
    await expect(canvas.getByText("Welcome")).toBeInTheDocument();

    await userEvent.type(canvas.getByLabelText(/email/i), "user@example.com");
    await userEvent.type(canvas.getByLabelText(/password/i), "securePass123");
    await userEvent.click(canvas.getByRole("checkbox", { name: /accept terms/i }));
    await userEvent.click(canvas.getByRole("button", { name: /sign up/i }));

    await waitFor(async () => {
      await expect(args.onSubmit).toHaveBeenCalledWith({
        email: "user@example.com",
        password: "securePass123",
        acceptedTerms: true
      });
    });
  }
});
```

## Test-Only Stories

Use `tags: ["test-only"]` for stories that should run in tests but not appear in Storybook UI:

```typescript
export const TestOnlyStory = meta.story({
  tags: ["test-only"],
  play: async ({ canvas }) => {
    // This story runs in tests but is hidden from Storybook sidebar
    await expect(canvas.getByRole("main")).toBeVisible();
  }
});
```

## Keyboard Navigation Testing

```typescript
export const KeyboardNavigation = meta.story({
  play: async ({ canvas, userEvent }) => {
    const firstInput = canvas.getByLabelText(/first name/i);
    firstInput.focus();

    await userEvent.tab();
    await expect(canvas.getByLabelText(/last name/i)).toHaveFocus();

    await userEvent.tab();
    await expect(canvas.getByLabelText(/email/i)).toHaveFocus();

    await userEvent.keyboard("{Enter}");
    // Verify form submission
  }
});
```
