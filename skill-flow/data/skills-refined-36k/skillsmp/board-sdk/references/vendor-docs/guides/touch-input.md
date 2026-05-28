# Touch Input Guide

Implementation guide for handling touch contacts in your game.

New to Board's touch system? Read the Touch System overview first to understand how Board handles unlimited contacts, noise rejection, and Piece recognition.

## Getting Active Contacts

Access current contacts through BoardInput.GetActiveContacts():

```csharp
using Board.Input;

void Update()
{
    // Get all active contacts (fingers and Pieces)
    var contacts = BoardInput.GetActiveContacts();

    foreach (var contact in contacts)
    {
        ProcessContact(contact);
    }
}
```

## Filtering by Type

Filter contacts by type to handle fingers and Pieces separately:

```csharp
// Only finger touches
var fingers = BoardInput.GetActiveContacts(BoardContactType.Finger);

// Only Pieces
var pieces = BoardInput.GetActiveContacts(BoardContactType.Glyph);

// Both (explicit)
var all = BoardInput.GetActiveContacts(BoardContactType.Finger, BoardContactType.Glyph);
```

## Checking if a Contact is Active

```csharp
// Check if a specific contact ID is still active
bool isActive = BoardInput.IsContactIdActive(contactId);
```

## Contact Properties

Each BoardContact provides:

- contactId (int) - Unique identifier for this contact session
- type (BoardContactType) - Finger or Glyph
- screenPosition (Vector2) - Position in screen coordinates (pixels)
- previousScreenPosition (Vector2) - Position in the previous frame
- orientation (float) - Rotation in degrees (Pieces only)
- previousOrientation (float) - Rotation in the previous frame
- phase (BoardContactPhase) - Current contact phase
- isTouched (bool) - Whether a finger is touching the Piece
- glyphId (int) - Which Piece from the set (Pieces only)
- bounds (Rect) - Contact bounding rectangle

### Position

Screen position is in pixel coordinates matching the display resolution (1920×1080):

```csharp
Vector2 position = contact.screenPosition;

// Convert to world position (for 2D games)
Vector3 worldPos = Camera.main.ScreenToWorldPoint(
    new Vector3(position.x, position.y, 10f)
);
```

### Orientation

Piece rotation in degrees (0–360):

```csharp
float rotation = contact.orientation;

// Apply to a transform
transform.rotation = Quaternion.Euler(0, 0, -rotation);
```

### Delta Values

Calculate movement and rotation between frames:

```csharp
Vector2 deltaPosition = contact.screenPosition - contact.previousScreenPosition;
float deltaRotation = contact.orientation - contact.previousOrientation;
```

## Contact Phases

Contact phases indicate the lifecycle of a touch or Piece placement:

- Began - Contact started this frame
- Moved - Contact position or rotation changed
- Stationary - Contact is active but unchanged
- Ended - Contact ended normally (lifted)
- Canceled - Contact ended abnormally (e.g., pause screen opened)

Note: When the pause screen opens, all active contacts are canceled. Your game should handle this by cleaning up any contact-related state when receiving Canceled phases.

### Handling Phases

```csharp
void ProcessContact(BoardContact contact)
{
    switch (contact.phase)
    {
        case BoardContactPhase.Began:
            // Create visual representation, start tracking
            SpawnContactVisual(contact);
            break;

        case BoardContactPhase.Moved:
            // Update position/rotation
            UpdateContactVisual(contact);
            break;

        case BoardContactPhase.Stationary:
            // Contact unchanged, may still need processing
            break;

        case BoardContactPhase.Ended:
        case BoardContactPhase.Canceled:
            // Clean up
            RemoveContactVisual(contact);
            break;
    }
}
```

### Phase Helper Methods

```csharp
// True for Began, Moved, or Stationary
bool isActive = contact.phase.IsActive();

// True for Ended or Canceled
bool isFinished = contact.phase.IsEndedOrCanceled();

// Alternative property
bool isInProgress = contact.isInProgress;
```

## Piece Touch State

Pieces report whether a finger is touching them:

```csharp
if (contact.type == BoardContactType.Glyph)
{
    if (contact.isTouched)
    {
        // Player is holding the Piece
        HighlightPiece(contact);
    }
    else
    {
        // Piece is on Board but not being touched
        ShowIdleState(contact);
    }
}
```

This enables interactions like:

- Highlighting Pieces when picked up
- Different behavior for touched vs. resting Pieces
- Detecting when a player releases a Piece

## Glyph IDs

For Piece contacts, glyphId identifies which Piece from the set:

```csharp
if (contact.type == BoardContactType.Glyph)
{
    int pieceType = contact.glyphId;

    // Map to game objects
    switch (pieceType)
    {
        case 0:
            SpawnWarrior(contact);
            break;
        case 1:
            SpawnMage(contact);
            break;
        case 2:
            SpawnArcher(contact);
            break;
    }
}
```

Note: Glyph IDs are indices (0 to N-1) within your Piece Set. To determine which ID corresponds to which physical Piece, place each Piece on Board one at a time and log the glyph ID.

## Input Settings

Configure tracking behavior through BoardInputSettings:

- Translation Smoothing (default 0.5) - Smooths position updates. 0 = raw values, 1 = maximum smoothing. Lower values improve responsiveness; higher values reduce jitter.
- Rotation Smoothing (default 0.5) - Smooths orientation updates. Same range as translation smoothing. Higher values help with rotational jitter.
- Persistence (default 4) - How many frames a Piece remains tracked after losing detection. Higher values keep Pieces "alive" during brief detection gaps.

### Changing Settings at Runtime

```csharp
// Load a different settings asset
BoardInput.settings = myAlternateSettings;

// Note: This cancels all active contacts
```

## Debug Overlay UI

Visualize contacts during development:

```csharp
// Enable the overlay
BoardInput.enableDebugView = true;

// Check current state
if (BoardInput.enableDebugView)
{
    // Overlay is active
}
```

The overlay displays:

- Contact position and orientation
- Contact ID and glyph ID
- Touch state indicator
- Contact type (finger vs. Piece)

Note: The debug overlay only works in Development builds. Enable Development Build in Build Settings.

### When to Use

- Verifying Piece detection accuracy
- Debugging position/rotation tracking
- Testing touch responsiveness
- Diagnosing false positive contacts

## UI Input

Add BoardUIInputModule to your EventSystem GameObject. The standard InputSystemUIInputModule will not work because Board suppresses system-level touch events.

See Project Setup for configuration details.

## See Also

- Touch System - How Board's touch technology works
- Simulator - Test input without hardware
- Hardware - Touch panel specifications
- Concepts - Terminology and definitions
