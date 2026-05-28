# Build & Deployment Reference

Compilation, optimization, and deployment workflows.

## Build Commands

```bash
# Single build
npx rbxtsc

# Watch mode
npx rbxtsc -w

# Verbose output
npx rbxtsc -w --verbose

# Type check only
npx rbxtsc --noEmit

# Production build
npx rbxtsc --production
```

## Compiler Options

### Watch Mode
Automatically rebuilds on file changes. Best for development.

### Verbose Mode
Shows detailed compilation steps. Good for debugging.

### Production Mode
Optimizes output Luau code.

## Rojo Integration

```bash
# Terminal 1: Compiler
npx rbxtsc -w

# Terminal 2: Rojo
rojo serve default.project.json
```

In Roblox Studio: Plugins → Rojo → Connect

## Publishing

1. Build production: `npx rbxtsc --production`
2. Publish place file in Studio
3. Test in live environment
4. Monitor for errors

## Troubleshooting

**Compilation errors**: Check tsconfig.json syntax
**Missing types**: Install @rbxts/types
**Rojo not syncing**: Verify outDir matches project paths
**Performance issues**: Use production mode
