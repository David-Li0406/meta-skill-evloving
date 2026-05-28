# Board.Session Namespace

Session and player management for multiplayer experiences.

## Classes

- [BoardSession](#boardsession)
- [BoardSessionPlayer](#boardsessionplayer)

## Structs

- [BoardSessionPlayerData](#boardsessionplayerdata)

---

## BoardSession

Provides access to Board's app session.

```csharp
public static class BoardSession
```

**Inheritance:** `Object` → `BoardSession`

### Properties

#### activeProfile

Gets the system-wide active profile.

```csharp
public static BoardPlayer activeProfile { get; }
```

**Type:** `BoardPlayer`

**Remarks:** The active profile may or may not be in the current session's players array.

---

#### players

Gets the array of active players in the current session.

```csharp
public static BoardSessionPlayer[] players { get; }
```

**Type:** [BoardSessionPlayer](#boardsessionplayer)[]

**Remarks:** At launch, contains the active profile. The session always requires at least one Profile player.

### Methods

#### PresentAddPlayerSelector()

Presents the native player selector to add a new player to the current session.

```csharp
public static async Task<bool> PresentAddPlayerSelector()
```

**Returns:** `Task<bool>` - `true` if a player was added; `false` if dismissed

**Throws:**

- `InvalidOperationException` - If a player selector is already open

**Remarks:** Only one player selector can be open at a time.

---

#### PresentReplacePlayerSelector(BoardSessionPlayer)

Presents the native player selector to replace or remove an existing player.

```csharp
public static async Task<bool> PresentReplacePlayerSelector(
    BoardSessionPlayer player
)
```

**Parameters:**

- `player` ([BoardSessionPlayer](#boardsessionplayer)) - The player to replace or remove

**Returns:** `Task<bool>` - `true` if the player was replaced or removed; `false` if dismissed

**Throws:**

- `InvalidOperationException` - If a player selector is already open

**Remarks:**

- If replacing the only Profile in the session, only other Profiles can be selected (no Guest option, no Remove button)
- If multiple Profiles exist, can replace with Profile/Guest or remove the player
- This ensures at least one Profile always remains in the session

---

#### ResetPlayers()

Resets the session players to the initial state (active profile only).

```csharp
public static bool ResetPlayers()
```

**Returns:** `bool` - `true` if successful

### Events

#### activeProfileChanged

Occurs when the system-wide active profile changes.

```csharp
public static event Action activeProfileChanged
```

**Event Type:** `Action`

---

#### playersChanged

Occurs when the active players in the session change.

```csharp
public static event Action playersChanged
```

**Event Type:** `Action`

**Remarks:** Fired when players are added, removed, replaced, or when loading a save game changes the player roster.

---

## BoardSessionPlayer

Represents a player in a Board session.

```csharp
public sealed class BoardSessionPlayer : BoardPlayer
```

**Inheritance:** `Object` → `BoardPlayer` → `BoardSessionPlayer`

### Properties

#### playerId

Gets the player's persistent app-specific identifier.

```csharp
public string playerId { get; }
```

**Type:** `string`

**Remarks:**

- Persists across sessions for the same profile playing the same app
- Use for persistent data like high scores and preferences
- Guest players have randomly generated values that differ each session

---

#### sessionId

Gets the player's unique identifier in the current session.

```csharp
public int sessionId { get; }
```

**Type:** `int`

**Remarks:**

- Only unique within the current session
- Use for tracking player state during gameplay
- When loading a save with deleted profiles, guests inherit the original sessionId but get new playerId

### Inherited Properties

From [BoardPlayer](Board.Core.md#boardplayer):

- `name` (string) - Display name
- `avatarId` (string) - Avatar identifier
- `avatar` (Texture2D) - Avatar texture (loads asynchronously)
- `type` (BoardPlayerType) - Profile or Guest

### Inherited Events

From [BoardPlayer](Board.Core.md#boardplayer):

- `avatarLoaded` - Occurs when avatar finishes loading

---

## BoardSessionPlayerData

Encapsulates session player data as defined in the native Board API.

```csharp
public struct BoardSessionPlayerData
```

**Remarks:** Internal struct using fixed byte arrays matching the native C++ structure. Used for marshalling player data between Unity and the Board platform. Most applications should use [BoardSessionPlayer](#boardsessionplayer) instead.

---

## See Also

- [Board.Core](Board.Core.md) - BoardPlayer base class, profile switcher
- [Board.Save](Board.Save.md) - Save games with player associations
