# Mobile UI Patterns

Platform-specific component patterns and mobile finishing touches.

---

## Navigation Patterns

| Pattern | Use Case | Platform |
|---------|----------|----------|
| Bottom navigation | 3-5 primary destinations | Both |
| Tab bar (top) | Content categories | Android |
| Navigation drawer | Many destinations, settings | Both |
| Bottom sheet nav | Contextual actions | Both |

**Bottom navigation rules:**

- 3-5 items maximum
- Icons required, labels recommended
- Active state: filled icon + color
- Badge for notifications

---

## App Bar Patterns

| Type | Use Case |
|------|----------|
| Standard | Title, leading icon, actions |
| Search | Integrated search field |
| Collapsing | Hero image + title that shrinks |
| Bottom app bar | FAB integration (Android) |

**Leading icons:**

- Menu hamburger (opens drawer)
- Back arrow (navigation pop)
- Close X (dismiss modal/sheet)

---

## List Patterns

| Pattern | When to Use |
|---------|-------------|
| Simple list | Text-only items |
| List with avatar | Person/entity lists |
| List with thumbnail | Media content |
| Two-line list | Title + subtitle |
| Three-line list | Title + subtitle + meta (dense info) |

**Interactive lists:**

- Swipe to delete/archive
- Long press for selection
- Pull to refresh

---

## Form Patterns

**Input fields:**

- Full width with horizontal padding
- Label above or floating
- Helper text below
- Error state: red border + message

**Buttons:**

- Primary action: Full width at bottom OR FAB
- Secondary: Outlined or text, paired with primary
- Vertical button stacks: Primary on top

---

## Feedback Patterns

| Feedback | Use Case |
|----------|----------|
| Snackbar | Transient message, optional action |
| Toast | Simple confirmation |
| Dialog | Requires decision |
| Bottom sheet | Multiple options |

**Loading states:**

- Skeleton screens (preferred)
- Shimmer effect
- Circular progress (centered)
- Linear progress (top of screen)

---

## Empty States

Critical for first-time users.

**Requirements:**

- Illustration or icon
- Clear title
- Helpful description
- Call-to-action button

**Don't:** Show just "No data" or empty list.

---

## Pull to Refresh

Standard mobile pattern for list refresh.

- Circular indicator appears on pull
- Should feel responsive
- Show loading state
- Snap back on release

---

## Supercharge Defaults

Mobile equivalents of web finishing touches:

- Custom checkbox/radio (brand colored)
- Styled switches (iOS or custom)
- Animated icons (loading, success)
- Hero animations between screens
- Haptic feedback on key actions
