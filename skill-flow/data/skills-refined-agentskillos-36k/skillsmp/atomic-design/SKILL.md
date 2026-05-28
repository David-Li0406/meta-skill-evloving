---
name: atomic-design
description: Atomic Design methodology for building scalable component systems
license: MIT
compatibility: opencode
metadata:
  category: architecture
  domain: frontend
  methodology: atomic-design
---

## What I do

I guide the implementation of Atomic Design principles for building scalable, maintainable component systems:

- **Atoms**: Smallest building blocks (buttons, inputs, labels)
- **Molecules**: Simple groups of atoms (form fields, search bars)
- **Organisms**: Complex groups of molecules (headers, forms, cards)
- **Templates**: Page-level layouts with placeholder content
- **Pages**: Specific instances of templates with real content

## When to use me

Load this skill when you need to:
- Structure a component library or design system
- Organize components in a scalable way
- Improve component reusability and consistency
- Build a frontend architecture from scratch
- Refactor an existing component structure

## Principles

### 1. Single Responsibility
Each component should do one thing well. Atoms should be pure and simple.

### 2. Composition Over Inheritance
Build complex components by composing simpler ones.

### 3. Prop Drilling Mitigation
Use composition and context to avoid excessive prop drilling.

### 4. Co-location
Keep related files together (component, styles, tests, stories).

## Directory Structure

```
src/
├── components/
│   ├── atoms/
│   │   ├── Button/
│   │   │   ├── Button.tsx
│   │   │   ├── Button.module.css
│   │   │   ├── Button.test.tsx
│   │   │   └── index.ts
│   │   ├── Input/
│   │   └── Label/
│   ├── molecules/
│   │   ├── FormField/
│   │   ├── SearchBar/
│   │   └── Card/
│   ├── organisms/
│   │   ├── Header/
│   │   ├── Footer/
│   │   └── LoginForm/
│   ├── templates/
│   │   ├── MainLayout/
│   │   └── DashboardLayout/
│   └── pages/
│       ├── HomePage/
│       └── DashboardPage/
```

## Component Examples

### Atom: Button
```typescript
// atoms/Button/Button.tsx
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  children: React.ReactNode;
  onClick?: () => void;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  disabled = false,
  children,
  onClick,
}) => {
  return (
    <button
      className={`btn btn--${variant} btn--${size}`}
      disabled={disabled}
      onClick={onClick}
    >
      {children}
    </button>
  );
};
```

### Molecule: FormField
```typescript
// molecules/FormField/FormField.tsx
import { Input } from '@/components/atoms/Input';
import { Label } from '@/components/atoms/Label';

interface FormFieldProps {
  id: string;
  label: string;
  error?: string;
  required?: boolean;
}

export const FormField: React.FC<FormFieldProps> = ({
  id,
  label,
  error,
  required,
  ...inputProps
}) => {
  return (
    <div className="form-field">
      <Label htmlFor={id} required={required}>
        {label}
      </Label>
      <Input
        id={id}
        aria-invalid={!!error}
        aria-describedby={error ? `${id}-error` : undefined}
        {...inputProps}
      />
      {error && (
        <span id={`${id}-error`} className="form-field__error">
          {error}
        </span>
      )}
    </div>
  );
};
```

### Organism: LoginForm
```typescript
// organisms/LoginForm/LoginForm.tsx
import { FormField } from '@/components/molecules/FormField';
import { Button } from '@/components/atoms/Button';

interface LoginFormProps {
  onSubmit: (email: string, password: string) => void;
}

export const LoginForm: React.FC<LoginFormProps> = ({ onSubmit }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(email, password);
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <FormField
        id="email"
        label="Email"
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
      />
      <FormField
        id="password"
        label="Password"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
      />
      <Button type="submit">Login</Button>
    </form>
  );
};
```

### Template: MainLayout
```typescript
// templates/MainLayout/MainLayout.tsx
import { Header } from '@/components/organisms/Header';
import { Footer } from '@/components/organisms/Footer';

interface MainLayoutProps {
  children: React.ReactNode;
}

export const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
  return (
    <div className="main-layout">
      <Header />
      <main className="main-layout__content">
        {children}
      </main>
      <Footer />
    </div>
  );
};
```

## Best Practices

### 1. Keep Atoms Pure and Simple
- No business logic
- Minimal or no state
- Highly reusable
- Well-documented props

### 2. Molecules Should Be Self-Contained
- Handle their own layout
- Manage internal state if needed
- Expose clear, focused API

### 3. Organisms Can Be Complex
- Can fetch data
- Can manage complex state
- Should still be reusable

### 4. Use Barrel Exports
```typescript
// components/atoms/index.ts
export { Button } from './Button';
export { Input } from './Input';
export { Label } from './Label';
```

### 5. Co-locate Tests and Stories
```
Button/
├── Button.tsx
├── Button.module.css
├── Button.test.tsx
├── Button.stories.tsx
└── index.ts
```

## When to Break the Rules

- **Skip levels**: Sometimes a molecule can skip directly to a template if it makes sense
- **Cross-level composition**: Pages can use atoms directly for simple cases
- **Shared utilities**: Common hooks, utilities can live outside the hierarchy

## References

- Atomic Design by Brad Frost
- Component-Driven Development
- Storybook for component development
