# Examples

Working code examples you can run and learn from.

## Available Examples

| Example | Description | Lines | Concepts |
|---------|-------------|-------|----------|
| `minimal-idle-game.tsx` | Complete single-file idle game | ~150 | Resources, upgrades, save, tick loop |

## Running the Example

### Option 1: Paste into existing project

1. Create a Vite + React + TypeScript project
2. Install dependencies: `npm install zustand`
3. Replace `App.tsx` with the example code
4. Run: `npm run dev`

### Option 2: Quick start

```bash
# Create project
npm create vite@latest my-idle-game -- --template react-ts
cd my-idle-game

# Install dependencies
npm install zustand

# Replace src/App.tsx with example code
# Replace src/index.css with basic styles

# Run
npm run dev
```

### Minimal CSS (add to index.css)

```css
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: system-ui, sans-serif;
  background: #0a0a0f;
  color: #e8e8e8;
  min-height: 100vh;
}

button {
  cursor: pointer;
  padding: 8px 16px;
  border: 1px solid #2d2d44;
  border-radius: 4px;
  background: #1a1a2e;
  color: #e8e8e8;
}

button:hover:not(:disabled) {
  background: #2d2d44;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
```

## What the Example Demonstrates

### 1. Game Loop (100ms tick)

```typescript
useEffect(() => {
  const interval = setInterval(() => {
    const delta = (Date.now() - lastTick) / 1000;
    addCredits(incomePerSecond * delta);
    setLastTick(Date.now());
  }, 100);
  return () => clearInterval(interval);
}, []);
```

### 2. Zustand State Management

```typescript
const useStore = create(persist(
  (set, get) => ({
    credits: 0,
    addCredits: (n) => set((s) => ({ credits: s.credits + n })),
  }),
  { name: 'save' }
));
```

### 3. Exponential Upgrade Costs

```typescript
const cost = Math.floor(baseCost * Math.pow(1.5, level));
```

### 4. Auto-save via Persist

The `persist` middleware automatically saves to localStorage.

## Extending the Example

### Add More Upgrades

```typescript
const UPGRADES = [
  { id: 'click', name: 'Better Clicks', baseCost: 10, effect: 0.1 },
  { id: 'auto', name: 'Auto Clicker', baseCost: 100, effect: 1 },
  { id: 'multi', name: 'Multiplier', baseCost: 1000, effect: 0.5 },
];
```

### Add Energy System

```typescript
interface State {
  credits: number;
  energy: number;
  maxEnergy: number;
}
```

### Add Items/Collection

```typescript
interface State {
  ownedItems: string[];
  addItem: (id: string) => void;
}
```

## Next Steps

After understanding this example:

1. Read [patterns/resource-system.md](../patterns/resource-system.md) for currency design
2. Read [patterns/upgrade-tree.md](../patterns/upgrade-tree.md) for upgrade systems
3. Copy [templates/](../templates/) for production-ready code
4. Check [references/](../references/) for complete architecture
