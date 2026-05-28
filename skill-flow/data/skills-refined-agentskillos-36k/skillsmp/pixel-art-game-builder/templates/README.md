# Templates

Ready-to-use code templates. Copy these into your project and adapt as needed.

## Usage

1. Copy the template file into your project
2. Adjust imports to match your project structure
3. Modify types and logic for your specific game

## Templates

| File | Description | Dependencies |
|------|-------------|--------------|
| `game-loop.tsx` | React hook for 100ms game tick with delta time | React |
| `save-system.ts` | Zustand store with persist middleware and migration | zustand, immer |
| `progression.ts` | Scaling formulas for costs and rewards | None (pure functions) |
| `sprite-renderer.tsx` | Canvas component with pixel-perfect rendering | React |

## Quick Integration

```tsx
// 1. Copy files to your project
// 2. Import in your App.tsx
import { useGameLoop } from './hooks/useGameLoop';
import { useGameStore } from './stores/gameStore';
import { SpriteRenderer } from './components/SpriteRenderer';

function App() {
  // Start game loop
  useGameLoop();

  const { credits, energy } = useGameStore();

  return (
    <div>
      <p>Credits: {credits}</p>
      <p>Energy: {energy}</p>
      <SpriteRenderer
        size={64}
        primaryColor="#00fff5"
        seed="my-item-001"
      />
    </div>
  );
}
```
