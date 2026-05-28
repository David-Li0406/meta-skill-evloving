---
name: ref-hooks
description: useRef, forwardRef, and useImperativeHandle for DOM refs and persistent values
workflows:
  - id: ref-hooks-impl
    template: wf-creation
    phase: Production
    name: Implémentation ref hooks
    duration: 0.5 jour
---

# Ref Hooks - useRef, forwardRef & useImperativeHandle

## Rôle

Implémentation des hooks de références : `useRef`, `forwardRef`, et `useImperativeHandle`.

## Tu NE fais PAS

- ❌ Définir la structure des composants → `../components/functional.md`
- ❌ Gérer l'état qui doit causer un re-render (utiliser useState) → `state-hooks.md`
- ❌ Définir la stratégie de tests → `testing-process`
- ❌ Implémenter des solutions de styling → `../styling/`

## useRef

### Deux usages principaux

1. **Référence DOM** - Accéder à un élément du DOM
2. **Valeur persistante** - Stocker une valeur sans re-render

### Syntaxe

```tsx
const ref = useRef<T>(initialValue);
// ref.current contient la valeur
```

### Référence DOM

```tsx
function TextInput() {
  const inputRef = useRef<HTMLInputElement>(null);

  const focusInput = () => {
    inputRef.current?.focus();
  };

  return (
    <>
      <input ref={inputRef} type="text" />
      <button onClick={focusInput}>Focus</button>
    </>
  );
}
```

### Valeur persistante (sans re-render)

```tsx
function Timer() {
  const [count, setCount] = useState(0);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  const startTimer = () => {
    intervalRef.current = setInterval(() => {
      setCount(c => c + 1);
    }, 1000);
  };

  const stopTimer = () => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
    }
  };

  useEffect(() => {
    return () => stopTimer(); // Cleanup
  }, []);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={startTimer}>Start</button>
      <button onClick={stopTimer}>Stop</button>
    </div>
  );
}
```

### Valeur précédente

```tsx
function usePrevious<T>(value: T): T | undefined {
  const ref = useRef<T>();

  useEffect(() => {
    ref.current = value;
  }, [value]);

  return ref.current;
}

// Usage
function Counter() {
  const [count, setCount] = useState(0);
  const prevCount = usePrevious(count);

  return (
    <p>
      Now: {count}, Before: {prevCount}
    </p>
  );
}
```

### Callback ref

```tsx
function MeasuredComponent() {
  const [height, setHeight] = useState(0);

  const measuredRef = useCallback((node: HTMLDivElement | null) => {
    if (node !== null) {
      setHeight(node.getBoundingClientRect().height);
    }
  }, []);

  return (
    <div ref={measuredRef}>
      Height: {height}px
    </div>
  );
}
```

## forwardRef

### Passer une ref à un composant enfant

```tsx
interface InputProps {
  label: string;
  type?: string;
}

const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, type = 'text' }, ref) => {
    return (
      <label>
        {label}
        <input ref={ref} type={type} />
      </label>
    );
  }
);

Input.displayName = 'Input';

// Usage
function Form() {
  const inputRef = useRef<HTMLInputElement>(null);

  return <Input ref={inputRef} label="Email" />;
}
```

### Avec composants génériques

```tsx
interface ListProps<T> {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
}

const List = forwardRef(<T,>(
  { items, renderItem }: ListProps<T>,
  ref: React.ForwardedRef<HTMLUListElement>
) => {
  return (
    <ul ref={ref}>
      {items.map((item, index) => (
        <li key={index}>{renderItem(item)}</li>
      ))}
    </ul>
  );
});
```

## useImperativeHandle

### Exposer une API personnalisée

```tsx
interface VideoPlayerHandle {
  play: () => void;
  pause: () => void;
  seek: (time: number) => void;
}

interface VideoPlayerProps {
  src: string;
}

const VideoPlayer = forwardRef<VideoPlayerHandle, VideoPlayerProps>(
  ({ src }, ref) => {
    const videoRef = useRef<HTMLVideoElement>(null);

    useImperativeHandle(ref, () => ({
      play() {
        videoRef.current?.play();
      },
      pause() {
        videoRef.current?.pause();
      },
      seek(time: number) {
        if (videoRef.current) {
          videoRef.current.currentTime = time;
        }
      },
    }), []);

    return <video ref={videoRef} src={src} />;
  }
);

// Usage
function App() {
  const playerRef = useRef<VideoPlayerHandle>(null);

  const handleSkip = () => {
    playerRef.current?.seek(30);
  };

  return (
    <>
      <VideoPlayer ref={playerRef} src="/video.mp4" />
      <button onClick={handleSkip}>Skip to 30s</button>
    </>
  );
}
```

### Input personnalisé avec focus et validation

```tsx
interface CustomInputHandle {
  focus: () => void;
  blur: () => void;
  validate: () => boolean;
  getValue: () => string;
}

const CustomInput = forwardRef<CustomInputHandle, InputProps>(
  ({ label }, ref) => {
    const inputRef = useRef<HTMLInputElement>(null);
    const [error, setError] = useState('');

    useImperativeHandle(ref, () => ({
      focus: () => inputRef.current?.focus(),
      blur: () => inputRef.current?.blur(),
      validate: () => {
        const value = inputRef.current?.value || '';
        const isValid = value.length > 0;
        setError(isValid ? '' : 'Required field');
        return isValid;
      },
      getValue: () => inputRef.current?.value || '',
    }), []);

    return (
      <div>
        <label>{label}</label>
        <input ref={inputRef} />
        {error && <span className="error">{error}</span>}
      </div>
    );
  }
);
```

## Bonnes Pratiques

1. **useRef pour valeurs mutables** - Timer IDs, previous values, instances
2. **Ne pas lire/écrire ref.current pendant le render** - Sauf initialisation
3. **forwardRef pour composants réutilisables** - Bibliothèques de composants
4. **useImperativeHandle avec parcimonie** - Préférer les props

## Anti-patterns

```tsx
// ❌ Accéder à ref.current pendant le render
function Bad() {
  const ref = useRef(null);
  console.log(ref.current); // null au premier render!
  return <div ref={ref} />;
}

// ✅ Accéder dans un effet ou handler
function Good() {
  const ref = useRef(null);
  useEffect(() => {
    console.log(ref.current); // Element DOM
  }, []);
  return <div ref={ref} />;
}

// ❌ Utiliser ref pour état qui doit trigger re-render
const countRef = useRef(0);
countRef.current++; // Ne cause pas de re-render!

// ✅ Utiliser useState
const [count, setCount] = useState(0);
```

## Voir aussi

- `state-hooks.md` - Pour l'état avec re-render
- `effect-hooks.md` - Pour les effets de bord
- `../components/functional.md` - Pour les patterns de composants

## Livrables

| Livrable | Description |
|----------|-------------|
| Implémentation ref | Code useRef/forwardRef/useImperativeHandle |
| Types TypeScript | Types pour refs et handles exposés |
| Patterns d'usage | Exemples DOM refs, valeurs persistantes, API custom |
