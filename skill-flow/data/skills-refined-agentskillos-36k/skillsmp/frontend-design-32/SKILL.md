---
name: frontend-design
description: Brutalist design principles for terminal UI with focus on clarity, function, and minimal aesthetic
---

# Frontend Design Skill

You are a UI/UX designer specializing in terminal interfaces with a brutalist aesthetic. Your role is to create functional, clear, and visually distinctive terminal experiences.

## Design Philosophy: Brutally Minimal

The glm-cli aesthetic is defined by:

1. **Function over decoration** - Every element serves a purpose
2. **Raw and honest** - No unnecessary embellishment
3. **Dense and information-forward** - Maximize useful content
4. **High contrast** - Clear visual hierarchy
5. **Monospace precision** - Embrace the grid

## Core Principles

### 1. Typography

**Font:** Monospace (terminal default)

**Hierarchy through weight, not size:**
- Bold for headings/labels
- Normal for content
- Dim for secondary information
- Italic for thinking/reasoning

**Text Treatments:**
```
UPPERCASE         Section headers
Normal case       Primary content
lowercase         Commands, paths
dim/muted         Secondary info, timestamps
italic            AI thinking, metadata
```

### 2. Color Palette

**Primary Colors:**
| Name | Hex | Usage |
|------|-----|-------|
| Bright Cyan | `#5cffff` | Primary accent, GLM branding |
| Dim Cyan | `#1a6666` | Gradient end, subtle accents |
| White | `#ffffff` | Primary text, important elements |
| Dim Gray | `#666666` | Secondary text, borders |

**Mode Colors:**
| Mode | Color | Hex |
|------|-------|-----|
| AUTO | White | `#ffffff` |
| AGENT | Cyan | `#5cffff` |
| PLANNER | Purple | `#b48eff` |
| PLAN-PRD | Blue | `#5c8fff` |
| DEBUG | Orange | `#ffaa5c` |

**Status Colors:**
| Status | Color | Hex |
|--------|-------|-----|
| Success | Green | `#6fca6f` |
| Warning | Yellow | `#e6c655` |
| Error | Red | `#ff6b6b` |
| Info | Blue | `#5c8fff` |

**Diff Colors:**
| Type | Color |
|------|-------|
| Addition | Green `#6fca6f` |
| Deletion | Red `#ff6b6b` |
| Context | Default white |

### 3. Spacing

**Grid:** 1 character = 1 unit

**Padding:**
- Minimal internal padding (1-2 chars)
- Consistent margins between sections

**Density:**
- Prefer dense layouts over spread out
- Use whitespace strategically, not liberally

### 4. Borders and Boxes

**Box Characters:**
```
┌──────────────────────┐
│  Single line box     │
└──────────────────────┘

╭──────────────────────╮
│  Rounded box         │
╰──────────────────────╯

════════════════════════
  Heavy horizontal rule
════════════════════════

────────────────────────
  Light horizontal rule
────────────────────────
```

**Usage:**
- Single line (`┌─┐`) for primary containers
- Horizontal rules (`────`) for section dividers
- No rounded corners in main UI (too soft)
- Minimal nested boxes

### 5. Icons and Indicators

**Prefer ASCII over emoji:**
```
Status:
  ▶  Collapsed/play
  ▼  Expanded
  ●  Status dot
  ✓  Success (or just [OK])
  ✗  Failure (or just [FAIL])
  │  Vertical connector
  
Progress:
  █  Filled block
  ░  Empty block
  [████████░░] 80%

Indicators:
  >  Prompt cursor
  @  File reference
  #  Line number
  |  Pipe/separator
```

**Never use emoji in the UI.**

### 6. Animation

**Pulse Wave Animation:**
```
Frame 1:    ·
Frame 2:   ·─·
Frame 3:  ·── ──·
Frame 4: ·──   ──·
(reverse back)
```

**Properties:**
- Subtle, not distracting
- Position: left of prompt box
- Color: Cyan gradient trail
- Timing: 120ms per cycle

**Spinner Alternative:**
```
Frame 1: ⠋
Frame 2: ⠙
Frame 3: ⠹
Frame 4: ⠸
Frame 5: ⠼
Frame 6: ⠴
Frame 7: ⠦
Frame 8: ⠧
Frame 9: ⠇
Frame 10: ⠏
```

### 7. Layout Patterns

**Welcome Screen:**
```
┌────────────────────────────────────────────────────┐
│                                                    │
│  [ASCII LOGO]                                      │
│                                                    │
│  v0.1.0                      built 01-19-2026     │
│  Model: GLM-4.7              Dir: ~/project       │
│                                                    │
└────────────────────────────────────────────────────┘

┌─ MODE (Thinking) ──────────────────────────────────┐
│                                                    │
│  > _                                               │
│                                                    │
│    Ghost text here...                              │
│                                                    │
└────────────────────────────────────────────────────┘
STATUS LINE HERE
```

**Session View:**
```
┌─ Session ──────────────────────────────────────────┐
│                                                    │
│  You                                    12:34 PM   │
│  ───                                               │
│  {user message}                                    │
│                                                    │
│  GLM-4.7                                12:34 PM   │
│  ────────                                          │
│  {assistant message}                               │
│                                                    │
│  ▶ tool_name path/to/file                   [OK]  │
│                                                    │
└────────────────────────────────────────────────────┘
```

**Overlay/Dialog:**
```
┌─ Dialog Title ─────────────────────────── [Esc] ──┐
│                                                    │
│  Content here                                      │
│                                                    │
│  [Action 1]    [Action 2]    [Cancel]              │
│                                                    │
└────────────────────────────────────────────────────┘
```

### 8. Status Line

**Format:**
```
MODEL | MODE | [PROGRESS] XX% | DIR |  BRANCH | MCPs: X/X | DATE
```

**Example:**
```
GLM-4.7 | AGENT | [██████░░░░] 62% | ~/project |  main | MCPs: 4/4 | 01-19-2026
```

**During activity:**
```
GLM-4.7 | AGENT | [████░░░░░░] 42% | ~/project |  main | MCPs: 4/4 | create_file...
```

### 9. Gradient Implementation

**ASCII Logo Gradient (left to right):**
```
Column 0                                    Column 55
   │                                            │
   ▼                                            ▼
#5cffff ─────────────────────────────────► #1a6666
Bright                                      Dim

Color stops:
  0%   #5cffff
  25%  #4ad4d4
  50%  #38a9a9
  75%  #267e7e
  100% #1a6666
```

### 10. Responsive Considerations

**Terminal Width:**
- Minimum: 80 columns
- Optimal: 120 columns
- Handle narrow terminals gracefully (truncate with ellipsis)

**Truncation:**
```
/very/long/path/to/file → .../to/file
very-long-function-name → very-long-fu...
```

## Component Reference

### Tool Block (Collapsed)
```
▶ tool_name path/to/file.ts                        [OK]
```

### Tool Block (Expanded)
```
▼ tool_name path/to/file.ts                        [OK]
  ┌──────────────────────────────────────────────────┐
  │ + line added                                     │
  │ - line removed                                   │
  │   context line                                   │
  └──────────────────────────────────────────────────┘
```

### Thinking Block (Streaming)
```
│ Thinking: Current thought content here...█        │
```

### Thinking Block (Collapsed)
```
▶ Thinking                                [collapsed]
```

### Autocomplete Dropdown
```
┌────────────────────────────────────────┐
│ > option 1 (selected)                  │
│   option 2                             │
│   option 3                        [DIR]│
└────────────────────────────────────────┘
```

### Session End Summary
```
────────────────────────────────────────────────────────
  GLM-CLI SESSION COMPLETE
────────────────────────────────────────────────────────

  Duration        1h 23m 45s
  Modes           AGENT (primary) → PLANNER (1 switch)
  
────────────────────────────────────────────────────────
  TOOLS
────────────────────────────────────────────────────────

  Calls           15 total        12 success      3 failed
  Code            +142 lines      -38 lines

────────────────────────────────────────────────────────

  Until next time!

────────────────────────────────────────────────────────
```

## Anti-Patterns

**AVOID:**
- Emoji anywhere in UI
- Rounded corners on main containers
- Excessive whitespace
- Multiple font sizes (it's monospace)
- Decorative elements with no function
- Low contrast text
- Blinking or flashing elements
- Complex nested boxes
