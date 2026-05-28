---
name: accessibility-audit
version: 1.0.0
lastUpdated: 2026-01-18
description: Perform WCAG accessibility audits on React components using automated tools and manual checks. Use when auditing accessibility, fixing a11y issues, or ensuring WCAG compliance.
tags: [accessibility, a11y, wcag, testing, audit]
author: Szum Tech Team
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, mcp__playwright__*
context: fork
agent: general-purpose
user-invocable: true
examples:
  - Audit Button component for WCAG compliance
  - Check form accessibility for LoginForm
  - Run accessibility audit on the dashboard page
  - Fix accessibility issues in NavBar component
---

# Accessibility Audit Skill

Perform comprehensive WCAG 2.1 accessibility audits on React components. This skill combines automated testing with manual review guidelines to ensure inclusive user experiences.

## Context

This skill helps you:

- Identify accessibility violations (WCAG 2.1 Level AA)
- Fix common accessibility issues
- Add proper ARIA attributes
- Ensure keyboard navigation
- Improve screen reader compatibility
- Document accessibility features

## Tools Used

- **Storybook a11y addon** - Automated checks in Storybook
- **Playwright** - Automated accessibility testing with axe-core
- **Manual checklist** - For issues automation can't catch

## Instructions

When the user requests an accessibility audit:

### 1. Analyze the Component

Read the component code and identify:
- Interactive elements (buttons, links, inputs)
- Images and media
- Form elements and labels
- Dynamic content updates
- Focus management
- Color usage

### 2. Run Automated Checks

#### Using Storybook a11y Addon

Check the Accessibility panel in Storybook for the component's stories.

```typescript
// Verify a11y addon is configured in .storybook/main.ts
addons: [
  '@storybook/addon-a11y',
  // ...
]
```

#### Using Playwright with axe-core

Create accessibility test:

```typescript
// tests/e2e/a11y/[component-name].a11y.spec.ts
import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

test.describe("Accessibility: [ComponentName]", () => {
  test("should have no accessibility violations", async ({ page }) => {
    // Navigate to Storybook story or page
    await page.goto("http://localhost:6006/?path=/story/component--default");

    // Wait for component to render
    await page.waitForSelector('[data-testid="component"]');

    // Run axe accessibility scan
    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"])
      .analyze();

    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test("should be keyboard navigable", async ({ page }) => {
    await page.goto("http://localhost:6006/?path=/story/component--default");

    // Test Tab navigation
    await page.keyboard.press("Tab");
    const focusedElement = await page.evaluate(() =>
      document.activeElement?.tagName
    );
    expect(focusedElement).toBeTruthy();

    // Test Enter/Space activation
    await page.keyboard.press("Enter");
    // Verify action occurred
  });
});
```

### 3. Manual Audit Checklist

#### Perceivable (WCAG 1.x)

```markdown
## 1.1 Text Alternatives
- [ ] All images have meaningful alt text
- [ ] Decorative images have alt=""
- [ ] Icon buttons have aria-label
- [ ] Complex images have long descriptions

## 1.2 Time-based Media
- [ ] Videos have captions
- [ ] Audio has transcripts
- [ ] No auto-playing media

## 1.3 Adaptable
- [ ] Content is structured with proper headings (h1-h6)
- [ ] Lists use proper list markup
- [ ] Tables have headers and captions
- [ ] Reading order is logical

## 1.4 Distinguishable
- [ ] Color contrast ratio >= 4.5:1 for normal text
- [ ] Color contrast ratio >= 3:1 for large text
- [ ] Information not conveyed by color alone
- [ ] Text can be resized to 200% without loss
- [ ] No horizontal scrolling at 320px viewport
```

#### Operable (WCAG 2.x)

```markdown
## 2.1 Keyboard Accessible
- [ ] All functionality available via keyboard
- [ ] No keyboard traps
- [ ] Focus visible on all interactive elements
- [ ] Logical tab order

## 2.2 Enough Time
- [ ] Users can extend time limits
- [ ] Users can pause moving content
- [ ] No content that flashes more than 3 times/second

## 2.3 Navigable
- [ ] Skip links available for navigation
- [ ] Page has descriptive title
- [ ] Focus order preserves meaning
- [ ] Link purpose clear from text

## 2.4 Input Modalities
- [ ] Touch targets at least 44x44px
- [ ] Functionality not dependent on motion
```

#### Understandable (WCAG 3.x)

```markdown
## 3.1 Readable
- [ ] Page language specified (lang attribute)
- [ ] Abbreviations explained

## 3.2 Predictable
- [ ] No unexpected context changes on focus
- [ ] Navigation consistent across pages
- [ ] Components identified consistently

## 3.3 Input Assistance
- [ ] Error messages are descriptive
- [ ] Labels or instructions provided
- [ ] Error prevention for important actions
- [ ] Form validation is accessible
```

#### Robust (WCAG 4.x)

```markdown
## 4.1 Compatible
- [ ] Valid HTML markup
- [ ] ARIA attributes used correctly
- [ ] Name, role, value programmatically determined
- [ ] Status messages announced to screen readers
```

### 4. Common Issues & Fixes

#### Missing Form Labels

```typescript
// ❌ Bad
<input type="text" placeholder="Email" />

// ✅ Good - explicit label
<label htmlFor="email">Email</label>
<input id="email" type="text" />

// ✅ Good - aria-label for icon inputs
<input type="text" aria-label="Search" />

// ✅ Good - visually hidden label
<label htmlFor="email" className="sr-only">Email</label>
<input id="email" type="text" placeholder="Email" />
```

#### Non-Descriptive Buttons

```typescript
// ❌ Bad
<button><Icon name="trash" /></button>

// ✅ Good
<button aria-label="Delete item">
  <Icon name="trash" aria-hidden="true" />
</button>

// ✅ Good - with visible text
<button>
  <Icon name="trash" aria-hidden="true" />
  <span>Delete</span>
</button>
```

#### Missing Image Alt Text

```typescript
// ❌ Bad
<Image src="/hero.jpg" />

// ✅ Good - meaningful alt
<Image src="/hero.jpg" alt="Team collaborating in modern office" />

// ✅ Good - decorative image
<Image src="/pattern.svg" alt="" aria-hidden="true" />
```

#### Color Contrast Issues

```typescript
// ❌ Bad - low contrast
<span className="text-gray-400">Important text</span>

// ✅ Good - sufficient contrast
<span className="text-gray-700">Important text</span>

// Use design system tokens that meet contrast requirements
<span className="text-foreground">Important text</span>
```

#### Missing Focus Indicators

```typescript
// ❌ Bad - removes focus outline
<button className="focus:outline-none">Click me</button>

// ✅ Good - visible focus
<button className="focus:ring-2 focus:ring-primary focus:ring-offset-2">
  Click me
</button>

// ✅ Good - using design system focus styles
<Button>Click me</Button> // Design system handles focus
```

#### Keyboard Accessibility

```typescript
// ❌ Bad - click only
<div onClick={handleClick}>Clickable div</div>

// ✅ Good - keyboard accessible
<button onClick={handleClick}>Clickable button</button>

// ✅ Good - if div is necessary
<div
  role="button"
  tabIndex={0}
  onClick={handleClick}
  onKeyDown={(e) => {
    if (e.key === "Enter" || e.key === " ") {
      handleClick();
    }
  }}
>
  Clickable div
</div>
```

#### Dynamic Content Announcements

```typescript
// ❌ Bad - silent updates
{isLoading && <Spinner />}
{error && <ErrorMessage>{error}</ErrorMessage>}

// ✅ Good - announced to screen readers
<div aria-live="polite" aria-atomic="true">
  {isLoading && <Spinner aria-label="Loading..." />}
  {error && <ErrorMessage role="alert">{error}</ErrorMessage>}
</div>

// ✅ Good - for important alerts
<div role="alert" aria-live="assertive">
  {criticalError}
</div>
```

#### Modal/Dialog Accessibility

```typescript
// ✅ Accessible modal pattern
<Dialog open={isOpen} onOpenChange={setIsOpen}>
  <DialogContent
    aria-labelledby="dialog-title"
    aria-describedby="dialog-description"
  >
    <DialogHeader>
      <DialogTitle id="dialog-title">Confirm Action</DialogTitle>
      <DialogDescription id="dialog-description">
        Are you sure you want to proceed?
      </DialogDescription>
    </DialogHeader>
    {/* Focus trapped inside dialog */}
    {/* Escape closes dialog */}
    {/* Focus returns to trigger on close */}
  </DialogContent>
</Dialog>
```

### 5. Audit Report Format

```markdown
# Accessibility Audit Report

**Component:** [ComponentName]
**Date:** [Date]
**WCAG Level:** AA

## Summary
- **Critical Issues:** X
- **Serious Issues:** X
- **Moderate Issues:** X
- **Minor Issues:** X

## Critical Issues (Must Fix)

### 1. [Issue Title]
- **WCAG Criterion:** X.X.X - [Name]
- **Location:** [file:line]
- **Description:** [What's wrong]
- **Impact:** [Who is affected]
- **Fix:**
  ```typescript
  // Before
  <bad code>

  // After
  <good code>
  ```

## Serious Issues

### 2. [Issue Title]
...

## Recommendations

1. [Recommendation 1]
2. [Recommendation 2]

## Passed Checks

- ✅ Color contrast meets requirements
- ✅ Form labels present
- ✅ Keyboard navigation works
```

### 6. Storybook Accessibility Tests

Add accessibility tests to stories:

```typescript
import type { Meta, StoryObj } from "@storybook/nextjs-vite";
import { expect, within } from "storybook/test";

const meta = {
  title: "Components/Button",
  component: Button,
  parameters: {
    a11y: {
      // axe-core configuration
      config: {
        rules: [
          { id: "color-contrast", enabled: true },
          { id: "button-name", enabled: true }
        ]
      }
    }
  }
} satisfies Meta<typeof Button>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Accessible: Story = {
  args: {
    children: "Click me"
  },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);

    // Verify button is accessible
    const button = canvas.getByRole("button", { name: /click me/i });
    await expect(button).toBeVisible();
    await expect(button).toBeEnabled();

    // Verify focus styles
    button.focus();
    await expect(button).toHaveFocus();
  }
};

export const WithIcon: Story = {
  args: {
    children: <Icon name="plus" />,
    "aria-label": "Add item"
  },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);

    // Icon button should be accessible via aria-label
    const button = canvas.getByRole("button", { name: /add item/i });
    await expect(button).toBeVisible();
  }
};
```

## Running Audits

```bash
# Run Storybook and check a11y panel
npm run storybook:dev

# Run Playwright a11y tests
npm run test:e2e -- tests/e2e/a11y/

# Generate a11y report
npm run test:e2e -- tests/e2e/a11y/ --reporter=html
```

## Best Practices

1. **Test with real assistive tech**: Use VoiceOver (Mac), NVDA (Windows)
2. **Keyboard-first development**: Navigate without mouse
3. **Use semantic HTML**: Right element for the job
4. **Don't disable focus styles**: Make them better instead
5. **Test at 200% zoom**: Content should remain usable
6. **Announce dynamic changes**: Use aria-live regions
7. **Provide alternatives**: Captions, transcripts, descriptions

## Questions to Ask

When performing an audit:

- What user actions does this component support?
- Are there any time-sensitive interactions?
- What happens on error states?
- Is there any dynamic content?
- Are there any custom interactive patterns?
- What's the expected screen reader experience?
