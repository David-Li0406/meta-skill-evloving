---
name: dojo-client
description: Use this skill to integrate Dojo with various game clients and frontends, generating typed bindings and connection code for platforms like JavaScript, Unity, and Unreal.
---

# Dojo Client Integration

Connect your game client or frontend to your deployed Dojo world across multiple platforms.

## When to Use This Skill

- "Set up JavaScript SDK for my Dojo game"
- "Integrate Dojo with Unity"
- "Generate TypeScript bindings"
- "Connect Unreal Engine to my world"
- "Integrate React app with Dojo"

## What This Skill Does

Handles client integration for:
- JavaScript/TypeScript SDK
- Unity (C#)
- Unreal Engine (C++)
- Rust client
- Godot, Bevy, and other platforms
- Typed binding generation
- Connection code
- Query/subscription patterns

## Quick Start

**JavaScript:**
```bash
npm install @dojoengine/sdk
# or
pnpm add @dojoengine/sdk
```

**Unity:**
```bash
"Integrate my Dojo world with Unity"
```

**Unreal:**
```bash
"Connect Unreal Engine to my deployed world"
```

## Supported Platforms

| Platform | Language | Package |
|----------|----------|---------|
| JavaScript/TypeScript | JS/TS | `@dojoengine/sdk` |
| Unity | C# | `dojo.unity` |
| Unreal Engine | C++ | `dojo.unreal` |
| Rust | Rust | `dojo::client` |
| Godot | GDScript | `dojo.godot` |
| Bevy | Rust | `dojo.bevy` |

## JavaScript/TypeScript Integration

### Installation

```bash
npm install @dojoengine/core @dojoengine/sdk @dojoengine/torii-client
# For React integration
pnpm add @dojoengine/create-burner @dojoengine/utils
```

### Generate Bindings

```bash
sozo build --typescript-output ./src/generated
```

### Basic Setup

```typescript
import { DojoProvider } from "@dojoengine/sdk";
import manifest from "./manifest.json";

// Create provider
const provider = new DojoProvider(
    manifest,
    "http://localhost:5050"  // Katana RPC
);

// Read a model
const position = await provider.getEntity("Position", playerId);
console.log(position.x, position.y);

// Execute a system
await provider.execute("actions", "spawn", []);
```

### Query Patterns

```typescript
// Get single entity
const player = await provider.getEntity("Player", address);

// Get multiple entities
const positions = await provider.getEntities("Position");

// Query with filters
const positions = await provider.query("Position", {
    where: { x: { $gt: 10 } }
});
```

### Subscriptions

```typescript
// Subscribe to entity changes
const unsubscribe = provider.subscribe(
    "Position",
    playerId,
    (position) => {
        console.log("Position updated:", position);
    }
);
```