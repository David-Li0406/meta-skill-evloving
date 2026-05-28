# Sample Scene

Explore the included sample scene to learn SDK features.

## Importing the Sample

The SDK includes a sample scene demonstrating common usage patterns.

1. Open **Window > Package Manager**
2. Select **Board SDK** from the installed packages
3. Expand the **Samples** section
4. Click **Import** next to **Input**

Imported samples appear in `Assets/Samples/Board SDK/<version>/`.

## BoardInput Sample

The primary sample scene for testing Piece detection and touch input.

### Location

After importing, find the scene at:

```
Assets/Samples/Board SDK/<version>/Input/Scenes/BoardInput.unity
```

### What It Demonstrates

- Real-time Piece detection and tracking
- Finger touch handling
- Debug overlay visualization
- BoardInputSettings configuration

### Running the Sample

1. Open the BoardInput scene
2. Enter Play mode
3. Use the **Simulator** to test Piece placement
4. Or deploy to Board to test with real Pieces

## Understanding the Sample Code

### BoardInputManager

The sample includes a `BoardInputManager` script that shows how to:

**Access active contacts:**

```csharp
// Get all active contacts
var contacts = BoardInput.GetActiveContacts();

// Filter by contact type
var fingers = BoardInput.GetActiveContacts(BoardContactType.Finger);
var pieces = BoardInput.GetActiveContacts(BoardContactType.Glyph);
```

**Process contact events:**

```csharp
void Update()
{
    foreach (var contact in BoardInput.GetActiveContacts())
    {
        switch (contact.phase)
        {
            case BoardContactPhase.Began:
                OnContactBegan(contact);
                break;
            case BoardContactPhase.Moved:
                OnContactMoved(contact);
                break;
            case BoardContactPhase.Ended:
                OnContactEnded(contact);
                break;
        }
    }
}
```

**Read contact properties:**

```csharp
void ProcessContact(BoardContact contact)
{
    // Position in screen coordinates
    Vector2 position = contact.screenPosition;

    // Rotation (for Pieces)
    float rotation = contact.orientation;

    // Whether finger is touching the Piece
    bool isTouched = contact.isTouched;

    // Unique identifier for this contact
    int id = contact.contactId;

    // Glyph ID (which Piece from the set)
    int glyphId = contact.glyphId;
}
```

## Enabling the Debug Overlay

The sample demonstrates the debug overlay that visualizes Piece detection:

```csharp
// Enable debug visualization
BoardInput.enableDebugView = true;
```

The overlay shows:

- Piece position and orientation
- Contact ID and glyph ID
- Touch state

**Note:** The debug overlay only functions in Development builds.

## Testing with Hardware

To test the sample on Board:

1. Configure BoardInputSettings with your Piece Set model
2. Add the BoardInput scene to your build
3. **Build & Deploy** to Board
4. Place Pieces on Board to see detection in action

## Building Your Own

Use the sample as a starting point:

- Study how BoardInputManager processes contacts
- Copy the input handling patterns into your own scripts
- Customize the visual feedback for your game's needs

## Next Steps

- **Simulator** - Test input without hardware
- **Touch Input** - Deep dive into input handling
- **Player Management** - Add player sessions
