---
id: ui-component-library
name: "UI Component Library"
domain: DEV
skill: faion-software-developer
category: "development"
---

# UI Component Library

## Overview

A UI component library provides reusable, consistent interface elements that accelerate development and ensure design consistency across applications. This includes atomic components, compound components, and design system integration.

## When to Use

- Building consistent user interfaces across products
- Team collaboration on frontend development
- Scaling design systems
- Reducing code duplication
- Ensuring accessibility compliance

## Key Principles

- **Composition over configuration**: Compose simple components
- **Single responsibility**: Each component does one thing well
- **Accessibility first**: Built-in ARIA support
- **Consistent API**: Predictable props across components
- **Customizable**: Allow theming and style overrides

## Best Practices

### Component Structure

```
src/
├── components/
│   ├── primitives/          # Basic building blocks
│   │   ├── Button/
│   │   │   ├── Button.tsx
│   │   │   ├── Button.test.tsx
│   │   │   ├── Button.stories.tsx
│   │   │   └── index.ts
│   │   ├── Input/
│   │   ├── Text/
│   │   └── Box/
│   │
│   ├── composite/           # Composed from primitives
│   │   ├── Card/
│   │   ├── Modal/
│   │   ├── Dropdown/
│   │   └── Form/
│   │
│   ├── patterns/            # Common UI patterns
│   │   ├── DataTable/
│   │   ├── Pagination/
│   │   └── SearchInput/
│   │
│   └── layout/              # Layout components
│       ├── Container/
│       ├── Stack/
│       ├── Grid/
│       └── Flex/
│
├── hooks/                   # Shared hooks
├── utils/                   # Utilities
├── tokens/                  # Design tokens
└── index.ts                 # Public exports
```

### Button Component Example

```tsx
// components/primitives/Button/Button.tsx
import { forwardRef, ButtonHTMLAttributes, ReactNode } from 'react';
import { clsx } from 'clsx';
import { Slot } from '@radix-ui/react-slot';
import styles from './Button.module.css';

export type ButtonVariant = 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger';
export type ButtonSize = 'sm' | 'md' | 'lg';

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  /** Visual variant of the button */
  variant?: ButtonVariant;
  /** Size of the button */
  size?: ButtonSize;
  /** Whether the button takes full width */
  fullWidth?: boolean;
  /** Loading state */
  isLoading?: boolean;
  /** Left icon */
  leftIcon?: ReactNode;
  /** Right icon */
  rightIcon?: ReactNode;
  /** Render as child element (for links styled as buttons) */
  asChild?: boolean;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      variant = 'primary',
      size = 'md',
      fullWidth = false,
      isLoading = false,
      leftIcon,
      rightIcon,
      asChild = false,
      className,
      disabled,
      children,
      ...props
    },
    ref
  ) => {
    const Comp = asChild ? Slot : 'button';

    return (
      <Comp
        ref={ref}
        className={clsx(
          styles.button,
          styles[variant],
          styles[size],
          fullWidth && styles.fullWidth,
          isLoading && styles.loading,
          className
        )}
        disabled={disabled || isLoading}
        {...props}
      >
        {isLoading && (
          <span className={styles.spinner} aria-hidden="true">
            <LoadingSpinner size={size} />
          </span>
        )}
        {leftIcon && !isLoading && (
          <span className={styles.icon} aria-hidden="true">
            {leftIcon}
          </span>
        )}
        <span className={styles.content}>{children}</span>
        {rightIcon && (
          <span className={styles.icon} aria-hidden="true">
            {rightIcon}
          </span>
        )}
      </Comp>
    );
  }
);

Button.displayName = 'Button';
```

```css
/* Button.module.css */
.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-family: inherit;
  font-weight: 500;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
}

.button:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
}

.button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Variants */
.primary {
  background: var(--color-primary);
  color: var(--color-primary-foreground);
  border: none;
}

.primary:hover:not(:disabled) {
  background: var(--color-primary-hover);
}

.secondary {
  background: var(--color-secondary);
  color: var(--color-secondary-foreground);
  border: none;
}

.outline {
  background: transparent;
  color: var(--color-foreground);
  border: 1px solid var(--color-border);
}

.outline:hover:not(:disabled) {
  background: var(--color-muted);
}

.ghost {
  background: transparent;
  color: var(--color-foreground);
  border: none;
}

.ghost:hover:not(:disabled) {
  background: var(--color-muted);
}

.danger {
  background: var(--color-danger);
  color: var(--color-danger-foreground);
  border: none;
}

/* Sizes */
.sm {
  height: 2rem;
  padding: 0 0.75rem;
  font-size: 0.875rem;
}

.md {
  height: 2.5rem;
  padding: 0 1rem;
  font-size: 1rem;
}

.lg {
  height: 3rem;
  padding: 0 1.5rem;
  font-size: 1.125rem;
}

.fullWidth {
  width: 100%;
}

/* Loading state */
.loading .content {
  opacity: 0;
}

.spinner {
  position: absolute;
}
```

### Compound Component Pattern

```tsx
// components/composite/Card/Card.tsx
import { createContext, useContext, ReactNode } from 'react';
import { clsx } from 'clsx';
import styles from './Card.module.css';

interface CardContextValue {
  variant: 'default' | 'elevated' | 'outlined';
}

const CardContext = createContext<CardContextValue | null>(null);

function useCardContext() {
  const context = useContext(CardContext);
  if (!context) {
    throw new Error('Card compound components must be used within Card');
  }
  return context;
}

// Root component
interface CardProps {
  children: ReactNode;
  variant?: 'default' | 'elevated' | 'outlined';
  className?: string;
}

function CardRoot({ children, variant = 'default', className }: CardProps) {
  return (
    <CardContext.Provider value={{ variant }}>
      <article className={clsx(styles.card, styles[variant], className)}>
        {children}
      </article>
    </CardContext.Provider>
  );
}

// Sub-components
function CardHeader({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <header className={clsx(styles.header, className)}>
      {children}
    </header>
  );
}

function CardTitle({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <h3 className={clsx(styles.title, className)}>
      {children}
    </h3>
  );
}

function CardDescription({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <p className={clsx(styles.description, className)}>
      {children}
    </p>
  );
}

function CardContent({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <div className={clsx(styles.content, className)}>
      {children}
    </div>
  );
}

function CardFooter({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <footer className={clsx(styles.footer, className)}>
      {children}
    </footer>
  );
}

function CardImage({ src, alt, className }: { src: string; alt: string; className?: string }) {
  return (
    <div className={clsx(styles.imageContainer, className)}>
      <img src={src} alt={alt} className={styles.image} />
    </div>
  );
}

// Export compound component
export const Card = Object.assign(CardRoot, {
  Header: CardHeader,
  Title: CardTitle,
  Description: CardDescription,
  Content: CardContent,
  Footer: CardFooter,
  Image: CardImage,
});

// Usage
function ProductCard({ product }: { product: Product }) {
  return (
    <Card variant="elevated">
      <Card.Image src={product.image} alt={product.name} />
      <Card.Header>
        <Card.Title>{product.name}</Card.Title>
        <Card.Description>{product.category}</Card.Description>
      </Card.Header>
      <Card.Content>
        <p>{product.description}</p>
        <p className="price">${product.price}</p>
      </Card.Content>
      <Card.Footer>
        <Button variant="primary">Add to Cart</Button>
        <Button variant="ghost">View Details</Button>
      </Card.Footer>
    </Card>
  );
}
```

### Input Component with Validation

```tsx
// components/primitives/Input/Input.tsx
import { forwardRef, InputHTMLAttributes, ReactNode, useId } from 'react';
import { clsx } from 'clsx';
import styles from './Input.module.css';

export interface InputProps extends Omit<InputHTMLAttributes<HTMLInputElement>, 'size'> {
  /** Label for the input */
  label?: string;
  /** Helper text below the input */
  helperText?: string;
  /** Error message */
  error?: string;
  /** Size variant */
  size?: 'sm' | 'md' | 'lg';
  /** Left addon */
  leftAddon?: ReactNode;
  /** Right addon */
  rightAddon?: ReactNode;
  /** Whether the field is required */
  required?: boolean;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  (
    {
      label,
      helperText,
      error,
      size = 'md',
      leftAddon,
      rightAddon,
      required,
      className,
      id: providedId,
      ...props
    },
    ref
  ) => {
    const generatedId = useId();
    const id = providedId || generatedId;
    const helperId = `${id}-helper`;
    const errorId = `${id}-error`;

    return (
      <div className={clsx(styles.wrapper, className)}>
        {label && (
          <label htmlFor={id} className={styles.label}>
            {label}
            {required && <span className={styles.required} aria-hidden="true">*</span>}
          </label>
        )}

        <div className={clsx(styles.inputWrapper, error && styles.hasError)}>
          {leftAddon && (
            <span className={styles.addon}>{leftAddon}</span>
          )}

          <input
            ref={ref}
            id={id}
            className={clsx(styles.input, styles[size])}
            aria-invalid={!!error}
            aria-describedby={
              error ? errorId : helperText ? helperId : undefined
            }
            aria-required={required}
            {...props}
          />

          {rightAddon && (
            <span className={styles.addon}>{rightAddon}</span>
          )}
        </div>

        {error && (
          <span id={errorId} className={styles.error} role="alert">
            {error}
          </span>
        )}

        {helperText && !error && (
          <span id={helperId} className={styles.helperText}>
            {helperText}
          </span>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';
```

### Modal with Portal

```tsx
// components/composite/Modal/Modal.tsx
import { ReactNode, useEffect, useCallback } from 'react';
import { createPortal } from 'react-dom';
import { clsx } from 'clsx';
import { Button } from '../../primitives/Button';
import styles from './Modal.module.css';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  description?: string;
  children: ReactNode;
  footer?: ReactNode;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  closeOnOverlayClick?: boolean;
  closeOnEscape?: boolean;
}

export function Modal({
  isOpen,
  onClose,
  title,
  description,
  children,
  footer,
  size = 'md',
  closeOnOverlayClick = true,
  closeOnEscape = true,
}: ModalProps) {
  // Handle escape key
  const handleKeyDown = useCallback(
    (event: KeyboardEvent) => {
      if (closeOnEscape && event.key === 'Escape') {
        onClose();
      }
    },
    [closeOnEscape, onClose]
  );

  // Lock body scroll when open
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
      document.addEventListener('keydown', handleKeyDown);

      return () => {
        document.body.style.overflow = '';
        document.removeEventListener('keydown', handleKeyDown);
      };
    }
  }, [isOpen, handleKeyDown]);

  if (!isOpen) return null;

  return createPortal(
    <div className={styles.overlay} onClick={closeOnOverlayClick ? onClose : undefined}>
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title"
        aria-describedby={description ? 'modal-description' : undefined}
        className={clsx(styles.modal, styles[size])}
        onClick={(e) => e.stopPropagation()}
      >
        <header className={styles.header}>
          <h2 id="modal-title" className={styles.title}>
            {title}
          </h2>
          <Button
            variant="ghost"
            size="sm"
            onClick={onClose}
            aria-label="Close modal"
          >
            <CloseIcon />
          </Button>
        </header>

        {description && (
          <p id="modal-description" className={styles.description}>
            {description}
          </p>
        )}

        <div className={styles.content}>{children}</div>

        {footer && <footer className={styles.footer}>{footer}</footer>}
      </div>
    </div>,
    document.body
  );
}

// Usage
function DeleteConfirmModal({ isOpen, onClose, onConfirm, itemName }) {
  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="Delete Item"
      description={`Are you sure you want to delete "${itemName}"? This action cannot be undone.`}
      size="sm"
      footer={
        <>
          <Button variant="outline" onClick={onClose}>
            Cancel
          </Button>
          <Button variant="danger" onClick={onConfirm}>
            Delete
          </Button>
        </>
      }
    >
      {/* Additional content if needed */}
    </Modal>
  );
}
```

### Component Documentation

```tsx
// Button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';
import { ArrowRightIcon, DownloadIcon } from '../icons';

const meta: Meta<typeof Button> = {
  title: 'Primitives/Button',
  component: Button,
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'secondary', 'outline', 'ghost', 'danger'],
      description: 'Visual style variant',
    },
    size: {
      control: 'select',
      options: ['sm', 'md', 'lg'],
    },
    isLoading: {
      control: 'boolean',
    },
    disabled: {
      control: 'boolean',
    },
    fullWidth: {
      control: 'boolean',
    },
  },
};

export default meta;
type Story = StoryObj<typeof Button>;

export const Primary: Story = {
  args: {
    children: 'Primary Button',
    variant: 'primary',
  },
};

export const AllVariants: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
      <Button variant="primary">Primary</Button>
      <Button variant="secondary">Secondary</Button>
      <Button variant="outline">Outline</Button>
      <Button variant="ghost">Ghost</Button>
      <Button variant="danger">Danger</Button>
    </div>
  ),
};

export const WithIcons: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '1rem' }}>
      <Button leftIcon={<DownloadIcon />}>Download</Button>
      <Button rightIcon={<ArrowRightIcon />}>Continue</Button>
    </div>
  ),
};

export const Loading: Story = {
  args: {
    children: 'Loading...',
    isLoading: true,
  },
};

export const AsLink: Story = {
  render: () => (
    <Button asChild>
      <a href="/dashboard">Go to Dashboard</a>
    </Button>
  ),
};
```

## Anti-patterns

- **Prop explosion**: Too many props making components hard to use
- **Tight coupling**: Components depending on specific parent structure
- **Inconsistent API**: Different prop names for same concept
- **Missing accessibility**: No ARIA attributes or keyboard support
- **Over-abstraction**: Components that are too generic to be useful
- **CSS leakage**: Styles affecting elements outside component

## References

- [Radix UI](https://www.radix-ui.com/)
- [shadcn/ui](https://ui.shadcn.com/)
- [Storybook](https://storybook.js.org/)
- [React Aria](https://react-spectrum.adobe.com/react-aria/)
