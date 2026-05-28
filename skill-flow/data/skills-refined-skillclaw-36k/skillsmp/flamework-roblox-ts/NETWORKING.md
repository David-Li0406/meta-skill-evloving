# Flamework Networking Reference

Complete guide to Flamework's networking module: RemoteEvents, RemoteFunctions, middleware, and type safety.

## Overview

Flamework networking provides:
- **Type-safe** remote communication
- **Automatic type guard generation**
- **Promise-based** RemoteFunctions
- **Middleware support**
- **Namespace organization**
- **Unreliable events** support

## Installation

```bash
npm i @flamework/networking
```

## RemoteEvents (One-Way Communication)

Use for fire-and-forget communication with no response needed.

### Creating RemoteEvents

```typescript
// shared/networking.ts
import { Networking } from "@flamework/networking";

// Define event interfaces
interface ClientToServerEvents {
    // Client fires, server handles
    playerJump(): void;
    damageDealt(targetId: string, amount: number): void;
}

interface ServerToClientEvents {
    // Server fires, client handles
    healthUpdate(newHealth: number): void;
    notification(message: string, type: "info" | "warning"): void;
}

// Create the global events object
export const GlobalEvents = Networking.createEvent<
    ClientToServerEvents,
    ServerToClientEvents
>();
```

### Re-exporting for Server/Client

**IMPORTANT:** Always create separate server and client files to hide server configuration from client.

```typescript
// server/networking.ts
import { GlobalEvents } from "shared/networking";

export const Events = GlobalEvents.createServer({
    // Server-only configuration
    // Guards are not exposed to client
});
```

```typescript
// client/networking.ts
import { GlobalEvents } from "shared/networking";

export const Events = GlobalEvents.createClient({
    // Client-only configuration
});
```

### Firing Events

#### Server

```typescript
import { Events } from "./networking";

// Fire to specific player
Events.healthUpdate.fire(player, 75);

// Fire to multiple players
Events.healthUpdate.fire([player1, player2], 75);

// Fire to all except specific player(s)
Events.healthUpdate.except(player, 75);
Events.healthUpdate.except([player1, player2], 75);

// Broadcast to all players
Events.healthUpdate.broadcast(75);

// Predict (simulate firing from player)
Events.playerJump.predict(player);

// Shorthand syntax (same as .fire)
Events.healthUpdate(player, 75);
```

#### Client

```typescript
import { Events } from "./networking";

// Fire to server
Events.playerJump.fire();
Events.damageDealt.fire("enemy-123", 25);

// Predict (simulate receiving)
Events.healthUpdate.predict(75);

// Shorthand syntax
Events.playerJump();
```

### Connecting to Events

```typescript
// Server (has player parameter)
Events.damageDealt.connect((player, targetId, amount) => {
    print(`${player.Name} dealt ${amount} damage to ${targetId}`);
});

// Client (no player parameter)
Events.healthUpdate.connect((newHealth) => {
    print(`Health updated: ${newHealth}`);
});

// Disconnecting
const connection = Events.healthUpdate.connect((health) => {});
connection.Disconnect();
```

### Unreliable Events

For high-frequency, non-critical data (follows Roblox 900 byte limit).

```typescript
interface ClientToServerEvents {
    // Regular reliable event
    playerAttack(targetId: string): void;
    
    // Unreliable event (good for position updates)
    playerPosition: Networking.Unreliable<(x: number, y: number, z: number) => void>;
}

// Usage is identical to reliable events
Events.playerPosition.fire(player, x, y, z);
```

### Namespaces

Organize events into logical groups.

```typescript
interface ClientToServerEvents {
    // Top-level events
    login(username: string): void;
    
    // Combat namespace
    combat: {
        attack(targetId: string): void;
        defend(): void;
        useAbility(abilityId: string): void;
    };
    
    // Social namespace
    social: {
        sendMessage(message: string): void;
        addFriend(userId: string): void;
    };
    
    // Nested namespaces supported
    inventory: {
        items: {
            use(itemId: string): void;
            drop(itemId: string): void;
        };
    };
}

// Access namespace events
Events.combat.attack.fire(player, "enemy-123");
Events.social.sendMessage.connect((player, message) => {
    print(`${player.Name}: ${message}`);
});
```

## RemoteFunctions (Two-Way Communication)

Use when you need a response from the receiver. Built on promises with 10-second default timeout.

### Creating RemoteFunctions

```typescript
// shared/networking.ts
import { Networking } from "@flamework/networking";

interface ClientToServerFunctions {
    // Client invokes, server responds
    getData(id: string): PlayerData;
    purchaseItem(itemId: string): PurchaseResult;
}

interface ServerToClientFunctions {
    // Server invokes, client responds (rare)
    confirmAction(message: string): boolean;
}

export const GlobalFunctions = Networking.createFunction<
    ClientToServerFunctions,
    ServerToClientFunctions
>();
```

```typescript
// server/networking.ts
export const Functions = GlobalFunctions.createServer();

// client/networking.ts
export const Functions = GlobalFunctions.createClient();
```

### Invoking Functions

```typescript
// Client invoking server function
Functions.getData.invoke("player-123")
    .then((data) => {
        print("Received:", data);
    })
    .catch((error) => {
        warn("Error:", error);
    });

// Async/await style
const data = await Functions.getData.invoke("player-123");

// With custom timeout (overrides default 10 seconds)
const data = await Functions.getData.invokeWithTimeout("player-123", 5);

// Shorthand syntax
const data = await Functions.getData("player-123");

// Predict (simulate invocation)
Functions.getData.predict("player-123").then(...);
```

### Handling Function Requests

```typescript
// Server handling client request
Functions.getData.setCallback((player, id) => {
    const data = getPlayerData(id);
    return data; // Return the result
});

// Async handler
Functions.purchaseItem.setCallback(async (player, itemId) => {
    const result = await processPurchase(player, itemId);
    return result;
});

// Only one callback per function - calling setCallback again overrides and warns
```

### Error Handling

Flamework provides typed errors via `NetworkingFunctionError` enum:

```typescript
import { NetworkingFunctionError } from "@flamework/networking";

Functions.getData.invoke("id")
    .then((data) => {
        // Success
    })
    .catch((error) => {
        if (error === NetworkingFunctionError.Timeout) {
            warn("Request timed out");
        } else if (error === NetworkingFunctionError.BadRequest) {
            warn("Invalid arguments sent");
        } else if (error === NetworkingFunctionError.InvalidResult) {
            warn("Server returned invalid data");
        } else if (error === NetworkingFunctionError.Unprocessed) {
            warn("No handler registered");
        } else if (error === NetworkingFunctionError.Cancelled) {
            warn("Request was cancelled");
        }
    });
```

**Error Types:**
- `Timeout` - Request exceeded timeout (default 10s)
- `Cancelled` - Request cancelled by receiver
- `BadRequest` - Invalid arguments rejected by guard
- `InvalidResult` - Server response failed type guard
- `Unprocessed` - No callback registered for function
- `Unknown` - Other error occurred

## Middleware

Middleware allows you to intercept, modify, delay, or reject requests before they reach handlers.

### Server Middleware Example

```typescript
// server/networking.ts
import { GlobalEvents } from "shared/networking";

// Logging middleware
const loggingMiddleware = (player: Player, args: unknown[]) => {
    print(`Request from ${player.Name}:`, args);
    return args; // Pass through unchanged
};

// Rate limiting middleware
const rateLimitMiddleware = (player: Player, args: unknown[]) => {
    if (isRateLimited(player)) {
        return; // Drop request
    }
    return args;
};

// Permission check middleware
const permissionMiddleware = (player: Player, args: unknown[]) => {
    if (!hasPermission(player)) {
        return; // Reject
    }
    return args;
};

export const Events = GlobalEvents.createServer({
    middleware: {
        // Apply to all events
        "*": [loggingMiddleware],
        
        // Apply to specific event
        damageDealt: [permissionMiddleware, rateLimitMiddleware],
        
        // Apply to namespace
        admin: {
            "*": [permissionMiddleware],
            kick: [loggingMiddleware],
        }
    }
});
```

### Middleware Order

Middleware runs in order. If any middleware returns `undefined`, the request is dropped.

```typescript
const middleware1 = (player: Player, args: unknown[]) => {
    print("First");
    return args;
};

const middleware2 = (player: Player, args: unknown[]) => {
    print("Second");
    return args;
};

export const Events = GlobalEvents.createServer({
    middleware: {
        myEvent: [middleware1, middleware2] // Runs in order
    }
});
```

## Type Guards

Flamework automatically generates type guards for your networking interfaces to validate data at runtime.

### Automatic Generation

```typescript
interface ClientToServerEvents {
    // Guard automatically generated
    updatePosition(x: number, y: number, z: number): void;
    
    // Complex types supported
    setData(data: { name: string; level: number }): void;
}

// Invalid arguments automatically rejected
// Client sends: Events.updatePosition("not a number", 0, 0)
// Server: Request rejected with BadRequest error
```

### Configuration

```typescript
// Enable warnings for invalid requests (default: enabled in Studio only)
export const Events = GlobalEvents.createServer({
    warnOnInvalidGuards: true // Warns when guards reject requests
});

export const Functions = GlobalFunctions.createServer({
    warnOnInvalidGuards: false // Silently reject
});
```

### Supported Types

Type guards support most TypeScript types:
- Primitives: `string`, `number`, `boolean`
- Roblox types: `Vector3`, `CFrame`, `Instance`, `buffer`, etc.
- Arrays: `string[]`, `number[][]`
- Objects: `{ name: string; age: number }`
- Unions: `"red" | "blue"`, `number | string`
- Optionals: `string?`, `number | undefined`
- Literals: `"exact string"`, `42`

## Event Handlers

### Global Event Handlers

Register handlers for networking events (errors, invalid requests).

```typescript
GlobalEvents.registerHandler("onBadRequest", (player) => {
    warn(`Bad request from ${player.Name}`);
});

GlobalEvents.registerHandler("onBadResponse", (player) => {
    warn(`Bad response to ${player.Name}`);
});
```

Available handlers:
- `onBadRequest` - Client sent invalid data
- `onBadResponse` - Server sent invalid data

## Complete Example

```typescript
// shared/networking.ts
import { Networking } from "@flamework/networking";

interface ClientToServerEvents {
    playerMove(x: number, z: number): void;
    chatMessage(message: string): void;
    
    combat: {
        attack(targetId: string): void;
        defend(): void;
    };
}

interface ServerToClientEvents {
    healthUpdate(health: number, maxHealth: number): void;
    enemySpawned(enemyId: string, position: Vector3): void;
}

interface ClientToServerFunctions {
    getPlayerData(playerId: string): PlayerData;
    purchaseItem(itemId: string, quantity: number): PurchaseResult;
}

interface ServerToClientFunctions {
    // Rarely used
}

export const GlobalEvents = Networking.createEvent<
    ClientToServerEvents,
    ServerToClientEvents
>();

export const GlobalFunctions = Networking.createFunction<
    ClientToServerFunctions,
    ServerToClientFunctions
>();

// server/networking.ts
import { GlobalEvents, GlobalFunctions } from "shared/networking";

const authMiddleware = (player: Player, args: unknown[]) => {
    if (!isAuthenticated(player)) return;
    return args;
};

export const Events = GlobalEvents.createServer({
    middleware: {
        "*": [authMiddleware]
    },
    warnOnInvalidGuards: true
});

export const Functions = GlobalFunctions.createServer();

// In a service
@Service()
export class CombatService implements OnStart {
    onStart() {
        Events.combat.attack.connect((player, targetId) => {
            this.handleAttack(player, targetId);
        });
        
        Functions.getPlayerData.setCallback((player, playerId) => {
            return this.getPlayerData(playerId);
        });
    }
}

// client/networking.ts
import { GlobalEvents, GlobalFunctions } from "shared/networking";

export const Events = GlobalEvents.createClient();
export const Functions = GlobalFunctions.createClient();

// In a controller
@Controller()
export class CombatController implements OnStart {
    onStart() {
        Events.healthUpdate.connect((health, maxHealth) => {
            this.updateHealthUI(health, maxHealth);
        });
    }
    
    async attack(targetId: string) {
        Events.combat.attack.fire(targetId);
        
        // Or with confirmation
        try {
            const result = await Functions.purchaseItem("sword", 1);
            if (result.success) {
                Events.combat.attack.fire(targetId);
            }
        } catch (error) {
            warn("Purchase failed:", error);
        }
    }
}
```

## Best Practices

1. **Always split server/client** - Create separate networking exports to hide server config
2. **Use interfaces** - Define clear event/function interfaces
3. **Organize with namespaces** - Group related events
4. **Prefer RemoteEvents** - Use RemoteFunctions only when response needed
5. **Handle errors** - Always catch RemoteFunction rejections
6. **Leverage middleware** - Use for authentication, rate limiting, logging
7. **Use unreliable sparingly** - Only for high-frequency, loss-tolerant data
8. **Trust type guards** - Let Flamework validate data automatically

## Troubleshooting

**"Bad request" warnings**
- Client sending invalid data
- Check type guard expectations
- Verify argument types match interface

**Functions timing out**
- Increase timeout with `invokeWithTimeout`
- Check if handler is registered
- Verify no errors in handler

**Middleware not running**
- Check middleware returns args (or undefined to drop)
- Verify middleware attached to correct event
- Check middleware order

**Events not firing**
- Verify connection before firing
- Check if event name matches interface
- Ensure proper server/client separation
