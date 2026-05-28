# TypeScript/JavaScript Debugging Guide

This guide covers debugging TypeScript and JavaScript applications with debug-run using the js-debug (Node.js) adapter.

## Prerequisites

### js-debug Adapter

The js-debug adapter is detected from two sources:

1. **VS Code js-debug extension** - Built into VS Code or install separately
2. **Installed via debug-run** - `npx debug-run install-adapter node`

Check availability:

```bash
npx debug-run list-adapters
# Should show: node - Status: installed (path)
```

### Installing js-debug

**Option 1: VS Code (Recommended)**
- js-debug is built into VS Code
- Or install the [JavaScript Debugger (Nightly)](https://marketplace.visualstudio.com/items?itemName=ms-vscode.js-debug-nightly) extension

**Option 2: debug-run installer**
```bash
npx debug-run install-adapter node
```

### Node.js

Ensure Node.js is installed:
```bash
node --version  # Should be v18+ recommended
```

## Build TypeScript Projects

For TypeScript, compile to JavaScript first:

```bash
# Install dependencies and build
npm install
npm run build  # or: npx tsc
```

## Launch Mode (Debug JavaScript)

### Basic Debugging

```bash
npx debug-run ./dist/index.js \
  -a node \
  -b "src/index.ts:42" \
  --pretty \
  -t 30s
```

Note: Set breakpoints using the **source TypeScript file path**, not the compiled JavaScript path. Source maps enable this mapping.

### With Expression Evaluation

```bash
npx debug-run ./dist/index.js \
  -a node \
  -b "src/services/OrderService.ts:55" \
  -e "order.total" \
  -e "order.items.length" \
  -e "this.config" \
  --pretty \
  -t 30s
```

### With Assertions

```bash
npx debug-run ./dist/index.js \
  -a node \
  -b "src/services/OrderService.ts:55" \
  --assert "order.total >= 0" \
  --assert "order.items.length > 0" \
  --assert "this.inventory !== null" \
  --pretty \
  -t 30s
```

### Exception Handling

Break on exceptions:

```bash
# Break on all exceptions
npx debug-run ./dist/index.js \
  -a node \
  --break-on-exception all \
  --pretty \
  -t 30s

# Break on uncaught exceptions only
npx debug-run ./dist/index.js \
  -a node \
  --break-on-exception uncaught \
  --pretty \
  -t 30s
```

## Adapter Aliases

Multiple aliases work for the Node.js adapter:

```bash
# These are all equivalent
npx debug-run ./dist/index.js -a node -b "src/index.ts:10" --pretty
npx debug-run ./dist/index.js -a nodejs -b "src/index.ts:10" --pretty
npx debug-run ./dist/index.js -a js -b "src/index.ts:10" --pretty
npx debug-run ./dist/index.js -a javascript -b "src/index.ts:10" --pretty
```

## Sample Application

A sample TypeScript application is included for testing:

```bash
# Build the sample
cd samples/typescript && npm install && npm run build && cd ../..

# Debug
npx debug-run samples/typescript/dist/index.js \
  -a node \
  -b "samples/typescript/src/index.ts:160" \
  --pretty \
  -t 30s
```

### With Expression Evaluation

```bash
npx debug-run samples/typescript/dist/index.js \
  -a node \
  -b "samples/typescript/src/index.ts:177" \
  -e "subtotal" \
  -e "tax" \
  -e "discount" \
  -e "order.orderId" \
  --pretty \
  -t 30s
```

### Good Breakpoint Locations (Sample App)

| Line | Location | Description |
|------|----------|-------------|
| 160 | `processOrder` | Start of order processing method |
| 177 | `processOrder` | After calculating subtotal, tax, discount |
| 168 | `processOrder` | Inside inventory check loop |
| 304 | `main` | Before processing first order |

## Source Maps

debug-run automatically uses source maps to map breakpoints from TypeScript source files to compiled JavaScript.

### Requirements

1. **Enable source maps in tsconfig.json**:
```json
{
  "compilerOptions": {
    "sourceMap": true,
    "outDir": "./dist"
  }
}
```

2. **Set breakpoints using TypeScript paths**:
```bash
# Correct: Use .ts source file
-b "src/services/OrderService.ts:42"

# Incorrect: Don't use .js compiled file
-b "dist/services/OrderService.js:42"
```

### How Source Maps Work

When you compile TypeScript:
- `src/index.ts` → `dist/index.js` + `dist/index.js.map`

debug-run tells js-debug to:
1. Run `dist/index.js`
2. Use source maps to show original TypeScript
3. Set breakpoints in TypeScript that map to correct JS locations

## Trace Mode

Follow execution flow after hitting a breakpoint:

```bash
# Basic trace
npx debug-run ./dist/index.js \
  -a node \
  -b "src/index.ts:42" \
  --trace \
  --pretty

# Trace into function calls
npx debug-run ./dist/index.js \
  -a node \
  -b "src/index.ts:42" \
  --trace \
  --trace-into \
  --trace-limit 50 \
  --pretty

# Trace with variable diffing
npx debug-run ./dist/index.js \
  -a node \
  -b "src/index.ts:42" \
  --trace \
  --diff-vars \
  --pretty
```

## JavaScript-Specific Notes

### Provisional Breakpoints

js-debug uses "provisional breakpoints" that start as unverified:
```json
{
  "type": "breakpoint_set",
  "verified": false,
  "message": "breakpoint.provisionalBreakpoint"
}
```

This is normal - breakpoints verify when the code is loaded.

### Internal Code

By default, debug-run configures js-debug to skip internal Node.js code:
```json
"skipFiles": ["<node_internals>/**"]
```

Stack traces may show `[Internal Code]` for Node.js internals.

### Expression Syntax

Use JavaScript syntax for expressions:

```bash
# JavaScript expressions
-e "items.length"
-e "order.items[0].price"
-e "order.items.reduce((sum, item) => sum + item.quantity, 0)"
-e "customer?.loyaltyTier ?? 'none'"
```

### this Context

In class methods, `this` is automatically captured in locals:

```json
{
  "locals": {
    "this": {
      "type": "OrderService",
      "value": {
        "config": {...},
        "inventory": {...}
      }
    }
  }
}
```

## Debugging Plain JavaScript

For plain JavaScript (no TypeScript):

```bash
npx debug-run ./index.js \
  -a node \
  -b "index.js:25" \
  --pretty \
  -t 30s
```

No build step needed - just point to the .js file directly.

## Debugging ESM vs CommonJS

debug-run works with both module systems:

```bash
# ESM (type: "module" in package.json)
npx debug-run ./dist/index.js -a node -b "src/index.ts:10" --pretty

# CommonJS
npx debug-run ./dist/index.js -a node -b "src/index.ts:10" --pretty
```

The adapter auto-detects the module system.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Adapter not installed" | Run `npx debug-run install-adapter node` or install VS Code |
| Breakpoint not hitting | Check source maps exist (`.js.map` files) |
| Wrong line numbers | Rebuild TypeScript (`npm run build`) |
| "Cannot find module" | Run `npm install` first |
| Provisional breakpoint never verifies | Check file path matches source exactly |

### Debug Adapter Communication

Enable verbose DAP logging:

```bash
DEBUG_DAP=1 npx debug-run ./dist/index.js -a node -b "src/index.ts:10" --pretty
```

### Verify Source Maps

Check that source maps are generated:
```bash
ls dist/*.js.map  # Should list .map files
```

Check tsconfig.json has `"sourceMap": true`.

## Common Patterns

### Debug with Arguments

```bash
npx debug-run ./dist/cli.js -- --input data.json --verbose \
  -a node \
  -b "src/cli.ts:15" \
  --pretty
```

Arguments after `--` are passed to your script.

### Debug Tests (Jest/Mocha)

For test debugging, run the test file directly:

```bash
# Jest (compile first if TypeScript)
npx debug-run ./node_modules/jest/bin/jest.js -- --runInBand tests/order.test.ts \
  -a node \
  -b "tests/order.test.ts:25" \
  --pretty \
  -t 60s

# Mocha
npx debug-run ./node_modules/mocha/bin/mocha.js -- dist/tests/**/*.js \
  -a node \
  -b "src/tests/order.test.ts:25" \
  --pretty \
  -t 60s
```

### Debug Express/Fastify Server

```bash
npx debug-run ./dist/server.js \
  -a node \
  -b "src/routes/orders.ts:42" \
  --pretty \
  -t 120s

# In another terminal, trigger the endpoint:
# curl http://localhost:3000/orders
```
