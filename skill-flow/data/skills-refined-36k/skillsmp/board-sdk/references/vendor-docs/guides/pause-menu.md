# Pause Menu

The Board SDK provides a native pause menu that integrates seamlessly with your Unity game. This guide covers how to configure and handle the pause menu.

## Overview

The pause menu API allows you to:

- Display your game's name in the pause menu
- Add custom action buttons with icons
- Provide audio volume sliders for music and sound effects
- Show a save option when exiting and receive confirmation when the user wants to save
- Receive callbacks when users interact with the menu

## How the Pause Menu Works

The pause menu is a pass-through system. Board renders the menu UI and captures user input, but your game handles all the actual logic. When a user taps a button, Board sends you a callback. Your code decides what happens next.

### Built-in Buttons

Board provides these buttons automatically:

- Resume - Always shown - Your responsibility: Unpause gameplay (e.g., restore Time.timeScale)
- Exit to Library - Always shown - Your responsibility: Perform any cleanup, then call BoardApplication.Exit()
- Exit & Save - Only when showSaveOptionUponExit is true - Your responsibility: Save the game, then call BoardApplication.Exit()

You cannot customize or remove these built-in buttons. You can only add custom buttons alongside them.

### Developer Responsibilities

Board does not take any actions on your behalf. You must:

- Pause your game when the menu opens (Board does not pause for you)
- Resume gameplay when the user taps Resume (restore Time.timeScale, unpause audio, etc.)
- Save the game when the user taps Exit & Save (use BoardSaveGameManager)
- Terminate the app when the user exits (call BoardApplication.Exit())
- Apply audio settings from the callback parameters

Warning: BoardApplication.Exit() is fire-and-forget. Once called, the app will terminate. The method does not return or allow additional processing.

## Basic Setup

### 1. Configure the Pause Menu

Call BoardApplication.SetPauseScreenContext() to configure your pause menu. All parameters are optional:

```csharp
using Board.Core;

// Full configuration
BoardApplication.SetPauseScreenContext(
    applicationName: "My Awesome Game",
    showSaveOptionUponExit: true,  // Show "Save & Exit" option
    customButtons: myButtons,       // Your custom buttons (see below)
    audioTracks: myAudioTracks     // Audio volume sliders (see below)
);
```

### 2. Register Event Handlers

Subscribe to events to handle user actions:

```csharp
void Start()
{
    BoardApplication.customPauseScreenButtonPressed += OnCustomButtonPressed;
    BoardApplication.pauseScreenActionReceived += OnPauseMenuAction;
}

void OnDestroy()
{
    BoardApplication.customPauseScreenButtonPressed -= OnCustomButtonPressed;
    BoardApplication.pauseScreenActionReceived -= OnPauseMenuAction;
}
```

## Configuration Options

### Application Appearance

- gameName (string, optional) - The title displayed in the pause menu. Defaults to Application.productName

- showSaveOptionUponExit (bool, optional) - Whether to show the "Save & Exit" option when the user presses Exit to Library from the pause screen. Defaults to false. When enabled, users can save their progress before exiting

### Custom Buttons

Create custom action buttons with the BoardPauseCustomButton constructor:

```csharp
var customButtons = new BoardPauseCustomButton[]
{
    new BoardPauseCustomButton("restart", "Restart Level", BoardPauseButtonIcon.CircularArrow),
    new BoardPauseCustomButton("quit", "Quit to Menu", BoardPauseButtonIcon.DoorWithArrow),
    new BoardPauseCustomButton("settings", "Settings", BoardPauseButtonIcon.Square),
    new BoardPauseCustomButton("info", "About")  // No icon
};
```

Constructor Parameters:

- id (string) - Unique identifier you'll receive in callbacks (max 64 characters)
- text (string) - Button text shown to users (max 128 characters)
- icon (BoardPauseButtonIcon, optional) - Icon to display (defaults to None)

Available Icons:

- BoardPauseButtonIcon.None - No icon
- BoardPauseButtonIcon.CircularArrow - Restart, retry
- BoardPauseButtonIcon.Square - Stop
- BoardPauseButtonIcon.LeftArrow - Back, return
- BoardPauseButtonIcon.DoorWithArrow - Exit, quit

Button Layout: Custom buttons appear in rows of two. If you have an even number of buttons, all buttons are half-width. If you have an odd number, the last button spans full width (like the built-in Resume and Exit to Library buttons).

### Audio Tracks

Define audio volume sliders using struct initialization:

```csharp
var audioTracks = new BoardPauseAudioTrack[]
{
    new BoardPauseAudioTrack { id = "music", name = "Music", value = 75 },
    new BoardPauseAudioTrack { id = "sfx", name = "Sound Effects", value = 85 },
    new BoardPauseAudioTrack { id = "voice", name = "Voice", value = 100 }
};
```

Fields:

- id (string) - Unique identifier (max 64 characters)
- name (string) - Label shown to users (max 128 characters)
- value (int) - Initial volume level (0-100)

## Handling User Actions

### Custom Button Callback

Implement the customPauseScreenButtonPressed event handler:

```csharp
private void OnCustomButtonPressed(string customButtonId, BoardPauseAudioTrack[] audioTracks)
{
    switch (customButtonId)
    {
        case "restart":
            RestartLevel();
            break;
        case "quit":
            ReturnToMainMenu();
            break;
        case "settings":
            OpenSettingsMenu();
            break;
    }

    // Apply updated audio settings
    ApplyAudioSettings(audioTracks);
}
```

Parameters:

- customButtonId - The id of the custom button that was pressed
- audioTracks - Updated audio track values after user adjustments

### Standard Pause Actions

Implement the pauseScreenActionReceived event handler:

```csharp
private async void OnPauseMenuAction(BoardPauseAction pauseAction, BoardPauseAudioTrack[] audioTracks)
{
    switch (pauseAction)
    {
        case BoardPauseAction.Resume:
            // User resumed the game
            ResumeGameplay();
            break;

        case BoardPauseAction.ExitGameSaved:
            // User chose to save and exit
            // You must save the game - Board does not save automatically
            await SaveGame();
            BoardApplication.Exit();
            break;

        case BoardPauseAction.ExitGameUnsaved:
            // User chose to exit without saving
            BoardApplication.Exit();
            break;
    }

    // Apply updated audio settings
    ApplyAudioSettings(audioTracks);
}
```

BoardPauseAction Values:

- BoardPauseAction.Resume - User resumed the game
- BoardPauseAction.ExitGameSaved - User exited after saving (only if showSaveOptionUponExit is true)
- BoardPauseAction.ExitGameUnsaved - User exited without saving
- BoardPauseAction.CustomButton - Custom button was pressed (handled by customButtonPressed event)

## Updating the Pause Menu

The Board SDK provides two methods for modifying the pause menu:

### Full Replacement with SetPauseScreenContext

SetPauseScreenContext() performs a full replacement of all pause menu settings. Unspecified optional parameters will use their default values:

Default Values:

- applicationName → Application.productName
- showSaveOptionUponExit → false
- customButtons → Empty array (no buttons)
- audioTracks → Empty array (no sliders)

```csharp
// Initial setup - sets all values
BoardApplication.SetPauseScreenContext(
    applicationName: "My Game",
    customButtons: menuButtons,
    audioTracks: myAudioTracks
);

// This REPLACES everything - custom buttons change, but audio tracks are CLEARED!
BoardApplication.SetPauseScreenContext(customButtons: gameplayButtons);
// Result: customButtons = gameplayButtons, audioTracks = []
```

### Partial Updates with UpdatePauseScreenContext

UpdatePauseScreenContext() performs a partial update, preserving any settings you don't specify:

```csharp
// Initial setup
BoardApplication.SetPauseScreenContext(
    applicationName: "My Game",
    customButtons: menuButtons,
    audioTracks: myAudioTracks
);

// Update ONLY buttons - audio tracks, colors, etc. are preserved
BoardApplication.UpdatePauseScreenContext(customButtons: gameplayButtons);

// Enable save option when player makes progress - everything else unchanged
BoardApplication.UpdatePauseScreenContext(showSaveOptionUponExit: true);

// Update multiple fields at once - unspecified fields are preserved
BoardApplication.UpdatePauseScreenContext(customButtons: bossButtons);
```

### Clearing Fields

To explicitly clear a field during an update, pass an empty array:

```csharp
// Remove all custom buttons but keep everything else
BoardApplication.UpdatePauseScreenContext(customButtons: new BoardPauseCustomButton[0]);

// Remove audio tracks
BoardApplication.UpdatePauseScreenContext(audioTracks: new BoardPauseAudioTrack[0]);
```

### When to Use Each Method

Use SetPauseScreenContext():

- Initial setup when you want to configure everything
- When transitioning to a completely different pause menu configuration
- When you want to reset to defaults

Use UpdatePauseScreenContext():

- Changing buttons based on game state (menu vs gameplay vs boss fight)
- Toggling save option based on player progress
- Updating any single field without affecting others

## Best Practices

- Set up the pause menu early - Configure it in your game's initialization or main menu scene
- Use UpdatePauseScreenContext for dynamic changes - When changing buttons or options based on game state, use UpdatePauseScreenContext() to preserve other settings
- Use SetPauseScreenContext for complete resets - When transitioning between major game modes (menu to gameplay), use SetPauseScreenContext() to ensure a clean slate
- Always apply audio settings - Both callbacks provide updated audio track values - apply them to your audio system
- Use meaningful button IDs - Choose clear, descriptive IDs for easier switch statement handling
- Choose appropriate icons - Match icons to button actions for better UX
- Handle all pause actions - Implement cases for Resume, ExitGameSaved, and ExitGameUnsaved

## Clearing the Pause Menu

To completely remove the pause menu context:

```csharp
BoardApplication.ClearPauseScreenContext();
```

## Default Behavior

The Board SDK automatically sets a default pause menu context during initialization:

- Application name: Application.productName
- No save option
- No custom buttons
- No audio tracks

You can override this at any time by calling BoardApplication.SetPauseScreenContext().
