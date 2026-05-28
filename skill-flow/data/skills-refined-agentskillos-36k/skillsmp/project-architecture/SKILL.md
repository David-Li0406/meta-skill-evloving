---
name: project-architecture
description: This skill should be used when the user asks about "namespaces", "singleton", "TileManager", "GameManager", "TokenManager", "InputManager", "data flow", "class responsibilities", "layers", "folder structure", "code organization", "design patterns", "ScriptableObject", "databases", or discusses Zero-Day Attack codebase architecture and patterns.
version: 0.3.0
---

# Zero-Day Attack Project Architecture

Expert knowledge of the Zero-Day Attack Unity codebase structure, design patterns, and architectural decisions.

## Design Principles

### 1. Separation of Concerns

The codebase organizes into distinct layers:

| Layer      | Location              | Purpose                                      |
| ---------- | --------------------- | -------------------------------------------- |
| **Data**   | `Core/Data/`          | Immutable data structures, ScriptableObjects |
| **State**  | `Core/State/`         | Mutable runtime game state                   |
| **Logic**  | `Core/GameManager.cs` | Game rules, orchestration                    |
| **View**   | `View/`               | Visual representation, Unity components      |
| **Input**  | `Input/`              | Board SDK abstraction                        |
| **Config** | `Config/`             | Static layout constants                      |

**CRITICAL - State Ownership:**

| Component      | Owns                              | Does NOT Own                  |
| -------------- | --------------------------------- | ----------------------------- |
| `GameState`    | Token positions, game phase, turn | Visual representations        |
| `TokenManager` | TokenView instances, visuals      | Token positions in game state |
| `GameManager`  | Game rules, state transitions     | View updates                  |

**Anti-pattern:** View layer (TokenManager) directly updating GameState or making game logic decisions. Always route state changes through GameManager.

### 2. Board SDK Isolation

Only `InputManager.cs` imports `Board.Input` namespace. This:

- Prevents SDK types leaking throughout codebase
- Enables testing without hardware
- Centralizes coordinate conversion

### 3. Singleton Managers

Core systems use singleton pattern with `Instance` property:

```csharp
GameManager.Instance   // Game state and logic
TileManager.Instance   // Tile spawning, positioning
TokenManager.Instance  // Token spawning, input handling
InputManager.Instance  // Board SDK event broadcasting
```

### 4. ScriptableObject Databases

Game data stored in ScriptableObjects:

- `TileDatabase` - 25 tile definitions with sprites and paths
- `TokenDatabase` - 6 token definitions with sprites and glyph IDs

## Namespace Organization

| Namespace                   | Purpose                            |
| --------------------------- | ---------------------------------- |
| `ZeroDayAttack.Config`      | Layout constants (`LayoutConfig`)  |
| `ZeroDayAttack.Core`        | Game orchestration (`GameManager`) |
| `ZeroDayAttack.Core.Data`   | Data structures, enums, databases  |
| `ZeroDayAttack.Core.State`  | Runtime state classes              |
| `ZeroDayAttack.View`        | Visual components, managers        |
| `ZeroDayAttack.Input`       | Board SDK wrapper                  |
| `ZeroDayAttack.Diagnostics` | Debug utilities                    |
| `ZeroDayAttack.Editor`      | Editor-only tools                  |

### Namespace Rules

When creating new scripts:

- Place in appropriate namespace based on responsibility
- Use full namespace declaration: `namespace ZeroDayAttack.View { }`
- Editor scripts: `ZeroDayAttack.Editor`
- Test scripts: Match the namespace being tested

## Folder Structure

```text
Assets/Scripts/
├── Config/
│   └── LayoutConfig.cs              # Static layout constants
│
├── Core/
│   ├── GameManager.cs               # Game orchestrator singleton
│   ├── Data/                        # Immutable data structures
│   │   ├── Enums.cs                 # EdgeNode, PathColor, Player, etc.
│   │   ├── PathSegment.cs           # Path connection between nodes
│   │   ├── TileData.cs              # Tile definition
│   │   ├── TileDatabase.cs          # ScriptableObject: all tiles
│   │   ├── TokenData.cs             # Token definition
│   │   └── TokenDatabase.cs         # ScriptableObject: all tokens
│   └── State/                       # Mutable runtime state
│       ├── BoardState.cs            # Grid, reserves, deck
│       ├── GameState.cs             # Phase, current player
│       └── TokenState.cs            # Token position, ownership
│
├── View/                            # Visual components
│   ├── TileManager.cs               # Singleton: tile spawning
│   ├── TileView.cs                  # Individual tile visual
│   ├── TokenManager.cs              # Singleton: token spawning
│   ├── TokenView.cs                 # Individual token visual
│   ├── BackgroundRenderer.cs        # Board background
│   ├── CameraController.cs          # Camera setup
│   └── GridOverlayRenderer.cs       # Grid lines with glow
│
├── Input/
│   └── InputManager.cs              # Board SDK wrapper (ONLY Board.Input)
│
├── Diagnostics/
│   └── SceneDiagnostic.cs           # Runtime debug
│
└── Editor/
    ├── TileParser.cs                # Menu: ZeroDayAttack > Parse Tiles
    └── TokenParser.cs               # Menu: ZeroDayAttack > Parse Tokens
```

## Class Responsibilities

### Core Layer

| Class         | Responsibility                                                        |
| ------------- | --------------------------------------------------------------------- |
| `GameManager` | Initialize game, manage phases, orchestrate state. No direct visuals. |
| `GameState`   | Hold `BoardState`, `TokenState[]`, current player, phase, actions     |
| `BoardState`  | 5×5 grid (`TileData[,]`), reserves, deck, discard                     |
| `TokenState`  | Token identity, position (tile, node), physical tracking              |

### Data Layer

| Class           | Responsibility                                             |
| --------------- | ---------------------------------------------------------- |
| `TileData`      | Define tile: ID, sprite, segments, rotation, grid position |
| `TokenData`     | Define token: ID, sprite, owner, type, glyph ID            |
| `PathSegment`   | Connect two `EdgeNode` values with `PathColor`             |
| `TileDatabase`  | ScriptableObject with `List<TileData>`                     |
| `TokenDatabase` | ScriptableObject with 6 token slots                        |

### View Layer

| Class                 | Responsibility                                             |
| --------------------- | ---------------------------------------------------------- |
| `TileManager`         | Spawn tiles, grid-to-world conversion, hold `TileDatabase` |
| `TokenManager`        | Spawn tokens, handle glyph events, snap to nodes           |
| `TileView`            | MonoBehaviour on tile GameObjects, manage sprite           |
| `TokenView`           | MonoBehaviour on token GameObjects, manage position        |
| `BackgroundRenderer`  | Render board background                                    |
| `GridOverlayRenderer` | Draw 5×5 grid with glow effect                             |
| `CameraController`    | Configure orthographic camera                              |

### Input Layer

| Class          | Responsibility                                        |
| -------------- | ----------------------------------------------------- |
| `InputManager` | Poll `BoardInput`, fire events, coordinate conversion |

## Data Flow

```text
Board Hardware (touch/glyph)
         │
         ▼
    InputManager ← Only Board.Input import
         │
    ┌────┴────┐
    ▼         ▼
TokenManager  (Future: Tile touch)
    │
    ▼
GameManager ← Game logic decisions
    │
┌───┴───┐
▼       ▼
GameState  TileManager
BoardState (spawn tiles)
TokenState
```

### Event-Driven State Updates

GameManager should expose events for state transitions:

```csharp
// GameManager events
public event Action OnSetupComplete;
public event Action<TokenState> OnTokenPlaced;
public event Action<TokenState> OnTokenMoved;
public event Action<Player> OnTurnChanged;
```

**Flow Example (Token Placement):**

1. `InputManager` detects glyph, fires `OnContactBegan`
2. `TokenManager` receives event, calls `GameManager.PlaceToken()`
3. `GameManager` validates placement, updates `GameState`
4. `GameManager` fires `OnTokenPlaced` event
5. `TokenManager` (subscribed) updates visual position

## Scene Hierarchy

```text
GameplayScene
├── MainCamera [CameraController]
├── GlobalLight2D
├── GameManager [GameManager]
├── TileManager [TileManager]
├── TokenManager [TokenManager]
├── InputManager [InputManager]
├── BackgroundRenderer [BackgroundRenderer]
├── GridOverlayRenderer [GridOverlayRenderer]
├── Tiles (spawned at runtime)
└── Tokens (spawned at runtime)
```

## Coordinate Systems

### Grid Coordinates

- Origin: (0, 0) = bottom-left of 5×5 grid
- Range: (0, 0) to (4, 4)
- Center tile: (2, 2)

### World Coordinates

- Origin: (0, 0) = screen center = grid center
- Grid spans: -5.0 to +5.0 in X and Y
- Tile size: 2.0 world units

### Conversion

```csharp
// Grid to World (via LayoutConfig)
float x = LayoutConfig.GridLeft + (gridX * LayoutConfig.TileSize) + (LayoutConfig.TileSize / 2f);
float y = LayoutConfig.GridBottom + (gridY * LayoutConfig.TileSize) + (LayoutConfig.TileSize / 2f);
```

## Key Patterns

### Creating New Managers

Follow singleton pattern:

```csharp
public class NewManager : MonoBehaviour
{
    public static NewManager Instance { get; private set; }

    void Awake()
    {
        if (Instance != null) { Destroy(gameObject); return; }
        Instance = this;
    }
}
```

### Creating New Data Types

For immutable data in `Core/Data/`:

```csharp
namespace ZeroDayAttack.Core.Data
{
    [System.Serializable]
    public class NewData
    {
        public string Id;
        // Serialized fields...
    }
}
```

### Creating New View Components

For visual components in `View/`:

```csharp
namespace ZeroDayAttack.View
{
    public class NewView : MonoBehaviour
    {
        [SerializeField] private SpriteRenderer spriteRenderer;
        // View logic...
    }
}
```

## Design Rationale

Key architectural decisions and their reasoning:

| Decision                         | Why                                                                   |
| -------------------------------- | --------------------------------------------------------------------- |
| **TileManager not BoardManager** | Avoids confusion with Board SDK (`BoardInput`, `BoardContact`)        |
| **Separate Tile/Token managers** | Different behaviors: tiles fixed, tokens move with players            |
| **InputManager singleton**       | Centralizes SDK, enables mocking, single coordinate conversion        |
| **ScriptableObject databases**   | Inspector-editable, survives refactoring, testable via Resources.Load |
| **Board SDK isolation**          | Only InputManager imports SDK, enables testing without hardware       |
| **Event-based communication**    | Decouples logic from presentation, multiple listeners                 |

For full rationale with examples, see `design-decisions.md` in references.

## Reference Files

This skill's `references/` folder contains:

| File                        | Contains                                              | Read When                           |
| --------------------------- | ----------------------------------------------------- | ----------------------------------- |
| `layer-model.md`            | The 6 layers: Data, State, Logic, View, Input, Config | Understanding layer boundaries      |
| `data-flow.md`              | State ownership diagram, event patterns               | Implementing state changes          |
| `class-responsibilities.md` | GameManager, TileManager, TokenManager, InputManager  | Adding features to existing classes |
| `scene-hierarchy.md`        | GameplayScene structure, GameObject organization      | Modifying scene or adding objects   |
| `design-decisions.md`       | Why singletons, naming conventions, SDK isolation     | Making architectural decisions      |

## Key Source Files

When modifying architecture, review:

| File              | Purpose                        |
| ----------------- | ------------------------------ |
| `LayoutConfig.cs` | All layout constants           |
| `GameManager.cs`  | Game orchestration singleton   |
| `TileManager.cs`  | Tile spawning, grid conversion |
| `InputManager.cs` | Board SDK wrapper              |
