# React Component Implementation Patterns

Implementation patterns and anti-patterns for React web components with TypeScript.

## Pattern: React.FC with Explicit Props

Use React.FC with explicit props interface for all components.

✅ **Good:**
```typescript
import React from 'react';

interface UserCardProps {
  name: string;
  email: string;
  avatar?: string;
}

export const UserCard: React.FC<UserCardProps> = ({ name, email, avatar }) => {
  return (
    <div>
      {avatar && <img src={avatar} alt={name} />}
      <h3>{name}</h3>
      <p>{email}</p>
    </div>
  );
};
```

❌ **Bad:**
```typescript
// Not using React.FC
export function UserCard({ name, email, avatar }) {
  return <div>{name}</div>;
}

// No types
export const UserCard = ({ name, email }) => {
  return <div>{name}</div>;
};

// Inline props type
export const UserCard: React.FC<{ name: string; email: string }> = ({ name, email }) => {
  return <div>{name}</div>;
};
```

**Why:** React.FC:
- Provides automatic `children` typing
- Improves type inference
- Consistent function signature
- Better IntelliSense support
- Explicit props interface is more maintainable

## Pattern: Props Interface Naming

Name props interfaces with ComponentName + "Props" suffix.

✅ **Good:**
```typescript
interface UserCardProps {
  name: string;
  email: string;
}

export const UserCard: React.FC<UserCardProps> = (props) => {
  // ...
};
```

❌ **Bad:**
```typescript
// Generic name
interface Props {
  name: string;
}

// No Props suffix
interface UserCard {
  name: string;
}

// Abbreviated
interface UCProps {
  name: string;
}
```

**Why:** Explicit naming:
- Prevents naming conflicts
- Self-documenting code
- Easy to find in codebase
- Consistent convention

## Pattern: Semantic HTML Elements

Use semantic HTML elements for accessibility and SEO.

✅ **Good:**
```typescript
import { Box } from '@/libs/zest';

export const ArticleCard: React.FC<ArticleCardProps> = ({ title, content, author }) => {
  return (
    <Box as="article">
      <Box as="h2">{title}</Box>
      <Box as="p">{content}</Box>
      <Box as="footer">By {author}</Box>
    </Box>
  );
};

// Or with native HTML
export const ArticleCard: React.FC<ArticleCardProps> = ({ title, content }) => {
  return (
    <article>
      <h2>{title}</h2>
      <p>{content}</p>
    </article>
  );
};
```

❌ **Bad:**
```typescript
// Using React Native components
import { View, Text } from 'react-native';

export const ArticleCard = ({ title, content }) => {
  return (
    <View>
      <Text>{title}</Text>
      <Text>{content}</Text>
    </View>
  );
};

// No semantic structure
export const ArticleCard = ({ title, content }) => {
  return (
    <div>
      <div>{title}</div>
      <div>{content}</div>
    </div>
  );
};
```

**Why:** Semantic HTML:
- Improves accessibility (screen readers)
- Better SEO (search engines understand structure)
- Native browser behaviors
- Keyboard navigation
- Standard web practices

**Common semantic elements:**
- `<article>` - Self-contained content
- `<section>` - Thematic grouping
- `<nav>` - Navigation links
- `<header>` - Introductory content
- `<footer>` - Footer content
- `<h1>-<h6>` - Headings hierarchy
- `<button>` - Interactive button
- `<main>` - Main content

## Pattern: Destructured Props

Destructure props in function parameter.

✅ **Good:**
```typescript
interface ButtonProps {
  label: string;
  onClick: () => void;
  disabled?: boolean;
}

export const Button: React.FC<ButtonProps> = ({ label, onClick, disabled = false }) => {
  return (
    <button onClick={onClick} disabled={disabled}>
      {label}
    </button>
  );
};
```

❌ **Bad:**
```typescript
export const Button: React.FC<ButtonProps> = (props) => {
  return (
    <button onClick={props.onClick} disabled={props.disabled}>
      {props.label}
    </button>
  );
};
```

**Why:** Destructuring:
- Reduces verbosity
- More readable code
- Easy to see all props at a glance
- Default values in one place

## Pattern: Optional Props with Defaults

Use optional props with default values.

✅ **Good:**
```typescript
interface ButtonProps {
  label: string;
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  label,
  variant = 'primary',
  size = 'md',
  disabled = false,
}) => {
  return (
    <button className={`btn-${variant} btn-${size}`} disabled={disabled}>
      {label}
    </button>
  );
};
```

❌ **Bad:**
```typescript
// No defaults - consumer must provide all props
interface ButtonProps {
  label: string;
  variant: 'primary' | 'secondary';
  size: 'sm' | 'md' | 'lg';
  disabled: boolean;
}

// Or defaults in component logic (messy)
export const Button: React.FC<ButtonProps> = (props) => {
  const variant = props.variant || 'primary';
  const size = props.size || 'md';
  const disabled = props.disabled || false;
  // ...
};
```

**Why:** Default values in destructuring:
- Easier API for consumers
- Clear default behavior
- Reduces boilerplate in usage
- Single source of truth

## Pattern: Conditional Rendering

Use appropriate conditional rendering patterns.

✅ **Good:**
```typescript
export const UserProfile: React.FC<UserProfileProps> = ({ user, isLoading, error }) => {
  // Early return for error state
  if (error) {
    return <ErrorMessage error={error} />;
  }

  // Early return for loading state
  if (isLoading) {
    return <Spinner />;
  }

  // Early return for missing data
  if (!user) {
    return null;
  }

  return (
    <div>
      <h1>{user.name}</h1>
      {/* && for simple show/hide */}
      {user.avatar && <img src={user.avatar} alt={user.name} />}

      {/* Ternary for if/else */}
      {user.isPremium ? (
        <Badge>Premium</Badge>
      ) : (
        <Button>Upgrade</Button>
      )}
    </div>
  );
};
```

❌ **Bad:**
```typescript
// Complex nested ternaries
export const UserProfile = ({ user, isLoading, error }) => {
  return error ? (
    <ErrorMessage error={error} />
  ) : isLoading ? (
    <Spinner />
  ) : !user ? (
    null
  ) : (
    <div>
      {user.avatar ? <img src={user.avatar} /> : user.isPremium ? <Badge>Premium</Badge> : <Button>Upgrade</Button>}
    </div>
  );
};

// No error/loading handling
export const UserProfile = ({ user }) => {
  return <div>{user.name}</div>; // Crashes if user is null
};
```

**Why:** Proper conditionals:
- Early returns for error/loading states
- Clear, readable logic
- Prevents crashes
- Easy to understand flow

**Conditional patterns:**
- **Early return**: For error, loading, null states
- **&& operator**: For simple show/hide
- **Ternary**: For if/else with two options
- **Switch/if-else**: For multiple complex conditions

## Pattern: Component Composition with Children

Use children prop for composable components.

✅ **Good:**
```typescript
interface CardProps {
  title: string;
  children: React.ReactNode;
  footer?: React.ReactNode;
}

export const Card: React.FC<CardProps> = ({ title, children, footer }) => {
  return (
    <div className="card">
      <h2>{title}</h2>
      <div className="card-content">{children}</div>
      {footer && <div className="card-footer">{footer}</div>}
    </div>
  );
};

// Usage - flexible content
<Card title="User Profile" footer={<Button>Edit</Button>}>
  <UserAvatar />
  <UserDetails />
  <UserStats />
</Card>
```

❌ **Bad:**
```typescript
// Props for every content piece
interface CardProps {
  title: string;
  avatar: React.ReactNode;
  details: React.ReactNode;
  stats: React.ReactNode;
  footer: React.ReactNode;
}

// Inflexible, many props
export const Card: React.FC<CardProps> = ({ title, avatar, details, stats, footer }) => {
  return (
    <div>
      <h2>{title}</h2>
      {avatar}
      {details}
      {stats}
      {footer}
    </div>
  );
};
```

**Why:** Children prop:
- Flexible composition
- Reusable container logic
- Simple API
- Natural React pattern

## Pattern: Extending HTML Attributes

Extend HTML attributes for native element wrappers.

✅ **Good:**
```typescript
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary';
  isLoading?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  isLoading = false,
  children,
  disabled,
  ...htmlProps
}) => {
  return (
    <button
      className={`btn-${variant}`}
      disabled={disabled || isLoading}
      {...htmlProps}
    >
      {isLoading ? <Spinner /> : children}
    </button>
  );
};

// Usage - all native attributes work
<Button
  variant="primary"
  onClick={handleClick}
  type="submit"
  aria-label="Submit form"
  data-testid="submit-btn"
>
  Submit
</Button>
```

❌ **Bad:**
```typescript
// Manually typing every HTML attribute
interface ButtonProps {
  variant?: 'primary' | 'secondary';
  onClick?: () => void;
  type?: 'button' | 'submit' | 'reset';
  disabled?: boolean;
  className?: string;
  id?: string;
  // Missing: aria-*, data-*, many others
}

// Can't use native button attributes
<Button onClick={handleClick} aria-label="Submit" /> // aria-label not typed!
```

**Why:** Extending HTML attributes:
- Type-safe native attributes
- No manual typing needed
- Supports all HTML attributes
- Maintains native behavior

## Pattern: Event Handlers with useCallback

Memoize event handlers passed to children.

✅ **Good:**
```typescript
import React, { useCallback } from 'react';

export const TodoList: React.FC<TodoListProps> = ({ todos, onToggle, onDelete }) => {
  const handleToggle = useCallback(
    (id: string) => {
      onToggle(id);
    },
    [onToggle]
  );

  const handleDelete = useCallback(
    (id: string) => {
      onDelete(id);
    },
    [onDelete]
  );

  return (
    <ul>
      {todos.map((todo) => (
        <TodoItem
          key={todo.id}
          todo={todo}
          onToggle={handleToggle}
          onDelete={handleDelete}
        />
      ))}
    </ul>
  );
};
```

❌ **Bad:**
```typescript
// New function on every render
export const TodoList = ({ todos, onToggle, onDelete }) => {
  return (
    <ul>
      {todos.map((todo) => (
        <TodoItem
          key={todo.id}
          todo={todo}
          onToggle={() => onToggle(todo.id)}      // New function every render
          onDelete={() => onDelete(todo.id)}      // Causes TodoItem re-render
        />
      ))}
    </ul>
  );
};
```

**Why:** useCallback:
- Stable function reference
- Prevents unnecessary child re-renders
- Better performance with React.memo
- Cleaner dependency arrays

## Pattern: Generic Components

Use generics for type-safe reusable components.

✅ **Good:**
```typescript
interface ListProps<T> {
  items: T[];
  renderItem: (item: T, index: number) => React.ReactNode;
  keyExtractor: (item: T) => string;
  emptyMessage?: string;
}

export function List<T>({
  items,
  renderItem,
  keyExtractor,
  emptyMessage = 'No items',
}: ListProps<T>) {
  if (items.length === 0) {
    return <p>{emptyMessage}</p>;
  }

  return (
    <ul>
      {items.map((item, index) => (
        <li key={keyExtractor(item)}>
          {renderItem(item, index)}
        </li>
      ))}
    </ul>
  );
}

// Usage - type-safe!
interface User { id: string; name: string; }

<List<User>
  items={users}
  renderItem={(user) => <div>{user.name}</div>}  // user is typed as User
  keyExtractor={(user) => user.id}
/>
```

❌ **Bad:**
```typescript
// Using any
interface ListProps {
  items: any[];
  renderItem: (item: any) => React.ReactNode;
  keyExtractor: (item: any) => string;
}

// No type safety
<List
  items={users}
  renderItem={(user) => <div>{user.name}</div>}  // user is any
  keyExtractor={(user) => user.id}
/>
```

**Why:** Generics:
- Type-safe items
- IntelliSense for item properties
- Reusable for any data type
- No type casting needed

## Pattern: Typed Event Handlers

Use React event types for event handlers.

✅ **Good:**
```typescript
interface SearchInputProps {
  onSearch: (query: string) => void;
}

export const SearchInput: React.FC<SearchInputProps> = ({ onSearch }) => {
  const [query, setQuery] = useState('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setQuery(e.target.value);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      onSearch(query);
    }
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    onSearch(query);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={query}
        onChange={handleChange}
        onKeyDown={handleKeyDown}
      />
    </form>
  );
};
```

❌ **Bad:**
```typescript
// Untyped events
const handleChange = (e: any) => {
  setQuery(e.target.value);
};

const handleKeyDown = (e: any) => {
  if (e.key === 'Enter') {
    onSearch(query);
  }
};

// Wrong event type
const handleChange = (e: React.MouseEvent) => {  // Wrong!
  setQuery(e.target.value);  // Type error
};
```

**Why:** Typed events:
- Type-safe event properties
- IntelliSense for event methods
- Catches errors at compile time
- Self-documenting code

**Common event types:**
- `React.ChangeEvent<HTMLInputElement>` - onChange
- `React.MouseEvent<HTMLButtonElement>` - onClick
- `React.KeyboardEvent<HTMLInputElement>` - onKeyDown
- `React.FocusEvent<HTMLInputElement>` - onFocus/onBlur
- `React.FormEvent<HTMLFormElement>` - onSubmit

## Anti-Pattern: Not Using Semantic HTML

Don't use generic divs when semantic elements exist.

❌ **Bad:**
```typescript
export const Article = ({ title, content, author }) => {
  return (
    <div>
      <div>{title}</div>
      <div>{content}</div>
      <div>By {author}</div>
    </div>
  );
};
```

✅ **Good:**
```typescript
export const Article: React.FC<ArticleProps> = ({ title, content, author }) => {
  return (
    <article>
      <h2>{title}</h2>
      <p>{content}</p>
      <footer>By {author}</footer>
    </article>
  );
};
```

**Why:** Semantic HTML improves accessibility, SEO, and maintainability.

## Anti-Pattern: Using React Native Components in Web

Don't use React Native components (View, Text) in web code.

❌ **Bad:**
```typescript
import { View, Text } from 'react-native';

export const UserCard = ({ name }) => {
  return (
    <View>
      <Text>{name}</Text>
    </View>
  );
};
```

✅ **Good:**
```typescript
import { Box } from '@/libs/zest';

export const UserCard: React.FC<UserCardProps> = ({ name }) => {
  return (
    <Box>
      <Box as="h3">{name}</Box>
    </Box>
  );
};

// Or native HTML
export const UserCard: React.FC<UserCardProps> = ({ name }) => {
  return (
    <div>
      <h3>{name}</h3>
    </div>
  );
};
```

**Why:** Web uses HTML elements, not React Native primitives.

## Anti-Pattern: Generic Props Interface Name

Don't use generic "Props" as interface name.

❌ **Bad:**
```typescript
interface Props {
  name: string;
}

export const UserCard: React.FC<Props> = ({ name }) => {
  return <div>{name}</div>;
};
```

✅ **Good:**
```typescript
interface UserCardProps {
  name: string;
}

export const UserCard: React.FC<UserCardProps> = ({ name }) => {
  return <div>{name}</div>;
};
```

**Why:** Explicit names prevent conflicts and improve code clarity.

## Anti-Pattern: Missing Keys in Lists

Always provide unique keys when rendering lists.

❌ **Bad:**
```typescript
// Using index as key
{items.map((item, index) => (
  <div key={index}>{item.name}</div>
))}

// No key at all
{items.map((item) => (
  <div>{item.name}</div>
))}
```

✅ **Good:**
```typescript
// Unique, stable key from data
{items.map((item) => (
  <div key={item.id}>{item.name}</div>
))}
```

**Why:** Stable keys improve React reconciliation and prevent bugs.

## Summary

**Key Patterns:**
- React.FC with explicit props interface
- Props interface naming: ComponentNameProps
- Semantic HTML elements
- Destructured props with defaults
- Conditional rendering (early returns, &&, ternary)
- Component composition with children
- Extending HTML attributes
- Event handlers with useCallback
- Generic components for reusability
- Typed event handlers

**Anti-Patterns to Avoid:**
- Not using React.FC
- Generic "Props" interface name
- Using React Native components (View, Text)
- Not destructuring props
- Missing types on events
- Not using semantic HTML
- Complex nested ternaries
- New functions in render (use useCallback)
- Using index as key
- Missing error/loading states
