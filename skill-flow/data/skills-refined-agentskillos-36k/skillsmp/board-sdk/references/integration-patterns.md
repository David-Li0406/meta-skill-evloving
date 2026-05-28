# Board SDK Integration Patterns for Zero-Day Attack

## Getting Contacts

```csharp
using Board.Input;

// Get all active contacts
var all = BoardInput.GetActiveContacts();

// Get only fingers
var fingers = BoardInput.GetActiveContacts(BoardContactType.Finger);

// Get only Pieces (glyphs)
var pieces = BoardInput.GetActiveContacts(BoardContactType.Glyph);

// Get both types
var both = BoardInput.GetActiveContacts(BoardContactType.Finger, BoardContactType.Glyph);

// Check if specific contact is active
bool active = BoardInput.IsContactIdActive(contactId);
```

## Polling Pattern (Recommended)

```csharp
public class InputManager : MonoBehaviour
{
    private Dictionary<int, BoardContact> trackedContacts = new();

    void Update()
    {
        var contacts = BoardInput.GetActiveContacts(BoardContactType.Glyph);

        foreach (var contact in contacts)
        {
            switch (contact.phase)
            {
                case BoardContactPhase.Began:
                    OnPiecePlaced(contact);
                    trackedContacts[contact.contactId] = contact;
                    break;

                case BoardContactPhase.Moved:
                    OnPieceMoved(contact);
                    trackedContacts[contact.contactId] = contact;
                    break;

                case BoardContactPhase.Stationary:
                    // IMPORTANT: Don't ignore this phase!
                    // Piece may be placed without moving
                    OnPieceStationary(contact);
                    break;

                case BoardContactPhase.Ended:
                case BoardContactPhase.Canceled:
                    OnPieceRemoved(contact);
                    trackedContacts.Remove(contact.contactId);
                    break;
            }
        }
    }
}
```

## Screen to World Conversion

```csharp
// Board SDK returns screen coordinates with origin at bottom-left
// Unity Camera.main.ScreenToWorldPoint expects same origin

public Vector3 ScreenToWorld(Vector2 screenPosition)
{
    Vector3 screenPoint = new Vector3(
        screenPosition.x,
        screenPosition.y,
        Camera.main.nearClipPlane
    );
    return Camera.main.ScreenToWorldPoint(screenPoint);
}
```

## GlyphId to Token Mapping

```csharp
public TokenType GetTokenType(int glyphId)
{
    // Map glyphId (0 to N-1) to game token
    // Must match TokenDatabase configuration
    return TokenDatabase.Instance.GetTokenByGlyphId(glyphId)?.TokenType;
}
```

## UI Input Module

**CRITICAL**: Use `BoardUIInputModule` instead of `InputSystemUIInputModule`:

```csharp
// In your EventSystem GameObject:
// REMOVE: InputSystemUIInputModule
// ADD: BoardUIInputModule

// BoardUIInputModule processes finger touches for UI
// while ignoring Piece contacts
```

## Pause Screen Integration

```csharp
using Board.Core;

// Set up pause menu
BoardApplication.SetPauseScreenContext(
    applicationName: "Zero-Day Attack",
    showSaveOptionUponExit: true,
    customButtons: new[] {
        new BoardPauseCustomButton("restart", "Restart Game", BoardPauseButtonIcon.CircularArrow)
    }
);

// Handle pause actions
BoardApplication.pauseScreenActionReceived += (action, audioTracks) =>
{
    switch (action)
    {
        case BoardPauseAction.Resume:
            ResumeGame();
            break;
        case BoardPauseAction.ExitGameSaved:
            SaveAndExit();
            break;
    }
};

BoardApplication.customPauseScreenButtonPressed += (buttonId, audioTracks) =>
{
    if (buttonId == "restart") RestartGame();
};
```

## Session Management

```csharp
using Board.Session;

// Get current players
var players = BoardSession.players;

// Add player
await BoardSession.PresentAddPlayerSelector();

// Replace/remove player
await BoardSession.PresentReplacePlayerSelector(playerToReplace);

// Reset to active profile only
BoardSession.ResetPlayers();

// Subscribe to changes
BoardSession.playersChanged += OnPlayersChanged;
```
