---
name: memoization
description: React.memo, useMemo, and useCallback for optimization
workflows:
  - id: react-perf-optim
    template: wf-evolution
    phase: Réalisation
    name: Optimisation performance React
    duration: 0.5-1 jour
---

# Memoization - React.memo, useMemo, useCallback

## Rôle

Optimisation des re-renders React avec les techniques de memoization.

## Tu NE fais PAS

- ❌ Optimiser le backend ou les APIs → `backend-developer`
- ❌ Implémenter les corrections (juste identifier et conseiller) → développeur
- ❌ Définir la stratégie de tests de performance → `testing-process`
- ❌ Optimiser le bundle et le build → `code-splitting.md` ou `devops`

## Quand Optimiser ?

### Règle d'or

> "Mesurer d'abord, optimiser ensuite"

### Signaux d'optimisation nécessaire

- UI laggy ou saccadée
- Composants re-render sans raison
- Calculs coûteux à chaque render
- Listes longues avec items complexes

### React DevTools Profiler

```tsx
// Activer le highlight des re-renders
// React DevTools → Settings → Highlight updates
```

## React.memo

### Quand utiliser

- Composant pur (même props = même output)
- Re-render fréquent du parent
- Render coûteux

### Syntaxe

```tsx
import { memo } from 'react';

interface UserCardProps {
  user: User;
  onSelect: (id: string) => void;
}

const UserCard = memo(function UserCard({ user, onSelect }: UserCardProps) {
  console.log('UserCard render:', user.id);

  return (
    <div onClick={() => onSelect(user.id)}>
      <h3>{user.name}</h3>
      <p>{user.email}</p>
    </div>
  );
});
```

### Comparaison personnalisée

```tsx
const UserCard = memo(
  function UserCard({ user, onSelect }: UserCardProps) {
    return (/* ... */);
  },
  (prevProps, nextProps) => {
    // Retourne true si les props sont égales (skip re-render)
    return prevProps.user.id === nextProps.user.id &&
           prevProps.user.name === nextProps.user.name;
  }
);
```

### Attention aux props objets/fonctions

```tsx
// ❌ Nouvelle référence à chaque render du parent
function Parent() {
  return (
    <MemoizedChild
      config={{ theme: 'dark' }}  // Nouvel objet
      onClick={() => console.log('click')}  // Nouvelle fonction
    />
  );
}

// ✅ Références stables
function Parent() {
  const config = useMemo(() => ({ theme: 'dark' }), []);
  const onClick = useCallback(() => console.log('click'), []);

  return <MemoizedChild config={config} onClick={onClick} />;
}
```

## useMemo

### Quand utiliser

- Calculs coûteux
- Référence stable pour objets/arrays
- Éviter de recréer des objets passés à des composants memoized

### Calcul coûteux

```tsx
function ProductList({ products, filter }: Props) {
  // Filtrer seulement quand products ou filter changent
  const filteredProducts = useMemo(() => {
    console.log('Filtering products...');
    return products.filter((p) => {
      // Logique de filtrage complexe
      return matchesFilter(p, filter);
    });
  }, [products, filter]);

  return (
    <ul>
      {filteredProducts.map((product) => (
        <ProductItem key={product.id} product={product} />
      ))}
    </ul>
  );
}
```

### Référence stable

```tsx
function Chart({ data }: { data: number[] }) {
  // Objet de configuration stable
  const chartOptions = useMemo(() => ({
    responsive: true,
    scales: {
      y: { beginAtZero: true },
    },
  }), []);

  // Données transformées stables
  const chartData = useMemo(() => ({
    labels: data.map((_, i) => `Day ${i + 1}`),
    datasets: [{
      label: 'Values',
      data,
    }],
  }), [data]);

  return <ChartComponent options={chartOptions} data={chartData} />;
}
```

### Calcul dérivé

```tsx
function Dashboard({ transactions }: { transactions: Transaction[] }) {
  const stats = useMemo(() => {
    const total = transactions.reduce((sum, t) => sum + t.amount, 0);
    const average = total / transactions.length;
    const max = Math.max(...transactions.map((t) => t.amount));

    return { total, average, max };
  }, [transactions]);

  return (
    <div>
      <Stat label="Total" value={stats.total} />
      <Stat label="Average" value={stats.average} />
      <Stat label="Max" value={stats.max} />
    </div>
  );
}
```

## useCallback

### Quand utiliser

- Fonction passée à un composant memoized
- Fonction dans les dépendances d'un useEffect
- Event handlers pour des listes

### Syntaxe

```tsx
function Parent() {
  const [count, setCount] = useState(0);

  // Stable tant que les deps ne changent pas
  const increment = useCallback(() => {
    setCount((c) => c + 1);
  }, []);

  const incrementBy = useCallback((amount: number) => {
    setCount((c) => c + amount);
  }, []);

  return (
    <>
      <MemoizedButton onClick={increment}>+1</MemoizedButton>
      <MemoizedButton onClick={() => incrementBy(5)}>+5</MemoizedButton>
    </>
  );
}
```

### Pour des listes

```tsx
function TodoList({ todos, onToggle, onDelete }: Props) {
  // Évite de recréer pour chaque item
  const handleToggle = useCallback((id: string) => {
    onToggle(id);
  }, [onToggle]);

  const handleDelete = useCallback((id: string) => {
    onDelete(id);
  }, [onDelete]);

  return (
    <ul>
      {todos.map((todo) => (
        <MemoizedTodoItem
          key={todo.id}
          todo={todo}
          onToggle={handleToggle}
          onDelete={handleDelete}
        />
      ))}
    </ul>
  );
}
```

## Patterns Avancés

### useEvent (pattern)

```tsx
// Hook pour callback stable qui voit toujours les dernières valeurs
function useEvent<T extends (...args: any[]) => any>(callback: T): T {
  const ref = useRef(callback);

  useLayoutEffect(() => {
    ref.current = callback;
  });

  return useCallback((...args: Parameters<T>) => {
    return ref.current(...args);
  }, []) as T;
}

// Usage
function Component() {
  const [count, setCount] = useState(0);

  // Toujours stable, mais voit le dernier count
  const logCount = useEvent(() => {
    console.log('Count:', count);
  });

  return <MemoizedChild onClick={logCount} />;
}
```

### Context Split

```tsx
// Éviter les re-renders avec Context

// ❌ Un seul contexte = tous re-render
const AppContext = createContext({ user, theme, settings });

// ✅ Contextes séparés
const UserContext = createContext(null);
const ThemeContext = createContext(null);
const SettingsContext = createContext(null);

// Composant qui n'utilise que theme ne re-render pas quand user change
```

### Virtualisation

```tsx
import { useVirtualizer } from '@tanstack/react-virtual';

function VirtualList({ items }: { items: Item[] }) {
  const parentRef = useRef<HTMLDivElement>(null);

  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50,
  });

  return (
    <div ref={parentRef} style={{ height: '400px', overflow: 'auto' }}>
      <div
        style={{
          height: `${virtualizer.getTotalSize()}px`,
          position: 'relative',
        }}
      >
        {virtualizer.getVirtualItems().map((virtualItem) => (
          <div
            key={virtualItem.key}
            style={{
              position: 'absolute',
              top: 0,
              transform: `translateY(${virtualItem.start}px)`,
              height: `${virtualItem.size}px`,
            }}
          >
            {items[virtualItem.index].name}
          </div>
        ))}
      </div>
    </div>
  );
}
```

## Anti-patterns

```tsx
// ❌ useMemo pour tout
const name = useMemo(() => `${first} ${last}`, [first, last]);

// ✅ Simple concaténation, pas besoin de memo
const name = `${first} ${last}`;

// ❌ memo sans stabiliser les props
const MemoizedChild = memo(Child);
<MemoizedChild onClick={() => {}} /> // Nouvelle fonction à chaque render!

// ❌ Dépendances manquantes
const callback = useCallback(() => {
  doSomething(value); // value devrait être dans les deps
}, []); // Stale closure!

// ❌ Premature optimization
// Ajouter memo/useMemo/useCallback partout "au cas où"
```

## Checklist

1. [ ] Profiler avec React DevTools d'abord
2. [ ] Identifier les composants qui re-render trop
3. [ ] memo() pour composants purs avec render coûteux
4. [ ] useMemo() pour calculs coûteux ou références stables
5. [ ] useCallback() pour fonctions passées à composants memoized
6. [ ] Vérifier les dépendances

## Voir aussi

- `code-splitting.md` - Réduction du bundle
- `../hooks/custom-hooks.md` - Hooks optimisés
- `../data/react-query.md` - Caching server state

## Livrables

| Livrable | Description |
|----------|-------------|
| Composants optimisés | Code avec React.memo et comparaison personnalisée |
| Patterns memoization | Implémentation useMemo/useCallback ciblée |
| Analyse de performance | Identification des bottlenecks avec React DevTools |
