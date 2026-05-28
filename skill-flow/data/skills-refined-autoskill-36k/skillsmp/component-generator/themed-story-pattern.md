# Themed Story Pattern

**All Storybook stories MUST use the themed Light/Dark pattern.**

## Why This Pattern?

- ✅ Tests components in both light and dark modes
- ✅ Ensures theme consistency across all variants
- ✅ Serves as both documentation and automated tests
- ✅ Reduces code duplication (no separate test files)
- ✅ Visual regression testing built-in

## Core Pattern

### 1. Import the Helper

```tsx
import { createThemedStories } from "@/components/story-helpers";
```

### 2. Define Base Story

```tsx
const primaryBase: Story = {
	args: {
		variant: "primary",
		children: "Primary Button",
	},
};
```

### 3. Wrap with createThemedStories

```tsx
const primaryThemed = createThemedStories({
	story: primaryBase,
	testMode: "both", // or "light", "dark", "none"
});
```

### 4. Export Light and Dark Variants

```tsx
export const PrimaryLight = primaryThemed.Light;
export const PrimaryDark = primaryThemed.Dark;
```

## Complete Example

```tsx
import type { Meta, StoryObj } from "storybook-solidjs-vite";
import { createThemedStories } from "@/components/story-helpers";
import { Button } from "./button";

const meta = {
	title: "UI/Button",
	component: Button,
	tags: ["autodocs"],
	argTypes: {
		variant: {
			control: "select",
			options: ["primary", "secondary", "outline"],
			description: "Button color variant",
		},
		size: {
			control: "select",
			options: ["sm", "md", "lg"],
			description: "Button size",
		},
	},
} satisfies Meta<typeof Button>;

export default meta;
type Story = StoryObj<typeof meta>;

// Primary variant
const primaryBase: Story = {
	args: {
		variant: "primary",
		children: "Primary Button",
	},
};

const primaryThemed = createThemedStories({
	story: primaryBase,
	testMode: "both",
});

export const PrimaryLight = primaryThemed.Light;
export const PrimaryDark = primaryThemed.Dark;

// Secondary variant
const secondaryBase: Story = {
	args: {
		variant: "secondary",
		children: "Secondary Button",
	},
};

const secondaryThemed = createThemedStories({
	story: secondaryBase,
	testMode: "both",
});

export const SecondaryLight = secondaryThemed.Light;
export const SecondaryDark = secondaryThemed.Dark;

// Small size
const smallBase: Story = {
	args: {
		size: "sm",
		children: "Small Button",
	},
};

const smallThemed = createThemedStories({
	story: smallBase,
	testMode: "both",
});

export const SmallLight = smallThemed.Light;
export const SmallDark = smallThemed.Dark;

// All variants showcase
const allVariantsBase: Story = {
	render: () => (
		<div style={{ display: "flex", gap: "1rem", "flex-wrap": "wrap" }}>
			<Button variant="primary">Primary</Button>
			<Button variant="secondary">Secondary</Button>
			<Button variant="outline">Outline</Button>
		</div>
	),
};

const allVariantsThemed = createThemedStories({
	story: allVariantsBase,
	testMode: "light", // Only test in light mode for showcase
});

export const AllVariantsLight = allVariantsThemed.Light;
export const AllVariantsDark = allVariantsThemed.Dark;
```

## testMode Options

| testMode | Behavior |
|----------|----------|
| `"both"` | Run interaction tests in both Light and Dark variants (default) |
| `"light"` | Run interaction tests only in Light variant |
| `"dark"` | Run interaction tests only in Dark variant |
| `"none"` | Skip interaction tests (visual-only stories) |

## When to Use Each testMode

### Use "both" (default):
- ✅ Most interactive components (buttons, inputs, dialogs)
- ✅ Components with click handlers or state changes
- ✅ Components with keyboard navigation
- ✅ Components that need comprehensive coverage

### Use "light":
- ✅ Showcase stories (AllVariants)
- ✅ Complex stories where testing once is sufficient
- ✅ Stories that are visually identical in light/dark

### Use "dark":
- ✅ Rare - only if testing dark-specific behavior
- ✅ Dark mode edge cases

### Use "none":
- ✅ Pure visual stories without interaction
- ✅ Static examples
- ✅ Documentation-only stories

## Interaction Tests with Themed Stories

If your story has a `play` function for interaction tests, it will run based on `testMode`:

```tsx
const interactiveBase: Story = {
	render: () => {
		const [value, setValue] = createSignal("");
		return (
			<div>
				<SearchInput value={value()} onValueChange={setValue} />
				<p data-testid="output">{value()}</p>
			</div>
		);
	},
	play: async ({ canvasElement }) => {
		const canvas = within(canvasElement);
		const input = canvas.getByPlaceholderText("Search...");

		await userEvent.type(input, "test");
		await expect(canvas.getByTestId("output")).toHaveTextContent("test");
	},
};

const interactiveThemed = createThemedStories({
	story: interactiveBase,
	testMode: "both", // Runs play() in BOTH Light and Dark
});

export const InteractiveLight = interactiveThemed.Light;
export const InteractiveDark = interactiveThemed.Dark;
```

## Important Notes

### Portal-Rendered Components

For components using Kobalte (which renders to `document.body` via Portal):

```tsx
play: async ({ canvasElement }) => {
	const canvas = within(canvasElement);
	const body = within(document.body); // Portal renders here

	const input = canvas.getByPlaceholderText("Search...");
	await userEvent.type(input, "test");

	// Search in document.body for Portal-rendered elements
	const option = body.getByRole("option", { name: /result/i });
	await userEvent.click(option);
}
```

### Naming Convention

**Always use this exact pattern:**

1. Create base story: `const primaryBase: Story = { ... }`
2. Wrap with helper: `const primaryThemed = createThemedStories({ ... })`
3. Export variants: `export const PrimaryLight = primaryThemed.Light;`
4. Export dark variant: `export const PrimaryDark = primaryThemed.Dark;`

**Why this naming?**
- Storybook alphabetizes exports
- `Light` and `Dark` suffix groups themed variants together
- Base story name describes what's being tested
- Themed wrapper has consistent naming

## Do NOT Do This

❌ **Single theme export:**
```tsx
export const Primary: Story = {
	args: { variant: "primary" },
};
```

❌ **Manual theme switching:**
```tsx
export const PrimaryLight: Story = {
	args: { variant: "primary" },
	parameters: { theme: "light" },
};

export const PrimaryDark: Story = {
	args: { variant: "primary" },
	parameters: { theme: "dark" },
};
```

❌ **Inconsistent naming:**
```tsx
export const Primary_Light = primaryThemed.Light;
export const primaryDarkMode = primaryThemed.Dark;
```

## Summary Checklist

When generating stories for a component:

- [ ] Import `createThemedStories` from `@/components/story-helpers`
- [ ] Define base story with args or render function
- [ ] Wrap with `createThemedStories({ story, testMode })`
- [ ] Export both `Light` and `Dark` variants
- [ ] Use consistent naming: `{Name}Base`, `{Name}Themed`, `{Name}Light`, `{Name}Dark`
- [ ] Set appropriate `testMode` ("both" for most cases)
- [ ] For Portal components, search `document.body` in tests
- [ ] Create themed pairs for each variant and size
- [ ] Include an AllVariants showcase story
