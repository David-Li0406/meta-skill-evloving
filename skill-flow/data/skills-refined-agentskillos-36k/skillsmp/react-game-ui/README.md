# React Game UI

React game UI patterns using shadcn/ui, Tailwind, and Framer Motion.

## Expertise

This skill provides:

- **Game UI Components**: HUDs, resource bars, inventories
- **Animation Patterns**: Micro-interactions, transitions
- **Responsive Design**: Mobile-first game interfaces
- **Accessibility**: Game UI that works for everyone
- **Performance**: Optimized rendering for games
- **shadcn/ui Integration**: Customizing for game aesthetics

## When to Use

Invoke this skill when you need to:

- Build game HUD elements
- Create inventory interfaces
- Design resource/health bars
- Implement score displays
- Add satisfying micro-interactions
- Build modals and tooltips for games

## Component Patterns

### Resource Bar

```tsx
import { motion } from "framer-motion";

interface ResourceBarProps {
  current: number;
  max: number;
  color: "health" | "mana" | "energy";
}

export function ResourceBar({ current, max, color }: ResourceBarProps) {
  const percentage = (current / max) * 100;

  const colors = {
    health: "bg-red-500",
    mana: "bg-blue-500",
    energy: "bg-yellow-500",
  };

  return (
    <div className="h-4 w-full rounded-full bg-gray-800 overflow-hidden">
      <motion.div
        className={`h-full ${colors[color]}`}
        initial={{ width: 0 }}
        animate={{ width: `${percentage}%` }}
        transition={{ type: "spring", stiffness: 100 }}
      />
    </div>
  );
}
```

### Inventory Grid

```tsx
export function InventoryGrid({ items, onSelect }: InventoryProps) {
  return (
    <div className="grid grid-cols-5 gap-2 p-4 bg-gray-900 rounded-lg">
      {items.map((item, i) => (
        <motion.button
          key={i}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => onSelect(item)}
          className="aspect-square rounded border-2 border-gray-700
                     hover:border-yellow-500 transition-colors"
        >
          {item && <img src={item.icon} alt={item.name} />}
        </motion.button>
      ))}
    </div>
  );
}
```

### Score Display

```tsx
export function ScoreDisplay({ score }: { score: number }) {
  return (
    <motion.div
      key={score}
      initial={{ scale: 1.2, color: "#fbbf24" }}
      animate={{ scale: 1, color: "#ffffff" }}
      className="font-bold text-2xl tabular-nums"
    >
      {score.toLocaleString()}
    </motion.div>
  );
}
```

### Tooltip

```tsx
import * as Tooltip from "@radix-ui/react-tooltip";

export function ItemTooltip({ item, children }: TooltipProps) {
  return (
    <Tooltip.Root>
      <Tooltip.Trigger asChild>{children}</Tooltip.Trigger>
      <Tooltip.Portal>
        <Tooltip.Content
          className="bg-gray-900 border border-gray-700 rounded-lg p-3
                     shadow-xl max-w-xs"
          sideOffset={5}
        >
          <h3 className="font-bold text-yellow-400">{item.name}</h3>
          <p className="text-sm text-gray-400">{item.description}</p>
          <Tooltip.Arrow className="fill-gray-900" />
        </Tooltip.Content>
      </Tooltip.Portal>
    </Tooltip.Root>
  );
}
```

## Animation Patterns

### Juice on Collect

```tsx
<motion.div
  initial={{ scale: 0, rotate: -180 }}
  animate={{ scale: 1, rotate: 0 }}
  exit={{ scale: 0, y: -50, opacity: 0 }}
  transition={{ type: "spring", bounce: 0.5 }}
>
  <CoinIcon />
</motion.div>
```

### Number Pop

```tsx
<motion.span
  key={value}
  initial={{ y: -20, opacity: 0 }}
  animate={{ y: 0, opacity: 1 }}
  className="text-green-400 font-bold"
>
  +{value}
</motion.span>
```

### Shake on Error

```tsx
<motion.div
  animate={hasError ? { x: [-10, 10, -10, 10, 0] } : {}}
  transition={{ duration: 0.4 }}
>
  {children}
</motion.div>
```

## Best Practices

### Performance
- Use `will-change` sparingly
- Prefer `transform` over `top/left`
- Virtualize long lists
- Memoize expensive components

### Accessibility
- Keyboard navigation for all UI
- Screen reader announcements
- Sufficient color contrast
- Reduced motion support

### Mobile
- Touch-friendly hit targets (44px+)
- Swipe gestures where intuitive
- Avoid hover-only interactions

## Integration

This skill works alongside:

- `game-assets-team` - Assets to display
- `zustand-game-patterns` - State to render
- `fun-advisor` - UI that feels good

## Usage in Claude Code

```
/react-game-ui

"Create an animated health bar component..."
"Design an inventory grid with drag-drop..."
"Add satisfying feedback when collecting coins..."
```
