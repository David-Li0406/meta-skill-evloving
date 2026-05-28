# Popular @rbxts Packages Reference

Essential packages for roblox-ts development.

## Type Validation

**@rbxts/t** - Runtime type checking
```bash
npm install @rbxts/t
```

```typescript
import { t } from "@rbxts/t";

const isPlayer = t.interface({
    name: t.string,
    health: t.number
});

if (isPlayer(data)) {
    print(data.name, data.health);
}
```

## Networking

**@rbxts/remo** - Type-safe remotes
```bash
npm install @rbxts/remo
```

**@rbxts/net** - Alternative networking
```bash
npm install @rbxts/net
```

## UI Frameworks

**@rbxts/roact** - React for Roblox
```bash
npm install @rbxts/roact
```

**@rbxts/roact-hooked** - React Hooks
```bash
npm install @rbxts/roact-hooked
```

## Utilities

**@rbxts/object-utils** - Object manipulation
**@rbxts/string-utils** - String helpers
**@rbxts/services** - Roblox services (essential)

## State Management

**@rbxts/reflex** - Redux-like state management
**@rbxts/rodux** - State containers
