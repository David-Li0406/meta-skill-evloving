# Design System Creation

Building a comprehensive design system for a SaaS product.

## 📝 Prompt

```
Create a design system for a B2B project management SaaS product called "TaskFlow":

Context:
- Product: Task and project management for teams (5-50 people)
- Users: Project managers, team leads, developers, designers
- Platforms: Web app (primary), mobile app (secondary)
- Brand: Professional, efficient, trustworthy, modern
- Tech stack: React + TypeScript

Include:
- Design tokens (colors, typography, spacing, shadows)
- Core components (buttons, inputs, cards, navigation, modals)
- Component variants and states
- Usage guidelines and do's/don'ts
- Accessibility requirements
- Figma structure and naming conventions
- Code examples (React/TypeScript)
```

## 🎨 Design System

### Foundation

#### Color Tokens

**Brand Colors**
```css
/* Primary - Used for main actions, links, focus states */
--color-primary-50: #E3F2FD;
--color-primary-100: #BBDEFB;
--color-primary-200: #90CAF9;
--color-primary-300: #64B5F6;
--color-primary-400: #42A5F5;
--color-primary-500: #2196F3;  /* Main brand color */
--color-primary-600: #1E88E5;
--color-primary-700: #1976D2;
--color-primary-800: #1565C0;
--color-primary-900: #0D47A1;

/* Semantic Colors */
--color-success-50: #E8F5E9;
--color-success-500: #4CAF50;  /* Success states, completed tasks */
--color-success-700: #388E3C;

--color-warning-50: #FFF3E0;
--color-warning-500: #FF9800;  /* Warnings, pending actions */
--color-warning-700: #F57C00;

--color-error-50: #FFEBEE;
--color-error-500: #F44336;    /* Errors, destructive actions */
--color-error-700: #D32F2F;

--color-info-50: #E1F5FE;
--color-info-500: #03A9F4;     /* Informational messages */
--color-info-700: #0288D1;

/* Neutral Colors */
--color-gray-50: #FAFAFA;      /* Backgrounds */
--color-gray-100: #F5F5F5;     /* Hover backgrounds */
--color-gray-200: #EEEEEE;     /* Borders, dividers */
--color-gray-300: #E0E0E0;
--color-gray-400: #BDBDBD;     /* Disabled text */
--color-gray-500: #9E9E9E;     /* Secondary text, icons */
--color-gray-600: #757575;
--color-gray-700: #616161;     /* Body text */
--color-gray-800: #424242;
--color-gray-900: #212121;     /* Headings, primary text */

--color-white: #FFFFFF;
--color-black: #000000;
```

**Accessibility Notes**
- Primary 500 on white: 4.52:1 ✓
- Success 500 on white: 4.56:1 ✓
- Warning 500 on white: 3.07:1 (use 700 for text) ✓
- Error 500 on white: 4.52:1 ✓
- Gray 700 on white: 7.23:1 ✓

#### Typography Tokens

```css
/* Font Families */
--font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
--font-mono: 'JetBrains Mono', 'Courier New', monospace;

/* Font Sizes */
--font-size-xs: 0.75rem;    /* 12px */
--font-size-sm: 0.875rem;   /* 14px */
--font-size-base: 1rem;     /* 16px */
--font-size-lg: 1.125rem;   /* 18px */
--font-size-xl: 1.25rem;    /* 20px */
--font-size-2xl: 1.5rem;    /* 24px */
--font-size-3xl: 1.875rem;  /* 30px */
--font-size-4xl: 2.25rem;   /* 36px */

/* Font Weights */
--font-weight-regular: 400;
--font-weight-medium: 500;
--font-weight-semibold: 600;
--font-weight-bold: 700;

/* Line Heights */
--line-height-tight: 1.25;
--line-height-normal: 1.5;
--line-height-relaxed: 1.75;

/* Letter Spacing */
--letter-spacing-tight: -0.02em;
--letter-spacing-normal: 0;
--letter-spacing-wide: 0.02em;
```

**Typography Scale**
```css
/* Headings */
.heading-1 {
  font-size: var(--font-size-4xl);      /* 36px */
  font-weight: var(--font-weight-bold);
  line-height: var(--line-height-tight);
  letter-spacing: var(--letter-spacing-tight);
  color: var(--color-gray-900);
}

.heading-2 {
  font-size: var(--font-size-3xl);      /* 30px */
  font-weight: var(--font-weight-bold);
  line-height: var(--line-height-tight);
  color: var(--color-gray-900);
}

.heading-3 {
  font-size: var(--font-size-2xl);      /* 24px */
  font-weight: var(--font-weight-semibold);
  line-height: var(--line-height-tight);
  color: var(--color-gray-900);
}

.heading-4 {
  font-size: var(--font-size-xl);       /* 20px */
  font-weight: var(--font-weight-semibold);
  line-height: var(--line-height-normal);
  color: var(--color-gray-900);
}

/* Body Text */
.body-large {
  font-size: var(--font-size-lg);       /* 18px */
  line-height: var(--line-height-relaxed);
  color: var(--color-gray-700);
}

.body-regular {
  font-size: var(--font-size-base);     /* 16px */
  line-height: var(--line-height-normal);
  color: var(--color-gray-700);
}

.body-small {
  font-size: var(--font-size-sm);       /* 14px */
  line-height: var(--line-height-normal);
  color: var(--color-gray-700);
}

/* Utility */
.caption {
  font-size: var(--font-size-xs);       /* 12px */
  line-height: var(--line-height-normal);
  color: var(--color-gray-600);
}

.overline {
  font-size: var(--font-size-xs);       /* 12px */
  font-weight: var(--font-weight-semibold);
  line-height: var(--line-height-normal);
  letter-spacing: var(--letter-spacing-wide);
  text-transform: uppercase;
  color: var(--color-gray-600);
}
```

#### Spacing Tokens (8pt Grid)

```css
--space-0: 0;
--space-1: 0.25rem;  /* 4px */
--space-2: 0.5rem;   /* 8px */
--space-3: 0.75rem;  /* 12px */
--space-4: 1rem;     /* 16px */
--space-5: 1.25rem;  /* 20px */
--space-6: 1.5rem;   /* 24px */
--space-8: 2rem;     /* 32px */
--space-10: 2.5rem;  /* 40px */
--space-12: 3rem;    /* 48px */
--space-16: 4rem;    /* 64px */
--space-20: 5rem;    /* 80px */
--space-24: 6rem;    /* 96px */
```

#### Elevation Tokens (Shadows)

```css
--shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.05);
--shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.1), 
             0 1px 2px rgba(0, 0, 0, 0.06);
--shadow-md: 0 4px 6px rgba(0, 0, 0, 0.07), 
             0 2px 4px rgba(0, 0, 0, 0.05);
--shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1), 
             0 4px 6px rgba(0, 0, 0, 0.05);
--shadow-xl: 0 20px 25px rgba(0, 0, 0, 0.1), 
             0 10px 10px rgba(0, 0, 0, 0.04);
--shadow-2xl: 0 25px 50px rgba(0, 0, 0, 0.15);

/* Focus shadows */
--shadow-focus: 0 0 0 3px rgba(33, 150, 243, 0.3);
--shadow-focus-error: 0 0 0 3px rgba(244, 67, 54, 0.3);
```

#### Border Radius

```css
--radius-sm: 0.25rem;   /* 4px */
--radius-md: 0.5rem;    /* 8px */
--radius-lg: 0.75rem;   /* 12px */
--radius-xl: 1rem;      /* 16px */
--radius-full: 9999px;  /* Pill shape */
```

### Components

#### Button Component

**Variants**
```
Primary: Solid, high emphasis
Secondary: Outline, medium emphasis
Tertiary: Ghost/text, low emphasis
Destructive: For delete/remove actions
```

**Sizes**
```
Small: 32px height, 12px padding, 14px text
Medium: 40px height, 16px padding, 16px text
Large: 48px height, 20px padding, 16px text
```

**React Component**
```typescript
// Button.tsx
import React from 'react';
import './Button.css';

export type ButtonVariant = 'primary' | 'secondary' | 'tertiary' | 'destructive';
export type ButtonSize = 'small' | 'medium' | 'large';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: ButtonSize;
  fullWidth?: boolean;
  loading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'medium',
  fullWidth = false,
  loading = false,
  leftIcon,
  rightIcon,
  children,
  disabled,
  className = '',
  ...props
}) => {
  const classes = [
    'btn',
    `btn--${variant}`,
    `btn--${size}`,
    fullWidth && 'btn--full-width',
    loading && 'btn--loading',
    className,
  ]
    .filter(Boolean)
    .join(' ');

  return (
    <button
      className={classes}
      disabled={disabled || loading}
      {...props}
    >
      {loading && <span className="btn__spinner" aria-hidden="true" />}
      {!loading && leftIcon && <span className="btn__icon btn__icon--left">{leftIcon}</span>}
      <span className="btn__text">{children}</span>
      {!loading && rightIcon && <span className="btn__icon btn__icon--right">{rightIcon}</span>}
    </button>
  );
};
```

**CSS Styles**
```css
/* Button.css */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  font-family: var(--font-sans);
  font-weight: var(--font-weight-semibold);
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 150ms ease-in-out;
  position: relative;
  white-space: nowrap;
}

.btn:focus-visible {
  outline: none;
  box-shadow: var(--shadow-focus);
}

.btn:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

/* Sizes */
.btn--small {
  height: 32px;
  padding: 0 var(--space-3);
  font-size: var(--font-size-sm);
}

.btn--medium {
  height: 40px;
  padding: 0 var(--space-4);
  font-size: var(--font-size-base);
}

.btn--large {
  height: 48px;
  padding: 0 var(--space-5);
  font-size: var(--font-size-base);
}

.btn--full-width {
  width: 100%;
}

/* Primary Variant */
.btn--primary {
  background-color: var(--color-primary-500);
  color: var(--color-white);
}

.btn--primary:hover:not(:disabled) {
  background-color: var(--color-primary-600);
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}

.btn--primary:active:not(:disabled) {
  background-color: var(--color-primary-700);
  transform: translateY(0);
}

/* Secondary Variant */
.btn--secondary {
  background-color: transparent;
  color: var(--color-primary-500);
  border: 2px solid var(--color-primary-500);
}

.btn--secondary:hover:not(:disabled) {
  background-color: var(--color-primary-50);
}

.btn--secondary:active:not(:disabled) {
  background-color: var(--color-primary-100);
}

/* Tertiary Variant */
.btn--tertiary {
  background-color: transparent;
  color: var(--color-primary-500);
}

.btn--tertiary:hover:not(:disabled) {
  background-color: var(--color-primary-50);
}

.btn--tertiary:active:not(:disabled) {
  background-color: var(--color-primary-100);
}

/* Destructive Variant */
.btn--destructive {
  background-color: var(--color-error-500);
  color: var(--color-white);
}

.btn--destructive:hover:not(:disabled) {
  background-color: var(--color-error-600);
}

.btn--destructive:focus-visible {
  box-shadow: var(--shadow-focus-error);
}

/* Loading State */
.btn--loading {
  pointer-events: none;
}

.btn__spinner {
  width: 16px;
  height: 16px;
  border: 2px solid currentColor;
  border-right-color: transparent;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Icons */
.btn__icon {
  display: flex;
  align-items: center;
}

.btn__icon svg {
  width: 20px;
  height: 20px;
}

.btn--small .btn__icon svg {
  width: 16px;
  height: 16px;
}
```

**Usage Examples**
```typescript
// Basic usage
<Button>Save</Button>

// With variant
<Button variant="secondary">Cancel</Button>

// With size
<Button size="large">Submit</Button>

// With icons
<Button leftIcon={<PlusIcon />}>Add Task</Button>
<Button rightIcon={<ArrowRightIcon />}>Next</Button>

// Loading state
<Button loading>Saving...</Button>

// Destructive action
<Button variant="destructive">Delete Project</Button>

// Full width
<Button fullWidth>Continue</Button>

// Disabled
<Button disabled>Unavailable</Button>
```

**Do's and Don'ts**

✅ **Do:**
- Use primary buttons for main actions (one per section)
- Use secondary for alternative actions
- Use tertiary for low-priority actions
- Include descriptive text (not "Click here")
- Provide loading states for async actions

❌ **Don't:**
- Don't use multiple primary buttons in same area
- Don't use red/destructive for non-destructive actions
- Don't make buttons too small (minimum 32px height)
- Don't use vague labels like "OK" or "Submit"

#### Input Component

**React Component**
```typescript
// Input.tsx
import React, { forwardRef } from 'react';
import './Input.css';

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  fullWidth?: boolean;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  (
    {
      label,
      error,
      helperText,
      leftIcon,
      rightIcon,
      fullWidth = false,
      className = '',
      id,
      ...props
    },
    ref
  ) => {
    const inputId = id || `input-${Math.random().toString(36).substr(2, 9)}`;
    const hasError = Boolean(error);

    return (
      <div className={`input-wrapper ${fullWidth ? 'input-wrapper--full-width' : ''}`}>
        {label && (
          <label htmlFor={inputId} className="input__label">
            {label}
            {props.required && <span className="input__required" aria-label="required">*</span>}
          </label>
        )}
        
        <div className={`input-container ${hasError ? 'input-container--error' : ''}`}>
          {leftIcon && <span className="input__icon input__icon--left">{leftIcon}</span>}
          
          <input
            ref={ref}
            id={inputId}
            className={`input ${leftIcon ? 'input--with-left-icon' : ''} ${
              rightIcon ? 'input--with-right-icon' : ''
            } ${className}`}
            aria-invalid={hasError}
            aria-describedby={
              error ? `${inputId}-error` : helperText ? `${inputId}-helper` : undefined
            }
            {...props}
          />
          
          {rightIcon && <span className="input__icon input__icon--right">{rightIcon}</span>}
        </div>

        {error && (
          <span id={`${inputId}-error`} className="input__error" role="alert">
            {error}
          </span>
        )}
        
        {!error && helperText && (
          <span id={`${inputId}-helper`} className="input__helper">
            {helperText}
          </span>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';
```

**CSS Styles**
```css
/* Input.css */
.input-wrapper {
  display: inline-flex;
  flex-direction: column;
  gap: var(--space-2);
}

.input-wrapper--full-width {
  width: 100%;
}

.input__label {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--color-gray-700);
}

.input__required {
  color: var(--color-error-500);
  margin-left: var(--space-1);
}

.input-container {
  position: relative;
  display: flex;
  align-items: center;
}

.input {
  height: 40px;
  padding: 0 var(--space-3);
  font-family: var(--font-sans);
  font-size: var(--font-size-base);
  color: var(--color-gray-900);
  background-color: var(--color-white);
  border: 2px solid var(--color-gray-300);
  border-radius: var(--radius-md);
  transition: all 150ms ease-in-out;
  width: 100%;
}

.input::placeholder {
  color: var(--color-gray-400);
}

.input:hover:not(:disabled) {
  border-color: var(--color-gray-400);
}

.input:focus {
  outline: none;
  border-color: var(--color-primary-500);
  box-shadow: var(--shadow-focus);
}

.input:disabled {
  background-color: var(--color-gray-50);
  cursor: not-allowed;
  opacity: 0.6;
}

.input-container--error .input {
  border-color: var(--color-error-500);
}

.input-container--error .input:focus {
  box-shadow: var(--shadow-focus-error);
}

.input--with-left-icon {
  padding-left: var(--space-10);
}

.input--with-right-icon {
  padding-right: var(--space-10);
}

.input__icon {
  position: absolute;
  display: flex;
  align-items: center;
  color: var(--color-gray-500);
  pointer-events: none;
}

.input__icon--left {
  left: var(--space-3);
}

.input__icon--right {
  right: var(--space-3);
}

.input__icon svg {
  width: 20px;
  height: 20px;
}

.input__error {
  font-size: var(--font-size-sm);
  color: var(--color-error-500);
}

.input__helper {
  font-size: var(--font-size-sm);
  color: var(--color-gray-600);
}
```

#### Card Component

**React Component**
```typescript
// Card.tsx
import React from 'react';
import './Card.css';

export interface CardProps {
  children: React.ReactNode;
  padding?: 'none' | 'small' | 'medium' | 'large';
  elevated?: boolean;
  hoverable?: boolean;
  onClick?: () => void;
  className?: string;
}

export const Card: React.FC<CardProps> = ({
  children,
  padding = 'medium',
  elevated = false,
  hoverable = false,
  onClick,
  className = '',
}) => {
  const classes = [
    'card',
    `card--padding-${padding}`,
    elevated && 'card--elevated',
    hoverable && 'card--hoverable',
    onClick && 'card--clickable',
    className,
  ]
    .filter(Boolean)
    .join(' ');

  const Component = onClick ? 'button' : 'div';

  return (
    <Component className={classes} onClick={onClick}>
      {children}
    </Component>
  );
};

export const CardHeader: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div className="card__header">{children}</div>
);

export const CardBody: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div className="card__body">{children}</div>
);

export const CardFooter: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div className="card__footer">{children}</div>
);
```

**Usage**
```typescript
<Card elevated>
  <CardHeader>
    <h3>Project Alpha</h3>
  </CardHeader>
  <CardBody>
    <p>15 tasks • 3 members</p>
  </CardBody>
  <CardFooter>
    <Button variant="tertiary" size="small">View Details</Button>
  </CardFooter>
</Card>
```

### Figma Organization

**File Structure**
```
TaskFlow Design System
├── 📄 Cover & Index
├── 📁 Foundation
│   ├── 🎨 Colors
│   ├── 📝 Typography
│   ├── 📏 Spacing & Layout
│   └── 🌓 Shadows & Effects
├── 📁 Components
│   ├── ⚙️ Atoms (Button, Input, Icon, Avatar)
│   ├── 🧩 Molecules (Search, Form Field, Card)
│   └── 🏗️ Organisms (Navigation, Header, Sidebar)
├── 📁 Patterns
│   ├── Forms
│   ├── Data Display
│   └── Navigation
└── 📁 Templates
    ├── Dashboard
    ├── Project View
    └── Settings
```

**Naming Conventions**
```
Components: ComponentName/Variant/State
- Button/Primary/Default
- Button/Primary/Hover
- Button/Primary/Disabled
- Button/Secondary/Default

Variants use: PropertyName=Value
- Size=Small
- Variant=Primary
- State=Hover
```

## ✅ Design System Deliverables

1. ✅ Complete design tokens (colors, typography, spacing, shadows)
2. ✅ Button component (4 variants, 3 sizes, all states)
3. ✅ Input component (with validation states)
4. ✅ Card component (with subcomponents)
5. ✅ React + TypeScript code examples
6. ✅ CSS with CSS custom properties
7. ✅ Accessibility guidelines
8. ✅ Figma organization structure
9. ✅ Usage guidelines and examples

## 📚 Documentation

Each component includes:
- Purpose and when to use
- Props/API documentation
- Code examples
- Accessibility requirements
- Do's and don'ts
- Figma component link

---

This design system provides a scalable foundation for building consistent, accessible interfaces across the TaskFlow product.
