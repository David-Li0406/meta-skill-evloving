# Player Management

Manage players and sessions in your Board game.

## Overview

Board supports multiple players in a single session. Each player has a profile with a name, avatar, and unique identifier. The SDK tracks who is playing and associates save games with the right players.

## Player Types

Board has two player types:

- Profile - A persistent identity stored on Board
- Guest - A temporary player for the current session only

Access the type via player.type:

```csharp
using Board.Core;
using Board.Session;

foreach (var player in BoardSession.players)
{
    if (player.type == BoardPlayerType.Profile)
    {
        // Persistent identity stored on Board
    }
    else if (player.type == BoardPlayerType.Guest)
    {
        // Temporary player for this session only
    }
}
```

## Accessing Session Players

The current players are available through BoardSession.players:

```csharp
using Board.Session;

// Get all players in the current session
BoardSessionPlayer[] players = BoardSession.players;

foreach (var player in players)
{
    Debug.Log($"Player: {player.name}");
}
```

At launch, BoardSession.players contains the active profile. The session always requires at least one Profile player. This constraint is enforced by Board and cannot be bypassed.

## Player Properties

Each BoardSessionPlayer provides:

- name (string) - Display name (not guaranteed unique)
- playerId (string) - App-specific persistent identifier
- sessionId (int) - Unique identifier for this session
- avatarId (string) - Avatar identifier
- avatar (Texture2D) - Avatar texture (loads asynchronously)
- type (BoardPlayerType) - Profile or Guest

### Player ID vs Session ID

- playerId - Persistent across sessions for the same profile playing the same app. Use for tracking player-specific data like high scores or preferences. Guest players have randomly generated playerId values that differ each session.

- sessionId - Unique only within the current session. Use for identifying players during gameplay.

```csharp
// For persistent player data, use playerId
PlayerPrefs.SetInt($"highscore_{player.playerId}", score);

// For session-specific tracking, use sessionId
playerStates[player.sessionId] = new PlayerState();
```

Note: When loading a save game, if a profile associated with that save no longer exists, Board replaces it with a Guest player. The Guest inherits the original sessionId but receives a new playerId. This preserves in-game state keyed by sessionId while breaking persistent data associations.

## Responding to Player Changes

Subscribe to BoardSession.playersChanged to react when players join or leave:

```csharp
void Start()
{
    BoardSession.playersChanged += OnPlayersChanged;
}

void OnDestroy()
{
    BoardSession.playersChanged -= OnPlayersChanged;
}

void OnPlayersChanged()
{
    // Refresh player list UI
    RefreshPlayerDisplay();

    // Check if expected players are still present
    ValidateGameState();
}
```

## Active Profile

The system-wide active profile is available separately:

```csharp
// Get the currently active Board profile
BoardPlayer activeProfile = BoardSession.activeProfile;

// React to profile changes
BoardSession.activeProfileChanged += OnActiveProfileChanged;
```

The active profile may or may not be in the current session's players array.

## Loading Avatars

Player avatars load asynchronously. Handle the avatarLoaded event:

```csharp
void DisplayPlayer(BoardSessionPlayer player)
{
    // Set placeholder or current avatar
    playerImage.texture = player.avatar;

    // Update when loaded
    player.avatarLoaded += OnAvatarLoaded;
}

void OnAvatarLoaded(BoardPlayer player)
{
    playerImage.texture = player.avatar;
}
```

For players not in the session (e.g., in save game UI), use the default avatar:

```csharp
var defaultAvatar = await BoardPlayer.GetDefaultAvatar();
unknownPlayerImage.texture = defaultAvatar;
```

## Adding Players

Present the player selector to add a player to the session:

```csharp
public async void OnAddPlayerButtonPressed()
{
    try
    {
        bool playerAdded = await BoardSession.PresentAddPlayerSelector();

        if (playerAdded)
        {
            Debug.Log("New player added to session");
            // playersChanged event will fire with updated list
        }
        else
        {
            Debug.Log("Player selector dismissed");
        }
    }
    catch (InvalidOperationException e)
    {
        Debug.LogError($"Failed to present player selector: {e.Message}");
    }
}
```

Note: Only one player selector can be open at a time. Attempting to open another throws an exception.

## Replacing Players

Replace or remove an existing player:

```csharp
public async void OnReplacePlayerPressed(BoardSessionPlayer player)
{
    try
    {
        bool replaced = await BoardSession.PresentReplacePlayerSelector(player);

        if (replaced)
        {
            Debug.Log("Player replaced or removed");
        }
    }
    catch (InvalidOperationException e)
    {
        Debug.LogError($"Failed to replace player: {e.Message}");
    }
}
```

### Replace Selector Behavior

The selector options change based on how many Profile players are in the session:

When replacing the only Profile in the session:

- No "Remove player" button appears
- No Guest option is shown
- The player can only be replaced with another Profile

When there are multiple Profiles in the session:

- "Remove player" button appears in the top-right corner
- Guest option is available alongside other Profiles
- The player can be replaced, removed, or swapped with a Guest

This behavior ensures the session always has at least one Profile player. The native selector enforces this constraint automatically.

Note: Only one player selector can be open at a time. Attempting to open another throws an InvalidOperationException.

## Resetting the Session

Reset players to the initial state (active profile only):

```csharp
public void OnResetPlayersPressed()
{
    bool success = BoardSession.ResetPlayers();

    if (success)
    {
        Debug.Log("Players reset to initial state");
    }
}
```

## Best Practices

- Use playerId for persistent data - Player IDs persist across sessions for the same profile. Use them for high scores, preferences, and unlocks.

- Use sessionId for in-game state - Session IDs are only unique within the current session. Use them for tracking player state during gameplay.

- Subscribe to playersChanged - React to players joining, leaving, or being replaced mid-session

- Handle guest replacements - When loading a save, deleted profiles are replaced with guests. The guest keeps the original sessionId but gets a new playerId.

## See Also

- Profile Switcher - Show the profile switching UI
- Save Game System - Associate saves with players
- Pause Menu - System pause screen integration
