---
name: tailwind-react
description: Tailwind CSS with React using cn and CVA
workflows:
  - id: tailwind-react-setup
    template: wf-creation
    phase: Production
    name: Setup Tailwind React
    duration: 0.5 jour
---

# Tailwind + React - Styling avec Classes Utilitaires

## Rôle

Implémentation de Tailwind CSS dans les projets React avec les meilleures pratiques.

## Tu NE fais PAS

- ❌ Implémenter la logique métier des composants → `../components/`
- ❌ Gérer la logique JavaScript complexe → `../hooks/`
- ❌ Définir les détails d'accessibilité (ARIA, rôles) → `frontend-developer`
- ❌ Définir les tokens du design system → `design-system-foundations`

## Installation

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### Configuration

```js
// tailwind.config.js
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

```css
/* src/index.css */
@tailwind base;
@tailwind components;
@tailwind layer;
```

## cn() - Conditional Classes

### Installation

```bash
npm install clsx tailwind-merge
```

### Utility

```tsx
// lib/utils.ts
import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

### Usage

```tsx
import { cn } from '@/lib/utils';

interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  className?: string;
  children: React.ReactNode;
}

function Button({
  variant = 'primary',
  size = 'md',
  className,
  children,
}: ButtonProps) {
  return (
    <button
      className={cn(
        // Base styles
        'rounded-md font-medium transition-colors focus:outline-none focus:ring-2',
        // Variants
        {
          'bg-blue-600 text-white hover:bg-blue-700': variant === 'primary',
          'bg-gray-200 text-gray-900 hover:bg-gray-300': variant === 'secondary',
          'bg-red-600 text-white hover:bg-red-700': variant === 'danger',
        },
        // Sizes
        {
          'px-2 py-1 text-sm': size === 'sm',
          'px-4 py-2 text-base': size === 'md',
          'px-6 py-3 text-lg': size === 'lg',
        },
        // Custom classes (override)
        className
      )}
    >
      {children}
    </button>
  );
}

// Usage
<Button variant="primary" size="lg" className="w-full">
  Submit
</Button>
```

## CVA - Class Variance Authority

### Installation

```bash
npm install class-variance-authority
```

### Définition de Variants

```tsx
// components/Button.tsx
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const buttonVariants = cva(
  // Base
  'inline-flex items-center justify-center rounded-md font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none',
  {
    variants: {
      variant: {
        primary: 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500',
        secondary: 'bg-gray-100 text-gray-900 hover:bg-gray-200 focus:ring-gray-500',
        outline: 'border border-gray-300 bg-transparent hover:bg-gray-100 focus:ring-gray-500',
        ghost: 'bg-transparent hover:bg-gray-100 focus:ring-gray-500',
        danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500',
        link: 'text-blue-600 underline-offset-4 hover:underline',
      },
      size: {
        sm: 'h-8 px-3 text-sm',
        md: 'h-10 px-4 text-sm',
        lg: 'h-12 px-6 text-base',
        icon: 'h-10 w-10',
      },
    },
    defaultVariants: {
      variant: 'primary',
      size: 'md',
    },
  }
);

interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;
}

function Button({
  className,
  variant,
  size,
  ...props
}: ButtonProps) {
  return (
    <button
      className={cn(buttonVariants({ variant, size, className }))}
      {...props}
    />
  );
}

export { Button, buttonVariants };
```

### Compound Variants

```tsx
const alertVariants = cva(
  'rounded-lg border p-4',
  {
    variants: {
      variant: {
        info: 'bg-blue-50 border-blue-200 text-blue-800',
        success: 'bg-green-50 border-green-200 text-green-800',
        warning: 'bg-yellow-50 border-yellow-200 text-yellow-800',
        error: 'bg-red-50 border-red-200 text-red-800',
      },
      size: {
        sm: 'text-sm',
        md: 'text-base',
        lg: 'text-lg',
      },
      withIcon: {
        true: 'flex items-start gap-3',
        false: '',
      },
    },
    compoundVariants: [
      {
        variant: 'error',
        size: 'lg',
        className: 'font-bold',
      },
    ],
    defaultVariants: {
      variant: 'info',
      size: 'md',
      withIcon: false,
    },
  }
);
```

## Patterns Communs

### Composant Card

```tsx
import { cn } from '@/lib/utils';

interface CardProps {
  className?: string;
  children: React.ReactNode;
}

function Card({ className, children }: CardProps) {
  return (
    <div className={cn(
      'rounded-lg border bg-white shadow-sm',
      className
    )}>
      {children}
    </div>
  );
}

function CardHeader({ className, children }: CardProps) {
  return (
    <div className={cn('border-b px-6 py-4', className)}>
      {children}
    </div>
  );
}

function CardContent({ className, children }: CardProps) {
  return (
    <div className={cn('px-6 py-4', className)}>
      {children}
    </div>
  );
}

function CardFooter({ className, children }: CardProps) {
  return (
    <div className={cn('border-t px-6 py-4', className)}>
      {children}
    </div>
  );
}

Card.Header = CardHeader;
Card.Content = CardContent;
Card.Footer = CardFooter;

export { Card };
```

### Input avec États

```tsx
import { cva, type VariantProps } from 'class-variance-authority';
import { forwardRef } from 'react';
import { cn } from '@/lib/utils';

const inputVariants = cva(
  'flex w-full rounded-md border bg-white px-3 py-2 text-sm transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-offset-0 disabled:cursor-not-allowed disabled:opacity-50',
  {
    variants: {
      variant: {
        default: 'border-gray-300 focus:border-blue-500 focus:ring-blue-500',
        error: 'border-red-500 focus:border-red-500 focus:ring-red-500',
        success: 'border-green-500 focus:border-green-500 focus:ring-green-500',
      },
      inputSize: {
        sm: 'h-8 text-xs',
        md: 'h-10 text-sm',
        lg: 'h-12 text-base',
      },
    },
    defaultVariants: {
      variant: 'default',
      inputSize: 'md',
    },
  }
);

interface InputProps
  extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'size'>,
    VariantProps<typeof inputVariants> {
  error?: string;
}

const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ className, variant, inputSize, error, ...props }, ref) => {
    return (
      <div className="space-y-1">
        <input
          className={cn(
            inputVariants({
              variant: error ? 'error' : variant,
              inputSize,
              className,
            })
          )}
          ref={ref}
          {...props}
        />
        {error && (
          <p className="text-sm text-red-600">{error}</p>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';

export { Input };
```

## Dark Mode

### Configuration

```js
// tailwind.config.js
export default {
  darkMode: 'class', // ou 'media'
  // ...
}
```

### Usage

```tsx
function ThemeToggle() {
  const [dark, setDark] = useState(false);

  useEffect(() => {
    document.documentElement.classList.toggle('dark', dark);
  }, [dark]);

  return (
    <button onClick={() => setDark(!dark)}>
      Toggle Theme
    </button>
  );
}

// Composant avec dark mode
function Card() {
  return (
    <div className="bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100">
      Content
    </div>
  );
}
```

## Responsive

```tsx
function ResponsiveGrid() {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      {items.map((item) => (
        <Card key={item.id} />
      ))}
    </div>
  );
}
```

## Animations

```tsx
// Hover
<button className="transition-transform hover:scale-105">
  Hover me
</button>

// Avec groupe
<div className="group">
  <div className="transition-opacity group-hover:opacity-100 opacity-0">
    Appears on hover
  </div>
</div>

// Custom animation
// tailwind.config.js
{
  theme: {
    extend: {
      animation: {
        'fade-in': 'fadeIn 0.3s ease-in-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
      },
    },
  },
}

// Usage
<div className="animate-fade-in">Content</div>
```

## Bonnes Pratiques

1. **cn() pour composition** - Toujours pour les composants réutilisables
2. **CVA pour variants** - Composants avec beaucoup de variantes
3. **className prop** - Permettre l'override
4. **Extraire les patterns** - Composants réutilisables
5. **@apply avec parcimonie** - Préférer cn/cva

## Voir aussi

- `css-in-js.md` - Alternative CSS-in-JS
- `../components/functional.md` - Composants React
- `design-system-foundations` skill - Tokens design

## Livrables

| Livrable | Description |
|----------|-------------|
| Composants Tailwind | Composants React avec classes utilitaires |
| cn() utility | Helper function avec clsx et tailwind-merge |
| CVA variants | Configuration class-variance-authority pour variants |
