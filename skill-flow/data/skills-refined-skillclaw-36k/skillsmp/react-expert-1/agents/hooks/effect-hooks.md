---
name: effect-hooks
description: useEffect and useLayoutEffect for side effects
workflows:
  - id: effect-hooks-impl
    template: wf-creation
    phase: Production
    name: Implémentation effect hooks
    duration: 0.5 jour
---

# Effect Hooks - useEffect & useLayoutEffect

## Rôle

Implémentation des hooks d'effets de bord : `useEffect` et `useLayoutEffect`.

## Tu NE fais PAS

- ❌ Définir la structure des composants → `../components/functional.md`
- ❌ Implémenter des solutions de styling → `../styling/`
- ❌ Définir la stratégie de tests → `testing-process`
- ❌ Gérer le server state (préférer React Query/SWR) → `../data/`

## useEffect

### Syntaxe

```tsx
useEffect(() => {
  // Effet
  return () => {
    // Cleanup (optionnel)
  };
}, [dependencies]);
```

### Patterns courants

#### Effet au montage uniquement
```tsx
useEffect(() => {
  console.log('Component mounted');

  return () => {
    console.log('Component unmounted');
  };
}, []); // Tableau vide = une seule exécution
```

#### Effet avec dépendances
```tsx
useEffect(() => {
  document.title = `Count: ${count}`;
}, [count]); // Se ré-exécute quand count change
```

#### Data fetching
```tsx
useEffect(() => {
  let cancelled = false;

  async function fetchData() {
    try {
      const response = await fetch(`/api/user/${userId}`);
      const data = await response.json();

      if (!cancelled) {
        setUser(data);
      }
    } catch (error) {
      if (!cancelled) {
        setError(error);
      }
    }
  }

  fetchData();

  return () => {
    cancelled = true;
  };
}, [userId]);
```

#### Avec AbortController (recommandé)
```tsx
useEffect(() => {
  const controller = new AbortController();

  async function fetchData() {
    try {
      const response = await fetch(`/api/user/${userId}`, {
        signal: controller.signal,
      });
      const data = await response.json();
      setUser(data);
    } catch (error) {
      if (error.name !== 'AbortError') {
        setError(error);
      }
    }
  }

  fetchData();

  return () => controller.abort();
}, [userId]);
```

#### Event listeners
```tsx
useEffect(() => {
  function handleResize() {
    setWindowSize({
      width: window.innerWidth,
      height: window.innerHeight,
    });
  }

  window.addEventListener('resize', handleResize);

  return () => {
    window.removeEventListener('resize', handleResize);
  };
}, []);
```

#### Subscriptions
```tsx
useEffect(() => {
  const subscription = eventEmitter.subscribe('event', handler);

  return () => subscription.unsubscribe();
}, [handler]);
```

#### Timers
```tsx
useEffect(() => {
  const intervalId = setInterval(() => {
    setTime(new Date());
  }, 1000);

  return () => clearInterval(intervalId);
}, []);
```

## useLayoutEffect

### Quand utiliser

- Mesurer le DOM avant le paint
- Synchroniser avec les mutations DOM
- Éviter les "flickering"

### Syntaxe identique

```tsx
useLayoutEffect(() => {
  // S'exécute de manière synchrone après les mutations DOM
  // mais AVANT le paint du navigateur
}, [dependencies]);
```

### Exemple : Mesure de tooltip
```tsx
function Tooltip({ children, targetRef }) {
  const [position, setPosition] = useState({ top: 0, left: 0 });
  const tooltipRef = useRef<HTMLDivElement>(null);

  useLayoutEffect(() => {
    if (!targetRef.current || !tooltipRef.current) return;

    const targetRect = targetRef.current.getBoundingClientRect();
    const tooltipRect = tooltipRef.current.getBoundingClientRect();

    setPosition({
      top: targetRect.top - tooltipRect.height - 8,
      left: targetRect.left + (targetRect.width - tooltipRect.width) / 2,
    });
  }, [targetRef]);

  return (
    <div ref={tooltipRef} style={{ position: 'fixed', ...position }}>
      {children}
    </div>
  );
}
```

### Attention SSR

```tsx
// useLayoutEffect génère un warning en SSR
// Solution : utiliser useEffect côté serveur
import { useEffect, useLayoutEffect } from 'react';

const useIsomorphicLayoutEffect =
  typeof window !== 'undefined' ? useLayoutEffect : useEffect;
```

## Règles des Dépendances

### Toutes les valeurs utilisées doivent être dans les deps

```tsx
// ❌ Bug potentiel
useEffect(() => {
  fetchUser(userId);
}, []); // userId manquant!

// ✅ Correct
useEffect(() => {
  fetchUser(userId);
}, [userId]);
```

### Fonctions stables

```tsx
// ❌ Nouvelle fonction à chaque render
useEffect(() => {
  const handler = () => console.log(count);
  window.addEventListener('click', handler);
  return () => window.removeEventListener('click', handler);
}, [count]);

// ✅ Avec useCallback si nécessaire
const handler = useCallback(() => {
  console.log(count);
}, [count]);

useEffect(() => {
  window.addEventListener('click', handler);
  return () => window.removeEventListener('click', handler);
}, [handler]);
```

## Bonnes Pratiques

1. **Toujours cleanup** - Éviter les fuites mémoire
2. **Une responsabilité par effet** - Séparer les effets distincts
3. **Éviter les dépendances objets** - Comparer par valeur
4. **Préférer useEffect** - useLayoutEffect seulement si nécessaire

## Anti-patterns

```tsx
// ❌ Effet sans cleanup pour subscription
useEffect(() => {
  socket.on('message', handler);
}, []);

// ❌ Dépendance objet qui change à chaque render
useEffect(() => {
  fetch(options);
}, [options]); // options = { method: 'GET' } recréé

// ❌ Logique synchrone dans useEffect
useEffect(() => {
  setValue(props.value); // Utiliser directement props.value
}, [props.value]);
```

## Voir aussi

- `state-hooks.md` - Pour la gestion d'état
- `custom-hooks.md` - Pour extraire les effets
- `../data/react-query.md` - Pour le data fetching

## Livrables

| Livrable | Description |
|----------|-------------|
| Implémentation effet | Code useEffect/useLayoutEffect avec cleanup |
| Gestion dépendances | Array de dépendances approprié et justifié |
| Patterns d'usage | Exemples avec subscriptions, timers, data fetching |
