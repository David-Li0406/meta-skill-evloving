# Common Component Test Templates

## Template: Form Component

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

// Essential stories for any form component
export const Empty = meta.story({
  args: { defaultValues: {} }
});

export const Prefilled = meta.story({
  args: { defaultValues: mockData }
});

export const WithValidationErrors = meta.story({
  play: async ({ canvas, userEvent }) => {
    await userEvent.click(canvas.getByRole("button", { name: /submit/i }));
    await waitFor(async () => {
      await expect(canvas.getByText(/required/i)).toBeInTheDocument();
    });
  }
});

export const SuccessfulSubmission = meta.story({
  play: async ({ canvas, userEvent, args }) => {
    await userEvent.type(canvas.getByLabelText(/email/i), "test@example.com");
    await userEvent.click(canvas.getByRole("button", { name: /submit/i }));
    await expect(args.onSubmit).toHaveBeenCalled();
  }
});

export const Loading = meta.story({
  args: { isSubmitting: true }
});
```

## Template: List/Table Component

```typescript
import preview from "~/.storybook/preview";
import { itemBuilder } from "~/features/item/test/builders";
import { ItemList } from "./ItemList";

const meta = preview.meta({
  component: ItemList
});

// Essential stories for list components
export const Empty = meta.story({
  args: { items: [] }
});

export const WithData = meta.story({
  args: { items: Array.from({ length: 5 }, () => itemBuilder.one()) }
});

export const Loading = meta.story({
  args: { isLoading: true }
});

export const WithPagination = meta.story({
  args: {
    items: Array.from({ length: 20 }, () => itemBuilder.one()),
    pageSize: 10
  },
  play: async ({ canvas, userEvent }) => {
    await userEvent.click(canvas.getByRole("button", { name: /next/i }));
    // Verify page changed
  }
});

export const WithSorting = meta.story({
  args: { items: Array.from({ length: 5 }, () => itemBuilder.one()) },
  play: async ({ canvas, userEvent }) => {
    await userEvent.click(canvas.getByRole("columnheader", { name: /name/i }));
    // Verify sort order
  }
});
```

## Template: Modal/Dialog Component

```typescript
import { expect, fn } from "storybook/test";
import preview from "~/.storybook/preview";
import { MyModal } from "./MyModal";

const meta = preview.meta({
  component: MyModal,
  args: {
    onClose: fn()
  }
});

// Essential stories for modal components
export const Closed = meta.story({
  args: { isOpen: false }
});

export const Open = meta.story({
  args: { isOpen: true }
});

export const CloseOnBackdrop = meta.story({
  args: { isOpen: true },
  play: async ({ canvasElement, userEvent, args }) => {
    const backdrop = canvasElement.parentElement?.querySelector("[data-backdrop]");
    if (backdrop) {
      await userEvent.click(backdrop);
      await expect(args.onClose).toHaveBeenCalled();
    }
  }
});

export const CloseOnEscape = meta.story({
  args: { isOpen: true },
  play: async ({ userEvent, args }) => {
    await userEvent.keyboard("{Escape}");
    await expect(args.onClose).toHaveBeenCalled();
  }
});

export const FocusTrap = meta.story({
  args: { isOpen: true },
  play: async ({ canvas }) => {
    const firstFocusable = canvas.getAllByRole("button")[0];
    await expect(firstFocusable).toHaveFocus();
  }
});
```

## Template: Button Component

```typescript
import { expect, fn } from "storybook/test";
import preview from "~/.storybook/preview";
import { Button } from "./Button";

const meta = preview.meta({
  component: Button,
  args: {
    onClick: fn()
  }
});

// Visual variants
export const Primary = meta.story({
  args: { variant: "primary", children: "Primary Button" }
});

export const Secondary = meta.story({
  args: { variant: "secondary", children: "Secondary Button" }
});

export const Destructive = meta.story({
  args: { variant: "destructive", children: "Delete" }
});

// Size variants
export const Small = meta.story({
  args: { size: "sm", children: "Small" }
});

export const Large = meta.story({
  args: { size: "lg", children: "Large" }
});

// State tests
export const Loading = meta.story({
  args: { isLoading: true, children: "Loading..." }
});

export const Disabled = meta.story({
  args: { disabled: true, children: "Disabled" }
});

// Interaction tests
export const ClickTest = meta.story({
  args: { children: "Click Me" },
  play: async ({ args, canvas, userEvent }) => {
    const button = canvas.getByRole("button");
    await userEvent.click(button);
    await expect(args.onClick).toHaveBeenCalledTimes(1);
  }
});

export const KeyboardAccessible = meta.story({
  args: { children: "Press Enter" },
  play: async ({ args, canvas, userEvent }) => {
    const button = canvas.getByRole("button");
    button.focus();
    await userEvent.keyboard("{Enter}");
    await expect(args.onClick).toHaveBeenCalled();
  }
});
```

## Template: Input/TextField Component

```typescript
import { expect, fn } from "storybook/test";
import preview from "~/.storybook/preview";
import { TextField } from "./TextField";

const meta = preview.meta({
  component: TextField,
  args: {
    onChange: fn()
  }
});

export const Empty = meta.story({
  args: { label: "Email", placeholder: "Enter your email" }
});

export const WithValue = meta.story({
  args: { label: "Email", value: "test@example.com" }
});

export const WithError = meta.story({
  args: {
    label: "Email",
    value: "invalid",
    error: "Invalid email address"
  }
});

export const Disabled = meta.story({
  args: { label: "Email", disabled: true }
});

export const TypeTest = meta.story({
  args: { label: "Email" },
  play: async ({ canvas, userEvent, args }) => {
    const input = canvas.getByRole("textbox");
    await userEvent.type(input, "test@example.com");
    await expect(args.onChange).toHaveBeenCalled();
    await expect(input).toHaveValue("test@example.com");
  }
});
```

## Template: Select/Dropdown Component

```typescript
import { expect, fn } from "storybook/test";
import preview from "~/.storybook/preview";
import { Select } from "./Select";

const meta = preview.meta({
  component: Select,
  args: {
    onChange: fn(),
    options: [
      { value: "1", label: "Option 1" },
      { value: "2", label: "Option 2" },
      { value: "3", label: "Option 3" }
    ]
  }
});

export const Default = meta.story({
  args: { label: "Choose an option" }
});

export const WithDefaultValue = meta.story({
  args: { label: "Choose an option", value: "2" }
});

export const Disabled = meta.story({
  args: { label: "Choose an option", disabled: true }
});

export const SelectOption = meta.story({
  args: { label: "Choose an option" },
  play: async ({ canvas, userEvent, args }) => {
    const select = canvas.getByRole("combobox");
    await userEvent.click(select);

    // Find option in portal (renders to document.body)
    const option = await screen.findByRole("option", { name: /option 2/i });
    await userEvent.click(option);

    await expect(args.onChange).toHaveBeenCalledWith("2");
  }
});
```

## Template: Card Component

```typescript
import preview from "~/.storybook/preview";
import { Card } from "./Card";

const meta = preview.meta({
  component: Card
});

export const WithTitle = meta.story({
  args: {
    title: "Card Title",
    children: "Card content goes here"
  }
});

export const WithFooter = meta.story({
  args: {
    title: "Card Title",
    children: "Card content",
    footer: <button>Action</button>
  }
});

export const Interactive = meta.story({
  args: {
    title: "Card Title",
    onClick: fn()
  }
});

export const Loading = meta.story({
  args: {
    isLoading: true
  }
});
```

## Template: Tabs Component

```typescript
import { expect } from "storybook/test";
import preview from "~/.storybook/preview";
import { Tabs } from "./Tabs";

const meta = preview.meta({
  component: Tabs,
  args: {
    tabs: [
      { id: "tab1", label: "Tab 1", content: "Content 1" },
      { id: "tab2", label: "Tab 2", content: "Content 2" },
      { id: "tab3", label: "Tab 3", content: "Content 3" }
    ]
  }
});

export const Default = meta.story({});

export const WithDefaultTab = meta.story({
  args: { defaultTab: "tab2" }
});

export const TabNavigation = meta.story({
  play: async ({ canvas, userEvent, step }) => {
    await step("Verify first tab is selected", async () => {
      const firstTab = canvas.getByRole("tab", { name: /tab 1/i });
      await expect(firstTab).toHaveAttribute("aria-selected", "true");
    });

    await step("Click second tab", async () => {
      const secondTab = canvas.getByRole("tab", { name: /tab 2/i });
      await userEvent.click(secondTab);
      await expect(secondTab).toHaveAttribute("aria-selected", "true");
    });

    await step("Verify content changed", async () => {
      await expect(canvas.getByText("Content 2")).toBeInTheDocument();
    });
  }
});
```

## Using These Templates

1. Copy the appropriate template for your component type
2. Customize props, args, and test scenarios
3. Add component-specific edge cases
4. Ensure all essential stories are covered
5. Run tests to verify they pass
