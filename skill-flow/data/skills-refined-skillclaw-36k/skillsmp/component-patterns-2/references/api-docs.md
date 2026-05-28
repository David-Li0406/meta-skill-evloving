# React Component Patterns - API Reference

**Version**: React 18.x with TypeScript 5.7.3

## Official Documentation

- **React Docs**: https://react.dev/
- **TypeScript React Cheatsheet**: https://react-typescript-cheatsheet.netlify.app/
- **React TypeScript**: https://react.dev/learn/typescript

## Core Types

### React.FC

Function component type with automatic children typing.

```typescript
import React from 'react';

// Basic usage
const MyComponent: React.FC = () => {
  return <div>Hello</div>;
};

// With props
interface MyComponentProps {
  name: string;
  age: number;
}

const MyComponent: React.FC<MyComponentProps> = ({ name, age }) => {
  return <div>{name} is {age} years old</div>;
};

// With children (automatically typed)
const Container: React.FC<{ title: string }> = ({ title, children }) => {
  return (
    <div>
      <h1>{title}</h1>
      {children}
    </div>
  );
};
```

**Returns**: JSX.Element | null

**Benefits**:
- Automatic `children` prop typing
- Better type inference
- Consistent function signature
- DisplayName support for DevTools

### React.ReactNode

Type for anything that can be rendered.

```typescript
interface Props {
  content: React.ReactNode;
}

// Accepts:
<Component content="text" />
<Component content={123} />
<Component content={<div>JSX</div>} />
<Component content={[<div key="1">a</div>, <div key="2">b</div>]} />
<Component content={null} />
<Component content={undefined} />
```

**Definition**: `React.ReactElement | string | number | React.ReactFragment | React.ReactPortal | boolean | null | undefined`

**Use for**: Props that accept any renderable content

### React.ReactElement

Type for JSX elements only (more strict than ReactNode).

```typescript
interface Props {
  icon: React.ReactElement;
}

// Only accepts JSX elements
<Component icon={<Icon />} />        // ✅
<Component icon="text" />            // ❌
<Component icon={123} />             // ❌
```

**Use for**: Props that must be JSX elements

### Children Props

```typescript
// Any content
interface Props {
  children: React.ReactNode;
}

// Must be JSX
interface Props {
  children: React.ReactElement;
}

// Multiple specific elements
interface Props {
  children: React.ReactElement<ButtonProps>[];
}

// Optional children
interface Props {
  children?: React.ReactNode;
}
```

## Props Patterns

### Basic Props Interface

```typescript
interface ButtonProps {
  label: string;              // Required string
  onClick: () => void;        // Required function
  disabled?: boolean;         // Optional boolean
  variant?: 'primary' | 'secondary';  // Optional union
  className?: string;         // Optional string
}

export const Button: React.FC<ButtonProps> = ({
  label,
  onClick,
  disabled = false,
  variant = 'primary',
  className,
}) => {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`btn-${variant} ${className || ''}`}
    >
      {label}
    </button>
  );
};
```

### Union Type Props

```typescript
interface ButtonProps {
  variant: 'primary' | 'secondary' | 'danger';
  size: 'sm' | 'md' | 'lg';
}

// Usage is type-checked
<Button variant="primary" size="md" />  // ✅
<Button variant="warning" size="xs" />  // ❌ TypeScript error
```

### Discriminated Union Props

```typescript
type MessageProps =
  | { type: 'success'; message: string }
  | { type: 'error'; message: string; retryFn: () => void }
  | { type: 'loading' };

export const Message: React.FC<MessageProps> = (props) => {
  switch (props.type) {
    case 'success':
      return <div className="success">{props.message}</div>;
    case 'error':
      return (
        <div className="error">
          {props.message}
          <button onClick={props.retryFn}>Retry</button>
        </div>
      );
    case 'loading':
      return <div>Loading...</div>;
  }
};

// Usage
<Message type="success" message="Done!" />
<Message type="error" message="Failed" retryFn={retry} />
<Message type="loading" />
```

### Extending HTML Attributes

```typescript
// Button with all native button attributes
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary';
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  children,
  ...htmlProps
}) => {
  return (
    <button className={`btn-${variant}`} {...htmlProps}>
      {children}
    </button>
  );
};

// Usage - all button attributes available
<Button
  variant="primary"
  onClick={handleClick}
  type="submit"
  disabled={isDisabled}
  aria-label="Submit form"
  data-testid="submit-btn"
>
  Submit
</Button>
```

**Common HTML attribute interfaces:**
```typescript
React.ButtonHTMLAttributes<HTMLButtonElement>
React.InputHTMLAttributes<HTMLInputElement>
React.TextareaHTMLAttributes<HTMLTextAreaElement>
React.SelectHTMLAttributes<HTMLSelectElement>
React.FormHTMLAttributes<HTMLFormElement>
React.ImgHTMLAttributes<HTMLImageElement>
React.AnchorHTMLAttributes<HTMLAnchorElement>
React.HTMLAttributes<HTMLDivElement>  // Generic div/span
```

### Generic Component Props

```typescript
interface ListProps<T> {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
  keyExtractor: (item: T) => string;
}

export function List<T>({ items, renderItem, keyExtractor }: ListProps<T>) {
  return (
    <ul>
      {items.map((item) => (
        <li key={keyExtractor(item)}>
          {renderItem(item)}
        </li>
      ))}
    </ul>
  );
}

// Usage - type-safe
interface User { id: string; name: string; }

<List<User>
  items={users}
  renderItem={(user) => <div>{user.name}</div>}  // user is typed as User
  keyExtractor={(user) => user.id}
/>
```

## Event Types

### Mouse Events

```typescript
interface Props {
  onClick: (e: React.MouseEvent<HTMLButtonElement>) => void;
  onDoubleClick: (e: React.MouseEvent<HTMLDivElement>) => void;
  onContextMenu: (e: React.MouseEvent<HTMLDivElement>) => void;
}

const Component: React.FC<Props> = ({ onClick }) => {
  const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    e.stopPropagation();
    console.log(e.clientX, e.clientY);  // Mouse coordinates
    onClick(e);
  };

  return <button onClick={handleClick}>Click me</button>;
};
```

### Keyboard Events

```typescript
interface Props {
  onKeyDown: (e: React.KeyboardEvent<HTMLInputElement>) => void;
  onKeyUp: (e: React.KeyboardEvent<HTMLInputElement>) => void;
  onKeyPress: (e: React.KeyboardEvent<HTMLInputElement>) => void;
}

const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
  if (e.key === 'Enter') {
    // Handle enter
  }
  if (e.key === 'Escape') {
    // Handle escape
  }
  if (e.ctrlKey && e.key === 's') {
    // Handle Ctrl+S
    e.preventDefault();
  }
};
```

### Form Events

```typescript
// Input change
const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
  const value = e.target.value;
  console.log(value);
};

// Textarea change
const handleTextareaChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
  const value = e.target.value;
};

// Select change
const handleSelectChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
  const value = e.target.value;
};

// Form submit
const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
  e.preventDefault();
  const formData = new FormData(e.currentTarget);
};

// Input focus/blur
const handleFocus = (e: React.FocusEvent<HTMLInputElement>) => {
  console.log('Input focused');
};
```

### Common Event Types

```typescript
React.MouseEvent<T>           // onClick, onMouseDown, onMouseUp
React.KeyboardEvent<T>        // onKeyDown, onKeyUp, onKeyPress
React.ChangeEvent<T>          // onChange (input, textarea, select)
React.FocusEvent<T>           // onFocus, onBlur
React.FormEvent<T>            // onSubmit
React.ClipboardEvent<T>       // onCopy, onPaste
React.DragEvent<T>            // onDrag, onDrop
React.TouchEvent<T>           // onTouchStart, onTouchEnd
React.WheelEvent<T>           // onWheel
React.AnimationEvent<T>       // onAnimationStart, onAnimationEnd
React.TransitionEvent<T>      // onTransitionEnd
```

## Ref Types

### useRef

```typescript
// DOM element ref
const inputRef = useRef<HTMLInputElement>(null);

useEffect(() => {
  inputRef.current?.focus();
}, []);

<input ref={inputRef} />

// Value ref (doesn't trigger re-render)
const countRef = useRef<number>(0);

const increment = () => {
  countRef.current += 1;
  console.log(countRef.current);
};
```

### forwardRef

```typescript
interface InputProps {
  label: string;
  type?: string;
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ label, type = 'text', ...props }, ref) => {
    return (
      <div>
        <label>{label}</label>
        <input ref={ref} type={type} {...props} />
      </div>
    );
  }
);

// Usage
const inputRef = useRef<HTMLInputElement>(null);

<Input ref={inputRef} label="Username" />
```

## Component Patterns

### Children Pattern

```typescript
interface ContainerProps {
  children: React.ReactNode;
}

export const Container: React.FC<ContainerProps> = ({ children }) => {
  return <div className="container">{children}</div>;
};

// Usage
<Container>
  <Header />
  <Content />
  <Footer />
</Container>
```

### Render Props Pattern

```typescript
interface DataFetcherProps {
  url: string;
  render: (data: any, loading: boolean, error: Error | null) => React.ReactNode;
}

export const DataFetcher: React.FC<DataFetcherProps> = ({ url, render }) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    fetch(url)
      .then(res => res.json())
      .then(setData)
      .catch(setError)
      .finally(() => setLoading(false));
  }, [url]);

  return <>{render(data, loading, error)}</>;
};

// Usage
<DataFetcher
  url="/api/user"
  render={(data, loading, error) => {
    if (loading) return <Spinner />;
    if (error) return <Error error={error} />;
    return <UserCard user={data} />;
  }}
/>
```

### Compound Components Pattern

```typescript
interface TabsProps {
  children: React.ReactNode;
  defaultTab?: string;
}

interface TabProps {
  label: string;
  children: React.ReactNode;
}

export const Tabs: React.FC<TabsProps> & {
  Tab: React.FC<TabProps>;
} = ({ children, defaultTab }) => {
  const [activeTab, setActiveTab] = useState(defaultTab);

  return (
    <div>
      <div className="tab-buttons">
        {React.Children.map(children, (child) => {
          if (React.isValidElement<TabProps>(child)) {
            return (
              <button
                onClick={() => setActiveTab(child.props.label)}
                className={activeTab === child.props.label ? 'active' : ''}
              >
                {child.props.label}
              </button>
            );
          }
        })}
      </div>
      <div className="tab-content">
        {React.Children.map(children, (child) => {
          if (React.isValidElement<TabProps>(child) && child.props.label === activeTab) {
            return child.props.children;
          }
        })}
      </div>
    </div>
  );
};

Tabs.Tab = ({ children }) => <>{children}</>;

// Usage
<Tabs defaultTab="profile">
  <Tabs.Tab label="profile">
    <ProfileContent />
  </Tabs.Tab>
  <Tabs.Tab label="settings">
    <SettingsContent />
  </Tabs.Tab>
</Tabs>
```

### Higher-Order Component (HOC)

```typescript
function withLoading<P extends object>(
  Component: React.ComponentType<P>
): React.FC<P & { isLoading: boolean }> {
  return ({ isLoading, ...props }: P & { isLoading: boolean }) => {
    if (isLoading) {
      return <div>Loading...</div>;
    }
    return <Component {...(props as P)} />;
  };
}

// Usage
const UserCardWithLoading = withLoading(UserCard);

<UserCardWithLoading user={user} isLoading={isLoading} />
```

## TypeScript Utilities

### Omit Props

```typescript
interface ButtonProps {
  variant: 'primary' | 'secondary';
  size: 'sm' | 'md' | 'lg';
  onClick: () => void;
  disabled?: boolean;
}

// Create new interface without onClick
type ButtonPropsWithoutClick = Omit<ButtonProps, 'onClick'>;

// Equivalent to:
// { variant: ..., size: ..., disabled?: boolean }
```

### Pick Props

```typescript
// Create new interface with only specific props
type ButtonSize = Pick<ButtonProps, 'size'>;

// Equivalent to:
// { size: 'sm' | 'md' | 'lg' }
```

### Partial Props

```typescript
// Make all props optional
type PartialButtonProps = Partial<ButtonProps>;

// Equivalent to:
// { variant?: ..., size?: ..., onClick?: ..., disabled?: boolean }
```

### Required Props

```typescript
// Make all props required
type RequiredButtonProps = Required<ButtonProps>;

// disabled is now required (no ?)
```

### Component Props Type Extraction

```typescript
// Extract props from existing component
type MyButtonProps = React.ComponentProps<typeof Button>;

// Extract props from HTML element
type DivProps = React.ComponentProps<'div'>;
type InputProps = React.ComponentProps<'input'>;
```

## Common Prop Types

### Callback Props

```typescript
interface Props {
  onClick: () => void;                        // No parameters
  onSubmit: (data: FormData) => void;         // With parameter
  onChange: (value: string) => void;          // Return void
  onValidate: (value: string) => boolean;     // Return boolean
  onSearch: (query: string) => Promise<void>; // Async
}
```

### Optional Props with Defaults

```typescript
interface Props {
  variant?: 'primary' | 'secondary';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
}

export const Button: React.FC<Props> = ({
  variant = 'primary',
  size = 'md',
  disabled = false,
}) => {
  // ...
};
```

### Conditional Props

```typescript
type Props =
  | { mode: 'edit'; onSave: () => void }
  | { mode: 'view'; onEdit: () => void };

export const Editor: React.FC<Props> = (props) => {
  if (props.mode === 'edit') {
    // TypeScript knows props.onSave exists
    return <button onClick={props.onSave}>Save</button>;
  }
  // TypeScript knows props.onEdit exists
  return <button onClick={props.onEdit}>Edit</button>;
};
```

## Key Considerations

- Use `React.FC<Props>` for all function components
- Name props interfaces `ComponentNameProps`
- Use `React.ReactNode` for children and content props
- Extend HTML attribute interfaces for native element wrappers
- Type event handlers with React event types
- Use generics for reusable components
- Use discriminated unions for complex conditional props
- Leverage TypeScript utilities (Omit, Pick, Partial) for prop manipulation
- Extract component props types with `React.ComponentProps<typeof Component>`
