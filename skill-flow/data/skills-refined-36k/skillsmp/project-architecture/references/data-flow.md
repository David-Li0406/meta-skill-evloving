# Data Flow and State Ownership

## Input to State Flow

```text
BoardInput → InputManager → TokenManager → GameManager → GameState
  (SDK)       (events)       (translate)    (validate)    (store)
```

## State Ownership Rules

**CRITICAL**: View layer does NOT own game state.

| Component      | Owns                              | Does NOT Own             |
| -------------- | --------------------------------- | ------------------------ |
| `GameState`    | Token positions, phase, turn      | Visual representations   |
| `TokenManager` | TokenView instances, visual state | Token positions in state |
| `GameManager`  | Game rules, state transitions     | View updates             |
| `InputManager` | Contact tracking                  | Game logic               |

## Correct Event Flow

1. `InputManager` detects glyph placement, fires event
2. `TokenManager` receives event, requests action from `GameManager`
3. `GameManager` validates against rules, updates `GameState`
4. `GameManager` fires event (e.g., `OnTokenPlaced`)
5. `TokenManager` subscribes to event, updates `TokenView` visuals

## GameManager Events

```csharp
public event Action OnSetupComplete;
public event Action<TokenState> OnTokenPlaced;
public event Action<TokenState> OnTokenMoved;
public event Action<Player> OnTurnChanged;
public event Action<Player> OnGameOver;
```

## Anti-Patterns

- TokenManager directly updating GameState
- View components making game logic decisions
- InputManager containing game rules
- State modifications without going through GameManager
