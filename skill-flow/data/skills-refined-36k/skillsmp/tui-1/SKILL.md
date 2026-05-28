---
name: tui
description: Create distinctive, production-grade terminal user interfaces (TUIs) using OpenTUI. Use this skill when the user asks to build CLI tools, terminal dashboards, interactive console applications, or any interface that runs in the terminal.
---

This skill guides creation of distinctive, production-grade terminal user interfaces that avoid generic "boring CLI" patterns. Build real working TUIs with OpenTUI that are functional, beautiful, and memorable.

## Critical Prerequisites

## TUI Design Thinking

Before coding, understand the context and commit to a CLEAR design direction:

- **Purpose**: What problem does this TUI solve? Who uses it? Is it a single-use tool or daily driver?
- **Tone**: Pick a direction: clean/minimal, data-dense/dashboard-like, playful/interactive, brutalist/raw, retro-terminal, modern/polished. Each tone has different trade-offs in complexity vs. usability.
- **Constraints**: Terminal size considerations, input methods (keyboard shortcuts, mouse), performance requirements.
- **Differentiation**: What makes this TUI memorable? What's the interaction pattern that stands out?

**CRITICAL**: Choose a clear design direction and execute it. Terminal interfaces benefit from restraint and clarity - don't overcomplicate simple tasks, but don't under-deliver on complex ones.

## OpenTUI Fundamentals

OpenTUI provides a single core package with multiple ways to build:

- **@opentui/core**: The main library with primitives like `BoxRenderable`, `TextRenderable`, `InputRenderable`, and declarative constructs like `Box()`, `Text()`, `Input()`. This is what you use.

**Installation**:
```bash
bun install @opentui/core
```

### Two Approaches: Imperative vs Declarative

**Imperative (Renderables)**: Create instances with `new` and compose via `.add()`:
```typescript
import { createCliRenderer, BoxRenderable, TextRenderable } from '@opentui/core';

const renderer = await createCliRenderer();
const box = new BoxRenderable(renderer, { id: 'my-box', width: 20, height: 10 });
const text = new TextRenderable(renderer, { content: 'Hello' });
box.add(text);
renderer.root.add(box);
renderer.start();
```

**Declarative (Constructs/VNodes)**: Use function calls that return VNodes:
```typescript
import { createCliRenderer, Box, Text } from '@opentui/core';

const renderer = await createCliRenderer();

const myBox = Box(
  { id: 'my-box', width: 20, height: 10 },
  Text({ content: 'Hello' })
);

renderer.root.add(myBox);
renderer.start();
```

**Choose based on**:
- Use **Declarative (Constructs)** for most TUIs - cleaner, composable, easier to reason about
- Use **Imperative (Renderables)** when you need direct control over instances or are migrating from low-level code

**IMPORTANT**: Both approaches require `createCliRenderer()` and `renderer.root.add()` - nothing renders without these.

## Terminal Aesthetics Guidelines

Focus on:

- **Typography**: Use monospace fonts (your terminal handles this), but leverage text styling (bold, dim, italic, underline) strategically. Don't over-style - terminal clutter is worse than terminal minimalism.
- **Color & Theme**: Commit to a cohesive palette. Use `RGBA.fromHex()` or color strings sparingly - 2-4 accent colors work best. Ensure high contrast for readability. Support dark themes by default; light themes are optional.
- **Layout**: Use Yoga flexbox-like properties (`flexDirection`, `justifyContent`, `alignItems`, `flexGrow`, `padding`) to create hierarchy. Respect terminal width (typically 80-120 chars) - design for 80 as baseline, expand gracefully.
- **Motion**: Use `renderAfter` hooks for custom animations. Keep them subtle - terminal motion should feel responsive, not flashy.
- **Navigation**: Design for keyboard-first. Arrow keys for navigation, Enter for selection, Esc for cancel/back. Use mnemonics (e.g., press 'q' to quit) for frequent actions. Document key bindings visibly.
- **State Management**: Keep state minimal and local. For complex TUIs, use simple objects or arrays to track state, and call `renderer.requestRender()` after updates.

NEVER use generic TUI patterns like unstyled text dumps, confusing keyboard shortcuts, invisible state changes, or poor handling of terminal resize.

## Essential OpenTUI Patterns

### 1. Basic Setup (Required for Every TUI)

```typescript
import { createCliRenderer } from '@opentui/core';

// Create the renderer
const renderer = await createCliRenderer({
  exitOnCtrlC: true,  // Automatically exit on Ctrl+C
  targetFps: 30,      // Target framerate for animations
});

// Set background color for the entire terminal
renderer.setBackgroundColor('#001122');

// ... add your renderables here ...

// Start the rendering loop
renderer.start();
```

### 2. Keyboard Input Handling

```typescript
import { type KeyEvent } from '@opentui/core';

// Access the keyboard handler
renderer.keyInput.on('keypress', (key: KeyEvent) => {
  console.log('Key name:', key.name);
  console.log('Ctrl pressed:', key.ctrl);
  console.log('Shift pressed:', key.shift);
  console.log('Alt pressed:', key.meta);
  console.log('Option pressed:', key.option);

  if (key.name === 'escape') {
    // Handle escape
  } else if (key.ctrl && key.name === 'c') {
    // Handle Ctrl+C (if exitOnCtrlC is false)
  } else if (key.name === 'q') {
    // Quit the application
    process.exit(0);
  }
});
```

### 3. Box Layout (Declarative)

```typescript
import { Box, Text } from '@opentui/core';

// A container with flexbox layout
const container = Box({
  flexDirection: 'column',
  justifyContent: 'center',
  alignItems: 'center',
  width: '100%',
  height: '100%',
  padding: 1,
  backgroundColor: '#333366',
  border: true,
  borderStyle: 'double',
  borderColor: '#FFFFFF',
  title: 'My Panel',
  titleAlignment: 'center',
});

renderer.root.add(container);
```

### 4. Text with Styling

```typescript
import { Text, TextAttributes, t, bold, underline, fg } from '@opentui/core';

// Simple styled text
const text1 = Text({
  content: 'Important Message',
  fg: '#FFFF00',
  attributes: TextAttributes.BOLD | TextAttributes.UNDERLINE,
});

// Using the template literal for complex styled text
const text2 = Text({
  content: t`${bold("Important")} ${fg("#FF0000")(underline("Alert"))}`,
});

renderer.root.add(text1);
renderer.root.add(text2);
```

### 5. Input Fields

```typescript
import { InputRenderable, InputRenderableEvents } from '@opentui/core';

const nameInput = new InputRenderable(renderer, {
  id: 'name-input',
  width: 30,
  height: 3,
  placeholder: 'Enter your name...',
  placeholderColor: '#666666',
  backgroundColor: '#001122',
  textColor: '#FFFFFF',
  cursorColor: '#FFFF00',
  focusedBackgroundColor: '#1a1a1a',
  position: 'absolute',
  left: 10,
  top: 5,
});

// Listen for changes
nameInput.on(InputRenderableEvents.CHANGE, (value) => {
  console.log('Input changed:', value);
});

// Listen for Enter key
nameInput.on(InputRenderableEvents.ENTER, (value) => {
  console.log('Submitted:', value);
});

renderer.root.add(nameInput);
nameInput.focus();
```

### 6. Select Menu

```typescript
import { SelectRenderable, SelectRenderableEvents, type SelectOption } from '@opentui/core';

const menu = new SelectRenderable(renderer, {
  id: 'menu',
  width: 30,
  height: 8,
  options: [
    { name: 'New File', description: 'Create a new file' },
    { name: 'Open File', description: 'Open an existing file' },
    { name: 'Save', description: 'Save current file' },
    { name: 'Exit', description: 'Exit the application' },
  ],
  position: 'absolute',
  left: 5,
  top: 3,
});

menu.on(SelectRenderableEvents.ITEM_SELECTED, (index, option) => {
  console.log('Selected:', option.name);
});

renderer.root.add(menu);
menu.focus();
// Default keybindings: up/k and down/j to navigate, enter to select
```

### 7. Focus Management and Delegation (Declarative)

When using constructs (VNodes), focus management can be tricky with nested components. Use `delegate` to specify which descendant should receive method calls:

```typescript
import { Box, Text, Input, delegate } from '@opentui/core';

// A labeled input component
function LabeledInput(props: { id: string; label: string; placeholder: string }) {
  return delegate(
    {
      focus: `${props.id}-input`,  // Focus should go to the input, not the container
    },
    Box(
      { flexDirection: 'row', id: `${props.id}-labeled-outer` },
      Text({ content: props.label + ' ' }),
      Input({
        id: `${props.id}-input`,
        placeholder: props.placeholder,
        width: 20,
        backgroundColor: 'white',
        textColor: 'black',
        cursorColor: 'blue',
        focusedBackgroundColor: 'orange',
      }),
    ),
  );
}

// Now you can focus it directly
const usernameInput = LabeledInput({ id: 'username', label: 'Username:', placeholder: 'Enter username...' });
usernameInput.focus();  // This works thanks to delegate!
renderer.root.add(usernameInput);
```

### 8. Colors (RGBA)

```typescript
import { RGBA, parseColor } from '@opentui/core';

// Multiple ways to create colors
const red1 = RGBA.fromInts(255, 0, 0, 255);         // RGB integers (0-255)
const red2 = RGBA.fromValues(1.0, 0.0, 0.0, 1.0);   // Float values (0.0-1.0)
const red3 = RGBA.fromHex('#FF0000');              // Hex string
const red4 = parseColor('#FF0000');                 // Parse any color format
const transparent = RGBA.fromValues(1.0, 1.0, 1.0, 0.5);  // Semi-transparent
```

## Common TUI Components

Build these patterns as needed:

### List View (Scrollable)
```typescript
// Use SelectRenderable with many options, it handles scrolling automatically
const list = new SelectRenderable(renderer, {
  id: 'list',
  width: 40,
  height: 10,
  options: Array.from({ length: 50 }, (_, i) => ({
    name: `Item ${i + 1}`,
    description: `Description for item ${i + 1}`,
  })),
  position: 'absolute',
  left: 5,
  top: 5,
});
renderer.root.add(list);
```

### Form with Validation
```typescript
const nameInput = new InputRenderable(renderer, {
  id: 'name',
  width: 30,
  placeholder: 'Name (min 2 chars)',
  position: 'absolute',
  left: 5,
  top: 2,
});

const emailInput = new InputRenderable(renderer, {
  id: 'email',
  width: 30,
  placeholder: 'Email address',
  position: 'absolute',
  left: 5,
  top: 6,
});

function validateName(value: string): boolean {
  return value.length >= 2;
}

function validateEmail(value: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(value);
}

nameInput.on(InputRenderableEvents.ENTER, (value) => {
  if (validateName(value)) {
    console.log('Name is valid!');
  } else {
    console.log('Name must be at least 2 characters');
  }
});

renderer.root.add(nameInput);
renderer.root.add(emailInput);
nameInput.focus();
```

### Dashboard Layout
```typescript
import { Box, Text } from '@opentui/core';

const mainLayout = Box({
  flexDirection: 'column',
  width: '100%',
  height: '100%',
  padding: 1,
});

const header = Box({
  height: 3,
  border: true,
  marginBottom: 1,
  justifyContent: 'center',
  backgroundColor: '#3b82f6',
});

const content = Box({
  flexDirection: 'row',
  flexGrow: 1,
});

const sidebar = Box({
  width: 20,
  border: true,
  marginRight: 1,
  backgroundColor: '#64748b',
});

const main = Box({
  flexGrow: 1,
  border: true,
  backgroundColor: '#333333',
});

const footer = Box({
  height: 3,
  border: true,
  marginTop: 1,
  justifyContent: 'center',
  backgroundColor: '#1e40af',
});

// Assemble the layout
header.add(Text({ content: 'Dashboard', attributes: TextAttributes.BOLD }));
mainLayout.add(header);

sidebar.add(Text({ content: 'Sidebar' }));
content.add(sidebar);

main.add(Text({ content: 'Main Content Area' }));
content.add(main);

mainLayout.add(content);

footer.add(Text({ content: 'Press q to quit' }));
mainLayout.add(footer);

renderer.root.add(mainLayout);
```

### Confirmation Modal
```typescript
import { Box, Text } from '@opentui/core';

let modalVisible = false;
let confirmCallback: (() => void) | null = null;

function showModal(message: string, onConfirm: () => void) {
  modalVisible = true;
  confirmCallback = onConfirm;

  const modal = Box({
    position: 'absolute',
    width: 40,
    height: 8,
    left: Math.floor((renderer.terminalWidth - 40) / 2),
    top: Math.floor((renderer.terminalHeight - 8) / 2),
    border: true,
    borderStyle: 'double',
    backgroundColor: '#444',
    zIndex: 1000,
    id: 'modal',
  });

  modal.add(Text({ content: message, padding: 1 }));
  modal.add(Text({ content: '[Enter] Yes  [Esc] No', justifyContent: 'center' }));

  renderer.root.add(modal);
}

function hideModal() {
  modalVisible = false;
  const modal = renderer.root.getRenderable('modal');
  if (modal) {
    renderer.root.remove('modal');
  }
}

// In your key handler:
renderer.keyInput.on('keypress', (key) => {
  if (modalVisible) {
    if (key.name === 'return' && confirmCallback) {
      confirmCallback();
      hideModal();
    } else if (key.name === 'escape') {
      hideModal();
    }
  }
});
```

## Best Practices

- **Handle Terminal Resize**: Use flexible layouts with `width: '100%'` and flex properties. The renderer emits 'resize' events:
  ```typescript
  renderer.on('resize', (width, height) => {
    console.log(`Terminal resized to ${width}x${height}`);
    // Adjust layouts if needed
  });
  ```

- **Exit Gracefully**: Always provide a way to quit (Ctrl+C or 'q'). Use `exitOnCtrlC: true` in createCliRenderer options for automatic handling.

- **Error Handling**: Show error messages clearly, don't crash silently. Use the built-in console overlay for debugging:
  ```typescript
  const renderer = await createCliRenderer({
    consoleOptions: {
      position: 'bottom',
      sizePercent: 20,
      startInDebugMode: false,
    },
  });

  // Toggle console with '?'
  renderer.keyInput.on('keypress', (key) => {
    if (key.name === 'question_mark') {
      renderer.console.toggle();
    }
  });

  console.log('This appears in the overlay');
  console.error('Errors are color-coded red');
  ```

- **Performance**: Batch updates, avoid excessive re-renders. Call `renderer.requestRender()` when you've updated multiple renderables.

- **Accessibility**: High contrast, clear focus states, keyboard-only navigation. Focus indicators are automatic when using Input/Select renderables.

- **Cleanup**: When done, remove renderables:
  ```typescript
  export function destroy(renderer: CliRenderer) {
    renderer.root.getRenderable('main-group')?.destroyRecursively();
    renderer.requestRender();
  }
  ```

## Quick Start Template

```typescript
import { createCliRenderer, Box, Text, InputRenderable, InputRenderableEvents, type KeyEvent } from '@opentui/core';

async function main() {
  const renderer = await createCliRenderer({
    exitOnCtrlC: true,
    targetFps: 30,
  });

  renderer.setBackgroundColor('#001122');

  // Create a simple input form
  const container = Box({
    flexDirection: 'column',
    width: '100%',
    height: '100%',
    justifyContent: 'center',
    alignItems: 'center',
  });

  renderer.root.add(container);

  const title = Text({
    content: 'OpenTUI Demo',
    attributes: TextAttributes.BOLD,
    fg: '#00FF00',
    marginBottom: 2,
  });
  container.add(title);

  const input = new InputRenderable(renderer, {
    id: 'demo-input',
    width: 30,
    height: 3,
    placeholder: 'Type something...',
    backgroundColor: '#001122',
    textColor: '#FFFFFF',
    cursorColor: '#FFFF00',
  });

  renderer.root.add(input);
  input.focus();

  const output = Text({
    content: '',
    marginTop: 1,
  });
  container.add(output);

  // Handle input
  input.on(InputRenderableEvents.CHANGE, (value) => {
    output.content = `You typed: ${value}`;
  });

  // Keyboard shortcuts
  renderer.keyInput.on('keypress', (key: KeyEvent) => {
    if (key.name === 'q') {
      process.exit(0);
    }
  });

  // Add instructions
  const instructions = Text({
    content: 'Press Ctrl+C or q to quit',
    marginTop: 2,
    fg: '#666666',
  });
  container.add(instructions);

  renderer.start();
}

main();
```

## Common Pitfalls to Avoid

1. **Forgetting to call renderer.root.add()**: Renderables/VNodes won't appear without this.

2. **Forgetting to call renderer.start()**: The rendering loop won't run without this.

3. **Trying to focus nested inputs without delegate()**: Use the `delegate()` helper to focus elements inside containers.

4. **Not handling terminal resize**: Use flexible layouts or listen to resize events.

5. **Overusing colors**: Stick to 2-4 accent colors for a cohesive look.

6. **Not providing a way to quit**: Always have Ctrl+C or 'q' to exit.

7. **Ignoring focus states**: Users need to know what element is active.

8. **Using JSX syntax**: OpenTUI uses function calls `Box({...}, children)`, NOT `<Box>...</Box>`.

## When to Use This Skill

Use when building:
- Interactive CLI tools with menus or forms
- Terminal dashboards for monitoring
- Interactive wizards or configuration tools
- File managers or navigation interfaces
- Any application that lives primarily in the terminal

Start simple. Add complexity only when needed. Remember: a working TUI that's simple beats a broken one that's ambitious.
