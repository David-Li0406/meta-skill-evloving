# Flamework Components Reference

Complete guide to Flamework's entity-component system for attaching behavior to Roblox instances.

## Overview

Flamework components allow you to attach TypeScript classes to Roblox instances using CollectionService tags. Components support:
- **Attribute binding** with type safety
- **Lifecycle events** (OnStart, OnTick, etc.)
- **Dependency injection**
- **StreamingEnabled support**
- **Instance validation**
- **Polymorphism** via interfaces

## Installation

```bash
npm i @flamework/components
```

## Basic Component

```typescript
import { Component, BaseComponent } from "@flamework/components";
import { OnStart } from "@flamework/core";

@Component({ tag: "Coin" })
export class CoinComponent extends BaseComponent implements OnStart {
    onStart() {
        print("Coin component started on:", this.instance);
        
        // Access the instance
        this.instance.Touched.Connect((hit) => {
            this.collect(hit);
        });
    }
    
    private collect(hit: BasePart) {
        print("Coin collected!");
        this.destroy(); // Clean up component
    }
}
```

**Usage in Roblox Studio:**
1. Select a Part/Model in workspace
2. Add CollectionService tag "Coin"
3. Component automatically created when instance loads

## Component with Attributes

```typescript
import { Component, BaseComponent } from "@flamework/components";
import { OnStart } from "@flamework/core";

// Define attributes interface
interface Attributes {
    health: number;
    maxHealth: number;
    damageMultiplier: number;
}

@Component({ tag: "Health" })
export class HealthComponent extends BaseComponent<Attributes> implements OnStart {
    onStart() {
        print(`Health: ${this.attributes.health}/${this.attributes.maxHealth}`);
        print(`Damage multiplier: ${this.attributes.damageMultiplier}`);
    }
    
    takeDamage(amount: number) {
        this.attributes.health -= amount * this.attributes.damageMultiplier;
        if (this.attributes.health <= 0) {
            this.die();
        }
    }
    
    private die() {
        print("Died!");
        this.destroy();
    }
}
```

**Set attributes in Roblox Studio:**
- Add tag "Health" to instance
- Set attributes: health, maxHealth, damageMultiplier

## Specifying Instance Type

```typescript
@Component({ tag: "Door" })
export class DoorComponent extends BaseComponent<{}, Model> implements OnStart {
    // this.instance is now typed as Model
    onStart() {
        const doorPart = this.instance.FindFirstChild("Door") as Part;
        if (doorPart) {
            this.setupDoor(doorPart);
        }
    }
}

// With attributes and instance type
interface ButtonAttributes {
    cooldown: number;
}

@Component({ tag: "Button" })
export class ButtonComponent extends BaseComponent<ButtonAttributes, Part> {
    // this.instance is Part
    // this.attributes has ButtonAttributes
}
```

## Component Configuration

### Default Attribute Values

```typescript
interface Attributes {
    speed: number;
    enabled: boolean;
}

@Component({
    tag: "Mover",
    defaults: {
        speed: 10,
        enabled: true
    }
})
export class MoverComponent extends BaseComponent<Attributes> {
    // If attributes not set in Studio, defaults are used
}
```

### Custom Type Guards for Attributes

```typescript
import { t } from "@rbxts/t";

interface Attributes {
    level: number; // Must be 1-100
    rarity: string; // Must be specific values
}

@Component({
    tag: "Item",
    attributes: {
        level: t.numberConstrained(1, 100),
        rarity: t.union(t.literal("common"), t.literal("rare"), t.literal("legendary"))
    }
})
export class ItemComponent extends BaseComponent<Attributes> {
    // Attributes validated on component creation
}
```

### Instance Predicate

Filter which instances should have components attached.

```typescript
@Component({
    tag: "UIElement",
    predicate: (instance) => {
        // Only create if inside PlayerGui
        return instance.FindFirstAncestorOfClass("PlayerGui") !== undefined;
    }
})
export class UIComponent extends BaseComponent {}
```

### Instance Guard (StreamingEnabled)

Validate instance structure before component creation. Supports StreamingEnabled.

```typescript
import { Flamework } from "@flamework/core";

interface ModelStructure {
    PrimaryPart: Part;
    Handle: Part;
}

@Component({
    tag: "Tool",
    instanceGuard: Flamework.createGuard<Model & ModelStructure>()
})
export class ToolComponent extends BaseComponent<{}, Model> implements OnStart {
    onStart() {
        // Instance guaranteed to have PrimaryPart and Handle
        const primaryPart = this.instance.PrimaryPart!;
        const handle = this.instance.FindFirstChild("Handle") as Part;
    }
}
```

**Behavior:**
- **Server:** Error if guard fails
- **Client (StreamingEnabled):** Waits for instance to fully load, then validates

### Attribute Refresh

Control whether attributes update after component creation.

```typescript
interface Attributes {
    value: number;
}

@Component({
    tag: "Counter",
    refreshAttributes: false // Attributes won't update after creation
})
export class CounterComponent extends BaseComponent<Attributes> {
    // this.attributes.value frozen at creation time
}
```

**Default:** `true` (attributes stay synchronized with instance)

### Ancestor Filtering

Control where components can be created based on ancestor services.

```typescript
// Only create in Workspace
@Component({
    tag: "WorldObject",
    ancestorWhitelist: [game.Workspace]
})
export class WorldObjectComponent extends BaseComponent {}

// Create anywhere except storage services
@Component({
    tag: "Active",
    ancestorBlacklist: [game.ServerStorage, game.ReplicatedStorage]
})
export class ActiveComponent extends BaseComponent {}
```

**Default blacklist:** ServerStorage, ReplicatedStorage, StarterPack, StarterGui, StarterPlayer

### StreamingEnabled Configuration

```typescript
import { ComponentStreamingMode } from "@flamework/components";

@Component({
    tag: "StreamedObject",
    streamingMode: ComponentStreamingMode.Watching // Actively watches for changes
    // or ComponentStreamingMode.Disabled // No streaming support
    // or ComponentStreamingMode.Contextual // Default - smart based on context
})
export class StreamedComponent extends BaseComponent {}
```

**Modes:**
- `Disabled` - No streaming support, instance guard runs once
- `Watching` - Monitors instance tree, reruns guards on changes
- `Contextual` (default) - Server: Disabled, Client: Watches unless Atomic model

### Warning Timeout

```typescript
@Component({
    tag: "DelayedLoad",
    warningTimeout: 30 // Warn after 30 seconds instead of default 5
    // or warningTimeout: 0 to disable warning
})
export class DelayedComponent extends BaseComponent {}
```

Flamework warns if component can't be created within timeout (default 5 seconds).

## Scripting API

Get references to components programmatically.

```typescript
import { Components } from "@flamework/components";
import { Dependency } from "@flamework/core";

const components = Dependency<Components>();

// Or via constructor injection
@Service()
export class MyService {
    constructor(private components: Components) {}
}
```

### Get Component

```typescript
// Get component on specific instance
const coin = components.getComponent<CoinComponent>(part);
if (coin) {
    coin.collect();
}

// Wait for component (returns Promise)
components.waitForComponent<CoinComponent>(part).then((coin) => {
    coin.collect();
});

// Cancellable promise
const promise = components.waitForComponent<CoinComponent>(part);
promise.cancel(); // Clean up if no longer needed
```

### Add/Remove Components

```typescript
// Add component to instance
components.addComponent<CoinComponent>(part);

// Remove component from instance
components.removeComponent<CoinComponent>(part);
```

**Warning:** Components added via scripting API are NOT automatically removed. Prefer CollectionService tags for automatic lifecycle management.

### Get Multiple Components (Polymorphism)

```typescript
// Define interface for common behavior
interface OnInteract {
    interact(player: Player): void;
}

// Multiple components can implement this
@Component({ tag: "Button" })
export class ButtonComponent extends BaseComponent implements OnInteract {
    interact(player: Player) {
        print("Button pressed!");
    }
}

@Component({ tag: "Lever" })
export class LeverComponent extends BaseComponent implements OnInteract {
    interact(player: Player) {
        print("Lever pulled!");
    }
}

// Get all components implementing OnInteract on an instance
const interactables = components.getComponents<OnInteract>(part);
for (const component of interactables) {
    component.interact(player);
}

// Get ALL components implementing OnInteract in the game
const allInteractables = components.getAllComponents<OnInteract>();
```

### Component Listeners

Listen for when components are added or removed.

```typescript
// Listen for specific component
const connection = components.onComponentAdded<CoinComponent>((coin) => {
    print("Coin added:", coin.instance);
});

components.onComponentRemoved<CoinComponent>((coin) => {
    print("Coin removed:", coin.instance);
});

// Disconnect listener
connection.Disconnect();

// Listen for interface implementations
interface OnInteract {
    interact(player: Player): void;
}

components.onComponentAdded<OnInteract>((component) => {
    print("Interactable added!");
    component.interact(somePlayer);
});
```

## Lifecycle Events

Components support the same lifecycle events as singletons.

```typescript
import { Component, BaseComponent } from "@flamework/components";
import { OnStart, OnTick, OnPhysics } from "@flamework/core";

@Component({ tag: "Physics" })
export class PhysicsComponent 
    extends BaseComponent 
    implements OnStart, OnTick, OnPhysics 
{
    onStart() {
        print("Component started");
    }
    
    onTick(dt: number) {
        // Runs every frame after physics
    }
    
    onPhysics(dt: number, time: number) {
        // Runs every frame before physics
    }
}
```

## Attribute Change Handlers

React to attribute changes at runtime.

```typescript
interface Attributes {
    health: number;
    enabled: boolean;
}

@Component({ tag: "Entity" })
export class EntityComponent extends BaseComponent<Attributes> implements OnStart {
    onStart() {
        // Called when health attribute changes
        this.onAttributeChanged("health", (newValue, oldValue) => {
            print(`Health changed from ${oldValue} to ${newValue}`);
            this.updateHealthBar();
        });
        
        // Called when enabled attribute changes
        this.onAttributeChanged("enabled", (newValue) => {
            if (newValue) {
                this.activate();
            } else {
                this.deactivate();
            }
        });
    }
}
```

## Dependencies in Components

Components support dependency injection.

```typescript
import { Component, BaseComponent, Components } from "@flamework/components";
import { OnStart } from "@flamework/core";
import { SoundService } from "../services/sound-service";

@Component({ tag: "Collectible" })
export class CollectibleComponent extends BaseComponent implements OnStart {
    constructor(
        private soundService: SoundService,
        private components: Components
    ) {
        super();
    }
    
    onStart() {
        this.instance.Touched.Connect((hit) => {
            this.soundService.playCollectSound();
            this.destroy();
        });
    }
}
```

## Complete Example

```typescript
// Health component with full features
import { Component, BaseComponent, Components } from "@flamework/components";
import { OnStart } from "@flamework/core";
import { t } from "@rbxts/t";

interface HealthAttributes {
    health: number;
    maxHealth: number;
    regeneration: number;
}

@Component({
    tag: "Health",
    defaults: {
        health: 100,
        maxHealth: 100,
        regeneration: 1
    },
    attributes: {
        health: t.numberMin(0),
        maxHealth: t.numberMin(1),
        regeneration: t.numberMin(0)
    },
    instanceGuard: Flamework.createGuard<Model>(),
    ancestorWhitelist: [game.Workspace]
})
export class HealthComponent extends BaseComponent<HealthAttributes, Model> 
    implements OnStart 
{
    private regenerating = false;
    
    constructor(private components: Components) {
        super();
    }
    
    onStart() {
        // Set health to max on start
        this.attributes.health = this.attributes.maxHealth;
        
        // Listen for attribute changes
        this.onAttributeChanged("health", (newHealth, oldHealth) => {
            print(`Health: ${newHealth}/${this.attributes.maxHealth}`);
            
            if (newHealth <= 0) {
                this.die();
            } else if (newHealth < oldHealth && !this.regenerating) {
                this.startRegeneration();
            }
        });
        
        // Setup humanoid listener if exists
        const humanoid = this.instance.FindFirstChildOfClass("Humanoid");
        if (humanoid) {
            humanoid.Died.Connect(() => this.die());
        }
    }
    
    takeDamage(amount: number) {
        this.attributes.health = math.max(0, this.attributes.health - amount);
    }
    
    heal(amount: number) {
        this.attributes.health = math.min(
            this.attributes.maxHealth,
            this.attributes.health + amount
        );
    }
    
    private startRegeneration() {
        this.regenerating = true;
        
        const connection = game.GetService("RunService").Heartbeat.Connect(() => {
            if (this.attributes.health >= this.attributes.maxHealth) {
                this.regenerating = false;
                connection.Disconnect();
                return;
            }
            
            this.attributes.health = math.min(
                this.attributes.maxHealth,
                this.attributes.health + this.attributes.regeneration
            );
        });
    }
    
    private die() {
        print(this.instance.Name, "died!");
        this.instance.Destroy();
        this.destroy();
    }
}

// Usage in a service
@Service()
export class CombatService implements OnStart {
    constructor(private components: Components) {}
    
    onStart() {
        // Listen for all health components
        this.components.onComponentAdded<HealthComponent>((health) => {
            print("New entity with health:", health.instance);
        });
    }
    
    damageEntity(entity: Model, amount: number) {
        const health = this.components.getComponent<HealthComponent>(entity);
        if (health) {
            health.takeDamage(amount);
        }
    }
}
```

## Best Practices

1. **Use CollectionService tags** for automatic lifecycle instead of scripting API
2. **Validate with instanceGuard** for complex instance structures
3. **Set sensible defaults** for attributes to avoid errors
4. **Use interfaces for polymorphism** when components share behavior
5. **Leverage attribute change handlers** for reactive updates
6. **Clean up properly** - call `this.destroy()` when component no longer needed
7. **Use StreamingEnabled modes** appropriately for your game
8. **Inject dependencies** via constructor for testability

## Troubleshooting

**Component not creating:**
- Check CollectionService tag matches decorator
- Verify ancestorBlacklist/Whitelist
- Check instanceGuard passes
- Look for attribute validation errors
- Check warningTimeout hasn't been disabled

**Attributes not updating:**
- Check `refreshAttributes` is true (default)
- Verify attribute names match interface
- Ensure attributes are set on instance in Studio

**StreamingEnabled issues:**
- Use appropriate streamingMode
- Ensure instanceGuard accounts for streaming
- Test with Watching mode for complex structures

**Component warnings:**
- "Component could not be created for 5+ seconds" - instanceGuard failing or instance structure incomplete
- Increase warningTimeout or fix instance structure
- Use Watching mode for streaming scenarios
