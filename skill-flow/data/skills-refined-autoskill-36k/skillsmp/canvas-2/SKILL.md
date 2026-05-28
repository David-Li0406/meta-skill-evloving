---
name: canvas
description: |
  Render interactive UIs in a browser window using file operations.
  Supports two modes: React (App.jsx) for rapid prototyping with pre-built components,
  and Vanilla (index.html) for standards-based, portable artifacts.
  Use when users ask to: show forms, render charts/graphs, create dashboards,
  display data tables, build visual interfaces, or show any UI component.
  Trigger phrases: "show me", "render", "display", "create a form/chart/table/dashboard".
---

# Browser Canvas

## Choosing a Mode

The server auto-detects the mode based on filename:

| File | Mode | Best For |
|------|------|----------|
| `App.jsx` | React | Rapid prototyping, complex forms, dashboards with charts |
| `index.html` | Vanilla | Portable artifacts, standards-based code, durability |

### React Mode (App.jsx)
- Pre-bundled shadcn/ui components (Button, Card, Dialog, etc.)
- Tailwind CSS styling
- useState/useEffect reactivity
- Recharts for data visualization
- Hot-reload preserves state

### Vanilla Mode (index.html)
- Standards-based HTML/CSS/JS
- Native HTML elements (`<dialog>`, `<details>`, `<select>`, `<input type="date">`)
- Web components for composition
- CSS variables for styling
- Import maps for libraries (Chart.js, etc.)
- No build step - files served directly
- Portable - works without the server

## Setup

Start the server once per session:

```bash
cd /path/to/browser-canvas && ./server.sh &
```

Wait for "Ready on http://localhost:9847" before proceeding.

## Design First

Before creating a canvas, consider the aesthetic direction:

1. **Check for brand guidelines** - Look for brand assets, style guides, or design tokens in the project (e.g., `brand/`, `design/`, `.claude/canvas/`)
2. **Read `references/frontend-design.md`** for guidance on:
   - Typography choices (avoid generic fonts like Inter/Arial)
   - Color palettes (commit to a cohesive theme)
   - Motion and animations
   - Spatial composition

Use the project's `.claude/canvas/styles.css` to implement custom fonts, colors, and effects.

## Creating a Canvas

Write an `App.jsx` file to a new folder in `.claude/artifacts/`:

```jsx
// Write to: .claude/artifacts/my-app/App.jsx

function App() {
  return (
    <Card className="w-96 mx-auto mt-8">
      <CardHeader>
        <CardTitle>Hello World</CardTitle>
      </CardHeader>
      <CardContent>
        <p>This renders in the browser!</p>
      </CardContent>
    </Card>
  );
}
```

The server auto-detects the new folder and opens a browser tab.

## Creating a Vanilla Canvas

Write an `index.html` file to a new folder:

```html
<!-- Write to: .claude/artifacts/my-app/index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>My App</title>
  <link rel="stylesheet" href="/base.css">
  <style>
    /* Canvas-specific styles */
    .container { padding: var(--space-6); max-width: 32rem; margin: 0 auto; }
  </style>
</head>
<body>
  <main class="container">
    <article class="card">
      <header class="card-header"><h2>Hello World</h2></header>
      <div class="card-body">
        <p>This renders in the browser!</p>
        <button id="action">Click Me</button>
      </div>
    </article>
  </main>

  <script type="module">
    document.getElementById('action').onclick = () => {
      window.canvasEmit('clicked', { timestamp: Date.now() })
    }
  </script>
</body>
</html>
```

### Vanilla CSS Variables (from base.css)

```css
--color-bg, --color-fg, --color-muted, --color-primary
--color-border, --color-input, --color-danger, --color-success
--space-1 (0.25rem) through --space-8 (2rem)
--radius-sm, --radius, --radius-lg
--shadow-sm, --shadow, --shadow-lg
```

### Vanilla Utility Classes

```css
.card, .card-header, .card-body, .card-footer
.flex, .flex-col, .items-center, .justify-between, .gap-2, .gap-4
.text-sm, .text-muted, .font-medium, .font-bold
button, button.secondary, button.danger, button.ghost
```

### Using Libraries in Vanilla Mode

Use import maps for external libraries:

```html
<script type="importmap">
{
  "imports": {
    "chart.js": "https://cdn.jsdelivr.net/npm/chart.js@4/auto/+esm",
    "marked": "https://cdn.jsdelivr.net/npm/marked@15/+esm"
  }
}
</script>

<script type="module">
  import Chart from 'chart.js'
  import { marked } from 'marked'
  // Use the libraries
</script>
```

### Web Components in Vanilla Mode

Define reusable components inline:

```html
<script>
  class StatCard extends HTMLElement {
    connectedCallback() {
      const value = this.getAttribute('value')
      const label = this.getAttribute('label')
      this.innerHTML = `
        <article class="card" style="padding: var(--space-4);">
          <div style="font-size: var(--text-2xl); font-weight: 700; color: var(--color-primary);">${value}</div>
          <div style="font-size: var(--text-sm); color: var(--color-muted);">${label}</div>
        </article>
      `
    }
  }
  customElements.define('stat-card', StatCard)
</script>

<!-- Use it -->
<stat-card value="$1,234" label="Revenue"></stat-card>
```

## Updating a Canvas

Edit the `App.jsx` or `index.html` file using the Edit tool. The browser hot-reloads automatically.

- **React mode:** Hot-reload preserves component state
- **Vanilla mode:** Full page refresh on change

## Automatic Validation Feedback

When you write or edit an `App.jsx` file, validation errors are automatically injected into your next response. You don't need to manually check `_log.jsonl` for validation issues—they'll appear as context after each write.

Validation checks: ESLint (undefined variables, syntax), scope (missing components), Tailwind (invalid classes), bundle size.

## Reading the Log

All canvas activity is logged to `_log.jsonl`. Use grep to filter by type:

```bash
# View all log entries
cat .claude/artifacts/my-app/_log.jsonl

# View recent events (user interactions)
grep '"type":"event"' .claude/artifacts/my-app/_log.jsonl | tail -10

# View errors only
grep '"severity":"error"' .claude/artifacts/my-app/_log.jsonl | head -5

# View validation notices
grep '"type":"notice"' .claude/artifacts/my-app/_log.jsonl | tail -10

# View specific issue categories
grep '"category":"scope"' .claude/artifacts/my-app/_log.jsonl    # Missing components
grep '"category":"lint"' .claude/artifacts/my-app/_log.jsonl     # Visual issues
grep '"category":"runtime"' .claude/artifacts/my-app/_log.jsonl  # Runtime crashes
```

### Log Entry Types

| Type | Description | Example |
|------|-------------|---------|
| `event` | User interactions | `{"type":"event","event":"submit","data":{"name":"John"}}` |
| `notice` | Validation issues | `{"type":"notice","severity":"error","category":"scope","message":"'Foo' is not available"}` |
| `render` | Render lifecycle | `{"type":"render","status":"success","duration":42}` |
| `screenshot` | Screenshot captures | `{"type":"screenshot","path":"_screenshot.png"}` |

### Notice Categories

| Category | Source | Description |
|----------|--------|-------------|
| `runtime` | Browser | Component crashes, uncaught errors |
| `lint` | Browser | axe-core visual issues (contrast, etc.) |
| `eslint` | Server | Code quality issues |
| `scope` | Server | Missing components or hooks |
| `tailwind` | Server | Invalid Tailwind classes |
| `overflow` | Browser | Layout overflow detection |
| `image` | Browser | Broken images |
| `bundle` | Server | Bundle size warnings |

### Severity Levels

- `error` - Must fix (component won't render or looks broken)
- `warning` - Should fix (code smell or minor issue)
- `info` - Optional improvement

## Canvas Operations (TypeScript API)

Use the `CanvasClient` for operations like screenshots and closing canvases:

```typescript
import { CanvasClient } from "browser-canvas"

const client = await CanvasClient.fromServerJson()

// Take a screenshot
const { path } = await client.screenshot("my-app")
// Screenshot saved to: .claude/artifacts/my-app/_screenshot.png

// Close a canvas
await client.close("my-app")

// Get/set state (alternative to file-based)
const state = await client.getState("my-app")
await client.setState("my-app", { step: 2 })

// Get validation status
const status = await client.getStatus("my-app")
// { errorCount: 0, warningCount: 1, notices: [...] }

// List all canvases
const canvases = await client.list()

// Check server health
const healthy = await client.health()
```

Run this as a script:

```bash
bun run my-script.ts
```

### Taking Screenshots

```typescript
import { CanvasClient } from "browser-canvas"

const client = await CanvasClient.fromServerJson()
await client.screenshot("my-app")
```

Then read the image: `.claude/artifacts/my-app/_screenshot.png`

### Closing a Canvas

```typescript
import { CanvasClient } from "browser-canvas"

const client = await CanvasClient.fromServerJson()
await client.close("my-app")
```

## Available Components

All components are pre-loaded and available without imports.

### React Hooks

```
useState, useEffect, useCallback, useMemo, useRef, useReducer
useCanvasState  # Two-way state sync with agent
```

### shadcn/ui Components

**Layout:**
- `Card`, `CardHeader`, `CardTitle`, `CardDescription`, `CardContent`, `CardFooter`
- `Dialog`, `DialogTrigger`, `DialogContent`, `DialogHeader`, `DialogTitle`, `DialogDescription`, `DialogFooter`
- `Sheet`, `SheetTrigger`, `SheetContent`
- `Tabs`, `TabsList`, `TabsTrigger`, `TabsContent`
- `Accordion`, `AccordionItem`, `AccordionTrigger`, `AccordionContent`

**Forms:**
- `Button`, `Input`, `Textarea`, `Label`
- `Select`, `SelectTrigger`, `SelectValue`, `SelectContent`, `SelectItem`
- `Checkbox`, `RadioGroup`, `RadioGroupItem`
- `Switch`, `Slider`

**Data Display:**
- `Table`, `TableHeader`, `TableBody`, `TableRow`, `TableHead`, `TableCell`
- `Badge`, `Avatar`, `AvatarImage`, `AvatarFallback`
- `Progress`, `Skeleton`

**Feedback:**
- `Alert`, `AlertTitle`, `AlertDescription`
- `Tooltip`, `TooltipTrigger`, `TooltipContent`, `TooltipProvider`

### Charts (Recharts)

```
LineChart, BarChart, PieChart, AreaChart, RadarChart
Line, Bar, Pie, Area, Radar
XAxis, YAxis, CartesianGrid, Tooltip, Legend
ResponsiveContainer, Cell
```

### Icons (Lucide)

All lucide-react icons are available:

```
Check, X, Plus, Minus, ChevronRight, ChevronDown, ChevronUp, ChevronLeft,
Search, Settings, User, Mail, Phone, Calendar, Clock, Bell,
FileText, Folder, Download, Upload, Trash, Edit, Copy, Save,
Home, Menu, MoreHorizontal, MoreVertical, ExternalLink, Link,
Eye, EyeOff, Lock, Unlock, Star, Heart, ThumbsUp, ThumbsDown,
ArrowRight, ArrowLeft, ArrowUp, ArrowDown, RefreshCw, Loader2,
AlertCircle, AlertTriangle, Info, HelpCircle, CheckCircle, XCircle
```

### Utilities

- `cn()` - className helper (clsx + tailwind-merge)
- `format()` - date-fns format function
- `Markdown` - react-markdown component for rendering markdown
- `remarkGfm` - GitHub Flavored Markdown plugin (tables, strikethrough, etc.)

## Emitting Events

Components send data back to Claude via `window.canvasEmit()`:

```jsx
<Button onClick={() => window.canvasEmit('clicked', { buttonId: 1 })}>
  Click Me
</Button>
```

Events appear in `_log.jsonl` for Claude to read.

### Event Format

```json
{"ts":"2026-01-07T10:30:00Z","type":"event","event":"eventName","data":{"key":"value"}}
```

Filter events with: `grep '"type":"event"' _log.jsonl | tail -10`

## Two-Way State Sync

For stateful artifacts that need bidirectional communication, use `_state.json`:

### How State Works

- **No state file?** `useCanvasState()` returns `{}` (empty object)
- **Agent writes first?** Canvas sees the state immediately on load
- **Canvas writes first?** Creates `_state.json` for agent to read
- **Either side updates?** Changes sync automatically via WebSocket

### Agent Sets State

Write state to control the canvas (can be done before or after canvas loads):

```json
// Write to: .claude/artifacts/my-wizard/_state.json
{
  "step": 2,
  "message": "Please confirm your details",
  "formData": { "name": "John" }
}
```

### Canvas Reads/Writes State

Use the `useCanvasState` hook:

```jsx
function App() {
  const [state, setState] = useCanvasState();

  return (
    <Card className="w-96 mx-auto mt-8">
      <CardHeader>
        <CardTitle>Step {state.step || 1}</CardTitle>
      </CardHeader>
      <CardContent>
        <p>{state.message || "Welcome!"}</p>
        <Input
          value={state.formData?.name || ""}
          onChange={(e) => setState({
            ...state,
            formData: { ...state.formData, name: e.target.value }
          })}
        />
      </CardContent>
      <CardFooter>
        <Button onClick={() => setState({ ...state, confirmed: true })}>
          Confirm
        </Button>
      </CardFooter>
    </Card>
  );
}
```

### Agent Reads Updated State

```bash
# Read: .claude/artifacts/my-wizard/_state.json
{"step":2,"message":"...","formData":{"name":"John"},"confirmed":true}
```

### State vs Events

| `_state.json` | `_log.jsonl` events |
|---------------|---------------------|
| Current snapshot | Append-only log |
| Two-way sync | One-way (canvas → agent) |
| "What's true now" | "What happened" |
| Good for: forms, wizards, settings | Good for: clicks, submissions, audit trail |

Use both together: state for current values, events for action history.

## Reusable Components

Pre-built components are auto-loaded and available in your App.jsx. Use them with props for customization.

### ContactForm

Validated form with customizable fields:

```jsx
function App() {
  return (
    <ContactForm
      title="Get in Touch"
      description="We'll respond within 24 hours"
      fields={[
        { name: "name", label: "Name", required: true },
        { name: "email", type: "email", label: "Email", required: true },
        { name: "company", label: "Company" },
        { name: "message", type: "textarea", label: "Message", required: true }
      ]}
      submitLabel="Send Message"
      onSubmit={(data) => window.canvasEmit("contact", data)}
    />
  )
}
```

**Props:** `title`, `description`, `fields`, `onSubmit`, `submitLabel`, `successMessage`, `showReset`, `className`

### DataChart

Flexible charting (line, bar, area, pie):

```jsx
function App() {
  const data = [
    { month: "Jan", sales: 4000, revenue: 2400 },
    { month: "Feb", sales: 3000, revenue: 1398 },
    { month: "Mar", sales: 2000, revenue: 9800 },
  ]

  return (
    <DataChart
      type="bar"
      data={data}
      xKey="month"
      series={[
        { dataKey: "sales", color: "#8884d8", label: "Sales" },
        { dataKey: "revenue", color: "#82ca9d", label: "Revenue" }
      ]}
      title="Monthly Performance"
      height={300}
    />
  )
}
```

**Props:** `type` (line/bar/area/pie), `data`, `xKey`, `series`, `title`, `description`, `height`, `onClick`, `showLegend`, `showGrid`, `formatValue`

### DataTable

Searchable, selectable data table:

```jsx
function App() {
  const users = [
    { id: 1, name: "Alice", email: "alice@example.com", status: "active" },
    { id: 2, name: "Bob", email: "bob@example.com", status: "pending" },
  ]

  return (
    <DataTable
      data={users}
      columns={[
        { key: "name", label: "Name" },
        { key: "email", label: "Email" },
        { key: "status", label: "Status", render: (v) => <Badge>{v}</Badge> }
      ]}
      title="Team Members"
      searchable
      selectable
      onRowClick={(row) => window.canvasEmit("user-click", row)}
      actions={[
        { icon: Pencil, onClick: (row) => window.canvasEmit("edit", row) },
        { icon: Trash2, variant: "ghost", onClick: (row) => window.canvasEmit("delete", row) }
      ]}
    />
  )
}
```

**Props:** `data`, `columns`, `title`, `description`, `searchable`, `selectable`, `onRowClick`, `onSelectionChange`, `actions`, `emptyMessage`

### StatCard

Single statistic display:

```jsx
<StatCard
  title="Total Revenue"
  value="$45,231"
  change="+20.1%"
  trend="up"
  icon={DollarSign}
/>
```

**Props:** `title`, `value`, `change`, `trend` (up/down), `icon`, `onClick`, `description`

### ActivityFeed

Recent activity list:

```jsx
<ActivityFeed
  items={[
    { id: 1, user: "Alice", avatar: "AJ", action: "completed order #1234", time: "2 min ago" },
    { id: 2, user: "Bob", avatar: "BS", action: "signed up", time: "15 min ago" },
  ]}
  title="Recent Activity"
  onItemClick={(item) => window.canvasEmit("activity-click", item)}
/>
```

**Props:** `items`, `title`, `description`, `onItemClick`, `emptyMessage`, `maxItems`, `showViewAll`, `onViewAll`

### ProgressList

Multiple progress bars:

```jsx
<ProgressList
  title="Goals Progress"
  items={[
    { label: "Revenue Target", current: 45231, max: 50000 },
    { label: "New Customers", value: 90 },
    { label: "Orders", current: 1234, max: 1500, format: (c, m) => `${c} of ${m}` },
  ]}
/>
```

**Props:** `items`, `title`, `description`, `showPercentage`

### MarkdownViewer

Beautiful markdown document renderer with refined typography:

```jsx
const markdown = `
# Document Title

This is a paragraph with **bold** and *italic* text.

## Section

- List item one
- List item two

\`\`\`javascript
const greeting = "Hello, world!"
\`\`\`
`

function App() {
  return (
    <MarkdownViewer
      content={markdown}
      title="Documentation"
      variant="default"
      showTableOfContents={true}
    />
  )
}
```

**Props:** `content` (markdown string), `title`, `variant` (default/compact/wide), `showTableOfContents`, `className`

**Features:** GFM tables, code blocks, blockquotes, lists, links, images, heading anchors

### Custom Project Components

Create project-specific components in `.claude/canvas/components/`:

```jsx
// .claude/canvas/components/MyWidget.jsx

/**
 * MyWidget - Custom component for this project
 * @prop {string} title - Widget title
 */
function MyWidget({ title }) {
  return (
    <Card>
      <CardHeader><CardTitle>{title}</CardTitle></CardHeader>
      <CardContent>Custom content here</CardContent>
    </Card>
  )
}
```

Components are auto-loaded on server start. Project components override skill components with the same name.

## Project Extensions

Add custom libraries, Tailwind plugins, or CSS by creating files in `.claude/canvas/`.

### Adding Libraries

Install packages and export them for use in canvas:

```bash
bun add react-markdown
```

```typescript
// .claude/canvas/scope.ts
import ReactMarkdown from "react-markdown"

export const extend = {
  ReactMarkdown
}
```

Then use in App.jsx:

```jsx
function App() {
  return <ReactMarkdown># Hello</ReactMarkdown>
}
```

### Adding Tailwind Plugins

```javascript
// .claude/canvas/tailwind.config.js
export default {
  plugins: [
    require('@tailwindcss/typography'),
  ],
}
```

### Custom CSS

```css
/* .claude/canvas/styles.css */
.custom-gradient {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.prose pre {
  background: #1e1e2e;
}
```

Extensions are detected at server startup and bundled automatically. Restart the server after adding extensions.

## Reference Documentation

Read these references as needed:

| Reference | When to Read |
|-----------|--------------|
| `references/frontend-design.md` | **Read first** - Before creating any new canvas |
| `references/components.md` | Need specific shadcn/ui component props or variants |
| `references/charts.md` | Building charts with Recharts |
| `references/patterns.md` | Building forms, tables, wizards, or dashboards |

## Canvas Directory Structure

Artifacts are stored in `.claude/artifacts/` by default (version-controllable):

```
.claude/artifacts/
├── server.json                 # Server state (port, active canvases)
├── _server.log                 # Server logs
├── my-form/                    # React canvas
│   ├── App.jsx                 # React component (you write this)
│   ├── _log.jsonl              # Unified log: events, notices, errors
│   ├── _state.json             # Two-way state (you + canvas write)
│   └── _screenshot.png         # Screenshot output (API writes)
├── data-viz/
│   └── App.jsx                 # Another React canvas
└── my-dashboard/               # Vanilla canvas
    ├── index.html              # HTML/CSS/JS (you write this)
    ├── _log.jsonl              # Same log format as React
    └── _state.json             # Same state sync as React
```

Both modes use the same file protocol for events, state, and screenshots.

## Browser Toolbar

The browser displays a toolbar at the top with:
- **Claude Canvas** branding
- **Artifact dropdown** to switch between canvases
- **Connection status** indicator

Use the dropdown to navigate between different artifacts without leaving the browser.

## Tips

1. Use Tailwind classes for styling - all utilities available
2. Use `useCanvasState` for two-way communication
3. Emit events for actions needing audit trail
4. Check `_state.json` for current form values
5. Grep `_log.jsonl` for errors: `grep '"severity":"error"' _log.jsonl`
6. Take screenshots to verify visual output
7. Edit incrementally - hot-reload preserves state

## Reporting Issues

Report bugs or request features:

```bash
gh issue create --repo parkerhancock/browser-canvas --title "Bug: [description]"
```
