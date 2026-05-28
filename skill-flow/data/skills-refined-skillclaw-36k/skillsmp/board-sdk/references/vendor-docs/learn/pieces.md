# Pieces

Board recognizes physical Pieces placed on the display, providing position, rotation, and interaction state for each Piece.

## Overview

Pieces are physical objects with conductive glyph patterns on their base. They have no batteries, sensors, or electronics. Board detects them purely through capacitive interaction with the display.

Unlike standard touch contacts, Pieces provide:

- **Position** - X/Y coordinates near pixel resolution (1920×1080)
- **Rotation** - Current angle with ~1 degree precision
- **Touch State** - Whether the Piece is being held or resting on the surface

## How Pieces Work

Each Piece has a unique conductive pattern (glyph) on its base. When placed on the display, this pattern creates a distinct response on the capacitive touch sensor. On-device machine learning identifies the pattern and tracks the Piece in real-time.

The Pieces themselves are passive, made from a blend of plastic and conductive material. This makes them durable, affordable, and reliable at any speed.

Some Pieces include a conductive body that connects electrically to the glyph pattern. When a player holds one of these Pieces, their body completes the circuit, changing the signal the touch sensor receives. This allows Board to detect whether the Piece is being held or resting on the surface, exposed through the `isTouched` property.

## Piece Sets

Pieces are organized into sets that are trained together for recognition. Examples include the Pieces from Mushka, Chop Chop, or Board Arcade.

Only one Piece set can be active at a time. You configure which set your game uses through BoardInputSettings.

## Piece Properties

Each Piece contact provides these properties through `BoardContact`:

| Property         | Type              | Description                                       |
| ---------------- | ----------------- | ------------------------------------------------- |
| `screenPosition` | Vector2           | Position in screen coordinates (pixels)           |
| `orientation`    | float             | Rotation in degrees (0-360)                       |
| `isTouched`      | bool              | Whether a finger is touching the Piece            |
| `glyphId`        | int               | Which Piece from the set                          |
| `phase`          | BoardContactPhase | Current contact phase (Began, Moved, Ended, etc.) |
| `contactId`      | int               | Unique identifier for this contact session        |

## Detecting Piece Placement

Filter for Piece contacts and check for the Began phase:

```csharp
using Board.Input;

void Update()
{
    var pieces = BoardInput.GetActiveContacts(BoardContactType.Glyph);

    foreach (var piece in pieces)
    {
        if (piece.phase == BoardContactPhase.Began)
        {
            // Piece was just placed
            OnPiecePlaced(piece.glyphId, piece.screenPosition);
        }
    }
}
```

## Tracking Piece Movement

Read position and rotation each frame to track Piece movement:

```csharp
using Board.Input;

void Update()
{
    var pieces = BoardInput.GetActiveContacts(BoardContactType.Glyph);

    foreach (var piece in pieces)
    {
        // Update position
        Vector3 worldPos = Camera.main.ScreenToWorldPoint(
            new Vector3(piece.screenPosition.x, piece.screenPosition.y, 10f)
        );

        // Update rotation
        float rotation = piece.orientation;

        // Apply to game object
        UpdatePieceVisual(piece.contactId, worldPos, rotation);
    }
}
```

## Detecting Hold State

The `isTouched` property indicates whether a finger is currently touching the Piece:

```csharp
using Board.Input;

void Update()
{
    var pieces = BoardInput.GetActiveContacts(BoardContactType.Glyph);

    foreach (var piece in pieces)
    {
        if (piece.isTouched)
        {
            // Player is holding this Piece
            HighlightPiece(piece.contactId);
        }
        else
        {
            // Piece is resting on the surface
            RemoveHighlight(piece.contactId);
        }
    }
}
```

## See Also

- **Concepts** - Core terminology including glyphs, contacts, and tracking
- **Touch Input** - Working with all contact types
- **Hardware** - Touch system specifications
