# e3 Data Viewer (`e3 view`)

Interactive Terminal UI for exploring and visualizing East data structures.

## Overview

A two-pane TUI data explorer inspired by `parqeye`, providing intuitive navigation and multiple visualization modes for East data.

## Architecture

### Layout Modes

**1. Split View (Default)**
```
┌─────────────────────────────┬──────────────────────────────────────┐
│ Tree Navigator (Left)       │ Detail View (Right)                  │
│ 40% width                   │ 60% width                            │
└─────────────────────────────┴──────────────────────────────────────┘
```

**2. Full Tree View**
```
┌──────────────────────────────────────────────────────────────────┐
│ Tree Navigator (Full Width)                                      │
│ Detail pane minimized - press 'd' to restore                     │
└──────────────────────────────────────────────────────────────────┘
```

### Render Modes (Detail Pane)

Users can cycle through applicable render modes with `Tab` key:

**Available for all types:**
- **Tree View**: Hierarchical .east representation
- **Type View**: Show type instead of value (uses `printType`)

**Type-specific renderers:**

| Type | Renderers | Default |
|------|-----------|---------|
| Primitive | Value, Type | Value |
| String | Value (wrapped), Type | Value |
| Blob | Hexdump, Type | Hexdump |
| Array | List, Type, Tree | List |
| Array<Struct> | **Tabular**, List, Type, Tree | Tabular |
| Struct | Fields, Type, Tree | Fields |
| Dict | Pairs, Type, Tree | Pairs |

**Renderer Descriptions:**

1. **Value**: Direct value display (primitives, strings with word-wrap)
2. **Type**: Show type signature only (`printType`)
3. **Tree**: Full .east pretty-printed format (`printFor`)
4. **Hexdump**: Binary view with ASCII sidebar (for blobs)
5. **List**: Array elements with indices `[0] value, [1] value, ...`
6. **Tabular**: Column-aligned table view for array-of-structs
7. **Fields**: Struct fields as key-value pairs
8. **Pairs**: Dict entries as key-value pairs

### Data Model

```typescript
// Tree node structure
type TreeNode = {
  key: string;           // Field name, array index, or "root"
  value: any;            // Actual East value
  type: any;             // EastType from parseInferred or decodeBeast2
  expanded: boolean;     // Expansion state
  selected: boolean;     // Current cursor position
  children?: TreeNode[]; // For composite types (struct, array, dict)
  depth: number;         // Indentation level (0 = root)
  path: string[];        // Path from root (for navigation)
}

// View state
type ViewerState = {
  tree: TreeNode;                 // Root node
  cursor: string[];               // Current selection path
  layoutMode: 'split' | 'full';   // Layout mode
  renderMode: RenderMode;         // Active detail renderer
  scrollOffset: number;           // Scroll position for detail pane
}

// Render mode type
type RenderMode =
  | 'value'
  | 'type'
  | 'tree'
  | 'hexdump'
  | 'list'
  | 'tabular'
  | 'fields'
  | 'pairs';
```

## Features

### Tree Navigation (Left Pane)

**Visual Indicators:**
- `▶` - Collapsed node (expandable)
- `▼` - Expanded node
- `•` - Leaf value (not expandable)
- `→` - Current selection (cursor)

**Display Format:**
```
▶ users [Array, 3 items]
▼ config [Struct]
  • host: "localhost" (String)
  • port: 8080 (Integer)
  ▶ settings [Struct, 5 fields]
• count: 42 (Integer)
```

**Keyboard Controls:**
- `↑/↓` or `j/k` - Navigate up/down
- `→` or `Enter` or `Space` - Expand node
- `←` or `Backspace` - Collapse node
- `Home/End` - Jump to first/last item
- `PageUp/PageDown` - Scroll by page

### Detail View (Right Pane)

**Header:**
```
Type: .Struct [(name="users", type=.Array .Struct [...]), ...]
Render: Tabular [Tab to cycle] | Path: root.users[0]
```

**Content Examples:**

**Tabular Renderer (Array of Structs):**
```
┌────────┬─────┬─────────────────────┐
│ name   │ age │ email               │
├────────┼─────┼─────────────────────┤
│ Alice  │ 30  │ alice@example.com   │
│ Bob    │ 25  │ bob@example.com     │
│ Carol  │ 35  │ carol@example.com   │
└────────┴─────┴─────────────────────┘
```

**Hexdump Renderer (Blob):**
```
00000000  48 65 6c 6c 6f 20 57 6f  72 6c 64 21 0a 00 00 00  |Hello World!....|
00000010  de ad be ef ca fe ba be  00 00 00 00 00 00 00 00  |................|
```

**Fields Renderer (Struct):**
```
host: "localhost"
port: 8080
enabled: true
settings: [Struct, 5 fields]
```

**Keyboard Controls:**
- `Tab` - Cycle through available render modes
- `t` - Toggle to type view
- `↑/↓` - Scroll content (when applicable)
- `Home/End` - Jump to top/bottom

### Global Controls

- `d` - Toggle detail pane (minimize/restore)
- `f` - Toggle full-screen tree mode
- `q` or `Esc` - Quit
- `/` - Search (future feature)
- `?` - Show help overlay

## Input Sources

```bash
# From file (auto-detect format)
e3 view data.beast2
e3 view result.east
e3 view config.json --type '.Struct (...)'

# From stdin
e3 get task-result --format beast2 | e3 view
cat data.east | e3 view
echo '[1, 2, 3]' | e3 view

# From repository by hash
e3 view abc123def456

# Specify input format explicitly
e3 view data.txt --from east
cat binary.dat | e3 view --from beast2
```

## Implementation Phases

### Phase 1: Foundation ✓ (Target: Basic Visual)
- [ ] Create `e3-cli/src/commands/view.tsx`
- [ ] Implement data loading (reuse from convert.tsx)
  - [ ] File input with format detection
  - [ ] stdin support
  - [ ] Parse with parseInferred/decodeBeast2
- [ ] Basic two-pane layout with ink
  - [ ] Left: Tree pane placeholder
  - [ ] Right: Detail pane placeholder
  - [ ] Bottom: Status bar with keybindings
- [ ] Build tree data structure from East value
- [ ] Simple tree rendering (no interaction yet)

### Phase 2: Tree Navigation ✓ (Target: Interactive Tree)
- [ ] Keyboard input handling with useInput
- [ ] Navigation state management
  - [ ] Cursor tracking (selected node path)
  - [ ] Expand/collapse state
- [ ] Tree interaction
  - [ ] Arrow key navigation
  - [ ] Expand/collapse with →/←/Enter
  - [ ] Visual cursor indicator
- [ ] Scroll handling for tall trees

### Phase 3: Detail Renderers ✓ (Target: Multiple Views)
- [ ] Implement base renderers
  - [ ] Value renderer (primitives, strings)
  - [ ] Type renderer (using printType)
  - [ ] Tree renderer (using printFor)
- [ ] Implement specialized renderers
  - [ ] Hexdump for blobs
  - [ ] Tabular for array-of-structs
  - [ ] List for arrays
  - [ ] Fields for structs
  - [ ] Pairs for dicts
- [ ] Render mode cycling (Tab key)
- [ ] Mode-specific rendering logic
  - [ ] Determine available modes per type
  - [ ] Smart defaults based on data shape

### Phase 4: Layout & UX ✓ (Target: Polished Experience)
- [ ] Layout modes
  - [ ] Toggle detail pane (d key)
  - [ ] Full-screen tree mode (f key)
  - [ ] Responsive sizing
- [ ] Navigation enhancements
  - [ ] Path display (breadcrumb)
  - [ ] Home/End navigation
  - [ ] PageUp/PageDown
- [ ] Visual polish
  - [ ] Borders and dividers
  - [ ] Header with type info
  - [ ] Status bar with hints
  - [ ] Keyboard shortcut legend

### Phase 5: Styling & Colors ✓ (Target: Beautiful UI)
- [ ] Color scheme
  - [ ] Type colors (Integer: blue, String: green, etc.)
  - [ ] Syntax highlighting in tree view
  - [ ] Cursor/selection highlighting
- [ ] Theme support
  - [ ] Light/dark mode detection
  - [ ] Custom color configuration
- [ ] Visual refinements
  - [ ] Box drawing characters
  - [ ] Alignment and padding
  - [ ] Truncation with ellipsis

### Phase 6: Advanced Features (Future)
- [ ] Search functionality (/)
  - [ ] Search by key name
  - [ ] Search by value
  - [ ] Regex support
- [ ] Filtering
  - [ ] Filter by type
  - [ ] Hide/show certain fields
- [ ] Export
  - [ ] Copy selected node
  - [ ] Export subtree to file
- [ ] Virtualization for huge datasets
- [ ] Diff mode (compare two values)

## Technical Notes

### Code Reuse

**From `convert.tsx`:**
- `parseInferred()` - Parse .east with type inference
- `decodeBeast2()` - Decode .beast2 self-describing format
- `printType()` - Render type signatures
- `printFor()` - Render values in .east format
- Format detection logic

**New Components:**
- `TreeNavigator` - Left pane tree view
- `DetailView` - Right pane content viewer
- `StatusBar` - Bottom keybinding hints
- Renderer components for each mode

### Performance Considerations

- Lazy tree building (don't expand all nodes immediately)
- Virtualized scrolling for arrays with 1000+ items
- Memoized rendering for static nodes
- Debounced keyboard input for smooth navigation

### Testing Strategy

**Test data:**
- Primitives: integers, strings, booleans
- Collections: arrays, structs, dicts
- Nested structures: deep trees
- Large datasets: 1000+ element arrays
- Special cases: empty arrays, null values, blobs

**Manual testing:**
- Keyboard navigation feels responsive
- All render modes display correctly
- Layout modes work properly
- Long strings wrap correctly
- Hexdump displays properly

## Design Inspirations

- **parqeye** - Split pane layout, tabular view
- **fx/jq** - JSON tree navigation
- **htop** - Keyboard hints, clean status bar
- **less** - Scrolling, navigation patterns
- **VSCode** - Tree expansion UX

## Future Enhancements

- **Copy to clipboard** - yank current value/path
- **Jump to path** - Enter path like `root.users[0].name`
- **Bookmarks** - Mark interesting nodes for quick return
- **History** - Back/forward navigation through selections
- **Watch mode** - Auto-refresh when file changes
- **Compare mode** - View two values side-by-side
- **Plugin renderers** - Custom visualizations for domain types
- **Export views** - Save current visualization as HTML/SVG

## Open Questions

1. How to handle circular references? (East shouldn't have them, but check)
2. Maximum practical tree depth before UX degrades?
3. Should we support editing values? (Probably not v1)
4. Color scheme: 16-color ANSI or full RGB?
5. Should tabular mode auto-detect column widths or allow manual resize?

## Status

**Current Phase:** Planning
**Next Action:** Implement Phase 1 (Foundation)
**Target Completion:** TBD

---

*Document Version: 1.0*
*Last Updated: 2025-11-19*
