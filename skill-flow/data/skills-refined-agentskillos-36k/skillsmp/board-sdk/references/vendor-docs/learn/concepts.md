# Concepts

Core terminology used throughout Board documentation.

## Touch Input

### Piece

A physical object with a conductive glyph pattern on its base. Pieces have no batteries, sensors, or electronics. They're detected purely through capacitive interaction with the display.

### Glyph

The unique conductive pattern on a Piece's base that identifies it. Each glyph creates a distinct response on the touch sensor, allowing Board to recognize which specific Piece is on the display.

In the SDK, Piece contacts are referred to as "glyph contacts" because the system identifies them by their glyph pattern.

### Piece Set

A collection of Pieces trained together for recognition. Examples include the Pieces from Mushka, Chop Chop, or Board Arcade.

Only one Piece set can be active at a time. You select which Piece set your game uses through the SDK configuration.

### Model

The machine learning file (.tflite) required to use a Piece Set in your game. Each model is trained to recognize the Pieces in its corresponding set.

Models are named after their associated game (e.g., "Board Arcade" model for arcade Pieces).

### Contact

Any physical object on the display detected by the touch sensor. All contacts have an ID, position, and phase. Piece contacts additionally include orientation and touched status.

There's no artificial limit on simultaneous contacts, only what physically fits on the display.

### Contact Type

The classification of what created the contact:

- **Finger** - A standard touch point from a finger
- **Glyph** - A contact from a Piece

### Contact Phase

The lifecycle state of a contact:

| Phase      | Description                             |
| ---------- | --------------------------------------- |
| Began      | Contact started this frame              |
| Moved      | Contact position or orientation changed |
| Stationary | Contact held in place with no change    |
| Ended      | Contact lifted from surface             |
| Canceled   | Contact tracking was interrupted        |

### Detection

The process of determining what is on the display: identifying fingers, Pieces, and filtering out noise like palms or arms.

### Tracking

The process of maintaining contact identity across frames. When a contact moves, tracking ensures the SDK reports it as the same contact rather than a new one. Each contact has a persistent ID for the duration of its lifecycle.

### Touch State

Indicates whether a Piece is being held by a player or resting on the surface. Pieces are detected regardless of touch state, so games can use this as additional input.

### Noise Rejection

Board filters out unintentional contact such as palms, arms, or elbows resting on the display. This happens automatically. Players can rest their hands on the surface or reach across without generating false inputs.

## Sessions and Players

### Session

The current play session managed by BoardOS. A session tracks which profiles are playing and persists across game launches.

### Profile

A persistent identity stored on Board. Profiles have a name, avatar, and associated save games. Multiple profiles can exist on a single Board.

### Player

A participant in the current game session. A player can be either a profile stored on the device or a guest.

The SDK provides player information including name, avatar, and a unique player ID.

## See Also

- **Architecture** - How SDK components work together
- **Pieces** - Working with physical Pieces
- **Touch Input** - Implementing touch input
