# UI Design Standards (Figma)

## Figma Project Structure

```
{Project}/
├── 🎨 Design System
│   ├── Colors, Typography, Spacing
│   └── Components
├── 📱 Screens (Desktop/Mobile)
├── 💻 TUI Designs (if CLI)
└── 🔄 User Flows
```

## Design Tokens

### Colors
```
Primary:   50 → 900 scale
Semantic:  success, warning, error, info
Neutral:   gray-50 → gray-900
```

### Typography
```
Headings: h1 (2.25rem) → h5 (1.125rem)
Body:     lg (1.125rem), base (1rem), sm (0.875rem)
Mono:     For TUI/code (0.875rem)
```

### Spacing
```
1: 0.25rem (4px)   4: 1rem (16px)    8: 2rem (32px)
2: 0.5rem (8px)    6: 1.5rem (24px)  12: 3rem (48px)
```

## Component States

Every interactive component needs:
- Default
- Hover
- Focus (visible ring)
- Active
- Disabled
- Loading
- Error

## TUI Design (for CLI tools)

### Box Characters
```
Light: ┌ ─ ┐ │ └ ┘ ├ ┤ ┬ ┴ ┼
Heavy: ╔ ═ ╗ ║ ╚ ╝ ╠ ╣ ╦ ╩ ╬
```

### Status Icons
```
✓ Success    ✗ Error    ⚠ Warning    ℹ Info
```

### Progress
```
Spinner: ⠋ ⠙ ⠹ ⠸ ⠼ ⠴ ⠦ ⠧ ⠇ ⠏
Bar:     [████████░░░░░░░░] 50%
```

### Layout Template
```
┌─────────────────────────────────────────┐
│ Title                           Status  │
├─────────────────────────────────────────┤
│                                         │
│  Main Content                           │
│                                         │
├─────────────────────────────────────────┤
│ q:quit  ↑↓:navigate  enter:select       │
└─────────────────────────────────────────┘
```

## Story Integration

Link designs in story files:

```markdown
## Design

| Screen | Figma Link | Status |
|--------|------------|--------|
| Main View | [Link](...) | ✅ Approved |
| Error State | [Link](...) | 🟡 Review |
```

## Handoff Checklist

- [ ] All states designed
- [ ] Responsive variants
- [ ] Design tokens used (no hardcoded values)
- [ ] Measurements annotated
- [ ] Accessibility reviewed
- [ ] Linked to user story
