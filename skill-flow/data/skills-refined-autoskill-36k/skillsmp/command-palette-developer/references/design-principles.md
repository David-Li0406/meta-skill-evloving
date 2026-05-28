# Command Palette Design Principles

Comprehensive UX patterns and best practices for command palette interfaces based on research from industry leaders (Raycast, Linear, GitHub, Notion) and design analysis.

## Core Philosophy

Command palettes represent a fundamental shift from spatial navigation (clicking through menus) to text-based command execution. The interface prioritizes:

1. **Speed** - Minimize keystrokes from intent to execution
2. **Discoverability** - Surface functionality users didn't know existed
3. **Keyboard-First** - Maintain flow state by avoiding mouse dependency
4. **Fuzzy Tolerance** - Accept approximate matches and typos
5. **Context Awareness** - Show relevant commands based on current state

## Essential Components

Every functional command palette requires exactly three elements:

### 1. Hotkey Trigger

**Standard conventions:**
- **Web applications:** ⌘K (or Ctrl+K on Windows/Linux)
- **Desktop/Editors:** ⌘+Shift+P (or Ctrl+Shift+P)
- **Alternative:** ⌘/ (secondary web convention)

**Why these matter:**
- ⌘K has become the de facto web standard (GitHub, Linear, Vercel, Notion)
- ⌘+Shift+P follows Sublime Text/VS Code precedent for desktop apps
- Avoid ⌘P (conflicts with browser Print dialog)
- Must toggle (open/close) on repeated presses

**Implementation:**
```typescript
useEffect(() => {
  const down = (e: KeyboardEvent) => {
    if (e.key === 'k' && (e.metaKey || e.ctrlKey)) {
      e.preventDefault();
      setOpen((open) => !open); // Toggle behavior
    }
  };
  document.addEventListener('keydown', down);
  return () => document.removeEventListener('keydown', down);
}, []);
```

### 2. Text Input Field

**Requirements:**
- Auto-focus when palette opens
- Clear visual cursor/caret
- Real-time search with instant feedback (<100ms)
- Placeholder text guiding usage ("Search or type a command...")
- Clear/reset button (X icon) or ESC key

**Search behavior:**
- Incremental filtering as user types
- No explicit "submit" button - results update live
- Empty query shows default state (recent, favorites, or all commands)
- Search across: command labels, keywords, descriptions, shortcuts

### 3. Results List

**Visual hierarchy:**
- Clearly selected/highlighted item (keyboard navigation target)
- Grouped sections with visual separators
- Icons for command types (navigation, action, create, delete)
- Keyboard shortcuts displayed on right side
- Metadata (descriptions, breadcrumbs) in muted text

**Interaction:**
- Arrow keys (↑↓) navigate
- Enter/Return executes selected command
- ESC closes palette
- Tab/Shift+Tab for tab navigation (if using tab filters)
- Click/tap also works (mouse users)

## Critical UX Features

### Comprehensive Action Inclusion

**Include all menu items and context actions** in the command palette. Users should access any functionality through the palette that they could access through traditional UI.

**Bad example (Sublime Text):**
- Includes "Rename File" but omits "Delete File"
- Inconsistent access creates friction and user confusion

**Good example (Raycast):**
- Every action accessible through menus is also palette-searchable
- Includes context-specific actions based on current selection
- Third-party extensions integrate seamlessly

**What to exclude:**
- Individual configuration toggles (unless actionable)
- Redundant settings (put in settings panel, not palette)
- Per-field form inputs (use palette for form-level actions)

### Keyboard Shortcut Visibility

**Display shortcuts for every command that has one:**
- Helps users learn keyboard shortcuts over time
- Reduces reliance on palette for frequently-used commands
- Shows both palette-specific shortcuts (⌘+1-9) and app shortcuts (⌘S)

**Advanced: In-Palette Shortcut Assignment**
CommandBar pioneered allowing users to reassign shortcuts directly from the palette interface. Consider this for advanced power users.

**Format examples:**
- Single key: `⌘S`
- Combo: `⌘⇧P`
- Sequence: `G then D` or `G→D`

### Fuzzy Search Implementation

**Why fuzzy search matters:**
- Users forget exact command names
- Accommodates typos without breaking flow
- Enables faster typing (no need to slow down for accuracy)
- Prioritizes relevant matches over exact substring matching

**Match types (in priority order):**
1. **Exact prefix match:** "git" → "Git Push"
2. **Word start match:** "gp" → "Git Push"
3. **Acronym match:** "gco" → "Git Checkout"
4. **Fuzzy substring:** "gitpsh" → "Git Push" (typo tolerance)

**Implementation libraries:**
- Use `fuzzy-search.ts` utility (included in this skill)
- Or: Fuse.js (heavyweight but feature-rich)
- Or: match-sorter (lightweight, good defaults)

**cmdk** handles fuzzy search by default with quality ranking.

### Discovery & Initial State

**The empty query problem:**
Users opening the palette with no query should see helpful content, not an empty list or alphabetical dump.

**Best practices:**

**1. Contextual suggestions** (GitHub approach):
```typescript
// Show different suggestions based on context
if (currentPage === 'repository') {
  suggest(['Create Issue', 'New Pull Request', 'Clone Repository']);
} else if (currentPage === 'pull-request') {
  suggest(['Approve', 'Request Changes', 'Merge']);
}
```

**2. Recent commands** (Raycast approach):
- Show last 5-10 commands executed
- Optionally grouped separately from main results
- Clear recent history option

**3. Frequency-based** (Linear approach):
- Track command execution count
- Surface top 10 most-used commands
- Combine with recency for ranking

**4. Guided onboarding** (Notion approach):
- First-time users see tutorial commands
- Examples: "Try typing 'create' to see options"
- Progressive disclosure of advanced features

**Anti-pattern:**
Alphabetical listing of all commands (overwhelming, low value).

### Favorites & Quick Access

**⌘+Number shortcuts (Raycast pattern):**
- ⌘+1 through ⌘+9 execute first 9 results
- ⌘+0 for 10th result
- Enables single-keystroke command execution
- Most powerful for frequently-used commands

**Pinning/Favorites:**
```typescript
interface Command {
  id: string;
  label: string;
  isPinned?: boolean; // User-pinnable
  frequency?: number;  // Auto-tracked
}

// Sort: pinned first, then by frequency
commands.sort((a, b) => {
  if (a.isPinned && !b.isPinned) return -1;
  if (!a.isPinned && b.isPinned) return 1;
  return (b.frequency || 0) - (a.frequency || 0);
});
```

**Persistence:**
Store in localStorage or user preferences:
```typescript
{
  "pinnedCommands": ["navigate-home", "create-task"],
  "recentCommands": ["git-push", "deploy", "navigate-settings"],
  "commandFrequency": {
    "navigate-home": 47,
    "create-task": 23
  }
}
```

## Advanced Capabilities

### Extensibility Architecture

**Plugin/Extension Integration:**

Command palettes must support third-party command providers without duplicating the interface or requiring separate palettes.

**Bad example (fragmented):**
```
App Commands      - ⌘K
Git Commands      - ⌘G
Deploy Commands   - ⌘D
```
Users must remember different shortcuts and context-switch between palettes.

**Good example (unified):**
```
All Commands - ⌘K
  ├─ App: Navigate to Dashboard
  ├─ Git: Commit Changes
  ├─ Deploy: Production
  └─ Custom Plugin: Export Data
```

**Implementation pattern:**
See `references/plugin-system.md` for complete plugin API design.

### Multi-Level Navigation

**When to use nested palettes:**
- Complex workflows requiring multiple selections
- Data browsing (repositories → branches → files)
- Configuration with categories (settings → appearance → theme)

**Raycast pattern (recommended):**
```
Step 1: Select Repository
  ↓ Enter
Step 2: Select Action [Breadcrumb: Repository Name]
  ↓ Enter
Step 3: Execute [Show confirmation if destructive]
```

**Key features:**
- Breadcrumb trail showing navigation path
- Backspace or ESC in empty search goes back
- Maintain search context when possible

**Implementation:**
```typescript
const [commandStack, setCommandStack] = useState<Command[]>([]);

function navigateInto(command: Command) {
  setCommandStack([...commandStack, command]);
  setSearchQuery(''); // Reset search
}

function navigateBack() {
  setCommandStack(commandStack.slice(0, -1));
}
```

### Built-In Search

**Two approaches:**

**1. Unified search** (GitHub):
Commands and data in single results list:
```
"repo" query shows:
  - Navigate to Repository X
  - Search in Repository Y
  - Repository Z (actual data)
```

**2. Prefix-based** (Notion):
Special prefixes trigger different search modes:
```
?query  → Search in content
@person → Mention user
/command → Slash command
```

**3. Tab-based** (Linear):
Tabs for different result types:
```
[All] [Actions] [Issues] [Projects] [People]
```

**Recommendation:** Start unified, add filters/tabs as command count grows beyond 100.

## Accessibility Requirements

### Keyboard Navigation

**Non-negotiable requirements:**
- **Tab trap:** Focus stays within palette while open
- **Arrow navigation:** ↑↓ through results
- **Escape:** Close palette and return focus
- **Enter:** Execute selected command
- **Shift+Tab:** Reverse tab through interactive elements

**Optional enhancements:**
- **⌘+Backspace:** Clear search query
- **⌘+↑/↓:** Jump to first/last result
- **Page Up/Down:** Scroll results by page
- **Home/End:** Jump to first/last result

### Screen Reader Support

**ARIA attributes:**
```tsx
<div role="dialog" aria-modal="true" aria-label="Command Palette">
  <input
    role="combobox"
    aria-expanded={isOpen}
    aria-controls="results-list"
    aria-activedescendant={selectedId}
  />
  <ul role="listbox" id="results-list">
    <li role="option" aria-selected={isSelected}>
      Command Label
    </li>
  </ul>
</div>
```

**Live regions for feedback:**
```tsx
<div role="status" aria-live="polite" aria-atomic="true">
  {resultCount} results found
</div>
```

**Announcements:**
- Result count when search updates
- "No results" when query returns empty
- Command executed confirmation

### Reduced Motion

Respect `prefers-reduced-motion`:
```css
@media (prefers-reduced-motion: reduce) {
  .palette-enter,
  .palette-exit {
    animation: none;
    transition: none;
  }
}
```

**Alternatives to animation:**
- Instant show/hide instead of fade
- No spring physics on open
- Immediate scroll instead of smooth

## Visual Design Patterns

### Result Item Anatomy

**Left-to-right layout:**
```
[Icon] Command Label           [Shortcut]
       Muted description        [Badge]
```

**Icon:**
- 16×16 or 20×20px
- Consistent style across all commands
- Color-coded by type (create=green, delete=red, navigate=blue)

**Label:**
- Primary font weight (500-600)
- Color: High contrast text color
- 14-16px font size

**Description:**
- Secondary font weight (400)
- Color: Muted (60% opacity of text color)
- 12-14px font size
- Single line with ellipsis overflow

**Shortcut:**
- Badge/pill styling
- Monospace font for key symbols
- Platform-aware (⌘ vs Ctrl)

**Badge (optional):**
- Small pill for metadata (New, Beta, Premium)
- Subtle colors, don't compete with primary info

### Grouping & Sections

**Visual separators:**
```
Recent
  Create New Task
  Navigate Home
────────────────
Actions
  Deploy to Production
  Run Tests
────────────────
Navigation
  Go to Dashboard
  Settings
```

**Sticky section headers:**
As user scrolls, current section remains visible at top.

**Collapsible groups:**
For power users with many commands, allow collapsing sections.

### Empty States

**Different contexts need different messaging:**

**No results from search:**
```
No commands found for "xyz"

Try:
• Checking your spelling
• Using different keywords
• Browsing all commands (clear search)
```

**First-time user:**
```
Welcome! Try typing:
• "create" to make new items
• "search" to find content
• "settings" to configure
```

**No commands registered:**
```
No commands available

Check your command registration
or install plugins to add functionality
```

## Performance Considerations

### Filtering Performance

**Targets:**
- <16ms to maintain 60fps during typing
- <100ms perceived delay for result updates
- <1000 items before virtualization required

**Optimization strategies:**
1. **Debounce search:** Wait 100-150ms after last keystroke
2. **Memoize results:** Cache filtered results for identical queries
3. **Web Workers:** Offload fuzzy search to background thread
4. **Virtual scrolling:** Render only visible items (see `references/virtual-scrolling.md`)

### Initial Load

**Lazy-load command definitions:**
```typescript
const commands = {
  'git-*': () => import('./commands/git'),
  'deploy-*': () => import('./commands/deploy'),
};

// Load on first search match
const results = await commands['git-*']();
```

**Preload critical commands:**
Load navigation and frequently-used commands immediately, defer less common commands.

## Common Anti-Patterns to Avoid

### 1. Multiple Specialized Palettes

**Bad:**
- ⌘K for general commands
- ⌘G for git commands
- ⌘F for file search

**Good:**
- ⌘K for everything
- Tabs or prefixes for filtering if needed

### 2. Non-Toggleable Overlay

**Bad:**
Pressing hotkey again doesn't close the palette.

**Good:**
Pressing ⌘K when open closes it.

### 3. Mixing Commands and Configuration

**Bad:**
Every setting toggle appears as a command.

**Good:**
Commands perform actions. Settings live in a settings panel.

### 4. Overwhelming Default State

**Bad:**
500 alphabetically-sorted commands on open.

**Good:**
Recent/frequent commands or contextual suggestions.

### 5. Ignoring Command Context

**Bad:**
Showing "Create Pull Request" when not in a repository.

**Good:**
Context-filter commands based on current state.

## Testing Checklist

**Functionality:**
- [ ] Palette opens on ⌘K
- [ ] Toggles (open/close) on repeated ⌘K
- [ ] Search filters in real-time
- [ ] Arrow keys navigate results
- [ ] Enter executes selected command
- [ ] ESC closes palette
- [ ] Clicking backdrop closes palette
- [ ] Recent commands tracked
- [ ] Favorites persist across sessions

**Accessibility:**
- [ ] Focus trap works (tab doesn't leave palette)
- [ ] Screen reader announces results count
- [ ] All commands keyboard-accessible
- [ ] Reduced motion respected
- [ ] Sufficient color contrast (WCAG AA)
- [ ] Keyboard shortcuts don't conflict with browser/OS

**Performance:**
- [ ] No jank during typing (60fps)
- [ ] Handles 1,000+ commands smoothly
- [ ] Virtual scrolling works for large lists
- [ ] Search completes in <100ms

**Edge Cases:**
- [ ] No results found handled gracefully
- [ ] Empty state shows helpful guidance
- [ ] Long command labels truncate properly
- [ ] Works on mobile (touch + virtual keyboard)
- [ ] Multiple palettes don't conflict (if applicable)

## Real-World Examples Analysis

### GitHub Command Palette

**Strengths:**
- Excellent contextual suggestions (repo-aware)
- Tab-based filtering (All, Files, Commands, etc.)
- Recent searches integration
- Deep linking (URLs update with palette state)

**Learnings:**
Unify data search and command execution in single interface.

### Raycast

**Strengths:**
- Beautiful animations and polish
- Strong plugin ecosystem
- Multi-step commands with breadcrumbs
- ⌘+Number shortcuts for instant execution

**Learnings:**
Nested commands enable complex workflows without overwhelming single-level interface.

### Linear

**Strengths:**
- Horizontal card scrolls for rich content
- Keyboard shortcuts prominently displayed
- Smooth integration with app state

**Learnings:**
Mix layout types (cards + lists) for different result types.

### Notion

**Strengths:**
- Inline/embedded palette (slash commands)
- Context-aware (different commands in different blocks)
- Quick actions (⌘+Click for inline)

**Learnings:**
Embedded palettes excel for contextual, inline actions.

## Additional Resources

- **Keyboard Navigation:** `references/keyboard-navigation.md`
- **State Management:** `references/state-management.md`
- **Theming:** `references/theming.md`
- **Testing:** `references/testing.md`
- **Plugin System:** `references/plugin-system.md`
