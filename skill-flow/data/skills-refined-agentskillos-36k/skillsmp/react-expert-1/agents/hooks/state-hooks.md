---
name: state-hooks
description: useState and useReducer for local state management
workflows:
  - id: state-hooks-impl
    template: wf-creation
    phase: Production
    name: Implémentation state hooks
    duration: 0.5 jour
---

# State Hooks - useState & useReducer

## Rôle

Implémentation des hooks de gestion d'état local : `useState` et `useReducer`.

## Tu NE fais PAS

- ❌ Définir la structure des composants → `../components/functional.md`
- ❌ Implémenter des solutions de styling → `../styling/`
- ❌ Définir la stratégie de tests → `testing-process`
- ❌ Implémenter les tests (donner des exemples uniquement) → `../testing/hooks-testing.md`

## useState

### Syntaxe de base

```tsx
const [state, setState] = useState<T>(initialValue);
```

### Patterns courants

#### État simple
```tsx
const [count, setCount] = useState(0);
const [name, setName] = useState('');
const [isOpen, setIsOpen] = useState(false);
```

#### État avec type explicite
```tsx
interface User {
  id: string;
  name: string;
  email: string;
}

const [user, setUser] = useState<User | null>(null);
```

#### Initialisation lazy
```tsx
// Pour les calculs coûteux, passer une fonction
const [data, setData] = useState(() => {
  return expensiveComputation();
});
```

#### Mise à jour fonctionnelle
```tsx
// ✅ Correct - utilise la valeur précédente
setCount(prev => prev + 1);

// ❌ Incorrect - peut causer des bugs avec batching
setCount(count + 1);
```

#### État objet
```tsx
const [form, setForm] = useState({ name: '', email: '' });

// Mise à jour partielle
setForm(prev => ({ ...prev, name: 'John' }));
```

## useReducer

### Quand utiliser useReducer

- État avec logique complexe
- Plusieurs valeurs liées
- Transitions d'état prévisibles
- Tests plus faciles (reducer pur)

### Syntaxe

```tsx
const [state, dispatch] = useReducer(reducer, initialState);
```

### Pattern complet

```tsx
// Types
interface State {
  count: number;
  step: number;
}

type Action =
  | { type: 'increment' }
  | { type: 'decrement' }
  | { type: 'reset' }
  | { type: 'setStep'; payload: number };

// Initial state
const initialState: State = {
  count: 0,
  step: 1,
};

// Reducer (fonction pure)
function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'increment':
      return { ...state, count: state.count + state.step };
    case 'decrement':
      return { ...state, count: state.count - state.step };
    case 'reset':
      return initialState;
    case 'setStep':
      return { ...state, step: action.payload };
    default:
      return state;
  }
}

// Composant
function Counter() {
  const [state, dispatch] = useReducer(reducer, initialState);

  return (
    <div>
      <p>Count: {state.count}</p>
      <button onClick={() => dispatch({ type: 'increment' })}>+</button>
      <button onClick={() => dispatch({ type: 'decrement' })}>-</button>
      <button onClick={() => dispatch({ type: 'reset' })}>Reset</button>
    </div>
  );
}
```

### Initialisation lazy

```tsx
function init(initialCount: number): State {
  return { count: initialCount, step: 1 };
}

const [state, dispatch] = useReducer(reducer, initialCount, init);
```

## Bonnes Pratiques

### useState

1. **Un état par concept** - Éviter les objets fourre-tout
2. **Mise à jour fonctionnelle** - Toujours quand dépend de l'état précédent
3. **Immutabilité** - Ne jamais muter directement

### useReducer

1. **Types discriminés** - Pour les actions TypeScript
2. **Exhaustive checks** - `never` dans le default
3. **Actions sémantiques** - Nommer par intention, pas par implémentation

## Anti-patterns

```tsx
// ❌ Mutation directe
state.count = 5;
setState(state);

// ✅ Copie
setState({ ...state, count: 5 });

// ❌ Oublier les dépendances avec useEffect
useEffect(() => {
  setCount(count + 1); // count dans les deps!
}, []);

// ✅ Mise à jour fonctionnelle
useEffect(() => {
  setCount(prev => prev + 1);
}, []);
```

## Voir aussi

- `effect-hooks.md` - Pour les effets de bord
- `custom-hooks.md` - Pour extraire la logique
- `../state/context.md` - Pour l'état partagé

## Livrables

| Livrable | Description |
|----------|-------------|
| Implémentation hook | Code useState ou useReducer avec types |
| Types d'état | Interfaces TypeScript pour state et actions |
| Patterns d'usage | Exemples d'utilisation et best practices |
