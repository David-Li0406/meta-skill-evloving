---
name: Component Patterns
description: Patterns de composants communs - HOC, Render Props, Compound Components, Headless
workflows:
  - id: patterns-creation
    template: wf-creation
    phase: Conception
    name: Architecture composants
    duration: 1-2 jours
  - id: patterns-refactor
    template: wf-evolution
    phase: Réalisation
    name: Refactoring patterns
    duration: 1-3 jours
---

# Agent Component Patterns

## Responsabilité

Maîtriser les patterns de composants réutilisables applicables à tous les frameworks front-end.

## Tu NE fais PAS

- ❌ Implémenter les spécificités React (hooks, Context) → `react-expert.md` ou skill `react-expert`
- ❌ Implémenter les spécificités Vue (Composition API, Pinia) → `vue-expert.md`
- ❌ Gérer le state management global → `state-management/`
- ❌ Tester les composants → `testing/component-testing.md`

## Compound Components

### Concept

Composants qui fonctionnent ensemble pour partager un état implicite.

```tsx
// Usage
<Tabs defaultValue="tab1">
  <Tabs.List>
    <Tabs.Trigger value="tab1">Tab 1</Tabs.Trigger>
    <Tabs.Trigger value="tab2">Tab 2</Tabs.Trigger>
  </Tabs.List>
  <Tabs.Content value="tab1">Contenu 1</Tabs.Content>
  <Tabs.Content value="tab2">Contenu 2</Tabs.Content>
</Tabs>
```

### Implémentation React

```tsx
import { createContext, useContext, useState, ReactNode } from 'react';

interface TabsContextType {
  activeTab: string;
  setActiveTab: (value: string) => void;
}

const TabsContext = createContext<TabsContextType | null>(null);

function useTabs() {
  const context = useContext(TabsContext);
  if (!context) {
    throw new Error('Tabs components must be used within a Tabs');
  }
  return context;
}

interface TabsProps {
  defaultValue: string;
  children: ReactNode;
}

function Tabs({ defaultValue, children }: TabsProps) {
  const [activeTab, setActiveTab] = useState(defaultValue);

  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div className="tabs">{children}</div>
    </TabsContext.Provider>
  );
}

function TabsList({ children }: { children: ReactNode }) {
  return <div role="tablist" className="tabs-list">{children}</div>;
}

interface TabsTriggerProps {
  value: string;
  children: ReactNode;
}

function TabsTrigger({ value, children }: TabsTriggerProps) {
  const { activeTab, setActiveTab } = useTabs();
  const isActive = activeTab === value;

  return (
    <button
      role="tab"
      aria-selected={isActive}
      onClick={() => setActiveTab(value)}
      className={`tab-trigger ${isActive ? 'active' : ''}`}
    >
      {children}
    </button>
  );
}

interface TabsContentProps {
  value: string;
  children: ReactNode;
}

function TabsContent({ value, children }: TabsContentProps) {
  const { activeTab } = useTabs();

  if (activeTab !== value) return null;

  return (
    <div role="tabpanel" className="tab-content">
      {children}
    </div>
  );
}

// Attacher les sous-composants
Tabs.List = TabsList;
Tabs.Trigger = TabsTrigger;
Tabs.Content = TabsContent;

export { Tabs };
```

## Render Props

### Concept

Passer une fonction en prop pour contrôler le rendu.

```tsx
// Usage
<MouseTracker>
  {({ x, y }) => (
    <div>Position: {x}, {y}</div>
  )}
</MouseTracker>
```

### Implémentation

```tsx
import { useState, useEffect, ReactNode } from 'react';

interface MousePosition {
  x: number;
  y: number;
}

interface MouseTrackerProps {
  children: (position: MousePosition) => ReactNode;
}

function MouseTracker({ children }: MouseTrackerProps) {
  const [position, setPosition] = useState<MousePosition>({ x: 0, y: 0 });

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setPosition({ x: e.clientX, y: e.clientY });
    };

    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  return <>{children(position)}</>;
}

// Variante avec prop render
interface MouseTrackerRenderProps {
  render: (position: MousePosition) => ReactNode;
}

function MouseTrackerAlt({ render }: MouseTrackerRenderProps) {
  const [position, setPosition] = useState<MousePosition>({ x: 0, y: 0 });
  // ... même logique
  return <>{render(position)}</>;
}
```

## Headless Components (Renderless)

### Concept

Composants qui gèrent la logique sans imposer de markup.

```tsx
// Usage
<Toggle>
  {({ isOn, toggle }) => (
    <button onClick={toggle}>
      {isOn ? 'ON' : 'OFF'}
    </button>
  )}
</Toggle>
```

### Implémentation Hook (React)

```tsx
// Hook headless
function useToggle(initialState = false) {
  const [isOn, setIsOn] = useState(initialState);

  const toggle = useCallback(() => setIsOn((prev) => !prev), []);
  const setOn = useCallback(() => setIsOn(true), []);
  const setOff = useCallback(() => setIsOn(false), []);

  return { isOn, toggle, setOn, setOff };
}

// Usage avec hook
function CustomToggle() {
  const { isOn, toggle } = useToggle();

  return (
    <div className="custom-toggle" onClick={toggle}>
      <span className={isOn ? 'active' : ''}>Toggle</span>
    </div>
  );
}

// Ou avec composant render prop
interface ToggleProps {
  children: (state: ReturnType<typeof useToggle>) => ReactNode;
}

function Toggle({ children }: ToggleProps) {
  const state = useToggle();
  return <>{children(state)}</>;
}
```

### Headless Dropdown

```tsx
function useDropdown<T>() {
  const [isOpen, setIsOpen] = useState(false);
  const [selected, setSelected] = useState<T | null>(null);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const open = () => setIsOpen(true);
  const close = () => setIsOpen(false);
  const toggle = () => setIsOpen((prev) => !prev);

  const select = (item: T) => {
    setSelected(item);
    close();
  };

  // Fermer au clic externe
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) {
        close();
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Fermer avec Escape
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') close();
    };

    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, []);

  return {
    isOpen,
    selected,
    dropdownRef,
    open,
    close,
    toggle,
    select,
  };
}
```

## Controlled vs Uncontrolled

### Controlled Component

```tsx
interface ControlledInputProps {
  value: string;
  onChange: (value: string) => void;
}

function ControlledInput({ value, onChange }: ControlledInputProps) {
  return (
    <input
      value={value}
      onChange={(e) => onChange(e.target.value)}
    />
  );
}

// Usage - le parent gère l'état
function Form() {
  const [name, setName] = useState('');

  return <ControlledInput value={name} onChange={setName} />;
}
```

### Uncontrolled Component

```tsx
import { forwardRef, useImperativeHandle, useRef } from 'react';

interface UncontrolledInputRef {
  getValue: () => string;
  focus: () => void;
}

const UncontrolledInput = forwardRef<UncontrolledInputRef>((props, ref) => {
  const inputRef = useRef<HTMLInputElement>(null);

  useImperativeHandle(ref, () => ({
    getValue: () => inputRef.current?.value || '',
    focus: () => inputRef.current?.focus(),
  }));

  return <input ref={inputRef} defaultValue="" />;
});

// Usage - accès via ref
function Form() {
  const inputRef = useRef<UncontrolledInputRef>(null);

  const handleSubmit = () => {
    const value = inputRef.current?.getValue();
    console.log(value);
  };

  return (
    <>
      <UncontrolledInput ref={inputRef} />
      <button onClick={handleSubmit}>Submit</button>
    </>
  );
}
```

### Pattern hybride (contrôlé optionnel)

```tsx
interface FlexibleInputProps {
  value?: string;
  defaultValue?: string;
  onChange?: (value: string) => void;
}

function FlexibleInput({ value, defaultValue = '', onChange }: FlexibleInputProps) {
  const isControlled = value !== undefined;
  const [internalValue, setInternalValue] = useState(defaultValue);

  const currentValue = isControlled ? value : internalValue;

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value;

    if (!isControlled) {
      setInternalValue(newValue);
    }

    onChange?.(newValue);
  };

  return <input value={currentValue} onChange={handleChange} />;
}

// Usage contrôlé
<FlexibleInput value={name} onChange={setName} />

// Usage non-contrôlé
<FlexibleInput defaultValue="John" onChange={console.log} />
```

## Slot Pattern (Vue-like en React)

```tsx
interface SlotProps {
  header?: ReactNode;
  footer?: ReactNode;
  children: ReactNode;
}

function Card({ header, footer, children }: SlotProps) {
  return (
    <div className="card">
      {header && <header className="card-header">{header}</header>}
      <main className="card-body">{children}</main>
      {footer && <footer className="card-footer">{footer}</footer>}
    </div>
  );
}

// Usage
<Card
  header={<h2>Titre</h2>}
  footer={<button>Action</button>}
>
  <p>Contenu principal</p>
</Card>
```

## Provider Pattern

```tsx
// Créer un provider réutilisable
function createProvider<T>(
  defaultValue: T,
  displayName: string
) {
  const Context = createContext<T | undefined>(undefined);

  function Provider({
    value,
    children,
  }: {
    value: T;
    children: ReactNode;
  }) {
    return <Context.Provider value={value}>{children}</Context.Provider>;
  }

  function useContextValue() {
    const context = useContext(Context);
    if (context === undefined) {
      throw new Error(`use${displayName} must be used within ${displayName}Provider`);
    }
    return context;
  }

  Provider.displayName = `${displayName}Provider`;

  return [Provider, useContextValue] as const;
}

// Usage
const [ThemeProvider, useTheme] = createProvider<Theme>(
  { mode: 'light' },
  'Theme'
);
```

## Composition over Inheritance

```tsx
// ❌ Éviter l'héritage
class Button extends BaseButton {
  render() { /* ... */ }
}

// ✅ Préférer la composition
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary';
  size?: 'sm' | 'md' | 'lg';
  leftIcon?: ReactNode;
  rightIcon?: ReactNode;
}

function Button({
  variant = 'primary',
  size = 'md',
  leftIcon,
  rightIcon,
  children,
  className,
  ...props
}: ButtonProps) {
  return (
    <button
      className={cn('btn', `btn-${variant}`, `btn-${size}`, className)}
      {...props}
    >
      {leftIcon && <span className="btn-icon-left">{leftIcon}</span>}
      {children}
      {rightIcon && <span className="btn-icon-right">{rightIcon}</span>}
    </button>
  );
}

// Variantes via composition
function IconButton(props: Omit<ButtonProps, 'children'> & { icon: ReactNode }) {
  return <Button {...props}>{props.icon}</Button>;
}
```

## Mots-clés de routage

`pattern`, `compound components`, `render props`, `headless`, `renderless`, `controlled`, `uncontrolled`, `slot`, `provider`, `composition`, `HOC`, `higher-order component`

## Livrables

| Livrable | Description |
|----------|-------------|
| Bibliothèque de patterns | Implémentations des patterns (Compound, Headless, Render Props) |
| Composants génériques | Composants réutilisables framework-agnostic |
| Guide des patterns | Documentation des use cases et exemples d'implémentation |
