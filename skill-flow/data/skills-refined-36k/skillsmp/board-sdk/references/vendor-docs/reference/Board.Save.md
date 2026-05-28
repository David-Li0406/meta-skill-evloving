# Board.Save Namespace

Save game system with automatic player associations and metadata management.

## Classes

- [BoardSaveGameManager](#boardsavegamemanager)
- [BoardSaveGameMetadata](#boardsavegamemetadata)
- [BoardSaveGameMetadataChange](#boardsavegamemetadatachange)
- [BoardSaveGameMetadataExtensions](#boardsavegamemetadataextensions)
- [BoardSaveGamePlayer](#boardsavegameplayer)
- [ImageProcessor](#imageprocessor)

## Structs

- [BoardAppStorageInfo](#boardappstorageinfo)
- [BoardSaveGameData](#boardsavegamedata)
- [BoardSaveGamePlayerData](#boardsavegameplayerdata)

---

## BoardSaveGameManager

Manages access to Board's saved game system.

```csharp
public static class BoardSaveGameManager
```

**Inheritance:** `Object` → `BoardSaveGameManager`

### Methods

#### CreateSaveGame(byte[], BoardSaveGameMetadataChange)

Creates a saved game with the specified payload and metadata.

```csharp
public static async Task<BoardSaveGameMetadata> CreateSaveGame(
    byte[] payload,
    BoardSaveGameMetadataChange metadata
)
```

**Parameters:**

- `payload` (byte[]) - Game state data (max 16 MB)
- `metadata` ([BoardSaveGameMetadataChange](#boardsavegamemetadatachange)) - Save metadata

**Returns:** `Task<BoardSaveGameMetadata>` - Metadata for the created save

**Remarks:** Save is automatically associated with all players in `BoardSession.players` at creation time.

**Throws:**

- `InvalidOperationException` - If save creation fails

---

#### GetAppStorageInfo()

Gets storage information for save games.

```csharp
public static async Task<BoardAppStorageInfo> GetAppStorageInfo()
```

**Returns:** `Task<BoardAppStorageInfo>` - Storage info including used, total, and remaining space

---

#### GetMaxAppStorage()

Gets the maximum allowed total storage size for all save games.

```csharp
public static long GetMaxAppStorage()
```

**Returns:** `long` - Maximum storage in bytes (64 MB)

---

#### GetMaxPayloadSize()

Gets the maximum allowed size for individual save game payloads.

```csharp
public static long GetMaxPayloadSize()
```

**Returns:** `long` - Maximum payload size in bytes (16 MB)

---

#### GetMaxSaveDescriptionLength()

Gets the maximum allowed length for save file descriptions.

```csharp
public static int GetMaxSaveDescriptionLength()
```

**Returns:** `int` - Maximum description length (100 characters)

---

#### GetSaveGamesMetadata()

Gets metadata for all save games for the current application.

```csharp
public static async Task<BoardSaveGameMetadata[]> GetSaveGamesMetadata()
```

**Returns:** `Task<BoardSaveGameMetadata[]>` - Array of save game metadata, sorted by `updatedAt` (most recent first)

---

#### LoadSaveGame(string)

Loads and returns a saved game's payload.

```csharp
public static async Task<byte[]> LoadSaveGame(string saveId)
```

**Parameters:**

- `saveId` (string) - Unique identifier of the save to load

**Returns:** `Task<byte[]>` - The save game payload

**Remarks:** Loading a save automatically activates the players associated with that save, modifying `BoardSession.players`. Subscribe to `BoardSession.playersChanged` to handle roster changes.

**Throws:**

- `InvalidOperationException` - If load fails

---

#### LoadSaveGameCoverImage(string)

Loads the cover image for a saved game.

```csharp
public static async Task<Texture2D> LoadSaveGameCoverImage(string saveId)
```

**Parameters:**

- `saveId` (string) - Unique identifier of the save

**Returns:** `Task<Texture2D>` - The cover image (432×243 pixels), or `null` if no image exists

**Throws:**

- `InvalidOperationException` - If load fails

---

#### RemoveActiveProfileFromSaveGame(string)

Removes only the active profile from the specified saved game.

```csharp
public static async Task<bool> RemoveActiveProfileFromSaveGame(string saveId)
```

**Parameters:**

- `saveId` (string) - Unique identifier of the save

**Returns:** `Task<bool>` - `true` if successful

**Remarks:** If no players remain associated after removal, the save is automatically deleted.

**Throws:**

- `InvalidOperationException` - If removal fails

---

#### RemovePlayersFromSaveGame(string)

Removes current session players from the specified saved game.

```csharp
public static async Task<bool> RemovePlayersFromSaveGame(string saveId)
```

**Parameters:**

- `saveId` (string) - Unique identifier of the save

**Returns:** `Task<bool>` - `true` if successful

**Remarks:** If no players remain associated after removal, the save is automatically deleted. There is no confirmation and no way to recover.

**Throws:**

- `InvalidOperationException` - If removal fails

---

#### UpdateSaveGame(string, byte[], BoardSaveGameMetadataChange)

Updates an existing saved game with new payload and metadata.

```csharp
public static async Task<BoardSaveGameMetadata> UpdateSaveGame(
    string saveId,
    byte[] payload,
    BoardSaveGameMetadataChange metadata
)
```

**Parameters:**

- `saveId` (string) - Unique identifier of the save to update
- `payload` (byte[]) - New game state data
- `metadata` ([BoardSaveGameMetadataChange](#boardsavegamemetadatachange)) - New metadata

**Returns:** `Task<BoardSaveGameMetadata>` - Updated metadata

**Throws:**

- `InvalidOperationException` - If update fails

---

## BoardSaveGameMetadata

Represents the metadata for a save game.

```csharp
public class BoardSaveGameMetadata
```

**Inheritance:** `Object` → `BoardSaveGameMetadata`

**Remarks:** Read-only properties are set by the native layer. Use [BoardSaveGameMetadataChange](#boardsavegamemetadatachange) to create/update metadata.

### Properties

#### coverImageChecksum

Gets the SHA-256 checksum of the cover image.

```csharp
public string coverImageChecksum { get; }
```

**Type:** `string`

---

#### createdAt

Gets the timestamp when the save was created.

```csharp
public ulong createdAt { get; }
```

**Type:** `ulong`

**Remarks:** Unix timestamp in milliseconds.

---

#### description

Gets the description of the saved game.

```csharp
public string description { get; }
```

**Type:** `string`

---

#### gameVersion

Gets the game version associated with this save.

```csharp
public string gameVersion { get; }
```

**Type:** `string`

---

#### hasCoverImage

Gets a value indicating whether this save has a cover image.

```csharp
public bool hasCoverImage { get; }
```

**Type:** `bool`

---

#### id

Gets the unique identifier of the saved game.

```csharp
public string id { get; }
```

**Type:** `string`

---

#### payloadChecksum

Gets the SHA-256 checksum of the save game payload.

```csharp
public string payloadChecksum { get; }
```

**Type:** `string`

---

#### playedTime

Gets how long players have played the saved game.

```csharp
public ulong playedTime { get; }
```

**Type:** `ulong`

**Remarks:** Duration in seconds.

---

#### playerIds

Gets the player identifiers associated with this save.

```csharp
public string[] playerIds { get; }
```

**Type:** `string[]`

---

#### players

Gets the collection of players associated with this save.

```csharp
public BoardSaveGamePlayer[] players { get; }
```

**Type:** [BoardSaveGamePlayer](#boardsavegameplayer)[]

---

#### updatedAt

Gets the timestamp when the save was last updated.

```csharp
public ulong updatedAt { get; }
```

**Type:** `ulong`

**Remarks:** Unix timestamp in milliseconds.

---

## BoardSaveGameMetadataChange

Encapsulates required metadata for save game creation and updates.

```csharp
public class BoardSaveGameMetadataChange
```

**Inheritance:** `Object` → `BoardSaveGameMetadataChange`

### Constructors

#### BoardSaveGameMetadataChange()

Initializes a new instance.

```csharp
public BoardSaveGameMetadataChange()
```

---

#### BoardSaveGameMetadataChange(string, Texture2D, ulong, string)

Initializes a new instance with specified values.

```csharp
public BoardSaveGameMetadataChange(
    string description,
    Texture2D coverImage,
    ulong playedTime,
    string gameVersion
)
```

**Parameters:**

- `description` (string) - Save description (max 100 characters)
- `coverImage` (Texture2D) - Cover image (will be converted to 432×243 PNG)
- `playedTime` (ulong) - Play time in seconds
- `gameVersion` (string) - Game version

### Properties

#### coverImage

Gets or sets the cover image.

```csharp
public Texture2D coverImage { get; set; }
```

**Type:** `Texture2D`

**Remarks:** Will be automatically converted to 432×243 PNG.

---

#### description

Gets or sets the description.

```csharp
public string description { get; set; }
```

**Type:** `string`

**Remarks:** Max 100 characters.

---

#### gameVersion

Gets or sets the game version.

```csharp
public string gameVersion { get; set; }
```

**Type:** `string`

---

#### playedTime

Gets or sets the played time.

```csharp
public ulong playedTime { get; set; }
```

**Type:** `ulong`

**Remarks:** Duration in seconds.

---

## BoardAppStorageInfo

Encapsulates app storage information on the Board device.

```csharp
public struct BoardAppStorageInfo
```

### Properties

#### remainingStorage

Gets the remaining storage available.

```csharp
public long remainingStorage { get; }
```

**Type:** `long`

**Remarks:** In bytes.

---

#### totalStorage

Gets the total storage allocated.

```csharp
public long totalStorage { get; }
```

**Type:** `long`

**Remarks:** In bytes (64 MB).

---

#### usagePercentage

Gets the storage usage as a percentage.

```csharp
public float usagePercentage { get; }
```

**Type:** `float`

**Remarks:** Range: 0.0 to 1.0

---

#### usedStorage

Gets the currently used storage.

```csharp
public long usedStorage { get; }
```

**Type:** `long`

**Remarks:** In bytes.

---

## BoardSaveGameMetadataExtensions

Provides extension methods for BoardSaveGameMetadata.

```csharp
public static class BoardSaveGameMetadataExtensions
```

### Methods

#### GetUniquePlayers(this BoardSaveGameMetadata[])

Gets unique players across multiple save games.

```csharp
public static BoardSaveGamePlayer[] GetUniquePlayers(
    this BoardSaveGameMetadata[] saves
)
```

**Parameters:**

- `saves` ([BoardSaveGameMetadata](#boardsavegamemetadata)[]) - Array of save game metadata

**Returns:** `BoardSaveGamePlayer[]` - Array of unique players

---

## BoardSaveGamePlayer

Represents player display information for save games.

```csharp
public class BoardSaveGamePlayer
```

**Inheritance:** `Object` → `BoardSaveGamePlayer`

**Remarks:** Contains player information stored with save game metadata. Used in [BoardSaveGameMetadata.players](#players-1).

### Properties

#### playerId

Gets the player's persistent app-specific identifier.

```csharp
public string playerId { get; }
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

#### avatarId

Gets the player's avatar identifier.

```csharp
public string avatarId { get; }
```

**Type:** `string`

---

#### type

Gets the player type.

```csharp
public BoardPlayerType type { get; }
```

**Type:** `BoardPlayerType`

---

## ImageProcessor

Utility class for processing images and converting between formats.

```csharp
public static class ImageProcessor
```

**Inheritance:** `Object` → `ImageProcessor`

**Remarks:** Provides standardized image handling for the Board SDK, including resizing and format conversion for save game cover images. Used internally by [BoardSaveGameManager](#boardsavegamemanager).

---

## BoardSaveGameData

Encapsulates save game data as defined in the native Board API.

```csharp
public struct BoardSaveGameData
```

**Remarks:** Internal struct using fixed byte arrays matching the native C++ `UnitySaveGameMetadata` structure. Used for marshalling save data between Unity and the Board platform. Most applications should use [BoardSaveGameMetadata](#boardsavegamemetadata) instead.

---

## BoardSaveGamePlayerData

Encapsulates save game player data as defined in the native Board API.

```csharp
public struct BoardSaveGamePlayerData
```

**Remarks:** Internal struct using fixed byte arrays matching the native C++ structure. Used for marshalling player data within save games. Most applications should use [BoardSaveGamePlayer](#boardsavegameplayer) instead.

---

## See Also

- [Board.Session](Board.Session.md) - Session and player management
- [Board.Core](Board.Core.md) - Pause menu with save option
