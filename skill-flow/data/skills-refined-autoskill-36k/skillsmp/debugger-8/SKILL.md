---
name: debugger
description: Debug JavaScript/TypeScript applications using browser DevTools protocol, VS Code debugger, or Node.js inspector
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: debugging
---

## What I do

I help debug JavaScript and TypeScript applications using various debugging tools. I can launch debuggers, set breakpoints, inspect variables, and analyze stack traces in browsers or Node.js environments.

## When to use me

Use this when:

- You need to debug runtime behavior
- You're investigating bugs or unexpected outputs
- You want to set breakpoints and step through code
- You're debugging React component renders

## Browser Debugging

```bash
# Chrome DevTools
--inspect-brk           # Break on start
chrome://inspect        # Open DevTools

# VS Code
Debug: Open Link        # Use debug URL
F5                      # Start debugging
F10                     # Step over
F11                     # Step into
Shift+F11               # Step out
```

## Node.js Debugging

```bash
node --inspect index.ts         # Start with inspector
node --inspect-brk index.ts     # Break on start
# Open chrome://inspect in Chrome
```

## Key Concepts

- **Breakpoints**: Pause execution at specific lines
- **Watch Expressions**: Monitor variable values
- **Call Stack**: View execution path
- **Console**: Evaluate expressions in context
- **Source Maps**: Map minified to source code

## Source Files

- `package.json`: Debug scripts and configurations
- `.vscode/launch.json`: VS Code debugger configurations

## Code Patterns

- Use source maps for minified production builds
- Set conditional breakpoints for specific conditions
- Use `debugger` statement for quick breakpoints
- Log objects with `console.dir()` for deep inspection

## Operational Constraints

- Don't leave `debugger` statements in committed code
- Use appropriate debugger for the environment (browser vs Node.js)
- Clean up debug configurations before committing
- Remember to remove breakpoints after debugging
