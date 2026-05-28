---
name: peekaboo-macos
description: Full API reference for peekaboo macOS automation. Use for UI automation, screenshots, clicking, typing, and app control.
---

# Peekaboo macOS Automation

TypeScript interface for macOS UI automation via the `peekaboo` CLI.

```typescript
import { peekaboo } from "./agent-scripts";
```

## Core - Vision & Screenshots

### see() - Detect UI Elements

```typescript
// Detect all UI elements on screen
const { data } = await peekaboo.see({ annotate: true });
// Returns elements with IDs like B1, B2, T1, T2, etc.
// B = Button, T = Text, I = Image, etc.

// Focus on specific app
const { data } = await peekaboo.see({ app: "Safari", annotate: true });
```

### image() - Screenshots

```typescript
// Full screen
await peekaboo.image({ path: "/tmp/screenshot.png" });

// Specific app window
await peekaboo.image({ app: "Safari", path: "/tmp/safari.png" });

// With element annotations
await peekaboo.image({ annotate: true, path: "/tmp/annotated.png" });
```

### list() - List Windows/Apps

```typescript
// List all windows
const windows = await peekaboo.list({ type: "windows" });

// List running apps
const apps = await peekaboo.list({ type: "apps" });
```

## Interaction

### click() - Click Elements

```typescript
// Click by element ID (from see())
await peekaboo.click({ on: "B1" });

// Click by coordinates
await peekaboo.click({ x: 100, y: 200 });

// Click by text content
await peekaboo.click({ text: "Submit" });

// Right-click
await peekaboo.click({ on: "B1", button: "right" });

// Double-click
await peekaboo.click({ on: "B1", clicks: 2 });
```

### type() - Type Text

```typescript
// Type text at current cursor
await peekaboo.type({ text: "Hello world" });

// Type with delay between characters (ms)
await peekaboo.type({ text: "Slow typing", delay: 50 });
```

### hotkey() - Keyboard Shortcuts

```typescript
// Cmd+C (copy)
await peekaboo.hotkey({ keys: ["cmd", "c"] });

// Cmd+Shift+S (save as)
await peekaboo.hotkey({ keys: ["cmd", "shift", "s"] });

// Cmd+Tab (switch apps)
await peekaboo.hotkey({ keys: ["cmd", "tab"] });
```

### press() - Press Keys

```typescript
// Single key
await peekaboo.press({ key: "enter" });
await peekaboo.press({ key: "escape" });
await peekaboo.press({ key: "tab" });

// Arrow keys
await peekaboo.press({ key: "down" });
await peekaboo.press({ key: "up" });
```

### scroll() - Scroll

```typescript
// Scroll down
await peekaboo.scroll({ direction: "down", amount: 3 });

// Scroll up
await peekaboo.scroll({ direction: "up", amount: 5 });

// Scroll in specific app
await peekaboo.scroll({ app: "Safari", direction: "down" });
```

### move() - Move Mouse

```typescript
// Move to coordinates
await peekaboo.move({ x: 500, y: 300 });

// Move to element
await peekaboo.move({ on: "B1" });
```

### drag() - Drag and Drop

```typescript
// Drag from one point to another
await peekaboo.drag({ from: { x: 100, y: 100 }, to: { x: 300, y: 300 } });

// Drag element to location
await peekaboo.drag({ from: "B1", to: { x: 300, y: 300 } });
```

### paste() - Paste from Clipboard

```typescript
// Paste current clipboard
await peekaboo.paste();

// Set clipboard and paste
await peekaboo.clipboard.set({ text: "Hello" });
await peekaboo.paste();
```

## System - Apps & Windows

### app - Application Control

```typescript
// Launch app
await peekaboo.app.launch({ name: "Safari" });

// Quit app
await peekaboo.app.quit({ name: "Safari" });

// Activate (bring to front)
await peekaboo.app.activate({ name: "Safari" });

// Hide app
await peekaboo.app.hide({ name: "Safari" });

// List running apps
const apps = await peekaboo.app.list();
```

### window - Window Control

```typescript
// Focus window
await peekaboo.window.focus({ app: "Safari" });

// Minimize
await peekaboo.window.minimize({ app: "Safari" });

// Maximize/fullscreen
await peekaboo.window.maximize({ app: "Safari" });

// Move window
await peekaboo.window.move({ app: "Safari", x: 100, y: 100 });

// Resize window
await peekaboo.window.resize({ app: "Safari", width: 1200, height: 800 });

// Close window
await peekaboo.window.close({ app: "Safari" });
```

### clipboard - Clipboard Operations

```typescript
// Get clipboard content
const content = await peekaboo.clipboard.get();

// Set clipboard
await peekaboo.clipboard.set({ text: "Copied text" });
```

### menu - Menu Bar

```typescript
// Click menu item
await peekaboo.menu.click({ app: "Safari", path: ["File", "New Window"] });

// Get menu structure
const menus = await peekaboo.menu.list({ app: "Safari" });
```

### dialog - System Dialogs

```typescript
// Handle file open dialog
await peekaboo.dialog.fileOpen({ path: "/path/to/file.txt" });

// Handle file save dialog
await peekaboo.dialog.fileSave({ path: "/path/to/save.txt" });
```

### dock - Dock Control

```typescript
// Click dock item
await peekaboo.dock.click({ app: "Safari" });
```

### open - Open Files/URLs

```typescript
// Open URL in default browser
await peekaboo.open({ url: "https://example.com" });

// Open file with default app
await peekaboo.open({ path: "/path/to/file.pdf" });

// Open with specific app
await peekaboo.open({ path: "/path/to/file.txt", app: "TextEdit" });
```

### space - Mission Control / Spaces

```typescript
// Switch to space
await peekaboo.space.switch({ index: 2 });

// Show Mission Control
await peekaboo.space.missionControl();
```

## AI - Agent Mode

### agent() - AI-Powered Automation

```typescript
// Execute natural language command
await peekaboo.agent({ task: "Open Safari and go to google.com" });

// Agent with specific app context
await peekaboo.agent({
  task: "Find the search box and type hello",
  app: "Safari",
});
```

## Utility

### sleep() - Wait

```typescript
// Wait for 1 second
await peekaboo.sleep(1000);
```

## Common Workflow Pattern

```typescript
import { peekaboo } from "./agent-scripts";

// 1. Launch app
await peekaboo.app.launch({ name: "Safari" });
await peekaboo.sleep(1000);

// 2. See what's on screen
const { data } = await peekaboo.see({ app: "Safari", annotate: true });

// 3. Interact with elements
await peekaboo.click({ on: "T1" }); // Click URL bar (text field 1)
await peekaboo.type({ text: "https://example.com" });
await peekaboo.press({ key: "enter" });

// 4. Wait and verify
await peekaboo.sleep(2000);
await peekaboo.image({ app: "Safari", path: "/tmp/result.png" });
```

## Source Files

For implementation details and types, read:

- `agent-scripts/lib/peekaboo/index.ts` - Main exports and namespace
- `agent-scripts/lib/peekaboo/types.ts` - Type definitions
- `agent-scripts/lib/peekaboo/*.ts` - Individual command modules
