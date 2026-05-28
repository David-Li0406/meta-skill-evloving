---
name: composition
description: Advanced composition patterns - Compound components, Render Props, and HOC
workflows:
  - id: react-patterns-impl
    template: wf-evolution
    phase: Réalisation
    name: Implémentation patterns avancés
    duration: 1-2 jours
---

# Composition Patterns - Compound, Render Props, HOC

## Rôle

Patterns avancés de composition de composants React.

## Tu NE fais PAS

- ❌ Implémenter la logique complexe des hooks → `../hooks/custom-hooks.md`
- ❌ Gérer l'état avec Context, Zustand ou Redux → `../state/`
- ❌ Définir la stratégie de tests → `testing-process`
- ❌ Implémenter des solutions de styling → `../styling/`

## Compound Components

### Principe

Composants qui fonctionnent ensemble avec un état partagé implicite.

### Exemple : Tabs

```tsx
import { createContext, useContext, useState, ReactNode } from 'react';

// Context
interface TabsContextType {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

const TabsContext = createContext<TabsContextType | null>(null);

function useTabsContext() {
  const context = useContext(TabsContext);
  if (!context) {
    throw new Error('Tabs compound components must be used within Tabs');
  }
  return context;
}

// Parent Component
interface TabsProps {
  defaultTab: string;
  children: ReactNode;
}

function Tabs({ defaultTab, children }: TabsProps) {
  const [activeTab, setActiveTab] = useState(defaultTab);

  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div className="tabs">{children}</div>
    </TabsContext.Provider>
  );
}

// Sub-components
interface TabListProps {
  children: ReactNode;
}

function TabList({ children }: TabListProps) {
  return <div className="tab-list" role="tablist">{children}</div>;
}

interface TabProps {
  value: string;
  children: ReactNode;
}

function Tab({ value, children }: TabProps) {
  const { activeTab, setActiveTab } = useTabsContext();

  return (
    <button
      role="tab"
      aria-selected={activeTab === value}
      className={activeTab === value ? 'tab active' : 'tab'}
      onClick={() => setActiveTab(value)}
    >
      {children}
    </button>
  );
}

interface TabPanelProps {
  value: string;
  children: ReactNode;
}

function TabPanel({ value, children }: TabPanelProps) {
  const { activeTab } = useTabsContext();

  if (activeTab !== value) return null;

  return (
    <div role="tabpanel" className="tab-panel">
      {children}
    </div>
  );
}

// Attach sub-components
Tabs.List = TabList;
Tabs.Tab = Tab;
Tabs.Panel = TabPanel;

// Usage
function App() {
  return (
    <Tabs defaultTab="profile">
      <Tabs.List>
        <Tabs.Tab value="profile">Profile</Tabs.Tab>
        <Tabs.Tab value="settings">Settings</Tabs.Tab>
        <Tabs.Tab value="notifications">Notifications</Tabs.Tab>
      </Tabs.List>

      <Tabs.Panel value="profile">
        <ProfileContent />
      </Tabs.Panel>
      <Tabs.Panel value="settings">
        <SettingsContent />
      </Tabs.Panel>
      <Tabs.Panel value="notifications">
        <NotificationsContent />
      </Tabs.Panel>
    </Tabs>
  );
}
```

### Exemple : Accordion

```tsx
const AccordionContext = createContext<{
  openItems: Set<string>;
  toggle: (id: string) => void;
} | null>(null);

function Accordion({ children, multiple = false }: AccordionProps) {
  const [openItems, setOpenItems] = useState<Set<string>>(new Set());

  const toggle = (id: string) => {
    setOpenItems((prev) => {
      const next = new Set(multiple ? prev : []);
      if (next.has(id)) {
        next.delete(id);
      } else {
        next.add(id);
      }
      return next;
    });
  };

  return (
    <AccordionContext.Provider value={{ openItems, toggle }}>
      <div className="accordion">{children}</div>
    </AccordionContext.Provider>
  );
}

function AccordionItem({ id, title, children }: AccordionItemProps) {
  const { openItems, toggle } = useAccordionContext();
  const isOpen = openItems.has(id);

  return (
    <div className="accordion-item">
      <button onClick={() => toggle(id)} aria-expanded={isOpen}>
        {title}
        <ChevronIcon direction={isOpen ? 'up' : 'down'} />
      </button>
      {isOpen && <div className="accordion-content">{children}</div>}
    </div>
  );
}

Accordion.Item = AccordionItem;
```

## Render Props

### Principe

Passer une fonction comme children ou prop pour partager la logique.

### Exemple : Mouse Tracker

```tsx
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
    const handleMove = (e: MouseEvent) => {
      setPosition({ x: e.clientX, y: e.clientY });
    };

    window.addEventListener('mousemove', handleMove);
    return () => window.removeEventListener('mousemove', handleMove);
  }, []);

  return <>{children(position)}</>;
}

// Usage
function App() {
  return (
    <MouseTracker>
      {({ x, y }) => (
        <div>
          Mouse position: {x}, {y}
        </div>
      )}
    </MouseTracker>
  );
}
```

### Exemple : Toggle avec render prop

```tsx
interface ToggleRenderProps {
  isOn: boolean;
  toggle: () => void;
  setOn: () => void;
  setOff: () => void;
}

interface ToggleProps {
  initialValue?: boolean;
  render: (props: ToggleRenderProps) => ReactNode;
}

function Toggle({ initialValue = false, render }: ToggleProps) {
  const [isOn, setIsOn] = useState(initialValue);

  const renderProps: ToggleRenderProps = {
    isOn,
    toggle: () => setIsOn((v) => !v),
    setOn: () => setIsOn(true),
    setOff: () => setIsOn(false),
  };

  return <>{render(renderProps)}</>;
}

// Usage
<Toggle
  render={({ isOn, toggle }) => (
    <button onClick={toggle}>
      {isOn ? 'ON' : 'OFF'}
    </button>
  )}
/>
```

## Higher-Order Components (HOC)

### Principe

Fonction qui prend un composant et retourne un nouveau composant enrichi.

### Exemple : withAuth

```tsx
interface WithAuthProps {
  user: User | null;
}

function withAuth<P extends object>(
  WrappedComponent: React.ComponentType<P & WithAuthProps>
) {
  return function WithAuthComponent(props: P) {
    const { user, loading } = useAuth();

    if (loading) {
      return <Spinner />;
    }

    if (!user) {
      return <Navigate to="/login" />;
    }

    return <WrappedComponent {...props} user={user} />;
  };
}

// Usage
function Dashboard({ user }: { user: User }) {
  return <div>Welcome, {user.name}</div>;
}

const ProtectedDashboard = withAuth(Dashboard);
```

### Exemple : withErrorBoundary

```tsx
interface WithErrorBoundaryOptions {
  fallback: ReactNode;
  onError?: (error: Error, info: ErrorInfo) => void;
}

function withErrorBoundary<P extends object>(
  WrappedComponent: React.ComponentType<P>,
  options: WithErrorBoundaryOptions
) {
  return function WithErrorBoundaryComponent(props: P) {
    return (
      <ErrorBoundary
        fallback={options.fallback}
        onError={options.onError}
      >
        <WrappedComponent {...props} />
      </ErrorBoundary>
    );
  };
}

// Usage
const SafeChart = withErrorBoundary(Chart, {
  fallback: <div>Chart failed to load</div>,
  onError: (error) => logError(error),
});
```

### Conventions HOC

```tsx
// 1. Ne pas modifier le composant original
// 2. Copier les static methods
// 3. Transférer les refs avec forwardRef
// 4. Nommer pour le debugging

function withLogging<P extends object>(
  WrappedComponent: React.ComponentType<P>
) {
  const WithLogging = forwardRef<unknown, P>((props, ref) => {
    useEffect(() => {
      console.log(`${WrappedComponent.displayName} mounted`);
    }, []);

    return <WrappedComponent {...props} ref={ref} />;
  });

  // DisplayName pour DevTools
  WithLogging.displayName = `withLogging(${
    WrappedComponent.displayName || WrappedComponent.name || 'Component'
  })`;

  return WithLogging;
}
```

## Slots Pattern

### Inspiré de Vue/Svelte

```tsx
interface CardProps {
  header?: ReactNode;
  footer?: ReactNode;
  children: ReactNode;
}

function Card({ header, footer, children }: CardProps) {
  return (
    <div className="card">
      {header && <div className="card-header">{header}</div>}
      <div className="card-body">{children}</div>
      {footer && <div className="card-footer">{footer}</div>}
    </div>
  );
}

// Usage
<Card
  header={<h2>Title</h2>}
  footer={<Button>Submit</Button>}
>
  <p>Card content</p>
</Card>
```

## Quand Utiliser Quoi

| Pattern | Cas d'usage |
|---------|-------------|
| **Compound** | Composants qui fonctionnent ensemble (Tabs, Menu, Accordion) |
| **Render Props** | Partager comportement avec flexibilité totale |
| **HOC** | Réutiliser logique cross-cutting (auth, logging, error handling) |
| **Slots** | Layouts flexibles avec zones définies |

## Préférer les Hooks

```tsx
// ❌ HOC complexe
const EnhancedComponent = withAuth(withTheme(withI18n(MyComponent)));

// ✅ Hooks composables
function MyComponent() {
  const { user } = useAuth();
  const { theme } = useTheme();
  const { t } = useI18n();

  // ...
}
```

## Voir aussi

- `functional.md` - Composants de base
- `../hooks/custom-hooks.md` - Alternative aux HOC
- `../state/context.md` - Pour le state partagé

## Livrables

| Livrable | Description |
|----------|-------------|
| Pattern de composition | Implémentation Compound/Render Props/HOC |
| Types TypeScript | Interfaces pour props et contexte |
| Exemples d'usage | Cas d'utilisation du pattern choisi |
