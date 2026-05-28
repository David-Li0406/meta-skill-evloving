# Testing @szum-tech/design-system Components

When testing components that use the design system, follow these patterns:

## Testing DS Form Components

```typescript
import { expect, fn, waitFor } from "storybook/test";
import preview from "~/.storybook/preview";
import { MyForm } from "./MyForm";

const meta = preview.meta({
  component: MyForm,
  args: {
    onSubmit: fn()
  }
});

export const FormValidation = meta.story({
  play: async ({ canvas, userEvent, args }) => {
    // DS Input components use specific ARIA patterns
    const emailInput = canvas.getByRole("textbox", { name: /email/i });
    const submitBtn = canvas.getByRole("button", { name: /submit/i });

    // Test validation error display
    await userEvent.click(submitBtn);

    await waitFor(async () => {
      await expect(canvas.getByText(/required/i)).toBeInTheDocument();
    });

    // Test successful submission
    await userEvent.type(emailInput, "test@example.com");
    await userEvent.click(submitBtn);
    await expect(args.onSubmit).toHaveBeenCalled();
  }
});
```

## Testing DS Modal/Dialog Components

```typescript
export const ModalInteraction = meta.story({
  play: async ({ canvas, canvasElement, userEvent }) => {
    // Open modal
    await userEvent.click(canvas.getByRole("button", { name: /open/i }));

    // DS modals use dialog role - query parent for portals
    const dialog = await screen.findByRole("dialog");
    await expect(dialog).toBeInTheDocument();

    // Test close on Escape
    await userEvent.keyboard("{Escape}");
    await expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
  }
});
```

## Testing DS Select/Dropdown Components

```typescript
export const SelectInteraction = meta.story({
  play: async ({ canvas, canvasElement, userEvent }) => {
    // DS Select uses combobox role
    const select = canvas.getByRole("combobox");
    await userEvent.click(select);

    // Options appear in portal (document.body)
    const option = await screen.findByRole("option", { name: /option 1/i });
    await userEvent.click(option);

    await expect(select).toHaveTextContent("Option 1");
  }
});
```

## Testing DS Tooltip Components

```typescript
export const TooltipInteraction = meta.story({
  play: async ({ canvas, canvasElement, userEvent, step }) => {
    await step("Hover to show tooltip", async () => {
      const trigger = canvas.getByRole("button", { name: /info/i });
      await userEvent.hover(trigger);
    });

    await step("Verify tooltip content", async () => {
      const tooltip = await screen.findByRole("tooltip");
      await expect(tooltip).toHaveTextContent(/helpful info/i);
    });

    await step("Unhover to hide tooltip", async () => {
      const trigger = canvas.getByRole("button", { name: /info/i });
      await userEvent.unhover(trigger);
    });
  }
});
```

## Testing DS Button Components

```typescript
export const ButtonStates = meta.story({
  play: async ({ canvas, userEvent, args }) => {
    const button = canvas.getByRole("button");

    // Test enabled state
    await userEvent.click(button);
    await expect(args.onClick).toHaveBeenCalledTimes(1);

    // Test loading state (aria-busy)
    await expect(button).toHaveAttribute("aria-busy", "false");

    // Test disabled state
    await expect(button).not.toBeDisabled();
  }
});
```

## Testing DS Toast/Notification Components

```typescript
export const ToastNotification = meta.story({
  play: async ({ canvas, userEvent }) => {
    // Trigger action that shows toast
    await userEvent.click(canvas.getByRole("button", { name: /show toast/i }));

    // Toast should appear with role="status" or role="alert"
    const toast = await canvas.findByRole("status");
    await expect(toast).toHaveTextContent(/success/i);

    // Wait for auto-dismiss (if applicable)
    await waitFor(
      async () => {
        await expect(canvas.queryByRole("status")).not.toBeInTheDocument();
      },
      { timeout: 5000 }
    );
  }
});
```

## Testing DS Tabs Components

```typescript
export const TabNavigation = meta.story({
  play: async ({ canvas, userEvent, step }) => {
    await step("Verify initial tab is selected", async () => {
      const firstTab = canvas.getByRole("tab", { name: /first/i });
      await expect(firstTab).toHaveAttribute("aria-selected", "true");
    });

    await step("Click second tab", async () => {
      const secondTab = canvas.getByRole("tab", { name: /second/i });
      await userEvent.click(secondTab);
      await expect(secondTab).toHaveAttribute("aria-selected", "true");
    });

    await step("Verify panel content changed", async () => {
      const panel = canvas.getByRole("tabpanel");
      await expect(panel).toHaveTextContent(/second panel content/i);
    });
  }
});
```

## Common DS Patterns

### Portal Queries
Many DS components render in portals (modals, dropdowns, tooltips) to document.body. Use `screen` for these:

```typescript
import { screen } from "storybook/test";

// Portal content renders to document.body
const dialog = await screen.findByRole("dialog");
const option = await screen.findByRole("option");
const tooltip = await screen.findByRole("tooltip");
```

### ARIA Patterns
DS components follow strict ARIA patterns. Use appropriate roles:

```typescript
// Buttons
canvas.getByRole("button", { name: /label/i });

// Inputs
canvas.getByRole("textbox", { name: /email/i });

// Checkboxes
canvas.getByRole("checkbox", { name: /agree/i });

// Radio buttons
canvas.getByRole("radio", { name: /option/i });

// Comboboxes
canvas.getByRole("combobox");

// Dialogs
portal.getByRole("dialog");

// Tooltips
portal.getByRole("tooltip");
```

### Async Components
DS components may have animations/transitions. Use `findBy*` queries:

```typescript
// Wait for element to appear
const dialog = await portal.findByRole("dialog");

// Wait for element to disappear
await waitFor(async () => {
  await expect(portal.queryByRole("dialog")).not.toBeInTheDocument();
});
```

### Focus Management
DS modals and dialogs manage focus automatically:

```typescript
export const FocusTest = meta.story({
  play: async ({ canvas, userEvent }) => {
    // Open dialog
    await userEvent.click(canvas.getByRole("button", { name: /open/i }));

    // Verify focus is inside dialog (portal renders to document.body)
    const dialog = await screen.findByRole("dialog");
    const focusedElement = dialog.querySelector(":focus");
    await expect(focusedElement).toBeInTheDocument();
  }
});
```

## Design System Documentation

For complete DS component APIs and patterns, see the [design system documentation](https://szum-tech-design-system.vercel.app/?path=/docs/components--docs).
