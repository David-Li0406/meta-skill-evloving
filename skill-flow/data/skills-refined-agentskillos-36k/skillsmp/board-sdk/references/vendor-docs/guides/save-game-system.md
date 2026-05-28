# Save Game System

Persistent save game storage with player associations.

## Overview

Board provides a save game system that:

- Automatically associates saves with session players
- Stores metadata (description, cover image, play time)
- Manages storage limits per app
- Handles player removal and save cleanup

All save operations are asynchronous.

## Save Metadata

Each BoardSaveGameMetadata contains:

- id (string) - Unique identifier for this save
- description (string) - User-visible description
- gameVersion (string) - Version that created the save
- createdAt (ulong) - Creation timestamp (Unix ms)
- updatedAt (ulong) - Last update timestamp (Unix ms)
- playedTime (ulong) - Total play time in seconds
- playerIds (string[]) - Associated player IDs
- players (BoardSaveGamePlayer[]) - Player info (name, avatar)
- hasCoverImage (bool) - Whether a cover image exists
- payloadChecksum (string) - Checksum of save data

## Creating a Save Game

Create a new save with payload and metadata:

```csharp
using Board.Save;

public async void SaveGame()
{
    // Serialize your game state
    byte[] payload = SerializeGameState();

    // Create metadata
    var metadata = new BoardSaveGameMetadataChange
    {
        description = "Chapter 3 - The Forest",
        gameVersion = Application.version,
        playedTime = (ulong)totalPlayTimeSeconds,
        coverImage = CaptureScreenshot()  // Optional Texture2D
    };

    try
    {
        var savedMetadata = await BoardSaveGameManager.CreateSaveGame(payload, metadata);
        Debug.Log($"Save created: {savedMetadata.id}");
    }
    catch (InvalidOperationException e)
    {
        Debug.LogError($"Save failed: {e.Message}");
    }
}
```

The save is automatically associated with all players currently in BoardSession.players at the moment of creation. You cannot specify players manually.

If you need to create a save for specific players, first modify the session roster using BoardSession.PresentAddPlayerSelector() or BoardSession.PresentReplacePlayerSelector().

## Loading a Save Game

Load save data by ID:

```csharp
public async void LoadGame(string saveId)
{
    try
    {
        byte[] payload = await BoardSaveGameManager.LoadSaveGame(saveId);

        // Deserialize and restore game state
        DeserializeGameState(payload);

        Debug.Log("Game loaded successfully");
    }
    catch (InvalidOperationException e)
    {
        Debug.LogError($"Load failed: {e.Message}");
    }
}
```

Important: Loading a save is not a read-only operation. Board automatically activates the players associated with that save, which modifies BoardSession.players.

If a profile no longer exists on Board, it is replaced with a Guest player that inherits the original sessionId but receives a new playerId.

Always subscribe to BoardSession.playersChanged to handle roster changes after loading.

## Listing Save Games

Get all saves for the current app:

```csharp
public async void DisplaySaveSlots()
{
    var saves = await BoardSaveGameManager.GetSaveGamesMetadata();

    foreach (var save in saves)
    {
        Debug.Log($"Save: {save.description}");
        Debug.Log($"  Created: {save.createdAt}");
        Debug.Log($"  Updated: {save.updatedAt}");
        Debug.Log($"  Play time: {save.playedTime} seconds");
        Debug.Log($"  Players: {save.playerIds.Length}");
    }
}
```

Saves are returned sorted by updatedAt (most recent first).

## Loading Cover Images

Load a save's cover image separately:

```csharp
public async void LoadCoverImage(BoardSaveGameMetadata save)
{
    if (!save.hasCoverImage)
    {
        coverImage.texture = defaultCover;
        return;
    }

    try
    {
        var texture = await BoardSaveGameManager.LoadSaveGameCoverImage(save.id);
        coverImage.texture = texture ?? defaultCover;
    }
    catch (InvalidOperationException e)
    {
        Debug.LogError($"Failed to load cover: {e.Message}");
        coverImage.texture = defaultCover;
    }
}
```

Cover images are standardized to 432×243 pixels.

## Updating a Save Game

Update an existing save with new data:

```csharp
public async void UpdateSave(string saveId)
{
    byte[] payload = SerializeGameState();

    var metadata = new BoardSaveGameMetadataChange
    {
        description = currentLevelName,
        gameVersion = Application.version,
        playedTime = (ulong)totalPlayTimeSeconds,
        coverImage = CaptureScreenshot()
    };

    try
    {
        var updated = await BoardSaveGameManager.UpdateSaveGame(saveId, payload, metadata);
        Debug.Log($"Save updated: {updated.updatedAt}");
    }
    catch (InvalidOperationException e)
    {
        Debug.LogError($"Update failed: {e.Message}");
    }
}
```

## Removing Players from Saves

Remove the current session players from a save:

```csharp
public async void RemoveFromSave(string saveId)
{
    try
    {
        bool success = await BoardSaveGameManager.RemovePlayersFromSaveGame(saveId);

        if (success)
        {
            Debug.Log("Players removed from save");
            // If no players remain, the save is deleted
        }
    }
    catch (InvalidOperationException e)
    {
        Debug.LogError($"Remove failed: {e.Message}");
    }
}
```

To remove only the active profile:

```csharp
await BoardSaveGameManager.RemoveActiveProfileFromSaveGame(saveId);
```

If no players remain associated with a save after removal, the save is automatically deleted. There is no confirmation and no way to recover the save. Check playerIds.Length before removal if you need to warn users.

## Storage Limits

Board enforces storage limits per app:

```csharp
public async void CheckStorage()
{
    // Get storage info
    var info = await BoardSaveGameManager.GetAppStorageInfo();
    Debug.Log($"Used: {info.usedStorage} bytes");
    Debug.Log($"Total: {info.totalStorage} bytes");
    Debug.Log($"Remaining: {info.remainingStorage} bytes");
    Debug.Log($"Usage: {info.usagePercentage:P0}");

    // Check limits
    long maxPayload = BoardSaveGameManager.GetMaxPayloadSize();
    int maxDescLength = BoardSaveGameManager.GetMaxSaveDescriptionLength();
    Debug.Log($"Max payload: {maxPayload} bytes");
    Debug.Log($"Max description: {maxDescLength} chars");
}
```

Limits:

- Max payload size: 16 MB
- Max total storage: 64 MB
- Max description length: 100 characters

Handle storage limits in your UI:

```csharp
public async void OnSavePressed()
{
    var info = await BoardSaveGameManager.GetAppStorageInfo();

    if (info.remainingStorage < estimatedSaveSize)
    {
        ShowStorageFullDialog();
        return;
    }

    await SaveGame();
}
```

## Player Associations

Saves are automatically linked to BoardSession.players when created. This enables:

- Filtering saves by current player
- Showing which players are in a save
- Restoring correct players when loading

### Finding Saves for Active Profile

```csharp
public async Task<BoardSaveGameMetadata[]> GetSavesForActiveProfile()
{
    var allSaves = await BoardSaveGameManager.GetSaveGamesMetadata();
    var activeId = BoardSession.activeProfile?.playerId;

    if (string.IsNullOrEmpty(activeId))
        return allSaves;

    return allSaves
        .Where(s => s.playerIds.Contains(activeId))
        .ToArray();
}
```

### Getting Unique Players Across Saves

```csharp
var saves = await BoardSaveGameManager.GetSaveGamesMetadata();
var uniquePlayers = saves.GetUniquePlayers();

foreach (var player in uniquePlayers)
{
    Debug.Log($"Player in saves: {player.name}");
}
```

## Capturing Cover Images

```csharp
Texture2D CaptureScreenshot()
{
    // Capture at save moment
    var rt = new RenderTexture(Screen.width, Screen.height, 24);
    Camera.main.targetTexture = rt;
    Camera.main.Render();

    RenderTexture.active = rt;
    var screenshot = new Texture2D(rt.width, rt.height, TextureFormat.RGB24, false);
    screenshot.ReadPixels(new Rect(0, 0, rt.width, rt.height), 0, 0);
    screenshot.Apply();

    Camera.main.targetTexture = null;
    RenderTexture.active = null;
    Destroy(rt);

    return screenshot;
}
```

The SDK automatically scales and converts to PNG. Target aspect ratio is 16:9.

## Best Practices

- Check storage limits before saving - Use GetAppStorageInfo() to verify space is available before attempting to save
- Subscribe to playersChanged after loading - Loading a save modifies BoardSession.players to match the save's associated players
- Warn before removing the last player - When no players remain associated with a save, it is automatically deleted with no confirmation
- Use UpdateSaveGame for existing saves - Track the current save ID and update rather than creating duplicates

## See Also

- Player Management - Understanding session players
- Pause Menu - Save option in pause screen
- Profile Switcher - Reload saves on profile change
