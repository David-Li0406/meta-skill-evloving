# Flamework Modding Reference

Complete guide to extending Flamework with custom decorators, metadata, and the modding API.

## Overview

Flamework's modding API allows you to:
- Create custom decorators
- Generate compile-time metadata
- Hook into Flamework's lifecycle
- Build framework extensions

## Creating Custom Decorators

### Meta Decorators (Metadata Only)

Meta decorators generate metadata without runtime code.

```typescript
import { Modding } from "@flamework/core";

// Create a meta decorator for classes
export const Priority = Modding.createMetaDecorator<[number]>("Class");

// Usage
@Priority(10)
@Service()
export class HighPriorityService {}

// Create meta decorator for methods
export const Validate = Modding.createMetaDecorator<[string]>("Method");

// Usage
@Service()
export class MyService {
    @Validate("input")
    processData(data: string) {}
}

// Create meta decorator for properties
export const Required = Modding.createMetaDecorator<[]>("Property");

// Usage
@Service()
export class ConfigService {
    @Required()
    apiKey!: string;
}
```

### Regular Decorators (With Runtime Logic)

Regular decorators run code when applied.

```typescript
import { Modding } from "@flamework/core";

// Class decorator
export const LogCreation = Modding.createDecorator<[string]>("Class", (descriptor, [name]) => {
    print("Created class:", descriptor.object);
    print("With name:", name);
});

// Usage
@LogCreation("MyService")
@Service()
export class MyService {}

// Method decorator
export const Benchmark = Modding.createDecorator<[]>("Method", (descriptor, []) => {
    const originalMethod = descriptor.object[descriptor.property];
    
    descriptor.object[descriptor.property] = (...args: unknown[]) => {
        const start = os.clock();
        const result = originalMethod(...args);
        const elapsed = os.clock() - start;
        print(`${tostring(descriptor.object)}.${descriptor.property}() took ${elapsed}s`);
        return result;
    };
});

// Usage
@Service()
export class MyService {
    @Benchmark()
    expensiveOperation() {
        // ...
    }
}

// Property decorator
export const ReadOnly = Modding.createDecorator<[]>("Property", (descriptor, []) => {
    print("Making property read-only:", descriptor.property);
    // Could add runtime protection here
});
```

### Decorator Parameters

Decorators can accept parameters:

```typescript
// Single parameter
export const SetPriority = Modding.createMetaDecorator<[number]>("Class");

// Multiple parameters
export const Configure = Modding.createMetaDecorator<[string, boolean, number]>("Class");

@Configure("mode", true, 100)
export class MyService {}

// Optional parameters (use union with undefined)
export const OptionalConfig = Modding.createMetaDecorator<[string, number?]>("Class");

@OptionalConfig("mode")        // Second param omitted
@OptionalConfig("mode", 100)   // Both params provided
export class MyService {}
```

## Decorator Reflection

### Getting Decorators

```typescript
import { Modding, Service, OnStart } from "@flamework/core";

// Define decorator
export const Priority = Modding.createMetaDecorator<[number]>("Class");

// Use decorator
@Priority(10)
@Service()
export class MyService {}

// Reflect on decorators
@Service()
export class DecoratorService implements OnStart {
    onStart() {
        // Get all classes using Priority decorator
        const decorated = Modding.getDecorators<typeof Priority>();
        
        for (const { object, arguments: args } of decorated) {
            const [priority] = args;
            print(object, "has priority:", priority);
        }
    }
}
```

### Getting Single Decorator

```typescript
// Get decorator from specific object
const decorator = Modding.getDecorator<typeof Priority>(MyService);

if (decorator) {
    const [priority] = decorator.arguments;
    print("Priority:", priority);
}
```

### Property Decorators

```typescript
// Define property decorator
export const Validate = Modding.createMetaDecorator<[string]>("Property");

@Service()
export class DataService {
    @Validate("email")
    email!: string;
    
    @Validate("url")
    website!: string;
}

// Reflect on property decorators
@Service()
export class ValidationService implements OnStart {
    onStart() {
        // Get all properties with Validate decorator
        const properties = Modding.getPropertyDecorators<typeof Validate>(DataService);
        
        for (const [propertyName, decorator] of properties) {
            const [validationType] = decorator.arguments;
            print(`Property ${propertyName} validates as:`, validationType);
        }
    }
}
```

## Decorator Listeners

Listen for when decorators are applied.

```typescript
import { Modding, Service, OnStart } from "@flamework/core";

export const Register = Modding.createMetaDecorator<[string]>("Class");

@Service()
export class RegistryService implements OnStart {
    private registered = new Map<string, object>();
    
    onStart() {
        // Listen for new @Register decorators
        Modding.onListenerAdded<typeof Register>((object) => {
            const decorator = Modding.getDecorator<typeof Register>(object);
            if (decorator) {
                const [name] = decorator.arguments;
                this.registered.set(name, object);
                print("Registered:", name);
            }
        });
        
        // Process existing decorators
        const existing = Modding.getDecorators<typeof Register>();
        for (const { object, arguments: args } of existing) {
            const [name] = args;
            this.registered.set(name, object);
        }
    }
    
    get(name: string) {
        return this.registered.get(name);
    }
}
```

## Metadata System

### Requesting Metadata

Use `@metadata` JSDoc tag to request metadata generation.

```typescript
/**
 * @metadata flamework:parameters
 */
@Service()
export class MyService {
    constructor(param1: string, param2: number) {}
}
```

### Available Metadata

#### Class Metadata

```typescript
/**
 * Generate unique identifier
 * @metadata identifier
 */

/**
 * Generate list of implemented interfaces
 * @metadata flamework:implements
 */

/**
 * Generate parameter type IDs
 * @metadata flamework:parameters
 */

/**
 * Generate parameter names
 * @metadata flamework:parameter_names
 */

/**
 * Generate parameter type guards
 * @metadata flamework:parameter_guards
 */
```

#### Method/Property Metadata

```typescript
/**
 * Generate return type ID
 * @metadata flamework:return_type
 */

/**
 * Generate return type guard
 * @metadata flamework:return_guard
 */

/**
 * Generate parameter type IDs
 * @metadata flamework:parameters
 */

/**
 * Generate parameter names
 * @metadata flamework:parameter_names
 */

/**
 * Generate parameter type guards
 * @metadata flamework:parameter_guards
 */
```

### Link Metadata

Reference types in metadata.

```typescript
type ConstructorConstraint = new () => defined;

/**
 * Constrain to specific constructor signature
 * @metadata {@link ConstructorConstraint constraint}
 */
@MyDecorator()
export class MyService {
    constructor() {}  // Must match constraint
}
```

### Metadata on Decorators

```typescript
/**
 * Request metadata for users of this decorator
 * @metadata flamework:parameters
 */
export const Injectable = Modding.createMetaDecorator<[]>("Class");

// Classes using @Injectable will have parameters metadata generated
@Injectable()
export class MyService {
    constructor(dependency: OtherService) {}
    // parameters metadata automatically generated
}
```

### Metadata on Interfaces

```typescript
/**
 * Request metadata for implementors
 * @metadata flamework:implements
 */
interface OnStartup {
    onStartup(): void;
}

// Classes implementing OnStartup will have implements metadata
@Service()
export class MyService implements OnStartup {
    onStartup() {}
}
```

## User Macros

Create compile-time macros that generate code or metadata.

### Modding.Generic<T, Kind>

Generate metadata for type parameter.

```typescript
import { Modding } from "@flamework/core";

// Get type ID
type ServiceId = Modding.Generic<MyService, "id">;  // string

// Get type guard
type DataGuard = Modding.Generic<PlayerData, "guard">;  // t.check<PlayerData>

// Use in function
function validateData<T>(data: unknown): data is T {
    const guard = Modding.Generic<T, "guard">();
    return guard(data);
}
```

### Modding.Caller<Kind>

Get metadata about the caller.

```typescript
import { Modding } from "@flamework/core";

// Get caller ID
function logCaller() {
    const callerId = Modding.Caller<"id">();
    print("Called from:", callerId);
}

@Service()
export class MyService implements OnStart {
    onStart() {
        logCaller();  // Prints: "Called from: server/services/myService@MyService"
    }
}
```

### Modding.Many

Generate metadata for multiple types.

```typescript
import { Modding } from "@flamework/core";

// Old API (still works)
type Ids = Modding.GenericMany<[ServiceA, ServiceB], "id">;
// Returns { ServiceA: string, ServiceB: string }

// New API (preferred)
type IdA = Modding.Generic<ServiceA, "id">;
type IdB = Modding.Generic<ServiceB, "id">;
```

## Reflection API

### Modding.getObjectFromId

Get object reference from Flamework ID.

```typescript
import { Modding, Flamework } from "@flamework/core";

const serviceId = Flamework.id<MyService>();
const service = Modding.getObjectFromId(serviceId);

if (service) {
    print("Found service:", service);
}
```

## Native roblox-ts Decorators

Flamework supports native roblox-ts decorators with reflection.

```typescript
/**
 * @metadata reflect identifier flamework:parameters
 */
const MyDecorator = (ctor: new () => defined) => {
    print("Decorating:", ctor);
};

@MyDecorator
export class MyClass {
    constructor(param: string) {}
}
```

**Key differences:**
- Must explicitly specify metadata (including `identifier`)
- Cannot use Flamework modding APIs (listeners, getDecorator, etc.)
- Full control and generics support
- Better for advanced use cases

## Complete Example: Custom Lifecycle System

```typescript
import { Modding, Service, OnStart } from "@flamework/core";

// Define custom lifecycle decorator
/**
 * @metadata flamework:implements
 */
export const Timed = Modding.createMetaDecorator<[number]>("Class");

// Define lifecycle interface
interface OnInterval {
    onInterval(): void;
}

// Lifecycle manager service
@Service()
export class IntervalManager implements OnStart {
    private intervals = new Map<object, () => void>();
    
    onStart() {
        // Listen for new @Timed classes
        Modding.onListenerAdded<typeof Timed>((object) => {
            this.setupInterval(object);
        });
        
        // Setup existing @Timed classes
        const existing = Modding.getDecorators<typeof Timed>();
        for (const { object } of existing) {
            this.setupInterval(object);
        }
    }
    
    private setupInterval(object: object) {
        // Get interval duration
        const decorator = Modding.getDecorator<typeof Timed>(object);
        if (!decorator) return;
        const [interval] = decorator.arguments;
        
        // Check if implements OnInterval
        if (!Flamework.implements<OnInterval>(object)) {
            warn(object, "has @Timed but doesn't implement OnInterval");
            return;
        }
        
        // Setup interval
        print(`Starting interval for ${object} (${interval}s)`);
        
        const disconnect = game.GetService("RunService").Heartbeat.Connect(() => {
            // In real implementation, track timing
            object.onInterval();
        });
        
        this.intervals.set(object, () => disconnect.Disconnect());
    }
    
    destroy() {
        // Clean up all intervals
        for (const cleanup of this.intervals.values()) {
            cleanup();
        }
    }
}

// Usage
@Timed(5)  // Run every 5 seconds
@Service()
export class AnalyticsService implements OnInterval {
    onInterval() {
        print("Sending analytics...");
        // Send analytics
    }
}

@Timed(60)  // Run every minute
@Service()
export class BackupService implements OnInterval {
    onInterval() {
        print("Creating backup...");
        // Create backup
    }
}
```

## Best Practices

1. **Use meta decorators** when you only need metadata
2. **Use regular decorators** when you need runtime behavior
3. **Request minimal metadata** to avoid bloat
4. **Use listeners** for dynamic registration
5. **Leverage Flamework.implements** for interface checking
6. **Document metadata requirements** for your decorators
7. **Validate decorator arguments** in decorator functions
8. **Clean up resources** in lifecycle callbacks

## Advanced: Custom Singleton Types

Define your own singleton types beyond Service/Controller.

```typescript
/**
 * @metadata flamework:singleton
 * @metadata flamework:loadOrder
 * @metadata flamework:parameters
 */
export const Repository = Modding.createMetaDecorator<[]>("Class");

@Repository()
export class UserRepository {
    findById(id: string) {
        // Implementation
    }
}

// Flamework will treat this as a singleton
```

## Troubleshooting

**Decorator not found**
- Check decorator is exported
- Verify decorator called before reflection
- Ensure metadata requested if needed

**Listener not firing**
- Call `onListenerAdded` before decorators load
- Or process existing decorators separately

**Metadata not generated**
- Add `@metadata` JSDoc tag
- Check syntax is correct
- Verify Flamework transformer is enabled

**Type errors with user macros**
- Ensure type parameters resolve to concrete types
- Check Kind parameter is valid
- Verify supported by guard generation
