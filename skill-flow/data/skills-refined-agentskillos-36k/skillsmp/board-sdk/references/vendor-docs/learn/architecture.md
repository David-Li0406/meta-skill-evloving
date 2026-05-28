# Architecture

Overview of the Board Unity SDK components.

## Core Components

### BoardInput

The touch input subsystem. Receives contact data from Board hardware and provides it to your game.

**Responsibilities:**

- Tracking active contacts
- Contact phase management (began, moved, ended)
- Glyph recognition
- Input smoothing

**Key APIs:**

- `BoardInput.GetActiveContacts()` - Get current contacts
- Contact events and callbacks

See **Touch Input** for implementation details.

### BoardSession

Manages the current game session, players, and profiles.

**Responsibilities:**

- Tracking active profile
- Managing player list
- Notifying of player changes

**Key APIs:**

- `BoardSession.players` - Current players
- `BoardSession.playersChanged` - Change notifications

See **Player Management** for implementation details.

### BoardApplication

Main entry point for Board system features like pause screen and profile switcher.

**Responsibilities:**

- Pause screen configuration and events
- Profile switcher overlay
- System-level interactions

**Key APIs:**

- `BoardApplication.SetPauseScreenContext()` - Configure pause screen
- `BoardApplication.ShowProfileSwitcher()` - Show profile UI

See **Pause Menu** and **Profile Switcher** for implementation details.

### BoardSaveGameManager

Handles persistent save game storage.

**Responsibilities:**

- Creating and loading save games
- Managing save game metadata
- Player-save associations
- Storage quota management

**Key APIs:**

- `BoardSaveGameManager.CreateSaveGame()` - Save game data
- `BoardSaveGameManager.GetSaveGamesMetadata()` - List saves

See **Save Game System** for implementation details.

## Namespaces

| Namespace       | Purpose                                      |
| --------------- | -------------------------------------------- |
| `Board.Core`    | Application lifecycle, pause screen, logging |
| `Board.Input`   | Touch contacts, glyphs, input settings       |
| `Board.Session` | Players, profiles, sessions                  |
| `Board.Save`    | Save game management                         |

## See Also

- **Concepts** - Terminology and definitions
- **API Reference** - Complete API documentation
