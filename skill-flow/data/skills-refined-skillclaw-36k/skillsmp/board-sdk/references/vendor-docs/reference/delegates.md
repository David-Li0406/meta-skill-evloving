# Delegates Reference

Quick reference for all delegate types in the Board Unity SDK.

## Board.Core

### BoardPlayerAvatarLoadedHandler

Handler for avatar loaded events.

```csharp
public delegate void BoardPlayerAvatarLoadedHandler(BoardPlayer player)
```

**Parameters:**

- `player` - The player whose avatar loaded

**Used By:**

- `BoardPlayer.avatarLoaded` event

---

### PauseScreenActionReceivedHandler

Handler for pause screen action events.

```csharp
public delegate void PauseScreenActionReceivedHandler(
    BoardPauseAction action,
    BoardPauseAudioTrack[] audioTracks
)
```

**Parameters:**

- `action` - The pause action (Resume, ExitGameSaved, ExitGameUnsaved)
- `audioTracks` - Updated audio track values

**Used By:**

- `BoardApplication.pauseScreenActionReceived` event

**Example:**

```csharp
void OnPauseAction(BoardPauseAction action, BoardPauseAudioTrack[] audioTracks)
{
    switch (action)
    {
        case BoardPauseAction.Resume:
            ResumeGameplay();
            break;
        case BoardPauseAction.ExitGameSaved:
            await SaveGame();
            BoardApplication.Exit();
            break;
        case BoardPauseAction.ExitGameUnsaved:
            BoardApplication.Exit();
            break;
    }

    ApplyAudioSettings(audioTracks);
}
```

---

### PauseScreenCustomButtonPressedHandler

Handler for custom pause button events.

```csharp
public delegate void PauseScreenCustomButtonPressedHandler(
    string customButtonId,
    BoardPauseAudioTrack[] audioTracks
)
```

**Parameters:**

- `customButtonId` - ID of the custom button that was pressed
- `audioTracks` - Updated audio track values

**Used By:**

- `BoardApplication.customPauseScreenButtonPressed` event

**Example:**

```csharp
void OnCustomButton(string customButtonId, BoardPauseAudioTrack[] audioTracks)
{
    switch (customButtonId)
    {
        case "restart":
            RestartLevel();
            break;
        case "settings":
            OpenSettings();
            break;
    }

    ApplyAudioSettings(audioTracks);
}
```

---

## See Also

- [Board.Core](Board.Core.md) - Core delegates and events
