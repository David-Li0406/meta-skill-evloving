# GameKit Framework - Complete Guide

**High-level game development framework integrated with Unity-AI-Forge MCP tools.**

GameKit provides production-ready components for rapid game development, including actors, managers, UI command systems, resource management with Machinations-inspired economics, scene flow, and interactions.

## Table of Contents

1. [GameKit Overview](#gamekit-overview)
2. [GameKit Actor](#gamekit-actor)
3. [GameKit Manager](#gamekit-manager)
4. [GameKit UICommand](#gamekit-uicommand)
5. [GameKit Machinations (Resource System)](#gamekit-machinations)
6. [GameKit SceneFlow](#gamekit-sceneflow)
7. [GameKit Interaction](#gamekit-interaction)
8. [Complete Game Examples](#complete-game-examples)

---

## GameKit Overview

### What is GameKit?

GameKit is a high-level framework that sits on top of Unity's standard components, providing:

- **🎭 Actor System**: Player/NPC controllers with input abstraction
- **📊 Manager System**: Game state, resources, turns, events
- **🎮 UI Command System**: Bridge UI to game logic
- **💰 Resource Economics**: Machinations-inspired resource flows
- **🎬 Scene Flow**: State-based scene transitions
- **⚡ Interaction System**: Trigger-based game events

### Architecture

```
GameKit Framework
├── Actors (Controller-Behavior separation)
│   ├── Input Controllers (DirectController, AI, UI, Script)
│   ├── Movement Behaviors (2D/3D Physics, Grid, NavMesh, etc.)
│   └── UnityEvents (OnMove, OnJump, OnAction, OnLook)
│
├── Managers (Centralized game systems)
│   ├── TurnManager (Turn-based games)
│   ├── StateManager (FSM for game states)
│   ├── ResourceManager (Economy & resources)
│   ├── RealtimeManager (Real-time event coordination)
│   └── EventHub (Global event system)
│
├── UICommand (UI → Game Logic bridge)
│   ├── Actor Commands (Move, Jump, Action)
│   └── Manager Commands (Resources, State, Turn, Scene)
│
├── Machinations (Economic system)
│   ├── Resource Pools (Storage with constraints)
│   ├── Resource Flows (Automatic generation/consumption)
│   ├── Converters (Transform resources)
│   └── Triggers (Threshold events)
│
├── SceneFlow (Scene management)
│   ├── State Machine (Scene transitions)
│   ├── Additive Loading (Shared scenes)
│   └── Persistent Manager (Cross-scene data)
│
└── Interaction (Event triggers)
    ├── Collision/Trigger Zones
    ├── Proximity Detection
    ├── Input-based Triggers
    └── Declarative Actions
```

### MCP Tools for GameKit

All GameKit components are accessible via MCP tools with the `gamekit*` prefix:

| Tool | Purpose |
|------|---------|
| `gamekitActor` | Create and manage game actors |
| `gamekitManager` | Create and manage game managers |
| `gamekitUICommand` | Create UI command panels |
| `gamekitMachinations` | Manage Machinations asset diagrams |
| `gamekitSceneflow` | Manage scene transitions |
| `gamekitInteraction` | Create interaction triggers |

---

## GameKit Actor

### Overview

**GameKitActor** is a controller-behavior hub that separates input from movement logic using UnityEvents.

### Control Modes

1. **DirectController**: Player input (New Input System or legacy)
2. **AIAutonomous**: AI-driven behavior (patrol, follow, wander)
3. **UICommand**: Button/UI-driven control
4. **ScriptTriggerOnly**: Event-driven from scripts

### Behavior Profiles

| Profile | Description | Use Case |
|---------|-------------|----------|
| `2dLinear` | Simple 2D movement | Side-scrollers, puzzle games |
| `2dPhysics` | Rigidbody2D physics | Physics platformers |
| `2dTileGrid` | Grid-based movement | Turn-based tactics, roguelikes |
| `graphNode` | A* pathfinding | Strategy games, AI navigation |
| `splineMovement` | Rail-based movement | Rail shooters, 2.5D games |
| `3dCharacterController` | CharacterController-based | FPS, TPS games |
| `3dPhysics` | Rigidbody physics | Physics-based 3D games |
| `3dNavMesh` | NavMesh agent | RTS, MOBA, strategy games |

### Creating Actors via MCP

```python
# Create a 3D player character
gamekit Actor({
    "operation": "create",
    "actorId": "Player",
    "controlMode": "directController",  # Player input
    "behaviorProfile": "3dCharacterController",
    "position": {"x": 0, "y": 1, "z": 0}
})

# Create an AI enemy with NavMesh
gamekitActor({
    "operation": "create",
    "actorId": "EnemyGuard",
    "controlMode": "aiAutonomous",  # AI-driven
    "behaviorProfile": "3dNavMesh",
    "position": {"x": 10, "y": 0, "z": 5}
})

# Create a 2D platformer player
gamekitActor({
    "operation": "create",
    "actorId": "Player2D",
    "controlMode": "directController",
    "behaviorProfile": "2dPhysics",
    "spritePath": "Assets/Sprites/Player.png"
})

# Create a grid-based tactical unit
gamekitActor({
    "operation": "create",
    "actorId": "TacticalUnit",
    "controlMode": "uiCommand",  # Controlled by UI buttons
    "behaviorProfile": "2dTileGrid"
})
```

### Actor UnityEvents

Actors expose UnityEvents that behaviors listen to:

- `OnMoveInput(Vector3)` - Movement direction
- `OnJumpInput()` - Jump action
- `OnActionInput(string)` - Generic action with parameter
- `OnLookInput(Vector2)` - Camera/aim direction

---

## GameKit Manager

### Overview

**GameKitManager** is a centralized hub for game systems (resources, states, turns).

### Manager Types

| Type | Purpose | Use Case |
|------|---------|----------|
| `resourcePool` | Resource management | RPG stats, economy, crafting |
| `turnBased` | Turn-based game flow | Chess, card games, tactics |
| `stateManager` | Finite state machine | Menu states, game phases |
| `realtime` | Real-time coordination | Action games, simulations |
| `eventHub` | Global event system | Observer pattern, decoupling |

### Creating Managers via MCP

```python
# Create a resource manager for RPG
gamekitManager({
    "operation": "create",
    "managerId": "PlayerStats",
    "managerType": "resourcepool",
    "initialResources": {
        "health": 100,
        "mana": 50,
        "gold": 0,
        "experience": 0
    }
})

# Create a turn-based manager
gamekitManager({
    "operation": "create",
    "managerId": "BattleManager",
    "managerType": "turnBased",
    "turnPhases": ["PlayerTurn", "EnemyTurn", "ResolveEffects"]
})

# Create a game state manager
gamekitManager({
    "operation": "create",
    "managerId": "GameStateManager",
    "managerType": "stateManager",
    "persistent": True  # Don't destroy on scene load
})
```

### Resource Operations

```python
# Add resources
gamekitManager({
    "operation": "update",
    "managerId": "PlayerStats",
    "initialResources": {
        "health": 75,  # Update existing
        "gold": 100    # Existing + 100
    }
})

# Inspect resources
gamekitManager({
    "operation": "inspect",
    "managerId": "PlayerStats"
})
```

### State Persistence (Save/Load)

```python
# Export current state
result = gamekitManager({
    "operation": "exportState",
    "managerId": "PlayerStats"
})
# Returns JSON-serializable state

# Import saved state
gamekitManager({
    "operation": "importState",
    "managerId": "PlayerStats",
    "stateData": saved_state_json
})
```

---

## GameKit UICommand

### Overview

**GameKitUICommand** bridges UI controls (buttons, sliders) to **GameKitActor** or **GameKitManager** via UnityEvents.

### Target Types

- **Actor**: Control actors (move, jump, action)
- **Manager**: Control managers (resources, state, turns, scenes)

### Creating UI Command Panels

#### For Actor Control

```python
# Create a virtual joystick panel
gamekitUICommand({
    "operation": "createCommandPanel",
    "panelId": "VirtualJoystick",
    "canvasPath": "Canvas",
    "targetType": "actor",
    "targetActorId": "Player",
    "commands": [
        {
            "name": "moveUp",
            "label": "↑",
            "commandType": "move",
            "moveDirection": {"x": 0, "y": 0, "z": 1}
        },
        {
            "name": "moveDown",
            "label": "↓",
            "commandType": "move",
            "moveDirection": {"x": 0, "y": 0, "z": -1}
        },
        {
            "name": "jump",
            "label": "Jump",
            "commandType": "jump"
        },
        {
            "name": "attack",
            "label": "Attack",
            "commandType": "action",
            "commandParameter": "attack"
        }
    ]
})
```

#### For Manager Control

```python
# Create resource management UI
gamekitUICommand({
    "operation": "createCommandPanel",
    "panelId": "ShopPanel",
    "canvasPath": "Canvas",
    "targetType": "manager",  # Target manager instead of actor
    "targetManagerId": "PlayerEconomy",
    "commands": [
        {
            "name": "buyHealthPotion",
            "label": "HP Potion (50g)",
            "commandType": "consumeResource",  # Manager command
            "commandParameter": "gold",
            "resourceAmount": 50
        },
        {
            "name": "buyManaPotion",
            "label": "MP Potion (30g)",
            "commandType": "consumeResource",
            "commandParameter": "gold",
            "resourceAmount": 30
        },
        {
            "name": "endTurn",
            "label": "End Turn",
            "commandType": "nextTurn"  # Advance turn phase
        }
    ]
})
```

### Manager Command Types

| Command Type | Action | Example |
|-------------|--------|---------|
| `addResource` | Add resource amount | Give rewards |
| `setResource` | Set exact amount | Initialize values |
| `consumeResource` | Subtract if sufficient | Buy items, cast spells |
| `changeState` | Change game state | Menu → Game → GameOver |
| `nextTurn` | Advance turn phase | Player → Enemy turn |
| `triggerScene` | Trigger scene transition | Level complete → Next level |

---

## GameKit Machinations

### Overview

**GameKitMachinationsAsset** is a ScriptableObject that defines resource economies inspired by Machinations.io.

### Components

1. **Resource Pools**: Storage with min/max constraints
2. **Resource Flows**: Automatic generation/consumption over time
3. **Converters**: Transform one resource into another
4. **Triggers**: Fire events when thresholds are crossed

### Creating Machinations Diagrams

```python
# Create an RPG economy diagram
gamekitMachinations({
    "operation": "create",
    "diagramId": "RPGEconomy",
    "assetPath": "Assets/Economy/RPGEconomy.asset",
    "initialResources": [
        {
            "name": "health",
            "initialAmount": 100,
            "minValue": 0,
            "maxValue": 100
        },
        {
            "name": "mana",
            "initialAmount": 50,
            "minValue": 0,
            "maxValue": 100
        },
        {
            "name": "gold",
            "initialAmount": 0,
            "minValue": 0,
            "maxValue": 999999
        }
    ],
    "flows": [
        {
            "flowId": "manaRegen",
            "resourceName": "mana",
            "ratePerSecond": 1.0,
            "isSource": True,  # Generate mana
            "enabledByDefault": True
        },
        {
            "flowId": "poisonDamage",
            "resourceName": "health",
            "ratePerSecond": 2.0,
            "isSource": False,  # Drain health
            "enabledByDefault": False
        }
    ],
    "converters": [
        {
            "converterId": "buyHealthPotion",
            "fromResource": "gold",
            "toResource": "health",
            "conversionRate": 50,  # 1 gold → 50 HP
            "inputCost": 10
        }
    ],
    "triggers": [
        {
            "triggerName": "playerDied",
            "resourceName": "health",
            "thresholdType": "below",
            "thresholdValue": 1
        },
        {
            "triggerName": "lowHealth",
            "resourceName": "health",
            "thresholdType": "below",
            "thresholdValue": 20
        }
    ]
})
```

### Applying to Managers

```python
# Apply Machinations asset to a resource manager
gamekitMachinations({
    "operation": "apply",
    "assetPath": "Assets/Economy/RPGEconomy.asset",
    "managerId": "PlayerStats",
    "resetExisting": True
})
```

### Controlling Flows at Runtime

```python
# Enable/disable flows dynamically
# (Flows run automatically in ResourceManager.Update())
gamekit Manager({
    "operation": "setFlowEnabled",
    "managerId": "PlayerStats",
    "flowId": "poisonDamage",
    "enabled": True  # Start poison damage
})
```

---

## GameKit SceneFlow

### Overview

**GameKitSceneFlow** manages scene transitions using a state machine with **granular operations**. Build scene flows step by step by adding individual scenes and transitions.

### Granular Operations

SceneFlow now uses individual operations for precise control:

| Operation | Purpose |
|-----------|---------|
| `create` | Initialize empty scene flow |
| `addScene` | Add one scene with load mode and shared scenes |
| `removeScene` | Remove a scene definition |
| `updateScene` | Update scene properties |
| `addTransition` | Add one transition between scenes |
| `removeTransition` | Remove a transition |
| `addSharedScene` | Add a shared scene to a scene |
| `removeSharedScene` | Remove a shared scene from a scene |
| `inspect` | Get scene flow information |
| `delete` | Delete entire scene flow |
| `transition` | Trigger scene transition (runtime) |

### Creating Scene Flows (Step by Step)

```python
# 1. Create empty flow
gamekitSceneflow({
    "operation": "create",
    "flowId": "MainGameFlow"
})

# 2. Add scenes one by one
gamekitSceneflow({
    "operation": "addScene",
    "flowId": "MainGameFlow",
    "sceneName": "MainMenu",
    "scenePath": "Assets/Scenes/MainMenu.unity",
    "loadMode": "single"
})

gamekitSceneflow({
    "operation": "addScene",
    "flowId": "MainGameFlow",
    "sceneName": "GameLevel1",
    "scenePath": "Assets/Scenes/Level1.unity",
    "loadMode": "additive",
    "sharedScenePaths": [
        "Assets/Scenes/UIOverlay.unity",
        "Assets/Scenes/AudioManager.unity"
    ]
})

gamekitSceneflow({
    "operation": "addScene",
    "flowId": "MainGameFlow",
    "sceneName": "GameLevel2",
    "scenePath": "Assets/Scenes/Level2.unity",
    "loadMode": "additive",
    "sharedScenePaths": [
        "Assets/Scenes/UIOverlay.unity",
        "Assets/Scenes/AudioManager.unity"
    ]
})

# 3. Add transitions one by one
gamekitSceneflow({
    "operation": "addTransition",
    "flowId": "MainGameFlow",
    "fromScene": "MainMenu",
    "trigger": "startGame",
    "toScene": "GameLevel1"
})

gamekitSceneflow({
    "operation": "addTransition",
    "flowId": "MainGameFlow",
    "fromScene": "GameLevel1",
    "trigger": "levelComplete",
    "toScene": "GameLevel2"
})
```

### Managing Scenes

```python
# Update scene properties
gamekitSceneflow({
    "operation": "updateScene",
    "flowId": "MainGameFlow",
    "sceneName": "GameLevel1",
    "loadMode": "single",  # Change load mode
    "sharedScenePaths": ["Assets/Scenes/NewUI.unity"]  # Replace shared scenes
})

# Remove scene
gamekitSceneflow({
    "operation": "removeScene",
    "flowId": "MainGameFlow",
    "sceneName": "GameLevel1"
})

# Add shared scene to existing scene
gamekitSceneflow({
    "operation": "addSharedScene",
    "flowId": "MainGameFlow",
    "sceneName": "GameLevel2",
    "sharedScenePath": "Assets/Scenes/NewFeature.unity"
})

# Remove shared scene
gamekitSceneflow({
    "operation": "removeSharedScene",
    "flowId": "MainGameFlow",
    "sceneName": "GameLevel2",
    "sharedScenePath": "Assets/Scenes/OldFeature.unity"
})
```

### Managing Transitions

```python
# Add transition
gamekitSceneflow({
    "operation": "addTransition",
    "flowId": "MainGameFlow",
    "fromScene": "GameLevel2",
    "trigger": "victory",
    "toScene": "Victory"
})

# Remove transition
gamekitSceneflow({
    "operation": "removeTransition",
    "flowId": "MainGameFlow",
    "fromScene": "MainMenu",
    "trigger": "startGame"
})
```

### Triggering Transitions

```python
# Trigger scene transition at runtime
gamekitSceneflow({
    "operation": "transition",
    "flowId": "MainGameFlow",
    "triggerName": "startGame"
})
```

---

## GameKit Interaction

### Overview

**GameKitInteraction** creates trigger-based interactions with declarative actions.

### Trigger Types

- **collision**: OnCollisionEnter
- **trigger**: OnTriggerEnter
- **proximity**: Distance-based
- **input**: Key press
- **raycast**: Ray hit detection

### Creating Interactions

```python
# Create a collectible item
gamekitInteraction({
    "operation": "create",
    "interactionId": "GoldCoin",
    "parentPath": "Items/Coins",
    "triggerType": "trigger",
    "triggerShape": "sphere",
    "triggerSize": {"x": 1, "y": 1, "z": 1},
    "conditions": [
        {"type": "tag", "value": "Player"}
    ],
    "actions": [
        {
            "type": "sendMessage",
            "target": "GameManager",
            "parameter": "CollectGold:10"
        },
        {
            "type": "playSound",
            "parameter": "Assets/Audio/CoinPickup.wav"
        },
        {
            "type": "destroyObject",
            "target": "self"
        }
    ]
})

# Create a door that opens on proximity
gamekitInteraction({
    "operation": "create",
    "interactionId": "AutoDoor",
    "parentPath": "Environment/Doors",
    "triggerType": "proximity",
    "triggerSize": {"x": 3, "y": 2, "z": 3},
    "conditions": [
        {"type": "tag", "value": "Player"}
    ],
    "actions": [
        {
            "type": "sendMessage",
            "target": "AutoDoor",
            "parameter": "Open"
        }
    ]
})
```

---

## Complete Game Examples

### Example 1: RPG Character System

```python
# 1. Create resource manager for player stats
gamekitManager({
    "operation": "create",
    "managerId": "PlayerStats",
    "managerType": "resourcepool",
    "initialResources": {
        "health": 100,
        "mana": 50,
        "stamina": 100,
        "gold": 0,
        "experience": 0
    }
})

# 2. Create Machinations diagram for economy
gamekitMachinations({
    "operation": "create",
    "diagramId": "RPGEconomy",
    "assetPath": "Assets/Economy/RPG.asset",
    "initialResources": [
        {"name": "health", "initialAmount": 100, "minValue": 0, "maxValue": 100},
        {"name": "mana", "initialAmount": 50, "minValue": 0, "maxValue": 100}
    ],
    "flows": [
        {
            "flowId": "manaRegen",
            "resourceName": "mana",
            "ratePerSecond": 1.0,
            "isSource": True
        }
    ],
    "converters": [
        {
            "converterId": "castSpell",
            "fromResource": "mana",
            "toResource": "damage",
            "conversionRate": 10,
            "inputCost": 20
        }
    ],
    "triggers": [
        {
            "triggerName": "playerDied",
            "resourceName": "health",
            "thresholdType": "below",
            "thresholdValue": 1
        }
    ]
})

# 3. Apply Machinations to manager
gamekitMachinations({
    "operation": "apply",
    "assetPath": "Assets/Economy/RPG.asset",
    "managerId": "PlayerStats"
})

# 4. Create player actor
gamekitActor({
    "operation": "create",
    "actorId": "Player",
    "controlMode": "directController",
    "behaviorProfile": "3dCharacterController"
})

# 5. Create UI for resource management
gamekitUICommand({
    "operation": "createCommandPanel",
    "panelId": "PlayerUI",
    "canvasPath": "Canvas",
    "targetType": "manager",
    "targetManagerId": "PlayerStats",
    "commands": [
        {
            "name": "useHealthPotion",
            "label": "HP Potion",
            "commandType": "addResource",
            "commandParameter": "health",
            "resourceAmount": 50
        },
        {
            "name": "useManaPotion",
            "label": "MP Potion",
            "commandType": "addResource",
            "commandParameter": "mana",
            "resourceAmount": 30
        }
    ]
})
```

### Example 2: Tower Defense Economy

```python
# 1. Create economy manager
gamekitManager({
    "operation": "create",
    "managerId": "TowerDefenseEconomy",
    "managerType": "resourcepool",
    "initialResources": {
        "gold": 200,
        "lives": 20,
        "score": 0
    }
})

# 2. Create Machinations diagram
gamekitMachinations({
    "operation": "create",
    "diagramId": "TowerDefense",
    "assetPath": "Assets/Economy/TowerDefense.asset",
    "initialResources": [
        {"name": "gold", "initialAmount": 200, "minValue": 0, "maxValue": 999999},
        {"name": "lives", "initialAmount": 20, "minValue": 0, "maxValue": 20}
    ],
    "flows": [
        {
            "flowId": "passiveIncome",
            "resourceName": "gold",
            "ratePerSecond": 5.0,
            "isSource": True
        }
    ],
    "converters": [
        {
            "converterId": "buildBasicTower",
            "fromResource": "gold",
            "toResource": "defense",
            "conversionRate": 1,
            "inputCost": 50
        },
        {
            "converterId": "buildAdvancedTower",
            "fromResource": "gold",
            "toResource": "defense",
            "conversionRate": 3,
            "inputCost": 150
        }
    ],
    "triggers": [
        {
            "triggerName": "gameOver",
            "resourceName": "lives",
            "thresholdType": "below",
            "thresholdValue": 1
        }
    ]
})

# 3. Apply to manager
gamekitMachinations({
    "operation": "apply",
    "assetPath": "Assets/Economy/TowerDefense.asset",
    "managerId": "TowerDefenseEconomy"
})

# 4. Create build UI
gamekitUICommand({
    "operation": "createCommandPanel",
    "panelId": "BuildPanel",
    "canvasPath": "Canvas",
    "targetType": "manager",
    "targetManagerId": "TowerDefenseEconomy",
    "commands": [
        {
            "name": "buildBasic",
            "label": "Basic Tower (50g)",
            "commandType": "consumeResource",
            "commandParameter": "gold",
            "resourceAmount": 50
        },
        {
            "name": "buildAdvanced",
            "label": "Advanced Tower (150g)",
            "commandType": "consumeResource",
            "commandParameter": "gold",
            "resourceAmount": 150
        }
    ]
})
```

### Example 3: Turn-Based Strategy

```python
# 1. Create turn manager
gamekitManager({
    "operation": "create",
    "managerId": "BattleManager",
    "managerType": "turnBased",
    "turnPhases": ["PlayerTurn", "EnemyTurn", "ResolveEffects", "CheckVictory"]
})

# 2. Create tactical units
for i in range(3):
    gamekitActor({
        "operation": "create",
        "actorId": f"PlayerUnit{i}",
        "controlMode": "uiCommand",
        "behaviorProfile": "2dTileGrid",
        "position": {"x": i, "y": 0, "z": 0}
    })

# 3. Create unit command UI
gamekitUICommand({
    "operation": "createCommandPanel",
    "panelId": "UnitCommands",
    "canvasPath": "Canvas",
    "targetType": "actor",
    "targetActorId": "PlayerUnit0",  # Dynamically change target
    "commands": [
        {
            "name": "moveUp",
            "label": "Move Up",
            "commandType": "move",
            "moveDirection": {"x": 0, "y": 1, "z": 0}
        },
        {
            "name": "attack",
            "label": "Attack",
            "commandType": "action",
            "commandParameter": "attack"
        }
    ]
})

# 4. Create turn management UI
gamekitUICommand({
    "operation": "createCommandPanel",
    "panelId": "TurnPanel",
    "canvasPath": "Canvas",
    "targetType": "manager",
    "targetManagerId": "BattleManager",
    "commands": [
        {
            "name": "endTurn",
            "label": "End Turn",
            "commandType": "nextTurn"
        }
    ]
})
```

---

## Best Practices

### DO ✅

1. **Use Machinations for economies** - Model resource flows declaratively
2. **Separate input from behavior** - Use Actor's controller/behavior architecture
3. **UICommand for non-player control** - Perfect for strategy/tactics games
4. **Manager for centralized systems** - Resources, turns, states in one place
5. **Save/load with exportState/importState** - Easy persistence
6. **SceneFlow for complex transitions** - State machine-based scene management

### DON'T ❌

1. **Don't mix input in movement scripts** - Use Actor's event-driven design
2. **Don't scatter resources** - Centralize in ResourceManager
3. **Don't hardcode scene transitions** - Use SceneFlow
4. **Don't manually track game states** - Use StateManager
5. **Don't skip Machinations validation** - Check your economic balance

---

## Troubleshooting

### Actor not responding to input
- Check controlMode is `directController`
- Verify Input Actions asset is assigned
- Check behavior profile matches your setup (2D vs 3D)

### Manager resources not updating
- Verify manager exists with `inspect` operation
- Check resource names match exactly (case-sensitive)
- Ensure flows are enabled if using automatic generation

### UICommand buttons not working
- Check target Actor/Manager ID is correct
- Verify commandType matches target (Actor vs Manager commands)
- Ensure button onClick is properly connected

### Machinations flows not running
- Check `autoProcessFlows` is enabled in ResourceManager
- Verify flows are enabled (`SetFlowEnabled`)
- Ensure resource pools exist before flows start

---

**GameKit provides everything you need to build complete games. Start simple, scale up with assets!** 🎮

