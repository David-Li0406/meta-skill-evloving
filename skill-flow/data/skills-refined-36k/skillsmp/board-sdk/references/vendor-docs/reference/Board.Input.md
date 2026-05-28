# Board.Input Namespace

Touch input system for detecting fingers and Pieces on the Board display.

## Classes

- [BoardContactPhaseExtensions](#boardcontactphaseextensions)
- [BoardInput](#boardinput)
- [BoardInputSettings](#boardinputsettings)
- [BoardUIInputModule](#boarduiinputmodule)

## Structs

- [BoardContact](#boardcontact)
- [BoardContactEvent](#boardcontactevent)
- [BoardContactTypeMask](#boardcontacttypemask)

## Enums

- [BoardContactPhase](#boardcontactphase)
- [BoardContactType](#boardcontacttype)

---

## BoardInput

Provides access to Board's touch input system.

```csharp
public static class BoardInput
```

**Inheritance:** `Object` → `BoardInput`

### Properties

#### enableDebugView

Gets or sets whether the BoardInput debug view is enabled.

```csharp
public static bool enableDebugView { get; set; }
```

**Type:** `bool`

**Remarks:** Debug view only functions in Development builds.

---

#### settings

Gets or sets the current BoardInputSettings.

```csharp
public static BoardInputSettings settings { get; set; }
```

**Type:** [BoardInputSettings](#boardinputsettings)

**Remarks:** Changing settings cancels all active contacts.

### Methods

#### GetActiveContacts(BoardContactTypeMask)

Gets all currently active contacts on the Board.

```csharp
public static ReadOnlyArray<BoardContact> GetActiveContacts(
    BoardContactTypeMask contactTypeMask = default
)
```

**Parameters:**

- `contactTypeMask` ([BoardContactTypeMask](#boardcontacttypemask), optional) - Filter for contact types (default: all types)

**Returns:** `ReadOnlyArray<BoardContact>` - Array of active contacts

---

#### GetActiveContacts(params BoardContactType[])

Gets all currently active contacts on the Board filtered by type.

```csharp
public static ReadOnlyArray<BoardContact> GetActiveContacts(
    params BoardContactType[] contactTypes
)
```

**Parameters:**

- `contactTypes` ([BoardContactType](#boardcontacttype)[]) - Contact types to include

**Returns:** `ReadOnlyArray<BoardContact>` - Array of active contacts matching the specified types

**Example:**

```csharp
// Get only finger contacts
var fingers = BoardInput.GetActiveContacts(BoardContactType.Finger);

// Get both fingers and glyphs
var all = BoardInput.GetActiveContacts(BoardContactType.Finger, BoardContactType.Glyph);
```

---

#### IsContactIdActive(int)

Checks whether a contact with the specified ID is currently active.

```csharp
public static bool IsContactIdActive(int contactId)
```

**Parameters:**

- `contactId` (int) - The contact identifier to check

**Returns:** `bool` - `true` if a contact with the specified ID is active; otherwise, `false`

### Events

#### settingsChanged

Occurs when the current BoardInputSettings change.

```csharp
public static event Action settingsChanged
```

**Event Type:** `Action`

---

## BoardContact

Represents an ongoing contact on the Board's touch screen.

```csharp
public struct BoardContact
```

### Fields

#### kSizeInBytes

The size of a BoardContact in bytes.

```csharp
public const int kSizeInBytes = 64
```

**Type:** `int`

**Value:** 64

### Properties

#### bounds

Gets the screen-space bounds that encapsulate the contact.

```csharp
public Rect bounds { get; }
```

**Type:** `Rect`

---

#### contactId

Gets the unique identifier for the contact.

```csharp
public int contactId { get; }
```

**Type:** `int`

**Remarks:** This ID persists for the duration of the contact's lifecycle and can be used to track the same contact across frames.

---

#### glyphId

Gets the glyph identifier associated with the contact.

```csharp
public int glyphId { get; }
```

**Type:** `int`

**Remarks:** Only valid when [type](#type) is `BoardContactType.Glyph`. This is an index (0 to N-1) within the active Piece Set.

---

#### isInProgress

Gets a value indicating whether the contact is ongoing.

```csharp
public bool isInProgress { get; }
```

**Type:** `bool`

**Returns:** `true` if phase is Began, Moved, or Stationary; otherwise `false`

---

#### isNoneEndedOrCanceled

Gets a value indicating whether the phase is None, Ended, or Canceled.

```csharp
public bool isNoneEndedOrCanceled { get; }
```

**Type:** `bool`

---

#### isTouched

Gets a value indicating whether the contact is currently being touched.

```csharp
public bool isTouched { get; }
```

**Type:** `bool`

**Remarks:** For Piece contacts, indicates whether a finger is touching the Piece. Always `false` for finger contacts.

---

#### orientation

Gets the orientation of the contact in radians clockwise from vertical.

```csharp
public float orientation { get; }
```

**Type:** `float`

**Remarks:** Only valid for Piece (Glyph) contacts. Range: 0 to 2π radians (0-360 degrees).

---

#### phase

Gets the current phase of the contact.

```csharp
public BoardContactPhase phase { get; }
```

**Type:** [BoardContactPhase](#boardcontactphase)

---

#### previousOrientation

Gets the orientation in the previous frame.

```csharp
public float previousOrientation { get; }
```

**Type:** `float`

---

#### previousScreenPosition

Gets the position in the previous frame.

```csharp
public Vector2 previousScreenPosition { get; }
```

**Type:** `Vector2`

---

#### screenPosition

Gets the position in screen space pixel coordinates.

```csharp
public Vector2 screenPosition { get; }
```

**Type:** `Vector2`

**Remarks:** Coordinates are in pixels relative to the display resolution (1920×1080). Origin (0,0) is at the bottom-left corner.

---

#### timestamp

Gets the time when the contact began or was last mutated.

```csharp
public double timestamp { get; }
```

**Type:** `double`

**Remarks:** Time in seconds on the same timeline as `Time.realTimeSinceStartup`.

---

#### type

Gets the current type of the contact.

```csharp
public BoardContactType type { get; }
```

**Type:** [BoardContactType](#boardcontacttype)

---

## BoardInputSettings

Encapsulates all input settings for the Board platform.

```csharp
public class BoardInputSettings : ScriptableObject
```

**Inheritance:** `ScriptableObject` → `BoardInputSettings`

### Properties

#### glyphModelFilename

Gets the Glyph Model Filename setting value.

```csharp
public string glyphModelFilename { get; }
```

**Type:** `string`

**Remarks:** Name of the .tflite model file in StreamingAssets folder.

---

#### persistence

Gets the Persistence setting value.

```csharp
public int persistence { get; }
```

**Type:** `int`

**Remarks:** How many frames a Piece remains tracked after losing detection. Default: 4

---

#### rotationSmoothing

Gets the Rotation Smoothing setting value.

```csharp
public float rotationSmoothing { get; }
```

**Type:** `float`

**Remarks:** Smoothing applied to Piece rotation changes (0-1). Default: 0.5

---

#### translationSmoothing

Gets the Translation Smoothing setting value.

```csharp
public float translationSmoothing { get; }
```

**Type:** `float`

**Remarks:** Smoothing applied to Piece position changes (0-1). Default: 0.5

---

## BoardUIInputModule

UI input module for input from Board.

```csharp
public class BoardUIInputModule : PointerInputModule
```

**Inheritance:** `MonoBehaviour` → `UIBehaviour` → `BaseInputModule` → `PointerInputModule` → `BoardUIInputModule`

**Remarks:** Use this instead of `InputSystemUIInputModule` as Board suppresses system-level touch events. This module processes finger touches for UI while ignoring Piece contacts.

### Properties

#### forceModuleActive

Gets a value indicating whether the module should be forced to be active.

```csharp
public bool forceModuleActive { get; }
```

**Type:** `bool`

---

#### useFakeInput

Gets a value indicating whether the module should use the mouse as fake input.

```csharp
public bool useFakeInput { get; }
```

**Type:** `bool`

**Remarks:** Useful for testing UI in the Unity Editor.

---

## BoardContactPhase

Specifies the phase in the lifecycle of a contact on the Board.

```csharp
public enum BoardContactPhase
```

### Values

| Value            | Description                                                          |
| ---------------- | -------------------------------------------------------------------- |
| `None` (0)       | No activity has been registered. Default-initialized contact record. |
| `Began` (1)      | Contact has just begun (finger touched or Piece placed).             |
| `Moved` (2)      | Ongoing contact has changed position or orientation.                 |
| `Stationary` (5) | Ongoing contact has not moved in this frame.                         |
| `Ended` (3)      | Contact has ended (finger lifted or Piece removed).                  |
| `Canceled` (4)   | Contact ended abnormally (e.g., pause screen opened, focus lost).    |

### Extension Methods

#### IsActive()

Returns `true` if phase is Began, Moved, or Stationary.

```csharp
public static bool IsActive(this BoardContactPhase phase)
```

---

#### IsEndedOrCanceled()

Returns `true` if phase is Ended or Canceled.

```csharp
public static bool IsEndedOrCanceled(this BoardContactPhase phase)
```

---

## BoardContactType

Specifies the type of a contact on the Board.

```csharp
public enum BoardContactType
```

### Values

| Value        | Description                                                                      |
| ------------ | -------------------------------------------------------------------------------- |
| `Finger` (0) | Standard finger touch point.                                                     |
| `Glyph` (1)  | Physical Piece with glyph pattern. Provides position, rotation, and touch state. |
| `Blob` (2)   | Undefined blob (reserved for future use).                                        |

---

## BoardContactTypeMask

Provides a mechanism to filter by BoardContactType.

```csharp
public struct BoardContactTypeMask
```

### Implicit Conversions

```csharp
// Create from single type
BoardContactTypeMask mask = BoardContactType.Finger;

// Create from multiple types
BoardContactTypeMask mask = new[] { BoardContactType.Finger, BoardContactType.Glyph };
```

---

## BoardContactEvent

Represents a contact input event from the Board.

```csharp
public struct BoardContactEvent
```

**Remarks:** Used for event-based input handling as an alternative to polling with `BoardInput.GetActiveContacts()`.

### Properties

#### contact

Gets the contact associated with this event.

```csharp
public BoardContact contact { get; }
```

**Type:** [BoardContact](#boardcontact)

---

#### phase

Gets the phase of this contact event.

```csharp
public BoardContactPhase phase { get; }
```

**Type:** [BoardContactPhase](#boardcontactphase)

---

#### timestamp

Gets the time when this event occurred.

```csharp
public double timestamp { get; }
```

**Type:** `double`

**Remarks:** Time in seconds on the same timeline as `Time.realTimeSinceStartup`.

---

## See Also

- [Board.Core](Board.Core.md) - Application and pause menu
- [Board.Input.Debug](Board.Input.Debug.md) - Debug visualization
- [Board.Input.Simulation](Board.Input.Simulation.md) - Editor simulation
