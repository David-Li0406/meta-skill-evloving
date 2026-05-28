# TUI Design Principles

A comprehensive guide to designing effective terminal user interfaces.

## 1. Color Theory for Terminals

### Color Palette Guidelines

**Primary Colors**
- Use one accent color consistently for focus/selection states
- Reserve bright colors for important interactive elements
- Use muted colors for secondary information

**Semantic Colors**
| Purpose | Recommended Colors |
|---------|-------------------|
| Success | Green (#00FF00, #98C379) |
| Error | Red (#FF0000, #E06C75) |
| Warning | Yellow/Orange (#FFFF00, #E5C07B) |
| Info | Blue/Cyan (#00FFFF, #61AFEF) |
| Muted/Secondary | Gray (#808080, #5C6370) |

**Contrast Requirements**
- Text should have minimum 4.5:1 contrast ratio against background
- Interactive elements need clear visual distinction
- Test with both dark and light terminal themes

### Color Degradation Strategy

```
True Color (24-bit) → 256 Color → 16 Color → Monochrome
      ↓                  ↓            ↓           ↓
   Optimal          Acceptable    Functional    Usable
```

Always design for graceful degradation:
1. Start with true color design
2. Test in 256-color mode
3. Ensure basic 16-color fallback works
4. Verify monochrome remains usable (for accessibility)

## 2. Layout Principles

### The 80x24 Rule
- Classic terminal size is 80 columns × 24 rows
- Design core functionality to work at this minimum
- Use responsive layouts for larger terminals

### Panel Ratios
Common effective layouts:
- **70/30 split** - Primary content / sidebar (calendar + todo)
- **60/40 split** - Balanced two-panel views
- **Full width** - Single focus content (modals, editors)

### Whitespace Guidelines
```
┌─────────────────────────────────────┐
│ ← Padding (1-2 chars)               │
│   ┌─────────────────────────────┐   │
│   │ Content Area                │   │
│   │                             │   │
│   │ ← Inner padding (1 char)    │   │
│   └─────────────────────────────┘   │
│                                     │
│ ← Margin between sections (1 line)  │
└─────────────────────────────────────┘
```

- Use consistent padding (typically 1-2 characters)
- Separate logical sections with empty lines
- Avoid cramped layouts - breathing room improves readability

### Alignment Principles
- Left-align text content
- Right-align numeric data in columns
- Center titles and headings
- Maintain consistent indentation (2 or 4 spaces)

## 3. Visual Hierarchy

### Creating Emphasis

**Level 1 - Primary Focus**
- Bold text or bright colors
- Borders or boxes
- Larger visual weight

**Level 2 - Secondary Information**
- Normal text weight
- Standard colors
- Clear but not prominent

**Level 3 - Tertiary/Muted**
- Dim or gray text
- No decoration
- Minimal visual presence

### Border Styles

```
Light borders (subtle separation):
┌────────────────┐
│                │
└────────────────┘

Heavy borders (emphasis):
╔════════════════╗
║                ║
╚════════════════╝

Rounded borders (friendly):
╭────────────────╮
│                │
╰────────────────╯

Double borders (modals/dialogs):
╔════════════════╗
║   Important    ║
╚════════════════╝
```

### Focus Indicators
- **Color change** - Border or background color shift
- **Border style change** - Single → double line
- **Cursor position** - Blinking cursor or highlight
- **Text decoration** - Reverse video, underline

## 4. Navigation Patterns

### Keyboard Convention Families

**Vim-style**
| Key | Action |
|-----|--------|
| h/j/k/l | Left/Down/Up/Right |
| gg/G | Go to top/bottom |
| / | Search |
| n/N | Next/previous match |
| :q | Quit |

**Emacs-style**
| Key | Action |
|-----|--------|
| Ctrl+n/p | Next/previous line |
| Ctrl+f/b | Forward/backward char |
| Ctrl+a/e | Beginning/end of line |
| Ctrl+s | Search |
| Ctrl+g | Cancel |

**Standard/Arrow-based**
| Key | Action |
|-----|--------|
| Arrow keys | Navigation |
| Enter | Select/confirm |
| Esc | Cancel/back |
| Tab | Next field |
| Space | Toggle |

### Mode Indicators
Always show current mode clearly:
```
┌─ NORMAL ──────────────────────────────┐
│                                       │
└───────────────────────────────────────┘

┌─ INSERT ──────────────────────────────┐
│ █                                     │
└───────────────────────────────────────┘

┌─ SEARCH ──────────────────────────────┐
│ /query█                               │
└───────────────────────────────────────┘
```

### Navigation Consistency Rules
1. Same key should do same thing across contexts
2. Esc should always provide an "out"
3. Destructive actions need confirmation
4. Provide breadcrumbs for deep navigation

## 5. Feedback & Affordances

### Response Time Guidelines
| Response | User Perception |
|----------|-----------------|
| < 100ms | Instantaneous |
| 100-300ms | Fast |
| 300-1000ms | Noticeable delay |
| > 1000ms | Needs progress indicator |

### Loading States
```
Simple spinner:  ⠋ ⠙ ⠹ ⠸ ⠼ ⠴ ⠦ ⠧ ⠇ ⠏

Progress bar:    [████████░░░░░░░░░░░░] 40%

Status message:  Loading... (2/10 items)
```

### Error Display Patterns
```
Inline error:
┌─ Add Todo ─────────────────────────────┐
│ Title: █                               │
│ ⚠ Title cannot be empty                │
└────────────────────────────────────────┘

Modal error:
╔═ Error ════════════════════════════════╗
║ Failed to save: disk full              ║
║                                        ║
║              [OK]                      ║
╚════════════════════════════════════════╝
```

### Success Feedback
- Brief flash or highlight
- Status message that auto-clears
- Subtle animation (if supported)
- Checkmark or completion indicator

## 6. Discoverability

### Help System Layers

**Layer 1: Always visible**
- Help bar at bottom showing common shortcuts
- Mode indicator showing current state

**Layer 2: On-demand hints**
- Press `?` for full shortcut reference
- Contextual help in empty states

**Layer 3: Full documentation**
- Built-in help command
- Man page or external docs

### Help Bar Patterns
```
Minimal:
 q quit │ ? help

Contextual:
 ↑↓ navigate │ Enter select │ / search │ q quit

Grouped:
 Navigation: hjkl │ Actions: a add  e edit  d delete │ q quit
```

### Empty State Design
```
┌─ Todos ────────────────────────────────┐
│                                        │
│         No todos for this day          │
│                                        │
│         Press 'a' to add one           │
│                                        │
└────────────────────────────────────────┘
```

## 7. Responsive Design

### Terminal Size Handling

**Strategy 1: Minimum viable display**
- Define minimum dimensions (e.g., 80x24)
- Show error/warning if too small
- Core functionality always works

**Strategy 2: Progressive enhancement**
```
Small (< 80 cols):     Show essential content only
Medium (80-120 cols):  Add secondary panels
Large (> 120 cols):    Full feature display
```

**Strategy 3: Content adaptation**
- Truncate long text with ellipsis
- Collapse panels into tabs
- Hide optional information

### Breakpoint Guidelines
| Width | Typical Layout |
|-------|----------------|
| < 60 | Single column, stacked |
| 60-80 | Primary content only |
| 80-120 | Two panels (70/30) |
| > 120 | Full layout with margins |

## 8. Accessibility

### Screen Reader Compatibility
- Provide text alternatives for visual elements
- Avoid relying solely on color for meaning
- Use semantic structure where possible

### Cognitive Load Reduction
- Limit choices per screen (7±2 rule)
- Group related actions
- Use progressive disclosure
- Maintain consistency

### Motor Accessibility
- Allow key repeat for navigation
- Provide shortcuts for common actions
- Support both keyboard families (vim/standard)
- Avoid time-sensitive interactions

## 9. Performance Perception

### Rendering Optimization
- Minimize full redraws
- Update only changed regions
- Debounce rapid input
- Show immediate feedback, process in background

### Perceived Performance Tricks
- Show skeleton/placeholder while loading
- Optimistic UI updates
- Progressive content loading
- Prioritize above-the-fold content

## 10. Testing Checklist

### Visual Testing
- [ ] Works at 80x24 minimum size
- [ ] Works with light terminal theme
- [ ] Works with dark terminal theme
- [ ] Works with 256 colors
- [ ] Works with 16 colors
- [ ] Focus states are clearly visible
- [ ] Text has sufficient contrast

### Interaction Testing
- [ ] All features accessible via keyboard
- [ ] Esc always provides escape route
- [ ] Tab order is logical
- [ ] Destructive actions have confirmation
- [ ] Error states are handled gracefully
- [ ] Loading states are indicated

### UX Testing
- [ ] New user can complete basic task
- [ ] Current mode/state is always clear
- [ ] Help is easily accessible
- [ ] Common workflows are efficient
- [ ] Edge cases don't crash/hang
