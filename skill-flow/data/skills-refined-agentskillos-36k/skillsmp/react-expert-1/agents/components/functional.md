---
name: functional
description: React functional components with props, children, and composition patterns
workflows:
  - id: react-component-creation
    template: wf-creation
    phase: Production
    name: Création composants React
    duration: 0.5-1 jour
---

# Functional Components - Composants Fonctionnels

## Rôle

Création et patterns de composants fonctionnels React avec TypeScript.

## Tu NE fais PAS

- ❌ Implémenter la logique des hooks personnalisés → `../hooks/custom-hooks.md`
- ❌ Gérer l'état global ou les patterns de state management → `../state/`
- ❌ Définir la stratégie de tests des composants → `testing-process`
- ❌ Implémenter les tests (donner des exemples uniquement) → `../testing/rtl.md`

## Syntaxe de Base

### Composant simple

```tsx
interface GreetingProps {
  name: string;
}

function Greeting({ name }: GreetingProps) {
  return <h1>Hello, {name}!</h1>;
}
```

### Avec React.FC (optionnel)

```tsx
// FC ajoute implicitement children (deprecated en React 18)
const Greeting: React.FC<GreetingProps> = ({ name }) => {
  return <h1>Hello, {name}!</h1>;
};
```

### Recommandation : fonction nommée

```tsx
// ✅ Préféré - meilleur debugging, hoisting
function Button({ onClick, children }: ButtonProps) {
  return <button onClick={onClick}>{children}</button>;
}

// ❌ Moins recommandé
const Button = ({ onClick, children }: ButtonProps) => {
  return <button onClick={onClick}>{children}</button>;
};
```

## Props

### Props basiques

```tsx
interface UserCardProps {
  name: string;
  email: string;
  age?: number; // Optionnel
  isAdmin?: boolean;
}

function UserCard({ name, email, age, isAdmin = false }: UserCardProps) {
  return (
    <div className="user-card">
      <h2>{name}</h2>
      <p>{email}</p>
      {age && <p>Age: {age}</p>}
      {isAdmin && <span className="badge">Admin</span>}
    </div>
  );
}
```

### Props avec valeurs par défaut

```tsx
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  children: React.ReactNode;
  onClick?: () => void;
}

function Button({
  variant = 'primary',
  size = 'md',
  disabled = false,
  children,
  onClick,
}: ButtonProps) {
  return (
    <button
      className={`btn btn-${variant} btn-${size}`}
      disabled={disabled}
      onClick={onClick}
    >
      {children}
    </button>
  );
}
```

### Spread props

```tsx
interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: string;
}

function Input({ label, error, ...inputProps }: InputProps) {
  return (
    <div className="form-group">
      <label>{label}</label>
      <input {...inputProps} className={error ? 'input-error' : ''} />
      {error && <span className="error">{error}</span>}
    </div>
  );
}

// Usage
<Input
  label="Email"
  type="email"
  placeholder="john@example.com"
  error={errors.email}
/>
```

## Children

### React.ReactNode

```tsx
interface CardProps {
  title: string;
  children: React.ReactNode;
}

function Card({ title, children }: CardProps) {
  return (
    <div className="card">
      <h2>{title}</h2>
      <div className="card-content">{children}</div>
    </div>
  );
}

// Usage
<Card title="My Card">
  <p>Some content</p>
  <Button>Click me</Button>
</Card>
```

### Children comme fonction (Render Props)

```tsx
interface DataProviderProps<T> {
  data: T;
  children: (data: T) => React.ReactNode;
}

function DataProvider<T>({ data, children }: DataProviderProps<T>) {
  return <>{children(data)}</>;
}

// Usage
<DataProvider data={user}>
  {(user) => <UserProfile user={user} />}
</DataProvider>
```

### React.ReactElement (plus strict)

```tsx
interface WrapperProps {
  children: React.ReactElement; // Un seul élément React
}

function Wrapper({ children }: WrapperProps) {
  return React.cloneElement(children, {
    className: 'wrapped',
  });
}
```

## Patterns de Composition

### Container / Presentational

```tsx
// Container - logique
function UserListContainer() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUsers().then(setUsers).finally(() => setLoading(false));
  }, []);

  if (loading) return <Spinner />;
  return <UserList users={users} />;
}

// Presentational - affichage
function UserList({ users }: { users: User[] }) {
  return (
    <ul>
      {users.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

### Layout Components

```tsx
interface LayoutProps {
  header?: React.ReactNode;
  sidebar?: React.ReactNode;
  children: React.ReactNode;
  footer?: React.ReactNode;
}

function Layout({ header, sidebar, children, footer }: LayoutProps) {
  return (
    <div className="layout">
      {header && <header>{header}</header>}
      <div className="layout-body">
        {sidebar && <aside>{sidebar}</aside>}
        <main>{children}</main>
      </div>
      {footer && <footer>{footer}</footer>}
    </div>
  );
}

// Usage
<Layout
  header={<Navigation />}
  sidebar={<Sidebar />}
  footer={<Footer />}
>
  <PageContent />
</Layout>
```

## Conditional Rendering

### Patterns recommandés

```tsx
function ConditionalExample({ isLoggedIn, user, items }: Props) {
  // ✅ Early return
  if (!isLoggedIn) {
    return <LoginPrompt />;
  }

  // ✅ Ternaire pour alternative simple
  return (
    <div>
      {user.isAdmin ? <AdminPanel /> : <UserDashboard />}

      {/* ✅ && pour condition simple */}
      {items.length > 0 && <ItemList items={items} />}

      {/* ✅ Null coalescing */}
      <p>Welcome, {user.nickname ?? user.name}</p>
    </div>
  );
}
```

### Éviter les pièges

```tsx
// ❌ Peut afficher "0"
{count && <Items count={count} />}

// ✅ Correct
{count > 0 && <Items count={count} />}

// ❌ Ternaire complexe illisible
{condition1 ? (condition2 ? <A /> : <B />) : <C />}

// ✅ Extraire en variable ou fonction
const Component = getComponentForState(condition1, condition2);
return <Component />;
```

## Bonnes Pratiques

1. **Un composant = une responsabilité**
2. **Props explicites** - Éviter les spreads excessifs
3. **Nommage descriptif** - `UserProfileCard` > `Card`
4. **Colocation** - Styles et tests proches du composant
5. **Export nommé** - Préférer aux exports default

## Anti-patterns

```tsx
// ❌ Logique dans le render
function Bad() {
  const [items] = useState([1, 2, 3]);
  const sorted = items.sort(); // Mutation!
  return <List items={sorted} />;
}

// ✅ useMemo pour calculs
function Good() {
  const [items] = useState([1, 2, 3]);
  const sorted = useMemo(() => [...items].sort(), [items]);
  return <List items={sorted} />;
}
```

## Voir aussi

- `composition.md` - Patterns avancés
- `forms.md` - Composants de formulaire
- `../hooks/custom-hooks.md` - Extraction de logique

## Livrables

| Livrable | Description |
|----------|-------------|
| Code composant | Composant fonctionnel React avec TypeScript |
| Interface Props | Types TypeScript pour les props avec documentation |
| Exemples d'usage | Cas d'utilisation concrets du composant |
