# Board.Core Namespace

Application lifecycle, pause menu, logging, and core functionality.

## Classes

- [BoardApplication](#boardapplication)
- [BoardAvatarManager](#boardavatarmanager)
- [BoardGeneralSettings](#boardgeneralsettings)
- [BoardLogger](#boardlogger)
- [BoardPlayer](#boardplayer)
- [BoardSupport](#boardsupport)
- [BoardUnityContext](#boardunitycontext)

## Structs

- [BoardPauseAudioTrack](#boardpauseaudiotrack)
- [BoardPauseCustomButton](#boardpausecustombutton)
- [BoardPauseScreenContext](#boardpausescreencontext)
- [BoardPauseScreenResult](#boardpausescreenresult)
- [BoardUnityContext.BoardEnvironmentConfig](#boardunitycontextboardenvironmentconfig)

## Enums

- [BoardLogLevel](#boardloglevel)
- [BoardPauseAction](#boardpauseaction)
- [BoardPauseButtonIcon](#boardpausebuttonicon)
- [BoardPlayerType](#boardplayertype)

## Delegates

- [BoardPlayerAvatarLoadedHandler](#boardplayeravatarloadedhandler)
- [PauseScreenActionReceivedHandler](#pausescreenactionreceivedhandler)
- [PauseScreenCustomButtonPressedHandler](#pausescreencustombuttonpressedhandler)

---

## BoardApplication

Provides access to the application's runtime data and settings.

```csharp
public static class BoardApplication
```

**Inheritance:** `Object` → `BoardApplication`

### Methods

#### ClearPauseScreenContext()

Clears the current pause screen context and resets tracked state.

```csharp
public static void ClearPauseScreenContext()
```

---

#### Exit()

Exits the application. Functions similar to swiping the application away from the Recent Apps screen.

```csharp
public static void Exit()
```

**Remarks:** This is a fire-and-forget operation; the app will be terminated immediately and cannot receive a response.

---

#### HideProfileSwitcher()

Hides the profile switcher button overlay.

```csharp
public static void HideProfileSwitcher()
```

---

#### Initialize()

Initializes the session client in the native Board input SDK.

```csharp
public static void Initialize()
```

---

#### SetPauseScreenContext(BoardPauseScreenContext)

Sets the pause screen context for the current application.

```csharp
public static void SetPauseScreenContext(BoardPauseScreenContext context)
```

**Parameters:**

- `context` ([BoardPauseScreenContext](#boardpausescreencontext)) - The pause screen context

**Remarks:** This performs a full replacement of all pause screen settings. Unspecified parameters will be set to their default values. Use [UpdatePauseScreenContext](#updatepausescreencontext) to update only specific fields while preserving others.

---

#### SetPauseScreenContext(string, bool?, BoardPauseCustomButton[], BoardPauseAudioTrack[])

Sets the pause screen context for the current game with full replacement.

```csharp
public static void SetPauseScreenContext(
    string applicationName = null,
    bool? showSaveOptionUponExit = null,
    BoardPauseCustomButton[] customButtons = null,
    BoardPauseAudioTrack[] audioTracks = null
)
```

**Parameters:**

- `applicationName` (string, optional) - Name displayed in pause menu (default: Application.productName)
- `showSaveOptionUponExit` (bool?, optional) - Show save option when exiting (default: false)
- `customButtons` ([BoardPauseCustomButton](#boardpausecustombutton)[], optional) - Custom action buttons (default: empty)
- `audioTracks` ([BoardPauseAudioTrack](#boardpauseaudiotrack)[], optional) - Audio volume sliders (default: empty)

**Remarks:** This replaces ALL pause screen settings. Unspecified optional parameters will use default values. To update only specific fields while preserving others, use [UpdatePauseScreenContext](#updatepausescreencontext) instead.

---

#### ShowProfileSwitcher()

Shows the profile switcher button overlay in the top-left corner.

```csharp
public static void ShowProfileSwitcher()
```

---

#### UpdatePauseScreenContext(string, bool?, BoardPauseCustomButton[], BoardPauseAudioTrack[])

Updates specific fields of the pause screen context while preserving others.

```csharp
public static void UpdatePauseScreenContext(
    string applicationName = null,
    bool? showSaveOptionUponExit = null,
    BoardPauseCustomButton[] customButtons = null,
    BoardPauseAudioTrack[] audioTracks = null
)
```

**Parameters:**

- `applicationName` (string, optional) - Name displayed in pause menu
- `showSaveOptionUponExit` (bool?, optional) - Show save option when exiting
- `customButtons` ([BoardPauseCustomButton](#boardpausecustombutton)[], optional) - Custom action buttons
- `audioTracks` ([BoardPauseAudioTrack](#boardpauseaudiotrack)[], optional) - Audio volume sliders

**Remarks:** Only the parameters you specify will be updated. All other settings remain unchanged. Pass an empty array to clear a field (e.g., `customButtons: new BoardPauseCustomButton[0]`).

### Events

#### customPauseScreenButtonPressed

Occurs when a custom button is pressed in Board's pause screen.

```csharp
public static event PauseScreenCustomButtonPressedHandler customPauseScreenButtonPressed
```

**Event Type:** [PauseScreenCustomButtonPressedHandler](#pausescreencustombuttonpressedhandler)

---

#### pauseScreenActionReceived

Occurs when an action is received from Board's pause screen.

```csharp
public static event PauseScreenActionReceivedHandler pauseScreenActionReceived
```

**Event Type:** [PauseScreenActionReceivedHandler](#pausescreenactionreceivedhandler)

---

## BoardLogger

Provides a mechanism for logging in the Unity layer of the Board SDK.

```csharp
public static class BoardLogger
```

**Inheritance:** `Object` → `BoardLogger`

### Methods

#### SetLogLevel(BoardLogLevel)

Sets the log level for the Board SDK.

```csharp
public static void SetLogLevel(BoardLogLevel level)
```

**Parameters:**

- `level` ([BoardLogLevel](#boardloglevel)) - The log level to set

---

## BoardPlayer

Represents a player on Board.

```csharp
public class BoardPlayer
```

**Inheritance:** `Object` → `BoardPlayer`

### Properties

#### avatar

Gets the avatar texture for the player.

```csharp
public Texture2D avatar { get; }
```

**Type:** `Texture2D`

**Remarks:** Loads asynchronously. Subscribe to [avatarLoaded](#avatarloaded) event for notification when loading completes.

---

#### avatarId

Gets the avatar identifier.

```csharp
public string avatarId { get; }
```

**Type:** `string`

---

#### name

Gets the player's display name.

```csharp
public string name { get; }
```

**Type:** `string`

---

#### playerId

Gets the persistent player identifier.

```csharp
public string playerId { get; }
```

**Type:** `string`

**Remarks:** This ID persists across sessions for the same profile playing the same app.

---

#### type

Gets the player type.

```csharp
public BoardPlayerType type { get; }
```

**Type:** [BoardPlayerType](#boardplayertype)

### Events

#### avatarLoaded

Occurs when the player's avatar finishes loading.

```csharp
public event BoardPlayerAvatarLoadedHandler avatarLoaded
```

**Event Type:** [BoardPlayerAvatarLoadedHandler](#boardplayeravatarloadedhandler)

### Static Methods

#### GetDefaultAvatar()

Gets the default avatar texture.

```csharp
public static async Task<Texture2D> GetDefaultAvatar()
```

**Returns:** `Task<Texture2D>` - The default avatar texture

---

## BoardPauseAudioTrack

Represents an audio track to display in Board's pause screen.

```csharp
public struct BoardPauseAudioTrack
```

### Fields

#### id

Unique identifier for the audio track (max 64 characters).

```csharp
public string id
```

**Type:** `string`

---

#### name

Display name shown to users (max 128 characters).

```csharp
public string name
```

**Type:** `string`

---

#### value

Volume level (0-100).

```csharp
public int value
```

**Type:** `int`

---

## BoardPauseCustomButton

Represents a custom button for Board's pause screen.

```csharp
public struct BoardPauseCustomButton
```

### Constructors

#### BoardPauseCustomButton(string, string, BoardPauseButtonIcon)

Creates a new custom pause button.

```csharp
public BoardPauseCustomButton(
    string id,
    string text,
    BoardPauseButtonIcon icon = BoardPauseButtonIcon.None
)
```

**Parameters:**

- `id` (string) - Unique identifier (max 64 characters)
- `text` (string) - Button text (max 128 characters)
- `icon` ([BoardPauseButtonIcon](#boardpausebuttonicon), optional) - Button icon (default: None)

---

## BoardLogLevel

Specifies the level of logging in the Board SDK.

```csharp
public enum BoardLogLevel
```

### Values

| Value     | Description                                  |
| --------- | -------------------------------------------- |
| `None`    | No logging                                   |
| `Error`   | Error messages only                          |
| `Warning` | Warnings and errors                          |
| `Info`    | Informational messages, warnings, and errors |
| `Verbose` | All log messages including debug info        |

---

## BoardPauseAction

Specifies the action type for a button in the Board pause screen.

```csharp
public enum BoardPauseAction
```

### Values

| Value             | Description                |
| ----------------- | -------------------------- |
| `Resume`          | User resumed the game      |
| `ExitGameSaved`   | User exited after saving   |
| `ExitGameUnsaved` | User exited without saving |
| `CustomButton`    | Custom button was pressed  |

---

## BoardPauseButtonIcon

Specifies the icon type for a button in the Board pause screen.

```csharp
public enum BoardPauseButtonIcon
```

### Values

| Value           | Usage                  |
| --------------- | ---------------------- |
| `None`          | No icon                |
| `CircularArrow` | Restart, retry actions |
| `Square`        | Stop actions           |
| `LeftArrow`     | Back, return actions   |
| `DoorWithArrow` | Exit, quit actions     |

---

## BoardPlayerType

Specifies the type of a player on Board.

```csharp
public enum BoardPlayerType
```

### Values

| Value     | Description                               |
| --------- | ----------------------------------------- |
| `Profile` | Persistent identity stored on Board       |
| `Guest`   | Temporary player for current session only |

---

## Delegates

### BoardPlayerAvatarLoadedHandler

Represents the method that will handle the avatarLoaded event.

```csharp
public delegate void BoardPlayerAvatarLoadedHandler(BoardPlayer player)
```

**Parameters:**

- `player` ([BoardPlayer](#boardplayer)) - The player whose avatar loaded

---

### PauseScreenActionReceivedHandler

Represents the method that will handle the pauseScreenActionReceived event.

```csharp
public delegate void PauseScreenActionReceivedHandler(
    BoardPauseAction action,
    BoardPauseAudioTrack[] audioTracks
)
```

**Parameters:**

- `action` ([BoardPauseAction](#boardpauseaction)) - The pause action that occurred
- `audioTracks` ([BoardPauseAudioTrack](#boardpauseaudiotrack)[]) - Updated audio track values

---

### PauseScreenCustomButtonPressedHandler

Represents the method that will handle the customPauseScreenButtonPressed event.

```csharp
public delegate void PauseScreenCustomButtonPressedHandler(
    string customButtonId,
    BoardPauseAudioTrack[] audioTracks
)
```

**Parameters:**

- `customButtonId` (string) - ID of the custom button that was pressed
- `audioTracks` ([BoardPauseAudioTrack](#boardpauseaudiotrack)[]) - Updated audio track values

---

## BoardAvatarManager

Manages avatar loading and caching for Board players.

```csharp
public static class BoardAvatarManager
```

**Inheritance:** `Object` → `BoardAvatarManager`

**Remarks:** Handles retrieval and caching of player avatar textures. This is used internally by [BoardPlayer](#boardplayer) for avatar loading.

---

## BoardGeneralSettings

Encapsulates general settings for the Board platform.

```csharp
public class BoardGeneralSettings : ScriptableObject
```

**Inheritance:** `ScriptableObject` → `BoardGeneralSettings`

**Remarks:** Configure via **Assets > Board > Settings > BoardGeneralSettings** in the Unity Editor.

### Properties

#### applicationId

Gets the Application ID for Board platform services.

```csharp
public string applicationId { get; }
```

**Type:** `string`

**Remarks:** Must be a globally unique identifier (UUID/GUID format recommended). Required for session management and save games. The build will fail if empty.

---

## BoardSupport

Provides runtime support utilities for the Board platform.

```csharp
public static class BoardSupport
```

**Inheritance:** `Object` → `BoardSupport`

**Remarks:** Internal utility class for Board platform detection and initialization.

---

## BoardUnityContext

Encapsulates Unity context for Board's native API.

```csharp
public static class BoardUnityContext
```

**Inheritance:** `Object` → `BoardUnityContext`

**Remarks:** Bridges Unity engine with native Board functionality. Used internally by the SDK.

---

## BoardPauseScreenContext

Encapsulates configuration for Board's pause screen.

```csharp
public struct BoardPauseScreenContext
```

### Fields

#### applicationName

Display name shown in the pause menu.

```csharp
public string applicationName
```

**Type:** `string`

---

#### showSaveOptionUponExit

Whether to show save option when exiting.

```csharp
public bool showSaveOptionUponExit
```

**Type:** `bool`

---

#### customButtons

Custom action buttons for the pause menu.

```csharp
public BoardPauseCustomButton[] customButtons
```

**Type:** [BoardPauseCustomButton](#boardpausecustombutton)[]

---

#### audioTracks

Audio volume sliders for the pause menu.

```csharp
public BoardPauseAudioTrack[] audioTracks
```

**Type:** [BoardPauseAudioTrack](#boardpauseaudiotrack)[]

---

## BoardPauseScreenResult

Represents the result from a Board pause menu interaction.

```csharp
public struct BoardPauseScreenResult
```

### Properties

#### action

Gets the action taken by the user.

```csharp
public BoardPauseAction action { get; }
```

**Type:** [BoardPauseAction](#boardpauseaction)

---

#### audioTracks

Gets the updated audio track values.

```csharp
public BoardPauseAudioTrack[] audioTracks { get; }
```

**Type:** [BoardPauseAudioTrack](#boardpauseaudiotrack)[]

---

#### customButtonId

Gets the ID of the custom button pressed (if applicable).

```csharp
public string customButtonId { get; }
```

**Type:** `string`

**Remarks:** Only populated when `action` is `BoardPauseAction.CustomButton`.

---

## See Also

- [Board.Input](Board.Input.md) - Touch input system
- [Board.Session](Board.Session.md) - Session management
- [Board.Save](Board.Save.md) - Save game system
