# Floating UI for Embedded Palettes

Smart positioning for embedded command palettes using Floating UI middleware.

## Setup

```bash
npm install @floating-ui/react
```

## Basic Embedded Palette

```typescript
import { useFloating, offset, flip, shift, autoUpdate } from '@floating-ui/react';

function EmbeddedPalette() {
  const [isOpen, setIsOpen] = useState(false);
  const { refs, floatingStyles } = useFloating({
    open: isOpen,
    onOpenChange: setIsOpen,
    middleware: [
      offset(10), // 10px gap from trigger
      flip(), // Flip to opposite side if no space
      shift({ padding: 8 }), // Shift horizontally to stay in viewport
    ],
    whileElementsMounted: autoUpdate, // Update position on scroll
  });

  return (
    <>
      <button ref={refs.setReference} onClick={() => setIsOpen(!isOpen)}>
        Open Palette
      </button>

      {isOpen && (
        <div ref={refs.setFloating} style={floatingStyles} className="palette">
          <CommandPalette />
        </div>
      )}
    </>
  );
}
```

## Collision Detection

```typescript
import { size } from '@floating-ui/react';

const { refs, floatingStyles } = useFloating({
  middleware: [
    flip(),
    shift(),
    size({
      apply({ availableHeight, elements }) {
        // Constrain height to available space
        Object.assign(elements.floating.style, {
          maxHeight: `${availableHeight}px`,
        });
      },
    }),
  ],
});
```

## Placement Options

```typescript
const { refs, floatingStyles } = useFloating({
  placement: 'bottom-start', // bottom-start, bottom-end, top, left, right, etc.
  middleware: [offset(8), flip(), shift()],
});
```
