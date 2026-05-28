# Accessibility Reference

Complete guide to building accessible UIs with shadcn/ui components.

## WCAG Compliance

### Color Contrast

Minimum contrast ratios (WCAG AA):
- **Normal text**: 4.5:1
- **Large text (18px+ or 14px+ bold)**: 3:1
- **UI components**: 3:1

```tsx
// Good: Primary text on background
<p className="text-foreground">High contrast text</p>

// Good: Muted text meets contrast
<p className="text-muted-foreground">Secondary text</p>

// Check contrast in globals.css
// --foreground: 222.2 84% 4.9%  (dark)
// --background: 0 0% 100%        (white)
// Contrast ratio: ~15:1 ✓
```

### Focus States

All interactive elements must have visible focus:

```tsx
// Default focus ring in shadcn
className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"

// Custom focus for specific components
className="focus:ring-2 focus:ring-primary focus:ring-offset-2"
```

## Keyboard Navigation

### Focus Order

Ensure logical tab order:

```tsx
// Use tabIndex sparingly
<div tabIndex={0}>Focusable div (avoid if possible)</div>

// Prefer semantic elements
<button>Naturally focusable</button>
<a href="#">Naturally focusable</a>
<input />
```

### Keyboard Patterns

| Component | Keys | Action |
|-----------|------|--------|
| Button | Enter, Space | Activate |
| Dialog | Escape | Close |
| Menu | Arrow keys | Navigate items |
| Tabs | Arrow keys | Switch tabs |
| Checkbox | Space | Toggle |
| Select | Arrow keys | Navigate options |

### Skip Links

```tsx
// Add at the start of layout
<a
  href="#main-content"
  className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2 focus:bg-background focus:border"
>
  Skip to main content
</a>

<main id="main-content">
  {/* Page content */}
</main>
```

## ARIA Attributes

### Labels

```tsx
// Icon-only buttons MUST have labels
<Button variant="ghost" size="icon" aria-label="Close dialog">
  <X className="h-4 w-4" />
</Button>

// Form inputs with labels
<div>
  <Label htmlFor="email">Email</Label>
  <Input id="email" type="email" />
</div>

// Or use aria-label
<Input aria-label="Search" type="search" />
```

### Descriptions

```tsx
// Link descriptions to inputs
<div>
  <Label htmlFor="password">Password</Label>
  <Input
    id="password"
    type="password"
    aria-describedby="password-hint"
  />
  <p id="password-hint" className="text-sm text-muted-foreground">
    Must be at least 8 characters
  </p>
</div>
```

### Live Regions

```tsx
// Announce dynamic content
<div aria-live="polite" aria-atomic="true">
  {notification && <p>{notification}</p>}
</div>

// For urgent messages
<div aria-live="assertive" role="alert">
  {error && <p>{error}</p>}
</div>
```

## Component Patterns

### Dialog (Modal)

```tsx
<Dialog>
  <DialogTrigger asChild>
    <Button>Open Dialog</Button>
  </DialogTrigger>
  <DialogContent>
    {/* Focus is trapped inside */}
    <DialogHeader>
      <DialogTitle>Are you sure?</DialogTitle>
      <DialogDescription>
        This action cannot be undone.
      </DialogDescription>
    </DialogHeader>
    <DialogFooter>
      <DialogClose asChild>
        <Button variant="outline">Cancel</Button>
      </DialogClose>
      <Button>Confirm</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

### Alert

```tsx
<Alert variant="destructive" role="alert">
  <AlertCircle className="h-4 w-4" />
  <AlertTitle>Error</AlertTitle>
  <AlertDescription>
    Your session has expired. Please log in again.
  </AlertDescription>
</Alert>
```

### Form Validation

```tsx
<FormField
  control={form.control}
  name="email"
  render={({ field, fieldState }) => (
    <FormItem>
      <FormLabel>Email</FormLabel>
      <FormControl>
        <Input
          {...field}
          aria-invalid={!!fieldState.error}
          aria-describedby={
            fieldState.error ? "email-error" : undefined
          }
        />
      </FormControl>
      {fieldState.error && (
        <FormMessage id="email-error" role="alert">
          {fieldState.error.message}
        </FormMessage>
      )}
    </FormItem>
  )}
/>
```

### Dropdown Menu

```tsx
<DropdownMenu>
  <DropdownMenuTrigger asChild>
    <Button variant="ghost" size="icon" aria-label="More options">
      <MoreVertical className="h-4 w-4" />
    </Button>
  </DropdownMenuTrigger>
  <DropdownMenuContent>
    <DropdownMenuItem>Edit</DropdownMenuItem>
    <DropdownMenuItem>Duplicate</DropdownMenuItem>
    <DropdownMenuSeparator />
    <DropdownMenuItem className="text-destructive">
      Delete
    </DropdownMenuItem>
  </DropdownMenuContent>
</DropdownMenu>
```

## Reduced Motion

Respect user preferences for reduced motion:

```css
/* In globals.css */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

```tsx
// In React
const prefersReducedMotion = window.matchMedia(
  "(prefers-reduced-motion: reduce)"
).matches;

// Conditionally apply animations
<motion.div
  animate={prefersReducedMotion ? {} : { opacity: 1, y: 0 }}
>
  Content
</motion.div>
```

## Screen Reader Testing

### Common Screen Readers

- **NVDA** (Windows, free)
- **VoiceOver** (macOS/iOS, built-in)
- **JAWS** (Windows, commercial)
- **TalkBack** (Android, built-in)

### Testing Checklist

- [ ] All images have alt text
- [ ] Form inputs have labels
- [ ] Buttons have accessible names
- [ ] Links have descriptive text
- [ ] Headings follow hierarchy (h1 → h2 → h3)
- [ ] Tables have headers
- [ ] Dynamic content is announced
- [ ] Focus order is logical

## Accessibility Utilities

### sr-only (Screen Reader Only)

```tsx
// Visually hidden but accessible to screen readers
<span className="sr-only">Close</span>

// Tailwind class definition:
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

### focus-visible

```tsx
// Only show focus ring for keyboard navigation
className="focus-visible:ring-2 focus-visible:ring-ring"

// Not on mouse click
```

### not-sr-only

```tsx
// Show element when focused
<a
  href="#content"
  className="sr-only focus:not-sr-only focus:absolute"
>
  Skip to content
</a>
```
