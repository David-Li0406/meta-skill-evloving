# Profile Switcher

The Board SDK provides a native profile switcher button that allows users to switch between their Board profiles without leaving your game.

## Overview

The profile switcher is a native overlay button that appears in the top-left corner of your game screen. It provides a quick way for users to switch between different Board profiles during appropriate moments in your game.

## Basic Usage

### Show the Profile Switcher

Display the profile switcher button overlay:

```csharp
BoardApplication.ShowProfileSwitcher();
```

### Hide the Profile Switcher

Remove the profile switcher button overlay:

```csharp
BoardApplication.HideProfileSwitcher();
```

## Behavior

- Persistent overlay - The button remains visible on top of your game UI until you explicitly hide it
- Fixed position - Always appears in the top-left corner of the screen
- Native control - Managed by Board's native SDK, not part of your Unity UI hierarchy
- Profile switching - When tapped, opens the native profile selector for switching profiles
- Automatic updates - When a profile switch occurs, BoardSession.playersChanged event fires and BoardSession.players is automatically updated

## When to Show/Hide

### Show During:

- Main menus - Allow users to switch profiles before starting a game
- Lobby screens - Enable profile switching in multiplayer lobbies
- Settings screens - Provide access when users are configuring options
- Pause menus - Allow switching during non-critical moments
- Results/score screens - Enable switching after completing a level or match

### Hide During:

- Active gameplay - Prevent accidental profile switches during play
- Cutscenes - Avoid UI clutter during story moments
- Loading screens - Keep the UI minimal during transitions
- Dialogs/popups - Hide when other UI needs focus
- Tutorial sequences - Prevent interruptions during onboarding

## Listening for Profile Changes

Subscribe to the playersChanged event to react when users switch profiles:

```csharp
using UnityEngine;
using Board.Session;

public class ProfileManager : MonoBehaviour
{
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
        Debug.Log("Active profile changed!");

        var players = BoardSession.players;
        if (players != null && players.Length > 0)
        {
            var activeProfile = players[0];
            Debug.Log($"New active profile: {activeProfile.name}");

            // Reload player data, preferences, save games, etc.
            LoadPlayerData(activeProfile.playerId);
        }
    }

    void LoadPlayerData(string playerId)
    {
        // Load player-specific data (save games, settings, progress, etc.)
    }
}
```

## Best Practices

- Hide during gameplay - Prevent accidental profile switches by hiding the button during active gameplay
- Subscribe to playersChanged - Always listen for profile changes to update your game state
- Reload player data on switch - When a profile changes, reload save games, preferences, and player-specific settings
