# BoardContact Properties and Handling

## BoardContact Struct

### Position Properties

```csharp
Vector2 screenPosition      // Current position in screen pixels (1920x1080)
Vector2 previousScreenPosition  // Position in previous frame
Rect bounds                 // Screen-space bounding rect
```

**Note**: Origin (0,0) is bottom-left. Y-axis may need flipping for Unity world coordinates.

### Identification

```csharp
int contactId               // Unique ID for contact lifecycle
BoardContactType type       // Finger, Glyph, or Blob
int glyphId                 // Piece index (0 to N-1) - only valid for Glyph type
```

### Lifecycle

```csharp
BoardContactPhase phase     // Current phase
double timestamp            // When contact began/mutated (Time.realtimeSinceStartup)
```

### Orientation (Glyph only)

```csharp
float orientation           // Radians clockwise from vertical (0 to 2*PI)
float previousOrientation   // Orientation in previous frame
```

**Conversion**: `float degrees = orientation * Mathf.Rad2Deg;`

### Touch State

```csharp
bool isTouched              // Finger touching the Piece (Glyph only)
bool isInProgress           // True for Began, Moved, Stationary
bool isNoneEndedOrCanceled  // True for None, Ended, Canceled
```

## BoardContactPhase Enum

| Phase        | Value | Description                          |
| ------------ | ----- | ------------------------------------ |
| `None`       | 0     | Default state, no activity           |
| `Began`      | 1     | Just started (placed/touched)        |
| `Moved`      | 2     | Position or orientation changed      |
| `Stationary` | 5     | Active but unchanged this frame      |
| `Ended`      | 3     | Ended normally (lifted/removed)      |
| `Canceled`   | 4     | Ended abnormally (pause, focus lost) |

### Extension Methods

```csharp
phase.IsActive()           // True for Began, Moved, Stationary
phase.IsEndedOrCanceled()  // True for Ended, Canceled
```

## BoardContactType Enum

| Type     | Value | Description                 |
| -------- | ----- | --------------------------- |
| `Finger` | 0     | Standard finger touch       |
| `Glyph`  | 1     | Physical Piece with pattern |
| `Blob`   | 2     | Reserved for future use     |

## Typical Contact Lifecycle

### Finger

```text
Began → Moved* → Stationary* → Ended/Canceled
```

### Glyph (Piece)

```text
Began → Moved* → Stationary* → Ended/Canceled
         ↑         ↑
   (can have isTouched = true during any active phase)
```

**IMPORTANT**: Handle `Stationary` phase! A piece placed without moving goes:
`Began → Stationary → Ended` (never `Moved`)
