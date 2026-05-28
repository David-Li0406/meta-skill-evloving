# Testing Command Palettes

Unit testing with Vitest/Jest + React Testing Library, E2E with Playwright, and performance testing.

## Unit Testing with Vitest + RTL

### Setup

```bash
npm install -D vitest @testing-library/react @testing-library/user-event jsdom
```

### Basic Test

```typescript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { CommandPalette } from './CommandPalette';

describe('CommandPalette', () => {
  it('opens on ⌘K', async () => {
    const user = userEvent.setup();
    render(<CommandPalette />);

    await user.keyboard('{Meta>}k{/Meta}');

    expect(screen.getByPlaceholderText(/search/i)).toBeInTheDocument();
  });

  it('filters commands on search', async () => {
    const user = userEvent.setup();
    render(<CommandPalette />);

    const input = screen.getByRole('combobox');
    await user.type(input, 'create');

    expect(screen.getByText('Create Task')).toBeInTheDocument();
    expect(screen.queryByText('Delete Item')).not.toBeInTheDocument();
  });

  it('executes command on Enter', async () => {
    const user = userEvent.setup();
    const onSelect = vi.fn();
    render(<CommandPalette commands={[{ id: '1', label: 'Test', onSelect }]} />);

    await user.keyboard('{Enter}');

    expect(onSelect).toHaveBeenCalled();
  });
});
```

## E2E Testing with Playwright

### Setup

```bash
npm install -D @playwright/test
npx playwright install
```

### E2E Test

```typescript
import { test, expect } from '@playwright/test';

test.describe('Command Palette', () => {
  test('opens and closes with keyboard', async ({ page }) => {
    await page.goto('http://localhost:3000');

    await page.keyboard.press('Meta+K');
    await expect(page.locator('[role="dialog"]')).toBeVisible();

    await page.keyboard.press('Escape');
    await expect(page.locator('[role="dialog"]')).not.toBeVisible();
  });

  test('search and navigate with arrows', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await page.keyboard.press('Meta+K');

    await page.fill('[role="combobox"]', 'task');
    await page.keyboard.press('ArrowDown');
    await page.keyboard.press('Enter');

    await expect(page).toHaveURL(/.*tasks/);
  });
});
```

## Performance Testing

```typescript
test('handles 10,000 items without lag', async () => {
  const items = Array.from({ length: 10000 }, (_, i) => ({
    id: `${i}`,
    label: `Item ${i}`,
  }));

  const { container } = render(<VirtualizedPalette items={items} />);

  // Should render only visible items
  const renderedItems = container.querySelectorAll('[data-item]');
  expect(renderedItems.length).toBeLessThan(50); // ~20-30 visible items
});
```
