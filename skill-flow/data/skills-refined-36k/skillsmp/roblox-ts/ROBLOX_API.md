# Roblox API with TypeScript Reference

Type-safe Roblox API usage patterns, services, and best practices.

## Services

Always import services from @rbxts/services:

```typescript
import { 
    Workspace, 
    Players, 
    ReplicatedStorage,
    ServerScriptService,
    RunService,
    UserInputService,
    TweenService,
    DataStoreService
} from "@rbxts/services";
```

## Working with Instances

### Finding Instances

```typescript
// Type-safe finding with casting
const part = Workspace.FindFirstChild("MyPart") as Part | undefined;
if (part) {
    part.BrickColor = BrickColor.Red();
}

// WaitForChild (blocks until found)
const humanoid = character.WaitForChild("Humanoid") as Humanoid;

// FindFirstChildOfClass
const humanoid = character.FindFirstChildOfClass("Humanoid");
```

### Type Guards

```typescript
// classIs for runtime type checking
const child = workspace.FindFirstChild("Something");
if (child && classIs(child, "Part")) {
    child.Anchored = true; // TypeScript knows it's a Part
}

// Multiple checks
if (child && (classIs(child, "Part") || classIs(child, "MeshPart"))) {
    child.BrickColor = BrickColor.Red();
}
```

### Creating Instances

```typescript
const part = new Instance("Part");
part.Name = "MyPart";
part.Size = new Vector3(10, 1, 10);
part.Position = new Vector3(0, 5, 0);
part.Parent = Workspace;

// With type parameters
const folder = new Instance("Folder", ReplicatedStorage);
folder.Name = "Data";
```

## Player Management

```typescript
import { Players } from "@rbxts/services";

// Player joining
Players.PlayerAdded.Connect((player) => {
    print(`${player.Name} joined!`);
    
    // Wait for character
    player.CharacterAdded.Connect((character) => {
        setupCharacter(player, character);
    });
});

// Player leaving
Players.PlayerRemoving.Connect((player) => {
    print(`${player.Name} left!`);
    savePlayerData(player);
});

// Get all players
const allPlayers = Players.GetPlayers();

// Get player from character
function getPlayerFromCharacter(character: Model): Player | undefined {
    return Players.GetPlayerFromCharacter(character);
}
```

## Character Handling

```typescript
function setupCharacter(player: Player, character: Model) {
    const humanoid = character.WaitForChild("Humanoid") as Humanoid;
    const rootPart = character.WaitForChild("HumanoidRootPart") as Part;
    
    // Humanoid events
    humanoid.Died.Connect(() => {
        print(`${player.Name} died`);
    });
    
    humanoid.HealthChanged.Connect((health) => {
        print(`Health: ${health}`);
    });
    
    return { humanoid, rootPart };
}
```

## Remote Events/Functions

```typescript
// Create RemoteEvent
const damageEvent = new Instance("RemoteEvent", ReplicatedStorage);
damageEvent.Name = "DamageEvent";

// Server: Listen for client events
damageEvent.OnServerEvent.Connect((player, targetId: string, damage: number) => {
    print(`${player.Name} dealt ${damage} to ${targetId}`);
});

// Client: Fire to server
import { ReplicatedStorage } from "@rbxts/services";
const damageEvent = ReplicatedStorage.WaitForChild("DamageEvent") as RemoteEvent;
damageEvent.FireServer("enemy-123", 50);

// RemoteFunction (two-way)
const getData = new Instance("RemoteFunction", ReplicatedStorage);
getData.Name = "GetData";

// Server: Handle requests
getData.OnServerInvoke = (player, id: string) => {
    return getPlayerData(id);
};

// Client: Invoke
const data = getData.InvokeServer("player-123");
```

## DataStores

```typescript
import { DataStoreService } from "@rbxts/services";

interface PlayerData {
    coins: number;
    level: number;
}

const dataStore = DataStoreService.GetDataStore("PlayerData");

function saveData(userId: string, data: PlayerData) {
    const [success, err] = pcall(() => {
        dataStore.SetAsync(userId, data);
    });
    return success;
}

function loadData(userId: string): PlayerData | undefined {
    const [success, data] = pcall(() => {
        return dataStore.GetAsync(userId) as PlayerData | undefined;
    });
    return success ? data : undefined;
}
```

## TweenService

```typescript
import { TweenService } from "@rbxts/services";

const part = Workspace.FindFirstChild("MyPart") as Part;

const tweenInfo = new TweenInfo(
    2, // Duration
    Enum.EasingStyle.Quad,
    Enum.EasingDirection.Out
);

const tween = TweenService.Create(part, tweenInfo, {
    Position: new Vector3(0, 10, 0),
    Transparency: 0.5
});

tween.Play();
```

## Best Practices

1. Always use type guards with FindFirstChild
2. Import services from @rbxts/services
3. Use WaitForChild for guaranteed existence
4. Type RemoteEvent parameters
5. Use pcall for DataStore operations
6. Properly type Player character descendants
