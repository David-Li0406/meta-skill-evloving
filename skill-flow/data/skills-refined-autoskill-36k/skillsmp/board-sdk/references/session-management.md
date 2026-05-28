# Board Session Management

## Overview

`BoardSession` manages players in the current game session. Sessions always have at least one Profile player.

## Getting Players

```csharp
using Board.Session;

// Get all session players
BoardSessionPlayer[] players = BoardSession.players;

// Get active system profile (may not be in session)
BoardPlayer activeProfile = BoardSession.activeProfile;
```

## BoardSessionPlayer Properties

```csharp
string playerId     // Persistent app-specific ID (use for saves, prefs)
int sessionId       // Unique within current session only
string name         // Display name
string avatarId     // Avatar identifier
Texture2D avatar    // Avatar texture (loads async)
BoardPlayerType type // Profile or Guest
```

### Player Types

| Type      | Description                           |
| --------- | ------------------------------------- |
| `Profile` | Persistent identity stored on Board   |
| `Guest`   | Temporary player, new ID each session |

## Adding Players

```csharp
// Present native selector to add a player
bool added = await BoardSession.PresentAddPlayerSelector();
if (added)
{
    // New player is now in BoardSession.players
}
```

## Replacing/Removing Players

```csharp
var playerToReplace = BoardSession.players[1];

bool changed = await BoardSession.PresentReplacePlayerSelector(playerToReplace);
if (changed)
{
    // Player was replaced or removed
}
```

**Rules:**

- If replacing only Profile, can only select another Profile
- If multiple Profiles exist, can replace with Profile/Guest or remove
- At least one Profile always remains

## Resetting Session

```csharp
// Reset to just the active profile
BoardSession.ResetPlayers();
```

## Events

```csharp
// Players added/removed/replaced, or save loaded
BoardSession.playersChanged += () =>
{
    RefreshPlayerUI(BoardSession.players);
};

// System-wide active profile changed
BoardSession.activeProfileChanged += () =>
{
    var profile = BoardSession.activeProfile;
};
```

## Avatar Loading

Avatars load asynchronously:

```csharp
foreach (var player in BoardSession.players)
{
    if (player.avatar != null)
    {
        // Avatar already loaded
        SetPlayerAvatar(player.avatar);
    }
    else
    {
        player.avatarLoaded += (p) =>
        {
            SetPlayerAvatar(p.avatar);
        };
    }
}

// Or use default avatar
Texture2D defaultAvatar = await BoardPlayer.GetDefaultAvatar();
```

## Two-Player Setup for Zero-Day Attack

```csharp
async Task SetupTwoPlayers()
{
    // Start with active profile (always present)
    if (BoardSession.players.Length < 2)
    {
        // Add second player
        bool added = await BoardSession.PresentAddPlayerSelector();
        if (!added)
        {
            // User cancelled - could use AI or require second player
        }
    }

    var redPlayer = BoardSession.players[0];
    var bluePlayer = BoardSession.players.Length > 1
        ? BoardSession.players[1]
        : null;
}
```
