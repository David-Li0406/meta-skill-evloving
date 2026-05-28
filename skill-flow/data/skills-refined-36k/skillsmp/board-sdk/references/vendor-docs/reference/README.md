# Board Unity SDK - API Reference

Complete API documentation for the Board Unity SDK.

## Namespaces

### [Board.Core](Board.Core.md)

Core application functionality including pause menu, profile switching, and logging.

**Key Classes:**

- [BoardApplication](Board.Core.md#boardapplication) - Application lifecycle and pause menu
- [BoardLogger](Board.Core.md#boardlogger) - Logging utilities
- [BoardPlayer](Board.Core.md#boardplayer) - Player representation

### [Board.Input](Board.Input.md)

Touch input system for finger and Piece detection.

**Key Classes:**

- [BoardInput](Board.Input.md#boardinput) - Main input API
- [BoardContact](Board.Input.md#boardcontact) - Represents a touch contact
- [BoardInputSettings](Board.Input.md#boardinputsettings) - Input configuration

### [Board.Input.Debug](Board.Input.Debug.md)

Debug visualization for touch input.

**Key Classes:**

- [BoardInputDebugView](Board.Input.Debug.md#boardinputdebugview) - Debug overlay UI

### [Board.Input.Simulation](Board.Input.Simulation.md)

Editor simulation tools for testing without hardware.

**Key Classes:**

- [BoardContactSimulation](Board.Input.Simulation.md#boardcontactsimulation) - Simulation controller
- [BoardContactSimulationSettings](Board.Input.Simulation.md#boardcontactsimulationsettings) - Simulation configuration

### [Board.Save](Board.Save.md)

Save game system with player associations.

**Key Classes:**

- [BoardSaveGameManager](Board.Save.md#boardsavegamemanager) - Save game operations
- [BoardSaveGameMetadata](Board.Save.md#boardsavegamemetadata) - Save metadata

### [Board.Session](Board.Session.md)

Session and player management.

**Key Classes:**

- [BoardSession](Board.Session.md#boardsession) - Session management
- [BoardSessionPlayer](Board.Session.md#boardsessionplayer) - Player in session

## Common Enumerations

See [enums.md](enums.md) for complete enumeration reference.

- **BoardContactType** - Finger or Glyph
- **BoardContactPhase** - Began, Moved, Stationary, Ended, Canceled
- **BoardPlayerType** - Profile or Guest
- **BoardPauseAction** - Resume, ExitGameSaved, ExitGameUnsaved
- **BoardLogLevel** - None, Error, Warning, Info, Verbose

## Common Workflows

### Getting Touch Input

```csharp
using Board.Input;

// Get all active contacts
var contacts = BoardInput.GetActiveContacts();

// Filter by type
var fingers = BoardInput.GetActiveContacts(BoardContactType.Finger);
var pieces = BoardInput.GetActiveContacts(BoardContactType.Glyph);
```

### Managing Players

```csharp
using Board.Session;

// Get current players
var players = BoardSession.players;

// Add a player
bool added = await BoardSession.PresentAddPlayerSelector();

// Listen for changes
BoardSession.playersChanged += OnPlayersChanged;
```

### Save Games

```csharp
using Board.Save;

// Create a save
var metadata = new BoardSaveGameMetadataChange
{
    description = "Level 5",
    gameVersion = Application.version,
    playedTime = 3600
};
var saved = await BoardSaveGameManager.CreateSaveGame(payload, metadata);

// Load a save
byte[] payload = await BoardSaveGameManager.LoadSaveGame(saveId);
```

### Pause Menu

```csharp
using Board.Core;

// Configure pause menu
BoardApplication.SetPauseScreenContext(
    applicationName: "My Game",
    showSaveOptionUponExit: true,
    customButtons: new[] {
        new BoardPauseCustomButton("restart", "Restart", BoardPauseButtonIcon.CircularArrow)
    }
);

// Handle events
BoardApplication.pauseScreenActionReceived += OnPauseAction;
```

## Type Cross-Reference

For detailed member documentation, see the individual namespace markdown files linked above.
