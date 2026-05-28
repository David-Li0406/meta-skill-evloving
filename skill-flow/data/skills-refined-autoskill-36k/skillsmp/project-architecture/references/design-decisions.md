# Design Decisions

## Why "TileManager" instead of "BoardManager"?

The Board SDK uses "Board" extensively (`BoardInput`, `BoardContact`, `BoardContactType`). Using "BoardManager" would create ambiguity about whether it's SDK code or game code. "TileManager" clearly describes its function.

## Why separate TileManager and TokenManager?

Different behaviors:

- **Tiles**: Placed once, stay fixed, part of board structure
- **Tokens**: Physical pieces players move, track real-world position via glyphs

Separation enables independent development and testing.

## Why InputManager as a singleton?

- Centralizes Board SDK dependency
- Provides consistent event interface
- Enables mock implementation for testing
- Single point for coordinate conversion

## Why ScriptableObjects for databases?

- Inspector-editable without code changes
- Asset references survive code refactoring
- Can be loaded via `Resources.Load()` in tests
- Clear separation of data from logic

## Why Board SDK Isolation?

Only `InputManager.cs` imports `Board.Input` namespace:

- Prevents SDK types leaking throughout codebase
- Enables testing without hardware
- Centralizes coordinate conversion (screen to world)

## Why Event-Based Communication?

GameManager fires events for state transitions:

- View components subscribe for visual updates
- Maintains separation between logic and presentation
- Allows multiple listeners without coupling
- Testable without UI
