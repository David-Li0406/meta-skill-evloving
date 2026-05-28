# Flamework Core Reference

Comprehensive documentation for Flamework's core features: services, controllers, dependency injection, and lifecycle events.

## Singletons: Services and Controllers

Flamework uses decorators to create singletons - classes that are automatically instantiated once by the framework.

### @Service() - Server-side Singletons

```typescript
import { Service, OnStart } from "@flamework/core";

@Service()
export class MyService implements OnStart {
    onStart() {
        print("Service started!");
    }
}

// With load order configuration
@Service({ loadOrder: 0 })  // Lower = loads sooner, default is 1
export class EarlyService implements OnStart {
    onStart() {
        print("Loads before default services");
    }
}
```

### @Controller() - Client-side Singletons

```typescript
import { Controller, OnStart } from "@flamework/core";

@Controller()
export class MyController implements OnStart {
    onStart() {
        print("Controller started on client!");
    }
}
```

**Key Points:**
- Services run only on server
- Controllers run only on client
- Only one instance per class
- Load order automatically determined by dependencies
- Manual load order via `loadOrder` option (lower = earlier)

## Dependency Injection

Flamework provides two ways to get singleton references:

### Constructor Injection (Preferred)

```typescript
import { Service } from "@flamework/core";
import { DataService } from "./data-service";
import { LogService } from "./log-service";

@Service()
export class PlayerService {
    constructor(
        private dataService: DataService,
        private logService: LogService
    ) {}
    
    method() {
        this.dataService.load();
        this.logService.info("Player data loaded");
    }
}
```

**Benefits:**
- Automatic load order resolution
- Easy to test and stub
- Clear dependencies
- Type-safe

### Dependency Macro (Use Sparingly)

```typescript
import { Dependency } from "@flamework/core";
import { DataService } from "./data-service";

// Can be called from anywhere after Flamework.ignite()
const dataService = Dependency<DataService>();
dataService.load();
```

**When to use:**
- Utility functions that need singleton access
- Roact/React components
- Cases where constructor DI is not possible

**Warnings:**
- Cannot be called before `Flamework.ignite()`
- Obscures dependency graph
- Harder to test
- May cause circular dependency issues

## Lifecycle Events

Lifecycle events are optional interfaces that singletons and components can implement.

### OnStart (Recommended)

Called after all OnInit events complete. All OnStart events fire simultaneously (non-blocking).

```typescript
import { Service, OnStart } from "@flamework/core";

@Service()
export class MyService implements OnStart {
    onStart() {
        print("Service ready!");
        // Safe to use other services here
        // Yielding/promises won't block other services
    }
}
```

**Use OnStart for:**
- Service initialization
- Setting up listeners
- Starting main logic
- Most initialization tasks

### OnInit (Rare Cases Only)

Called sequentially before OnStart. Each OnInit must complete before the next one runs.

```typescript
import { Service, OnInit } from "@flamework/core";

@Service()
export class CriticalService implements OnInit {
    onInit() {
        // Blocks other OnInit events until complete
        print("Critical initialization");
        return Promise.resolve(); // Can return promise
    }
}
```

**When to use OnInit:**
- Critical initialization that must complete before anything else
- Rare cases requiring strict ordering

**Avoid:**
- Yielding (delays everything)
- Using dependencies (may not be ready)
- General initialization (use OnStart instead)

### OnTick (RunService.Heartbeat)

Runs after physics, every frame.

```typescript
import { Service, OnTick } from "@flamework/core";

@Service()
export class PhysicsService implements OnTick {
    onTick(dt: number) {
        // Runs every frame after physics
        // Good for: responding to physics changes
    }
}
```

### OnPhysics (RunService.Stepped)

Runs before physics, every frame.

```typescript
import { Service, OnPhysics } from "@flamework/core";

@Service()
export class MovementService implements OnPhysics {
    onPhysics(dt: number, time: number) {
        // Runs before physics
        // Good for: manipulating physics state
    }
}
```

### OnRender (RunService.RenderStepped) - Client Only

Runs before rendering, every frame. Client-side only.

```typescript
import { Controller, OnRender } from "@flamework/core";

@Controller()
export class CameraController implements OnRender {
    onRender(dt: number) {
        // Runs before rendering (client only)
        // Good for: camera updates, visual effects
    }
}
```

## Runtime Initialization

### Basic Setup

```typescript
// runtime.server.ts
import { Flamework } from "@flamework/core";

// Preload all singletons in specified directories
Flamework.addPaths("src/server/services/");
Flamework.addPaths("src/server/components/");

// Start the framework
Flamework.ignite();
```

```typescript
// runtime.client.ts
import { Flamework } from "@flamework/core";

Flamework.addPaths("src/client/controllers/");
Flamework.addPaths("src/client/components/");

Flamework.ignite();
```

### Path Options

```typescript
// Relative to project root
Flamework.addPaths("src/server/services/");

// Relative to current file (with ./)
Flamework.addPaths("./services/");

// Glob patterns (directories only, use trailing /)
Flamework.addPaths("src/*/server/");  // Wrong - matches files
Flamework.addPaths("src/*/server/");  // Correct - matches directories

// Using addPathsGlob for file patterns
Flamework.addPathsGlob("src/**/*.service.ts");
```

## Utility Macros

### Flamework.id<T>()

Get the unique identifier for a type.

```typescript
import { Flamework } from "@flamework/core";

const serviceId = Flamework.id<MyService>();
print(serviceId); // "server/services/myService@MyService"
```

### Flamework.implements<T>(obj)

Check if an object implements an interface at runtime.

```typescript
import { Flamework } from "@flamework/core";

interface OnInteract {
    interact(): void;
}

if (Flamework.implements<OnInteract>(obj)) {
    obj.interact();
}
```

### Flamework.createGuard<T>()

Create a type guard for runtime validation.

```typescript
import { Flamework } from "@flamework/core";

interface PlayerData {
    name: string;
    level: number;
}

const guard = Flamework.createGuard<PlayerData>();

if (guard(data)) {
    // data is PlayerData
    print(data.name, data.level);
}
```

### Flamework.hash(str, context)

Hash a string literal (deterministic across compilation).

```typescript
import { Flamework } from "@flamework/core";

const hash = Flamework.hash("my-string", "context");
// Always same hash within same compilation
```

## Load Order

Flamework automatically determines load order based on constructor dependencies. Manual specification rarely needed.

```typescript
// Automatic - DataService loads before PlayerService
@Service()
export class PlayerService {
    constructor(private dataService: DataService) {}
}

// Manual override if needed
@Service({ loadOrder: 0 })
export class EarlyService {}

@Service({ loadOrder: 1 })  // Default
export class NormalService {}

@Service({ loadOrder: 2 })
export class LateService {}
```

**Load order rules:**
- Lower number = loads earlier
- Default is 1
- Dependencies override manual load order
- Topologically sorted by dependency graph

## Common Patterns

### Service with Multiple Dependencies

```typescript
@Service()
export class GameService implements OnStart {
    constructor(
        private playerService: PlayerService,
        private dataService: DataService,
        private logService: LogService,
        private components: Components
    ) {}
    
    onStart() {
        // All dependencies ready
        this.initializeGame();
    }
    
    private initializeGame() {
        this.logService.info("Game initializing");
        this.playerService.setup();
    }
}
```

### Service with Lifecycle Events

```typescript
@Service()
export class TickService implements OnStart, OnTick {
    private active = false;
    
    onStart() {
        this.active = true;
    }
    
    onTick(dt: number) {
        if (!this.active) return;
        // Run every frame
    }
}
```

### Utility Function with Dependency

```typescript
import { Dependency } from "@flamework/core";
import { LogService } from "./log-service";

export function logError(message: string) {
    const log = Dependency<LogService>();
    log.error(message);
}
```

## Metadata Requirements

For dependency injection and lifecycle events to work, specific metadata must be generated.

### Required for Lifecycle Events

```typescript
/**
 * @metadata flamework:implements
 */
interface OnStart {
    onStart(): void;
}
```

### Required for Dependency Injection

```typescript
/**
 * @metadata flamework:parameters
 */
@Service()
export class MyService {
    constructor(other: OtherService) {}
}
```

**Note:** Flamework decorators automatically include necessary metadata. Manual metadata only needed for custom decorators or interfaces.

## Troubleshooting

**"Dependency called before ignition"**
- Move `Dependency<T>()` call after `Flamework.ignite()`
- Or use constructor DI instead

**Circular dependencies**
- Refactor to break the cycle
- Use `Dependency<T>()` macro as last resort (not recommended)

**Service not loading**
- Ensure path is included in `Flamework.addPaths()`
- Check that decorator is applied correctly
- Verify no TypeScript errors

**Load order issues**
- Let automatic resolution handle it
- Check dependency graph
- Use `loadOrder` only if automatic resolution insufficient
