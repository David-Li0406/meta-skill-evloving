# Headless Components

## Table of Contents

1. [What Are Headless Components](#what-are-headless-components)
2. [Why Use Them](#why-use-them)
3. [Implementation Patterns](#implementation-patterns)
4. [Radix-Style Composition](#radix-style-composition)
5. [Integrating with Radix UI Themes](#integrating-with-radix-ui-themes)
6. [Testing Headless Components](#testing-headless-components)
7. [When to Create vs. Use Existing](#when-to-create-vs-use-existing)
8. [Further Reading](#further-reading)

---

## What Are Headless Components

A headless component extracts all non-visual logic and state management, separating the "brain" of a component from its "looks."

**Key insight**: Since React components are functions that must return `ReactNode`, and hooks can return anything, components are effectively a subtype of hooks. A headless component is a hook that implements component-level logic (state management, event handling, accessibility) without returning pre-rendered JSX.

```tsx
// Traditional component: logic + presentation coupled
function Dropdown({ items }: DropdownProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [selected, setSelected] = useState<Item | null>(null)

  return (
    <div className="dropdown">
      <button onClick={() => setIsOpen(!isOpen)}>{selected?.label}</button>
      {isOpen && <ul>{/* render items */}</ul>}
    </div>
  )
}

// Headless: logic separated, presentation flexible
function useDropdown(items: Item[]) {
  const [isOpen, setIsOpen] = useState(false)
  const [selected, setSelected] = useState<Item | null>(null)

  return {
    isOpen,
    selected,
    toggle: () => setIsOpen(prev => !prev),
    select: (item: Item) => {
      setSelected(item)
      setIsOpen(false)
    },
    triggerProps: {
      onClick: () => setIsOpen(prev => !prev),
      'aria-expanded': isOpen,
      'aria-haspopup': 'listbox' as const,
    },
    listProps: {
      role: 'listbox' as const,
      'aria-activedescendant': selected?.id,
    },
  }
}
```

---

## Why Use Them

### Problems Headless Components Solve

| Problem                                        | Solution                                      |
| ---------------------------------------------- | --------------------------------------------- |
| Complex accessibility requirements             | Centralized ARIA attributes, focus management |
| Keyboard navigation                            | Encapsulated in hook, consistent across UIs   |
| Multiple UI variations with identical behavior | Same hook, different presentations            |
| Intertwined state and presentation             | Clean separation of concerns                  |
| Hard-to-test complex interactions              | Logic tested independently of DOM             |

### Benefits

- **Reusability**: Share logic across multiple visual implementations
- **Testability**: Test behavior without rendering UI
- **Flexibility**: Swap presentations without changing logic
- **Accessibility**: Handle ARIA, focus, keyboard in one place
- **Maintainability**: Changes to logic don't break styling, and vice versa

> The headless pattern is foundational to creating accessible components. For a complete guide on accessibility best practices, including semantic HTML, ARIA, and testing, see [accessibility.md](accessibility.md).

---

## Implementation Patterns

### Pattern 1: Custom Hook Returning Props Objects

The React Aria approach. Return prop objects that consumers spread onto elements.

```tsx
interface UseToggleReturn {
  isOn: boolean
  toggle: () => void
  buttonProps: {
    role: 'switch'
    'aria-checked': boolean
    onClick: () => void
    onKeyDown: (e: React.KeyboardEvent) => void
  }
}

function useToggle(defaultValue = false): UseToggleReturn {
  const [isOn, setIsOn] = useState(defaultValue)

  const toggle = useCallback(() => setIsOn(prev => !prev), [])

  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent) => {
      if (e.key === ' ' || e.key === 'Enter') {
        e.preventDefault()
        toggle()
      }
    },
    [toggle]
  )

  return {
    isOn,
    toggle,
    buttonProps: {
      role: 'switch',
      'aria-checked': isOn,
      onClick: toggle,
      onKeyDown: handleKeyDown,
    },
  }
}

// Usage: consumer controls presentation
function CustomSwitch() {
  const { isOn, buttonProps } = useToggle()

  return (
    <button {...buttonProps} className={cn('switch', isOn && 'switch--on')}>
      {isOn ? 'ON' : 'OFF'}
    </button>
  )
}
```

> **Note on Complex State**: For components with many interconnected states or complex transition logic (like a state machine), consider using `useReducer` instead of multiple `useState` calls. It can make your state logic more predictable and easier to test.

### Pattern 2: Compound Components with Context

The Radix UI approach. Provide composable parts that share state via context.

```tsx
// Context for shared state
interface DropdownContextValue {
  isOpen: boolean
  selectedValue: string | null
  toggle: () => void
  select: (value: string) => void
}

const DropdownContext = createContext<DropdownContextValue | null>(null)

function useDropdownContext() {
  const context = useContext(DropdownContext)
  if (!context) {
    throw new Error('Dropdown components must be used within Dropdown.Root')
  }
  return context
}

// Root: provides context
interface DropdownRootProps {
  children: React.ReactNode
  defaultValue?: string
  onValueChange?: (value: string) => void
}

function DropdownRoot({ children, defaultValue, onValueChange }: DropdownRootProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [selectedValue, setSelectedValue] = useState<string | null>(defaultValue ?? null)

  const toggle = useCallback(() => setIsOpen(prev => !prev), [])

  const select = useCallback(
    (value: string) => {
      setSelectedValue(value)
      setIsOpen(false)
      onValueChange?.(value)
    },
    [onValueChange]
  )

  return (
    <DropdownContext.Provider value={{ isOpen, selectedValue, toggle, select }}>
      {children}
    </DropdownContext.Provider>
  )
}

// Trigger: button that opens dropdown
interface DropdownTriggerProps {
  children: React.ReactNode
  asChild?: boolean
}

function DropdownTrigger({ children, asChild }: DropdownTriggerProps) {
  const { isOpen, toggle } = useDropdownContext()

  const props = {
    onClick: toggle,
    'aria-expanded': isOpen,
    'aria-haspopup': 'listbox' as const,
  }

  if (asChild && React.isValidElement(children)) {
    return React.cloneElement(children, props)
  }

  return <button {...props}>{children}</button>
}

// Content: the dropdown panel
interface DropdownContentProps {
  children: React.ReactNode
}

function DropdownContent({ children }: DropdownContentProps) {
  const { isOpen } = useDropdownContext()

  if (!isOpen) return null

  return <div role="listbox">{children}</div>
}

// Item: individual option
interface DropdownItemProps {
  value: string
  children: React.ReactNode
}

function DropdownItem({ value, children }: DropdownItemProps) {
  const { selectedValue, select } = useDropdownContext()
  const isSelected = selectedValue === value

  return (
    <div
      role="option"
      aria-selected={isSelected}
      onClick={() => select(value)}
      onKeyDown={e => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault()
          select(value)
        }
      }}
      tabIndex={0}
    >
      {children}
    </div>
  )
}

// Export as namespace
export const Dropdown = {
  Root: DropdownRoot,
  Trigger: DropdownTrigger,
  Content: DropdownContent,
  Item: DropdownItem,
}
```

Usage:

```tsx
<Dropdown.Root onValueChange={handleChange}>
  <Dropdown.Trigger>Select option</Dropdown.Trigger>
  <Dropdown.Content>
    <Dropdown.Item value="a">Option A</Dropdown.Item>
    <Dropdown.Item value="b">Option B</Dropdown.Item>
    <Dropdown.Item value="c">Option C</Dropdown.Item>
  </Dropdown.Content>
</Dropdown.Root>
```

---

## Radix-Style Composition

### The `asChild` Pattern

Radix uses `asChild` to give complete control over the rendered element. When `asChild` is true, the component clones its child and merges props.

```tsx
import { Slot } from '@radix-ui/react-slot';

interface ButtonProps {
  children: React.ReactNode;
  asChild?: boolean;
  onClick?: () => void;
}

function Button({ children, asChild, onClick }: ButtonProps) {
  const Comp = asChild ? Slot : 'button';

  return (
    <Comp onClick={onClick}>
      {children}
    </Comp>
  );
}

// Usage: renders as button
<Button onClick={handleClick}>Click me</Button>

// Usage: renders as anchor, inherits onClick
<Button asChild onClick={handleClick}>
  <a href="/page">Navigate</a>
</Button>
```

### Forwarding Refs

Always forward refs for composition with other libraries:

```tsx
const DropdownTrigger = forwardRef<HTMLButtonElement, DropdownTriggerProps>(
  ({ children, asChild }, ref) => {
    const { isOpen, toggle } = useDropdownContext()

    const Comp = asChild ? Slot : 'button'

    return (
      <Comp ref={ref} onClick={toggle} aria-expanded={isOpen} aria-haspopup="listbox">
        {children}
      </Comp>
    )
  }
)

DropdownTrigger.displayName = 'Dropdown.Trigger'
```

### Data Attributes for Styling

Expose state via data attributes for CSS styling:

```tsx
function DropdownItem({ value, children }: DropdownItemProps) {
  const { selectedValue, highlightedValue } = useDropdownContext()

  return (
    <div
      role="option"
      data-state={selectedValue === value ? 'checked' : 'unchecked'}
      data-highlighted={highlightedValue === value ? '' : undefined}
      aria-selected={selectedValue === value}
    >
      {children}
    </div>
  )
}
```

Style with attribute selectors:

```css
[data-state='checked'] {
  background-color: var(--accent-3);
}

[data-highlighted] {
  background-color: var(--accent-4);
}
```

---

## Integrating with Radix UI Themes

When building headless components that work with Radix UI Themes, follow these patterns:

### Use Theme Tokens

Reference Radix theme CSS variables:

```tsx
// Use semantic color tokens
<div style={{ backgroundColor: 'var(--accent-3)' }}>

// Or with Tailwind (configured for Radix tokens)
<div className="bg-accent-3">
```

### Compose with Radix Theme Components

Wrap or extend Radix Theme components:

```tsx
import { Button } from '@radix-ui/themes'

function DropdownTrigger({ children, asChild }: DropdownTriggerProps) {
  const { isOpen, toggle } = useDropdownContext()

  // Use Radix Theme's Button as the base
  if (!asChild) {
    return (
      <Button onClick={toggle} aria-expanded={isOpen} aria-haspopup="listbox">
        {children}
      </Button>
    )
  }

  // Or allow custom element with asChild
  return (
    <Slot onClick={toggle} aria-expanded={isOpen} aria-haspopup="listbox">
      {children}
    </Slot>
  )
}
```

### Respect Theme Context

Access theme values when needed:

```tsx
import { useThemeContext } from '@radix-ui/themes'

function CustomComponent() {
  const { accentColor, radius } = useThemeContext()
  // Adapt behavior based on theme settings
}
```

### Match Radix Anatomy

Structure components like Radix does:

```tsx
// Radix pattern: Root > Trigger > Content > Item
export const Select = {
  Root: SelectRoot,
  Trigger: SelectTrigger,
  Content: SelectContent,
  Item: SelectItem,
  ItemText: SelectItemText,
  ItemIndicator: SelectItemIndicator,
  Separator: SelectSeparator,
}
```

---

## Testing Headless Components

### Unit Test the Hook

Test logic independently with `renderHook`:

```tsx
import { renderHook, act } from '@testing-library/react'

describe('useDropdown', () => {
  it('toggles open state', () => {
    const { result } = renderHook(() => useDropdown())

    expect(result.current.isOpen).toBe(false)

    act(() => {
      result.current.toggle()
    })

    expect(result.current.isOpen).toBe(true)
  })

  it('selects item and closes', () => {
    const { result } = renderHook(() => useDropdown())

    act(() => {
      result.current.toggle() // open
      result.current.select('option-1')
    })

    expect(result.current.selectedValue).toBe('option-1')
    expect(result.current.isOpen).toBe(false)
  })
})
```

### Integration Test with Simple UI

Test complete behavior with a minimal presentation:

```tsx
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

describe('Dropdown', () => {
  it('opens on trigger click', async () => {
    render(
      <Dropdown.Root>
        <Dropdown.Trigger>Open</Dropdown.Trigger>
        <Dropdown.Content>
          <Dropdown.Item value="a">Option A</Dropdown.Item>
        </Dropdown.Content>
      </Dropdown.Root>
    )

    expect(screen.queryByRole('listbox')).not.toBeInTheDocument()

    await userEvent.click(screen.getByRole('button'))

    expect(screen.getByRole('listbox')).toBeInTheDocument()
  })

  it('selects item on click', async () => {
    const onValueChange = vi.fn()

    render(
      <Dropdown.Root onValueChange={onValueChange}>
        <Dropdown.Trigger>Open</Dropdown.Trigger>
        <Dropdown.Content>
          <Dropdown.Item value="a">Option A</Dropdown.Item>
        </Dropdown.Content>
      </Dropdown.Root>
    )

    await userEvent.click(screen.getByRole('button'))
    await userEvent.click(screen.getByText('Option A'))

    expect(onValueChange).toHaveBeenCalledWith('a')
  })

  it('supports keyboard navigation', async () => {
    render(
      <Dropdown.Root>
        <Dropdown.Trigger>Open</Dropdown.Trigger>
        <Dropdown.Content>
          <Dropdown.Item value="a">Option A</Dropdown.Item>
        </Dropdown.Content>
      </Dropdown.Root>
    )

    const trigger = screen.getByRole('button')
    trigger.focus()

    await userEvent.keyboard('{Enter}')
    expect(screen.getByRole('listbox')).toBeInTheDocument()

    await userEvent.keyboard('{Escape}')
    expect(screen.queryByRole('listbox')).not.toBeInTheDocument()
  })
})
```

---

## When to Create vs. Use Existing

### Component Source Priority

Always follow this priority when choosing component sources:

1. **Radix UI** - Check installed Radix primitives first, then [Radix docs](https://www.radix-ui.com/primitives/docs/overview/introduction)
2. **shadcn/ui** - Pre-built components using Radix + Tailwind
3. **Composition of existing components** - Build from what you have
4. **New components as a last resort** - Only when nothing else works

**Never introduce additional UI libraries.**

### Create Custom When

1. **No Radix primitive or shadcn component exists** for your interaction pattern
2. **Existing components are too opinionated** for your specific needs
3. **Performance critical** and you need minimal overhead
4. **Unique domain logic** that doesn't map to standard patterns

### Checklist Before Creating

- [ ] Checked installed Radix primitives
- [ ] Checked [Radix Primitives docs](https://www.radix-ui.com/primitives/docs/overview/introduction) for available components
- [ ] Checked [shadcn/ui](https://ui.shadcn.com/) for pre-built solution
- [ ] Checked [usehooks](https://usehooks.com/) for existing hook
- [ ] Interaction pattern is reused in 2+ places
- [ ] Accessibility requirements are well understood
- [ ] Keyboard navigation needs are documented

---

## Further Reading

- [Headless Component: a pattern for composing React UIs](https://martinfowler.com/articles/headless-component.html) - Martin Fowler
- [Sparkling Hooks](https://www.bbss.dev/posts/sparkling-hooks/) - Components as hook subtypes
- [Radix Primitives](https://www.radix-ui.com/primitives/docs/overview/introduction) - Reference implementation
- [Radix Themes](https://www.radix-ui.com/themes/docs/overview/getting-started) - Styled layer on primitives
- [React Aria](https://react-spectrum.adobe.com/react-aria/) - Adobe's accessibility hooks
