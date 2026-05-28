# Headless UI Patterns (Radix & Aria-Kit)

## Why Headless?
Headless libraries provide the accessibility logic (keyboard navigation, focus traps, ARIA attributes) without any styling. This allows the design system to fully own the visual layer via Tailwind 4.

---

### 1. The "Base Component" Pattern
Create unstyled wrappers around Radix primitives.

```tsx
import * as Dialog from "@radix-ui/react-dialog";

export const BaseModal = ({ children, trigger }) => (
  <Dialog.Root>
    <Dialog.Trigger asChild>{trigger}</Dialog.Trigger>
    <Dialog.Portal>
      <Dialog.Overlay className="fixed inset-0 bg-black/50 animate-in fade-in" />
      <Dialog.Content className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-surface p-6 shadow-xl rounded-modal animate-in zoom-in-95">
        {children}
      </Dialog.Content>
    </Dialog.Portal>
  </Dialog.Root>
);
```

---

### 2. High-Precision Interactivity
Headless UI ensures that complex components like "Combobox" or "Select" are fully usable with screen readers out of the box.

---

### 3. State-Driven Animations
Use Tailwind 4's native state selectors (e.g., `group-data-[state=open]:rotate-180`) to animate components based on their internal headless state.
