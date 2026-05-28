# Board Save Game System

## Overview

`BoardSaveGameManager` provides persistent save storage with automatic player association.

## Storage Limits

| Limit                  | Value            |
| ---------------------- | ---------------- |
| Max total storage      | 64 MB            |
| Max payload size       | 16 MB            |
| Max description length | 100 characters   |
| Cover image size       | 432 x 243 pixels |

## Creating a Save

```csharp
using Board.Save;

// Serialize game state
byte[] payload = SerializeGameState();

// Create metadata
var metadata = new BoardSaveGameMetadataChange
{
    description = "Turn 15 - Red leading",
    playedTime = (ulong)totalPlayTimeSeconds,
    gameVersion = Application.version,
    coverImage = CaptureCoverImage() // Optional, auto-resized to 432x243
};

// Create save (auto-associates with BoardSession.players)
BoardSaveGameMetadata save = await BoardSaveGameManager.CreateSaveGame(payload, metadata);

string saveId = save.id; // Use for future operations
```

## Loading a Save

```csharp
// Load payload
byte[] payload = await BoardSaveGameManager.LoadSaveGame(saveId);
DeserializeGameState(payload);

// IMPORTANT: Loading automatically updates BoardSession.players
// to match the saved player roster
```

## Updating a Save

```csharp
byte[] newPayload = SerializeGameState();
var newMetadata = new BoardSaveGameMetadataChange
{
    description = "Turn 23 - Blue winning",
    playedTime = (ulong)totalPlayTimeSeconds,
    gameVersion = Application.version
};

await BoardSaveGameManager.UpdateSaveGame(saveId, newPayload, newMetadata);
```

## Listing Saves

```csharp
// Get all saves (sorted by updatedAt, most recent first)
BoardSaveGameMetadata[] saves = await BoardSaveGameManager.GetSaveGamesMetadata();

foreach (var save in saves)
{
    Debug.Log($"{save.description} - {save.updatedAt}");
    Debug.Log($"Players: {string.Join(", ", save.players.Select(p => p.name))}");
}
```

## Loading Cover Images

```csharp
Texture2D cover = await BoardSaveGameManager.LoadSaveGameCoverImage(saveId);
if (cover != null)
{
    saveSlotImage.texture = cover;
}
```

## Removing Saves

```csharp
// Remove current session players from save
// (deletes save if no players remain)
await BoardSaveGameManager.RemovePlayersFromSaveGame(saveId);

// Remove only active profile from save
await BoardSaveGameManager.RemoveActiveProfileFromSaveGame(saveId);
```

## Checking Storage

```csharp
BoardAppStorageInfo info = await BoardSaveGameManager.GetAppStorageInfo();

Debug.Log($"Used: {info.usedStorage} bytes");
Debug.Log($"Remaining: {info.remainingStorage} bytes");
Debug.Log($"Usage: {info.usagePercentage * 100}%");

// Check limits
long maxTotal = BoardSaveGameManager.GetMaxAppStorage();      // 64 MB
long maxPayload = BoardSaveGameManager.GetMaxPayloadSize();   // 16 MB
int maxDesc = BoardSaveGameManager.GetMaxSaveDescriptionLength(); // 100
```

## BoardSaveGameMetadata Properties

```csharp
string id                   // Unique save identifier
string description          // User-facing description
ulong createdAt             // Unix timestamp (ms)
ulong updatedAt             // Unix timestamp (ms)
ulong playedTime            // Play time in seconds
string gameVersion          // App version when saved
bool hasCoverImage          // Whether cover exists
string payloadChecksum      // SHA-256 of payload
string coverImageChecksum   // SHA-256 of cover
BoardSaveGamePlayer[] players // Associated players
string[] playerIds          // Player ID array
```

## Player Association

- Saves are automatically associated with `BoardSession.players` at creation
- Loading a save updates `BoardSession.players` to match
- If a saved Profile was deleted, they become a Guest with same sessionId
- Subscribe to `BoardSession.playersChanged` to handle roster changes
