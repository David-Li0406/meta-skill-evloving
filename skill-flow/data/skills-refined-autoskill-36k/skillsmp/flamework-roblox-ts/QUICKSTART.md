# Flamework Quick Start Guide

Get up and running with Flamework in minutes.

## Installation

```bash
# Create project
mkdir my-game && cd my-game

# Initialize roblox-ts
npx rbxtsc init

# Install Flamework
npm i -D rbxts-transformer-flamework
npm i @flamework/core @flamework/networking @flamework/components
```

## Configuration

### tsconfig.json
```json
{
  "compilerOptions": {
    "experimentalDecorators": true,
    "plugins": [{ "transform": "rbxts-transformer-flamework" }],
    "typeRoots": ["node_modules/@rbxts", "node_modules/@flamework"]
  }
}
```

### default.project.json
```json
{
  "tree": {
    "ReplicatedStorage": {
      "node_modules": {
        "@rbxts": { "$path": "node_modules/@rbxts" },
        "@flamework": { "$path": "node_modules/@flamework" }
      }
    }
  }
}
```

## Project Structure

```
src/
├── server/
│   ├── runtime.server.ts
│   └── services/
│       └── player-service.ts
├── client/
│   ├── runtime.client.ts
│   └── controllers/
│       └── ui-controller.ts
└── shared/
    └── networking.ts
```

## Your First Service

**src/server/services/player-service.ts**
```typescript
import { Service, OnStart } from "@flamework/core";

@Service()
export class PlayerService implements OnStart {
    onStart() {
        print("PlayerService started!");
        
        game.Players.PlayerAdded.Connect((player) => {
            this.onPlayerJoin(player);
        });
    }
    
    private onPlayerJoin(player: Player) {
        print(player.Name, "joined the game!");
    }
}
```

## Your First Controller

**src/client/controllers/ui-controller.ts**
```typescript
import { Controller, OnStart } from "@flamework/core";

@Controller()
export class UIController implements OnStart {
    onStart() {
        print("UIController started!");
        this.setupUI();
    }
    
    private setupUI() {
        // Setup your UI here
    }
}
```

## Networking Setup

**src/shared/networking.ts**
```typescript
import { Networking } from "@flamework/networking";

interface ClientToServer {
    requestData(id: string): void;
}

interface ServerToClient {
    updateHealth(health: number): void;
}

export const GlobalEvents = Networking.createEvent<
    ClientToServer,
    ServerToClient
>();
```

**src/server/networking.ts**
```typescript
import { GlobalEvents } from "shared/networking";
export const Events = GlobalEvents.createServer();
```

**src/client/networking.ts**
```typescript
import { GlobalEvents } from "shared/networking";
export const Events = GlobalEvents.createClient();
```

## Using Networking

**Server Side:**
```typescript
import { Service, OnStart } from "@flamework/core";
import { Events } from "./networking";

@Service()
export class GameService implements OnStart {
    onStart() {
        Events.requestData.connect((player, id) => {
            print(player.Name, "requested data:", id);
            Events.updateHealth.fire(player, 100);
        });
    }
}
```

**Client Side:**
```typescript
import { Controller, OnStart } from "@flamework/core";
import { Events } from "./networking";

@Controller()
export class ClientController implements OnStart {
    onStart() {
        Events.updateHealth.connect((health) => {
            print("Health updated:", health);
        });
        
        // Request data from server
        Events.requestData.fire("player-data");
    }
}
```

## Your First Component

**src/server/components/coin-component.ts**
```typescript
import { Component, BaseComponent } from "@flamework/components";
import { OnStart } from "@flamework/core";

interface Attributes {
    value: number;
}

@Component({ 
    tag: "Coin",
    defaults: { value: 10 }
})
export class CoinComponent extends BaseComponent<Attributes, Part> 
    implements OnStart 
{
    onStart() {
        print("Coin component on:", this.instance.Name);
        
        this.instance.Touched.Connect((hit) => {
            this.collect(hit);
        });
    }
    
    private collect(hit: BasePart) {
        print("Collected coin worth:", this.attributes.value);
        this.instance.Destroy();
        this.destroy();
    }
}
```

**To use:** Add CollectionService tag "Coin" to any Part in Studio.

## Runtime Entry Points

**src/server/runtime.server.ts**
```typescript
import { Flamework } from "@flamework/core";

Flamework.addPaths("src/server/services/");
Flamework.addPaths("src/server/components/");
Flamework.ignite();
```

**src/client/runtime.client.ts**
```typescript
import { Flamework } from "@flamework/core";

Flamework.addPaths("src/client/controllers/");
Flamework.addPaths("src/client/components/");
Flamework.ignite();
```

## Build and Run

```bash
# Start watch mode
npm run watch

# Open in Roblox Studio
# Files will compile to out/ directory
# Sync with Rojo or manually
```

## Next Steps

- **Learn dependency injection**: See CORE.md
- **Explore lifecycle events**: OnTick, OnPhysics, OnRender
- **Add RemoteFunctions**: Two-way communication
- **Configure components**: Attributes, predicates, guards
- **Use macros**: Flamework.createGuard, Flamework.id

## Common Issues

**Decorators not working?**
- Check `experimentalDecorators: true` in tsconfig.json
- Verify transformer plugin is configured

**Modules not loading?**
- Ensure Flamework.addPaths() includes your directories
- Check decorator is applied (@Service, @Controller, @Component)

**TypeScript errors?**
- Run `npm install` to ensure types are installed
- Check typeRoots includes @flamework

## Resources

- Full documentation: See other .md files in this skill
- Official docs: https://flamework.fireboltofdeath.dev/
- GitHub: https://github.com/rbxts-flamework/core

## Quick Reference

```typescript
// Service (server)
@Service()
export class MyService implements OnStart {
    constructor(private other: OtherService) {}
    onStart() {}
}

// Controller (client)
@Controller()
export class MyController implements OnStart {
    onStart() {}
}

// Component
@Component({ tag: "MyTag" })
export class MyComponent extends BaseComponent {}

// RemoteEvent
interface Events {
    myEvent(param: string): void;
}
export const Events = Networking.createEvent<Events, {}>();

// RemoteFunction
interface Functions {
    getData(id: string): Data;
}
export const Functions = Networking.createFunction<Functions, {}>();

// Lifecycle Events
OnStart   - After initialization (use this)
OnInit    - During initialization (rare)
OnTick    - Every frame (after physics)
OnPhysics - Every frame (before physics)
OnRender  - Every frame (before render, client only)
```

Happy coding with Flamework! 🚀
