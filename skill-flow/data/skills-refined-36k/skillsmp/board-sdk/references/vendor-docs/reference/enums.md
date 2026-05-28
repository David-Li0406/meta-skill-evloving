# Enumerations Reference

Quick reference for all enumerations in the Board Unity SDK.

## Board.Core

### BoardLogLevel

```csharp
public enum BoardLogLevel
```

| Value   | Description                  |
| ------- | ---------------------------- |
| None    | No logging                   |
| Error   | Errors only                  |
| Warning | Warnings and errors          |
| Info    | Info, warnings, and errors   |
| Verbose | All messages including debug |

---

### BoardPauseAction

```csharp
public enum BoardPauseAction
```

| Value           | Description                |
| --------------- | -------------------------- |
| Resume          | User resumed game          |
| ExitGameSaved   | User exited after saving   |
| ExitGameUnsaved | User exited without saving |
| CustomButton    | Custom button pressed      |

---

### BoardPauseButtonIcon

```csharp
public enum BoardPauseButtonIcon
```

| Value         | Usage          |
| ------------- | -------------- |
| None          | No icon        |
| CircularArrow | Restart, retry |
| Square        | Stop           |
| LeftArrow     | Back, return   |
| DoorWithArrow | Exit, quit     |

---

### BoardPlayerType

```csharp
public enum BoardPlayerType
```

| Value   | Description                  |
| ------- | ---------------------------- |
| Profile | Persistent identity on Board |
| Guest   | Temporary session player     |

---

## Board.Input

### BoardContactPhase

```csharp
public enum BoardContactPhase
```

| Value          | Description                          |
| -------------- | ------------------------------------ |
| None (0)       | No activity registered               |
| Began (1)      | Contact just started                 |
| Moved (2)      | Contact position/orientation changed |
| Stationary (5) | Contact unchanged this frame         |
| Ended (3)      | Contact ended normally               |
| Canceled (4)   | Contact ended abnormally             |

**Extension Methods:**

- `IsActive()` - Returns true for Began, Moved, Stationary
- `IsEndedOrCanceled()` - Returns true for Ended, Canceled

---

### BoardContactType

```csharp
public enum BoardContactType
```

| Value      | Description                                  |
| ---------- | -------------------------------------------- |
| Finger (0) | Standard finger touch                        |
| Glyph (1)  | Physical Piece with rotation and touch state |
| Blob (2)   | Undefined blob (reserved)                    |

---

## See Also

- [Board.Core](Board.Core.md) - Core enumerations
- [Board.Input](Board.Input.md) - Input enumerations
