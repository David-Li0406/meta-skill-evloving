---
id: tailwind-patterns
name: "Tailwind Patterns"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Tailwind Patterns

## Overview

Tailwind CSS is a utility-first CSS framework that provides low-level utility classes for building custom designs. This methodology covers effective patterns for using Tailwind, including component extraction, responsive design, and customization.

## When to Use

- Rapid UI development
- Custom design implementations
- Component-based architectures
- Design systems with utility classes
- Projects preferring utility-first approach

## Key Principles

- **Utility-first**: Compose designs from utility classes
- **Component extraction**: Extract repeated patterns
- **Design tokens via config**: Customize through tailwind.config
- **Responsive by default**: Mobile-first breakpoints
- **State variants**: hover, focus, active via modifiers

## Best Practices

### Basic Component Patterns

```tsx
// Button component with Tailwind
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

// Utility for merging Tailwind classes
function cn(...inputs: (string | undefined | null | boolean)[]) {
  return twMerge(clsx(inputs));
}

// Variant configuration
const buttonVariants = {
  variant: {
    primary: 'bg-blue-600 text-white hover:bg-blue-700 active:bg-blue-800',
    secondary: 'bg-gray-100 text-gray-900 hover:bg-gray-200 active:bg-gray-300',
    outline: 'border border-gray-300 bg-transparent hover:bg-gray-50',
    ghost: 'bg-transparent hover:bg-gray-100',
    danger: 'bg-red-600 text-white hover:bg-red-700 active:bg-red-800',
  },
  size: {
    sm: 'h-8 px-3 text-sm',
    md: 'h-10 px-4 text-base',
    lg: 'h-12 px-6 text-lg',
  },
};

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: keyof typeof buttonVariants.variant;
  size?: keyof typeof buttonVariants.size;
}

export function Button({
  variant = 'primary',
  size = 'md',
  className,
  children,
  ...props
}: ButtonProps) {
  return (
    <button
      className={cn(
        // Base styles
        'inline-flex items-center justify-center font-medium',
        'rounded-md transition-colors duration-200',
        'focus-visible:outline-none focus-visible:ring-2',
        'focus-visible:ring-blue-500 focus-visible:ring-offset-2',
        'disabled:opacity-50 disabled:cursor-not-allowed',
        // Variant styles
        buttonVariants.variant[variant],
        buttonVariants.size[size],
        // Custom overrides
        className
      )}
      {...props}
    >
      {children}
    </button>
  );
}

// Usage
<Button variant="primary" size="lg">
  Click me
</Button>

<Button variant="outline" className="w-full">
  Full width
</Button>
```

### Class Variance Authority (CVA)

```tsx
// Using cva for type-safe variants
import { cva, type VariantProps } from 'class-variance-authority';

const buttonVariants = cva(
  // Base styles
  [
    'inline-flex items-center justify-center font-medium',
    'rounded-md transition-colors duration-200',
    'focus-visible:outline-none focus-visible:ring-2',
    'focus-visible:ring-blue-500 focus-visible:ring-offset-2',
    'disabled:opacity-50 disabled:cursor-not-allowed',
  ],
  {
    variants: {
      variant: {
        primary: 'bg-blue-600 text-white hover:bg-blue-700',
        secondary: 'bg-gray-100 text-gray-900 hover:bg-gray-200',
        outline: 'border border-gray-300 bg-transparent hover:bg-gray-50',
        ghost: 'bg-transparent hover:bg-gray-100',
        danger: 'bg-red-600 text-white hover:bg-red-700',
        link: 'text-blue-600 underline-offset-4 hover:underline',
      },
      size: {
        sm: 'h-8 px-3 text-sm',
        md: 'h-10 px-4 text-base',
        lg: 'h-12 px-6 text-lg',
        icon: 'h-10 w-10',
      },
    },
    compoundVariants: [
      {
        variant: 'outline',
        size: 'sm',
        className: 'border',
      },
    ],
    defaultVariants: {
      variant: 'primary',
      size: 'md',
    },
  }
);

type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement> &
  VariantProps<typeof buttonVariants> & {
    asChild?: boolean;
  };

export function Button({
  variant,
  size,
  className,
  children,
  ...props
}: ButtonProps) {
  return (
    <button
      className={cn(buttonVariants({ variant, size }), className)}
      {...props}
    >
      {children}
    </button>
  );
}
```

### Responsive Patterns

```tsx
// Responsive grid
function ProductGrid({ products }) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 md:gap-6">
      {products.map((product) => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  );
}

// Responsive navigation
function Navigation() {
  return (
    <nav className="flex flex-col md:flex-row md:items-center gap-4">
      <a href="/" className="text-lg font-semibold">
        Logo
      </a>

      {/* Mobile: column, Desktop: row */}
      <div className="flex flex-col md:flex-row gap-2 md:gap-4">
        <a href="/products" className="hover:text-blue-600">Products</a>
        <a href="/about" className="hover:text-blue-600">About</a>
        <a href="/contact" className="hover:text-blue-600">Contact</a>
      </div>

      {/* Hidden on mobile, visible on desktop */}
      <div className="hidden md:flex md:ml-auto gap-2">
        <Button variant="ghost" size="sm">Sign In</Button>
        <Button size="sm">Sign Up</Button>
      </div>
    </nav>
  );
}

// Responsive typography
function Hero() {
  return (
    <section className="text-center py-12 md:py-20 lg:py-32">
      <h1 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-bold">
        Build faster
      </h1>
      <p className="mt-4 text-lg md:text-xl text-gray-600 max-w-2xl mx-auto">
        Create beautiful websites with utility-first CSS
      </p>
    </section>
  );
}
```

### Component Composition

```tsx
// Card component with composable parts
interface CardProps {
  children: React.ReactNode;
  className?: string;
}

function Card({ children, className }: CardProps) {
  return (
    <div
      className={cn(
        'rounded-lg border border-gray-200 bg-white shadow-sm',
        className
      )}
    >
      {children}
    </div>
  );
}

function CardHeader({ children, className }: CardProps) {
  return (
    <div className={cn('p-4 md:p-6 border-b border-gray-200', className)}>
      {children}
    </div>
  );
}

function CardTitle({ children, className }: CardProps) {
  return (
    <h3 className={cn('text-lg font-semibold text-gray-900', className)}>
      {children}
    </h3>
  );
}

function CardContent({ children, className }: CardProps) {
  return <div className={cn('p-4 md:p-6', className)}>{children}</div>;
}

function CardFooter({ children, className }: CardProps) {
  return (
    <div
      className={cn(
        'p-4 md:p-6 border-t border-gray-200 flex items-center gap-2',
        className
      )}
    >
      {children}
    </div>
  );
}

// Usage
<Card>
  <CardHeader>
    <CardTitle>Payment Method</CardTitle>
  </CardHeader>
  <CardContent>
    <p className="text-gray-600">Add a new payment method to your account.</p>
  </CardContent>
  <CardFooter>
    <Button variant="outline">Cancel</Button>
    <Button>Save</Button>
  </CardFooter>
</Card>
```

### Form Patterns

```tsx
// Input component
const inputVariants = cva(
  [
    'w-full rounded-md border bg-white px-3 py-2',
    'text-sm text-gray-900 placeholder:text-gray-400',
    'focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
    'disabled:bg-gray-100 disabled:cursor-not-allowed',
  ],
  {
    variants: {
      state: {
        default: 'border-gray-300',
        error: 'border-red-500 focus:ring-red-500',
        success: 'border-green-500 focus:ring-green-500',
      },
    },
    defaultVariants: {
      state: 'default',
    },
  }
);

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  hint?: string;
}

function Input({
  label,
  error,
  hint,
  id,
  className,
  ...props
}: InputProps) {
  const inputId = id || label?.toLowerCase().replace(/\s/g, '-');

  return (
    <div className="space-y-1">
      {label && (
        <label
          htmlFor={inputId}
          className="block text-sm font-medium text-gray-700"
        >
          {label}
          {props.required && <span className="text-red-500 ml-1">*</span>}
        </label>
      )}

      <input
        id={inputId}
        className={cn(
          inputVariants({ state: error ? 'error' : 'default' }),
          className
        )}
        aria-invalid={!!error}
        aria-describedby={error ? `${inputId}-error` : hint ? `${inputId}-hint` : undefined}
        {...props}
      />

      {error && (
        <p id={`${inputId}-error`} className="text-sm text-red-600">
          {error}
        </p>
      )}

      {hint && !error && (
        <p id={`${inputId}-hint`} className="text-sm text-gray-500">
          {hint}
        </p>
      )}
    </div>
  );
}

// Form usage
<form className="space-y-4">
  <Input
    label="Email"
    type="email"
    placeholder="you@example.com"
    required
  />
  <Input
    label="Password"
    type="password"
    error="Password must be at least 8 characters"
    required
  />
  <Button type="submit" className="w-full">
    Sign In
  </Button>
</form>
```

### Dark Mode

```tsx
// tailwind.config.js
module.exports = {
  darkMode: 'class', // or 'media'
  // ...
};

// Component with dark mode
function Card({ children }) {
  return (
    <div
      className={cn(
        // Light mode
        'bg-white border-gray-200 text-gray-900',
        // Dark mode
        'dark:bg-gray-800 dark:border-gray-700 dark:text-gray-100',
        // Common
        'rounded-lg border p-4'
      )}
    >
      {children}
    </div>
  );
}

// Dark mode toggle
function ThemeToggle() {
  const [isDark, setIsDark] = useState(false);

  useEffect(() => {
    document.documentElement.classList.toggle('dark', isDark);
  }, [isDark]);

  return (
    <button
      onClick={() => setIsDark(!isDark)}
      className={cn(
        'p-2 rounded-md',
        'bg-gray-100 dark:bg-gray-800',
        'text-gray-600 dark:text-gray-400',
        'hover:bg-gray-200 dark:hover:bg-gray-700'
      )}
    >
      {isDark ? '☀️' : '🌙'}
    </button>
  );
}
```

### Animation Patterns

```tsx
// Tailwind animations
function LoadingSpinner() {
  return (
    <div className="animate-spin h-5 w-5 border-2 border-current border-t-transparent rounded-full" />
  );
}

function FadeIn({ children }) {
  return (
    <div className="animate-fade-in">
      {children}
    </div>
  );
}

// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      animation: {
        'fade-in': 'fadeIn 0.3s ease-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'slide-down': 'slideDown 0.3s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        slideDown: {
          '0%': { transform: 'translateY(-10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
    },
  },
};

// Transition utilities
function Dropdown({ isOpen, children }) {
  return (
    <div
      className={cn(
        'transition-all duration-200 ease-out',
        isOpen
          ? 'opacity-100 translate-y-0'
          : 'opacity-0 -translate-y-2 pointer-events-none'
      )}
    >
      {children}
    </div>
  );
}
```

### Tailwind Configuration

```javascript
// tailwind.config.js
const defaultTheme = require('tailwindcss/defaultTheme');

module.exports = {
  content: [
    './src/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#eff6ff',
          100: '#dbeafe',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
        },
      },
      fontFamily: {
        sans: ['Inter var', ...defaultTheme.fontFamily.sans],
      },
      spacing: {
        18: '4.5rem',
        22: '5.5rem',
      },
      borderRadius: {
        '4xl': '2rem',
      },
      fontSize: {
        '2xs': ['0.625rem', { lineHeight: '1rem' }],
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('@tailwindcss/aspect-ratio'),
  ],
};
```

### @apply for Reusable Styles

```css
/* styles/components.css */
@layer components {
  .btn {
    @apply inline-flex items-center justify-center font-medium;
    @apply rounded-md transition-colors duration-200;
    @apply focus-visible:outline-none focus-visible:ring-2;
    @apply focus-visible:ring-blue-500 focus-visible:ring-offset-2;
    @apply disabled:opacity-50 disabled:cursor-not-allowed;
  }

  .btn-primary {
    @apply btn bg-blue-600 text-white hover:bg-blue-700;
  }

  .btn-secondary {
    @apply btn bg-gray-100 text-gray-900 hover:bg-gray-200;
  }

  .input {
    @apply w-full rounded-md border border-gray-300 bg-white;
    @apply px-3 py-2 text-sm;
    @apply focus:outline-none focus:ring-2 focus:ring-blue-500;
    @apply focus:border-transparent;
  }

  .card {
    @apply rounded-lg border border-gray-200 bg-white shadow-sm;
  }
}

@layer utilities {
  .text-balance {
    text-wrap: balance;
  }
}
```

## Anti-patterns

- **Too many utility classes**: Extract components when repeating
- **Inconsistent spacing**: Not using spacing scale
- **Missing responsive design**: Desktop-only implementations
- **Overriding with !important**: Usually indicates a design issue
- **Not using config**: Hardcoding values instead of theme
- **Ignoring @apply**: Duplicating long class strings

## References

- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Tailwind UI](https://tailwindui.com/)
- [Headless UI](https://headlessui.dev/)
- [Class Variance Authority](https://cva.style/docs)
- [tailwind-merge](https://github.com/dcastil/tailwind-merge)
