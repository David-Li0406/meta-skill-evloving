# Flamework Macros Reference

Comprehensive guide to Flamework's utility macros and compile-time features.

## Overview

Flamework macros are compile-time functions that generate code or metadata. They provide powerful abstractions without runtime overhead.

## Flamework.addPaths()

Preload modules from specified directories.

### Basic Usage

```typescript
import { Flamework } from "@flamework/core";

// Single path
Flamework.addPaths("src/server/services/");

// Multiple paths
Flamework.addPaths(
    "src/server/services/",
    "src/server/components/",
    "src/shared/utilities/"
);
```

### Relative Paths

```typescript
// Relative to current file (must start with ./)
Flamework.addPaths("./services/");
Flamework.addPaths("../shared/");

// Cannot use .. without ./
Flamework.addPaths("../services/");  // ❌ Error
```

### Glob Patterns

```typescript
// Match directories (must end with /)
Flamework.addPaths("src/*/services/");      // Matches src/server/services/, src/client/services/
Flamework.addPaths("src/**/components/");   // Recursive match

// Wrong - matches files
Flamework.addPaths("src/*/services");       // ❌

// Using addPathsGlob for files
Flamework.addPathsGlob("src/**/*.service.ts");
```

**Important:**
- Globs only work with absolute paths (relative paths disabled)
- Directory globs require trailing `/`
- Use `addPathsGlob` for file patterns

### When to Use

Call before `Flamework.ignite()` to preload:
- Services and Controllers
- Components
- Any code with Flamework decorators

## Flamework.id<T>()

Get the unique identifier for a type.

```typescript
import { Flamework } from "@flamework/core";
import { MyService } from "./my-service";

// Get ID for a class
const serviceId = Flamework.id<MyService>();
print(serviceId);  // "server/services/myService@MyService"

// IDs are deterministic within compilation
const id1 = Flamework.id<MyService>();
const id2 = Flamework.id<MyService>();
print(id1 === id2);  // true
```

### ID Format

IDs vary based on `idGenerationMode` in tsconfig.json:

**full** (default):
```typescript
Flamework.id<MyService>()
// Game: "server/services/myService@MyService"
// Package: "@rbxts/my-package:server/services/myService@MyService"
```

**obfuscated**:
```typescript
Flamework.id<MyService>()
// "aZx3k"
```

**short**:
```typescript
Flamework.id<MyService>()
// "myService@MyService{aZx3k}"
```

**tiny**:
```typescript
Flamework.id<MyService>()
// "MyService{aZx3k}"
```

### Use Cases

- Debugging and logging
- Manual singleton resolution
- Metadata lookups
- Custom dependency systems

## Flamework.implements<T>(obj)

Runtime type checking for interfaces.

```typescript
import { Flamework } from "@flamework/core";

interface OnInteract {
    interact(player: Player): void;
}

function tryInteract(obj: unknown, player: Player) {
    if (Flamework.implements<OnInteract>(obj)) {
        // obj is now typed as OnInteract
        obj.interact(player);
    }
}
```

### With Classes

```typescript
@Component({ tag: "Button" })
export class ButtonComponent extends BaseComponent implements OnInteract {
    interact(player: Player) {
        print("Button pressed by", player.Name);
    }
}

// Check if component implements interface
const component = components.getComponent(instance);
if (Flamework.implements<OnInteract>(component)) {
    component.interact(player);
}
```

### Limitations

- Only works with Flamework classes (decorated with @Service, @Controller, @Component)
- Requires `flamework:implements` metadata
- Runtime check based on metadata, not actual implementation

## Flamework.createGuard<T>()

Generate runtime type guard for any TypeScript type.

```typescript
import { Flamework } from "@flamework/core";

interface PlayerData {
    name: string;
    level: number;
    inventory: string[];
}

// Create guard
const isPlayerData = Flamework.createGuard<PlayerData>();

// Use guard
function processData(data: unknown) {
    if (isPlayerData(data)) {
        // data is PlayerData
        print(data.name, data.level);
        for (const item of data.inventory) {
            print(item);
        }
    } else {
        warn("Invalid player data");
    }
}
```

### Supported Types

Guards support most TypeScript types:

```typescript
// Primitives
const isString = Flamework.createGuard<string>();
const isNumber = Flamework.createGuard<number>();
const isBoolean = Flamework.createGuard<boolean>();

// Arrays
const isStringArray = Flamework.createGuard<string[]>();
const isNumberMatrix = Flamework.createGuard<number[][]>();

// Objects
const isUser = Flamework.createGuard<{ name: string; age: number }>();

// Unions
const isStatus = Flamework.createGuard<"idle" | "running" | "complete">();
const isMixed = Flamework.createGuard<string | number>();

// Optionals
const isOptional = Flamework.createGuard<string | undefined>();
const isNullable = Flamework.createGuard<string?>();

// Roblox types
const isVector = Flamework.createGuard<Vector3>();
const isCFrame = Flamework.createGuard<CFrame>();
const isInstance = Flamework.createGuard<Instance>();
const isBuffer = Flamework.createGuard<buffer>();

// Complex nested types
interface Config {
    settings: {
        audio: {
            volume: number;
            enabled: boolean;
        };
        graphics: {
            quality: "low" | "medium" | "high";
            fps: number;
        };
    };
    players: Array<{ id: string; name: string }>;
}
const isConfig = Flamework.createGuard<Config>();
```

### Type Resolution

Guards resolve types based on TypeScript's type system:

```typescript
// Generics resolve to constraints
type MyGeneric<T extends string> = { value: T };
const guard = Flamework.createGuard<MyGeneric<"test">>();
// Resolves to { value: string }

// Conditionals resolve to union of both branches
type Conditional<T> = T extends string ? string : number;
const conditionalGuard = Flamework.createGuard<Conditional<unknown>>();
// Resolves to string | number
```

### Networking Integration

Guards are automatically generated for networking:

```typescript
import { Networking } from "@flamework/networking";

interface Events {
    sendData(data: { x: number; y: number }): void;
}

// Guard automatically generated and applied
const Events = Networking.createEvent<Events, {}>();

// Invalid data rejected automatically
Events.sendData({ x: "not a number", y: 0 });  // ❌ Rejected
```

## Flamework.hash(str, context)

Generate deterministic hash for string literals.

```typescript
import { Flamework } from "@flamework/core";

// Basic hash
const hash1 = Flamework.hash("my-identifier");
print(hash1);  // "x7Ka9p" (example)

// With context (separate hash spaces)
const remoteHash = Flamework.hash("getData", "remotes");
const eventHash = Flamework.hash("getData", "events");
print(remoteHash === eventHash);  // false

// Same string + context = same hash
const a = Flamework.hash("test", "ctx");
const b = Flamework.hash("test", "ctx");
print(a === b);  // true
```

### Hash Properties

- **Deterministic** - Same input = same output within compilation
- **Regenerated** - Hashes change when compilation restarts
- **Context-separated** - Different contexts yield different hashes
- **Collision-resistant** - Different inputs yield different hashes

### Use Cases

```typescript
// Unique identifiers
const uniqueId = Flamework.hash("my-system");

// Obfuscated networking
const eventName = Flamework.hash("PlayerJoined", "remotes");

// Cache keys
const cacheKey = Flamework.hash("playerData:" + userId);

// Internal namespacing
const namespace = Flamework.hash("combat-system", "internal");
```

### Default Context

```typescript
// Default context is "@"
Flamework.hash("test");         // Same as Flamework.hash("test", "@")
Flamework.hash("test", "@");    // Explicit default context
```

## Dependency<T>()

Retrieve singleton instance outside constructor.

```typescript
import { Dependency } from "@flamework/core";
import { MyService } from "./my-service";

// Get singleton reference
const myService = Dependency<MyService>();
myService.doSomething();
```

### Restrictions

⚠️ **Cannot be called before `Flamework.ignite()`**

```typescript
// ❌ Error - called before ignition
const service = Dependency<MyService>();
Flamework.ignite();

// ✅ Correct
Flamework.ignite();
const service = Dependency<MyService>();

// ✅ Also correct - called after ignition in function
Flamework.ignite();
function setup() {
    const service = Dependency<MyService>();
}
setup();
```

### When to Use

**Prefer constructor injection:**
```typescript
@Service()
export class MyService {
    constructor(private otherService: OtherService) {}
}
```

**Use Dependency<T>() for:**
- Utility functions
- Roact/React components  
- External libraries
- Cases where constructor DI not possible

```typescript
// Utility function example
export function logError(message: string) {
    const logger = Dependency<LogService>();
    logger.error(message);
}

// React component example
function MyComponent() {
    const dataService = Dependency<DataService>();
    const [data, setData] = useState(dataService.getData());
    return <div>{data}</div>;
}
```

## User Macros

Flamework supports custom compile-time macros via the modding API.

### Creating a Macro

```typescript
import { Modding } from "@flamework/core";

// Type-only macro (metadata generation)
type MyMacro<T> = Modding.Generic<T, "id">;

// Usage
type ServiceId = MyMacro<MyService>;  // Resolves to string at compile time
```

### Modding.Generic<T, Kind>

Generate metadata for type parameter.

```typescript
// Get ID
type Id = Modding.Generic<MyService, "id">;  // string

// Get type guard
type Guard = Modding.Generic<PlayerData, "guard">;  // t.check<PlayerData>
```

### Modding.Caller

Get metadata about the calling location.

```typescript
type CallerId = Modding.Caller<"id">;  // ID of calling class

// Use in decorator
function LogCaller() {
    const callerId = Modding.Caller<"id">();
    print("Called from:", callerId);
}
```

## Compile-Time vs Runtime

| Macro | Compile-Time | Runtime |
|-------|-------------|---------|
| `Flamework.addPaths()` | ✅ Preloads modules | No direct runtime cost |
| `Flamework.id<T>()` | ✅ Generates string | Returns string literal |
| `Flamework.implements<T>()` | ✅ Generates check | Runtime metadata check |
| `Flamework.createGuard<T>()` | ✅ Generates guard function | Returns guard function |
| `Flamework.hash()` | ✅ Generates hash | Returns string literal |
| `Dependency<T>()` | ✅ Generates resolution code | Runtime singleton lookup |

## Best Practices

1. **Use addPaths before ignite** - Ensure all code is preloaded
2. **Prefer constructor DI over Dependency<T>()** - Better testing and clarity
3. **Use createGuard for validation** - Runtime safety for user input
4. **Leverage type guards** - Let Flamework handle validation automatically
5. **Hash for obfuscation** - Use in production for security
6. **Context-separate hashes** - Avoid collisions between different systems

## Performance Considerations

### Compile-Time (No Runtime Cost)
- `Flamework.addPaths()` - Resolved during compilation
- `Flamework.id<T>()` - Inlined as string literal
- `Flamework.hash()` - Inlined as string literal
- Type resolution for guards - Generated once

### Runtime (Minimal Cost)
- `Flamework.createGuard<T>()` - Guard function created once, cached
- `Flamework.implements<T>()` - Metadata lookup (fast)
- `Dependency<T>()` - Singleton resolution (fast, cached)

### Optimization Tips

```typescript
// ✅ Create guards once, reuse
const isPlayerData = Flamework.createGuard<PlayerData>();
for (const data of dataArray) {
    if (isPlayerData(data)) {
        // ...
    }
}

// ❌ Don't recreate guards in loops
for (const data of dataArray) {
    const isPlayerData = Flamework.createGuard<PlayerData>();  // Wasteful
    if (isPlayerData(data)) {
        // ...
    }
}
```

## Troubleshooting

**"Macro not recognized"**
- Ensure Flamework transformer is in tsconfig.json
- Check import is from @flamework/core
- Verify no TypeScript errors

**"Called before ignition" warning**
- Move `Dependency<T>()` call after `Flamework.ignite()`
- Or use constructor injection instead

**Type guard not working**
- Check supported types (some advanced types may not work)
- Verify type is fully resolved (no unresolved generics)
- Test with simpler types first

**addPaths not loading modules**
- Check path is correct and ends with `/` for directories
- Verify modules have Flamework decorators
- Check for TypeScript compilation errors
