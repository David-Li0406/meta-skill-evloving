---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, or applications. Generates creative, polished code that avoids generic AI aesthetics.
---

# Frontend Design

Build polished, native-feeling interfaces for Raamattu Nyt using shadcn/ui, Tailwind CSS, and React.

## Tech Stack

- **Components**: shadcn/ui (Radix primitives)
- **Styling**: Tailwind CSS 3.4 with CSS variables
- **Icons**: Lucide React
- **State**: React Query + React Hook Form + Zod

## Quick Patterns

### Responsive Layout
```tsx
// Mobile-first with desktop override
<div className="flex flex-col md:flex-row gap-4">
  <div className="w-full md:w-1/3">Sidebar</div>
  <div className="flex-1">Content</div>
</div>
```

### Mobile Bottom Navigation
```tsx
<nav className="fixed bottom-0 left-0 right-0 z-50 bg-background/95 backdrop-blur-md border-t md:hidden safe-area-bottom">
  <div className="flex items-center justify-around h-16">
    {/* 44px+ touch targets */}
  </div>
</nav>
```

### Sheet for Mobile, Dialog for Desktop
```tsx
const isMobile = useIsMobile();

return isMobile ? (
  <Sheet>
    <SheetContent side="bottom" className="h-[85vh]">
      {content}
    </SheetContent>
  </Sheet>
) : (
  <Dialog>
    <DialogContent className="max-w-lg">
      {content}
    </DialogContent>
  </Dialog>
);
```

### Touch-Optimized Button
```tsx
<Button
  className="h-12 px-6 active:scale-95 transition-transform"
  variant="default"
>
  Touch Me
</Button>
```

## Mobile-Native Feel Checklist

- [ ] Bottom nav visible only on mobile (`md:hidden`)
- [ ] Touch targets min 44px (h-11/h-12)
- [ ] `active:scale-95` on tappable elements
- [ ] Safe area padding (`safe-area-bottom` class)
- [ ] Backdrop blur on overlays (`bg-background/95 backdrop-blur-md`)
- [ ] Swipe gestures where appropriate
- [ ] No hover-only interactions on mobile

## Design Tokens

```css
/* Use semantic colors */
--background, --foreground
--primary, --primary-foreground
--muted, --muted-foreground
--destructive
--border, --ring

/* Border radius */
--radius: 0.5rem (8px)
```

## When Building UI

1. **Read image inputs** - Analyze screenshots/mockups for layout and style
2. **Mobile-first** - Start with mobile, add `md:` breakpoint for desktop
3. **Use shadcn** - Import from `@ui/` not raw Radix
4. **Native feel** - Add touch feedback, proper spacing, animations
5. **Accessibility** - ARIA labels, focus states, keyboard nav

## References

- **Component patterns**: See [references/components.md](references/components.md)
- **Mobile patterns**: See [references/mobile.md](references/mobile.md)
- **Forms & validation**: See [references/forms.md](references/forms.md)
