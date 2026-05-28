# Testing Guide

Guide de référence pour tester les composants du design system.

## Structure de Tests Recommandée

```
src/
└── components/
    └── Button/
        ├── Button.tsx
        ├── Button.module.css
        ├── Button.test.tsx       ← Unit tests
        ├── Button.a11y.test.tsx  ← Accessibility tests
        └── Button.stories.tsx    ← Storybook (visual)
```

## Configuration Jest + Testing Library

```js
// jest.config.js
module.exports = {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/jest.setup.ts'],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
    '\\.css$': 'identity-obj-proxy',
  },
  collectCoverageFrom: [
    'src/components/**/*.{ts,tsx}',
    '!src/components/**/*.stories.tsx',
  ],
};
```

```ts
// jest.setup.ts
import '@testing-library/jest-dom';
import { toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);
```

## Tests Unitaires - Button

```tsx
// Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Button } from './Button';

describe('Button', () => {
  // ═══════════════════════════════════════════════════════════════════
  // RENDERING
  // ═══════════════════════════════════════════════════════════════════

  it('renders with default props', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button', { name: 'Click me' })).toBeInTheDocument();
  });

  it('renders all variants correctly', () => {
    const variants = ['primary', 'secondary', 'ghost', 'destructive', 'outline'] as const;

    variants.forEach((variant) => {
      const { unmount } = render(<Button variant={variant}>Button</Button>);
      expect(screen.getByRole('button')).toHaveClass(`btn--${variant}`);
      unmount();
    });
  });

  it('renders all sizes correctly', () => {
    const sizes = ['xs', 'sm', 'md', 'lg', 'xl'] as const;

    sizes.forEach((size) => {
      const { unmount } = render(<Button size={size}>Button</Button>);
      expect(screen.getByRole('button')).toHaveClass(`btn--${size}`);
      unmount();
    });
  });

  // ═══════════════════════════════════════════════════════════════════
  // INTERACTIONS
  // ═══════════════════════════════════════════════════════════════════

  it('calls onClick when clicked', async () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);

    await userEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('does not call onClick when disabled', async () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick} disabled>Click me</Button>);

    await userEvent.click(screen.getByRole('button'));
    expect(handleClick).not.toHaveBeenCalled();
  });

  it('handles keyboard activation', async () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);

    screen.getByRole('button').focus();
    await userEvent.keyboard('{Enter}');
    expect(handleClick).toHaveBeenCalledTimes(1);

    await userEvent.keyboard(' ');
    expect(handleClick).toHaveBeenCalledTimes(2);
  });

  // ═══════════════════════════════════════════════════════════════════
  // STATES
  // ═══════════════════════════════════════════════════════════════════

  it('shows disabled state correctly', () => {
    render(<Button disabled>Disabled</Button>);
    const button = screen.getByRole('button');

    expect(button).toBeDisabled();
    expect(button).toHaveAttribute('aria-disabled', 'true');
  });

  it('shows loading state correctly', () => {
    render(<Button loading>Loading</Button>);
    const button = screen.getByRole('button');

    expect(button).toHaveAttribute('aria-busy', 'true');
    expect(screen.getByRole('status')).toBeInTheDocument(); // Spinner
  });

  it('disables interaction during loading', async () => {
    const handleClick = jest.fn();
    render(<Button loading onClick={handleClick}>Loading</Button>);

    await userEvent.click(screen.getByRole('button'));
    expect(handleClick).not.toHaveBeenCalled();
  });

  // ═══════════════════════════════════════════════════════════════════
  // ICONS
  // ═══════════════════════════════════════════════════════════════════

  it('renders with left icon', () => {
    render(<Button leftIcon={<span data-testid="icon">+</span>}>Add</Button>);

    expect(screen.getByTestId('icon')).toBeInTheDocument();
    expect(screen.getByText('Add')).toBeInTheDocument();
  });

  it('renders icon-only button correctly', () => {
    render(
      <Button aria-label="Add item" iconOnly>
        <span>+</span>
      </Button>
    );

    expect(screen.getByRole('button', { name: 'Add item' })).toBeInTheDocument();
  });

  // ═══════════════════════════════════════════════════════════════════
  // REFS & POLYMORPHISM
  // ═══════════════════════════════════════════════════════════════════

  it('forwards ref correctly', () => {
    const ref = jest.fn();
    render(<Button ref={ref}>Button</Button>);
    expect(ref).toHaveBeenCalledWith(expect.any(HTMLButtonElement));
  });

  it('renders as anchor when href is provided', () => {
    render(<Button href="/page">Link Button</Button>);
    expect(screen.getByRole('link', { name: 'Link Button' })).toHaveAttribute('href', '/page');
  });
});
```

## Tests Accessibilité

```tsx
// Button.a11y.test.tsx
import { render } from '@testing-library/react';
import { axe } from 'jest-axe';
import { Button } from './Button';

describe('Button Accessibility', () => {
  it('has no accessibility violations (default)', async () => {
    const { container } = render(<Button>Click me</Button>);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('has no accessibility violations (all variants)', async () => {
    const { container } = render(
      <div>
        <Button variant="primary">Primary</Button>
        <Button variant="secondary">Secondary</Button>
        <Button variant="ghost">Ghost</Button>
        <Button variant="destructive">Destructive</Button>
        <Button variant="outline">Outline</Button>
      </div>
    );
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('has no accessibility violations (disabled)', async () => {
    const { container } = render(<Button disabled>Disabled</Button>);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('has no accessibility violations (loading)', async () => {
    const { container } = render(<Button loading>Loading</Button>);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('has no accessibility violations (icon-only with label)', async () => {
    const { container } = render(
      <Button aria-label="Add item" iconOnly>
        +
      </Button>
    );
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  // Test focus visibility
  it('has visible focus indicator', () => {
    const { container } = render(<Button>Focus me</Button>);
    const button = container.querySelector('button');

    button?.focus();
    const styles = window.getComputedStyle(button!);

    // Vérifie que le focus ring est visible
    expect(styles.outline).not.toBe('none');
    // Ou vérifie la box-shadow si vous utilisez focus-ring
  });
});
```

## Tests Input

```tsx
// Input.test.tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Input } from './Input';

describe('Input', () => {
  it('renders with label', () => {
    render(<Input label="Email" id="email" />);
    expect(screen.getByLabelText('Email')).toBeInTheDocument();
  });

  it('handles value changes', async () => {
    const handleChange = jest.fn();
    render(<Input label="Email" onChange={handleChange} />);

    await userEvent.type(screen.getByRole('textbox'), 'test@example.com');
    expect(handleChange).toHaveBeenCalled();
  });

  it('shows error state', () => {
    render(<Input label="Email" error="Invalid email" />);

    expect(screen.getByRole('textbox')).toHaveAttribute('aria-invalid', 'true');
    expect(screen.getByText('Invalid email')).toBeInTheDocument();
  });

  it('shows helper text', () => {
    render(<Input label="Email" helperText="We won't share your email" />);
    expect(screen.getByText("We won't share your email")).toBeInTheDocument();
  });

  it('associates error with input via aria-describedby', () => {
    render(<Input label="Email" error="Invalid" id="email-input" />);

    const input = screen.getByRole('textbox');
    const errorId = input.getAttribute('aria-describedby');
    expect(document.getElementById(errorId!)).toHaveTextContent('Invalid');
  });
});
```

## Tests Badge

```tsx
// Badge.test.tsx
import { render, screen } from '@testing-library/react';
import { Badge, NotificationBadge, StatusBadge } from './Badge';

describe('Badge', () => {
  it('renders content', () => {
    render(<Badge>New</Badge>);
    expect(screen.getByText('New')).toBeInTheDocument();
  });

  it('renders all color variants', () => {
    const variants = ['default', 'primary', 'success', 'warning', 'error'] as const;

    variants.forEach((variant) => {
      const { unmount } = render(<Badge variant={variant}>Badge</Badge>);
      expect(screen.getByText('Badge')).toBeInTheDocument();
      unmount();
    });
  });
});

describe('NotificationBadge', () => {
  it('displays count', () => {
    render(
      <NotificationBadge count={5}>
        <span>Icon</span>
      </NotificationBadge>
    );
    expect(screen.getByText('5')).toBeInTheDocument();
  });

  it('caps count at max', () => {
    render(
      <NotificationBadge count={150} max={99}>
        <span>Icon</span>
      </NotificationBadge>
    );
    expect(screen.getByText('99+')).toBeInTheDocument();
  });

  it('renders dot variant', () => {
    render(
      <NotificationBadge dot>
        <span>Icon</span>
      </NotificationBadge>
    );
    expect(screen.queryByText(/\d/)).not.toBeInTheDocument();
  });

  it('has accessible label', () => {
    render(
      <NotificationBadge count={5}>
        <span>Icon</span>
      </NotificationBadge>
    );
    expect(screen.getByLabelText('5 notifications')).toBeInTheDocument();
  });
});

describe('StatusBadge', () => {
  it('renders status with correct color', () => {
    render(<StatusBadge status="active" />);
    expect(screen.getByText('Active')).toBeInTheDocument();
  });

  it('allows custom label', () => {
    render(<StatusBadge status="pending" label="En attente" />);
    expect(screen.getByText('En attente')).toBeInTheDocument();
  });
});
```

## Tests Visuels (Chromatic/Storybook)

```tsx
// Button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';

const meta: Meta<typeof Button> = {
  title: 'Atoms/Button',
  component: Button,
  parameters: {
    // Chromatic options
    chromatic: { viewports: [320, 768, 1200] },
  },
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'secondary', 'ghost', 'destructive', 'outline'],
    },
    size: {
      control: 'select',
      options: ['xs', 'sm', 'md', 'lg', 'xl'],
    },
  },
};

export default meta;
type Story = StoryObj<typeof Button>;

// ═══════════════════════════════════════════════════════════════════
// VARIANTS
// ═══════════════════════════════════════════════════════════════════

export const Primary: Story = {
  args: { variant: 'primary', children: 'Primary Button' },
};

export const Secondary: Story = {
  args: { variant: 'secondary', children: 'Secondary Button' },
};

export const AllVariants: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
      <Button variant="primary">Primary</Button>
      <Button variant="secondary">Secondary</Button>
      <Button variant="ghost">Ghost</Button>
      <Button variant="destructive">Destructive</Button>
      <Button variant="outline">Outline</Button>
    </div>
  ),
};

// ═══════════════════════════════════════════════════════════════════
// SIZES
// ═══════════════════════════════════════════════════════════════════

export const AllSizes: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
      <Button size="xs">XS</Button>
      <Button size="sm">SM</Button>
      <Button size="md">MD</Button>
      <Button size="lg">LG</Button>
      <Button size="xl">XL</Button>
    </div>
  ),
};

// ═══════════════════════════════════════════════════════════════════
// STATES
// ═══════════════════════════════════════════════════════════════════

export const States: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '1rem' }}>
      <Button>Default</Button>
      <Button disabled>Disabled</Button>
      <Button loading>Loading</Button>
    </div>
  ),
};

// Chromatic: capture hover/focus states
export const Hover: Story = {
  args: { children: 'Hover me' },
  parameters: { pseudo: { hover: true } },
};

export const Focus: Story = {
  args: { children: 'Focus me' },
  parameters: { pseudo: { focus: true } },
};
```

## Script de Test

```bash
#!/bin/bash
# run-tests.sh

echo "🧪 Running Design System Tests..."

# Unit tests
echo "\n📋 Unit Tests"
npm run test -- --coverage

# Accessibility tests
echo "\n♿ Accessibility Tests"
npm run test -- --testPathPattern=a11y

# Type checking
echo "\n📝 Type Check"
npm run typecheck

# Lint
echo "\n🔍 Lint"
npm run lint

# Storybook build (for visual regression)
echo "\n📚 Storybook Build"
npm run build-storybook

echo "\n✅ All tests completed!"
```

## Checklist Testing

- [ ] Tests unitaires pour chaque composant
- [ ] Tests de tous les variants et sizes
- [ ] Tests des états (disabled, loading, error)
- [ ] Tests d'interaction (click, keyboard, focus)
- [ ] Tests d'accessibilité avec jest-axe
- [ ] Tests de ref forwarding
- [ ] Tests aria-* attributes
- [ ] Stories Storybook pour documentation visuelle
- [ ] Visual regression avec Chromatic (optionnel)
- [ ] Coverage > 80%
