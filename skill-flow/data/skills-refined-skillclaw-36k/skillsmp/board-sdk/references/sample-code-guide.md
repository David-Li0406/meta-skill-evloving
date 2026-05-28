# Board SDK Sample Code Guide

Walkthrough of the vendor sample project demonstrating Board SDK input handling patterns.

## Sample Location

```text
Assets/Samples/Board SDK/3.0.0/Input/
├── Scripts/
│   ├── BoardInputManager.cs       # Main input handling
│   └── BoardContactDebugInfo.cs   # Contact visualization
└── Scenes/
    └── BoardInput.unity           # Demo scene
```

## Importing the Sample

1. Window > Package Manager
2. Select "Board SDK"
3. Expand "Samples"
4. Click "Import" next to "Input"

---

## BoardInputManager.cs

Core input handling script demonstrating contact lifecycle management.

### Key Pattern: Dictionary Tracking by contactId

```csharp
private readonly Dictionary<int, BoardContactDebugInfo> m_ContactDebugInstances =
    new Dictionary<int, BoardContactDebugInfo>();
```

Each contact has a unique `contactId` that persists across frames. Use a Dictionary to track game objects or state per contact.

### Update Loop Structure

```csharp
void Update()
{
    // Process glyphs (Pieces)
    ProcessContacts(BoardInput.GetActiveContacts(BoardContactType.Glyph), m_GlyphsDebugLabel);

    // Process fingers (touches)
    ProcessContacts(BoardInput.GetActiveContacts(BoardContactType.Finger), m_TouchesDebugLabel);
}
```

**Pattern**: Separate processing for Glyph vs Finger contacts. Call `GetActiveContacts()` with a type filter.

### Contact Lifecycle Handling

```csharp
private void ProcessContacts(BoardContact[] contacts, Text debugText)
{
    for (var i = 0; i < contacts.Length; i++)
    {
        var contact = contacts[i];
        var position = contact.screenPosition;

        switch (contact.phase)
        {
            case BoardContactPhase.Began:
                // Prevent duplicates
                if (m_ContactDebugInstances.ContainsKey(contact.contactId))
                    return;

                // Create visual representation
                var info = Instantiate(m_ContactDebugPrefab, m_Canvas.transform);
                info.SetPositionAndRotation(contact);

                // Y-axis flip for UI positioning
                ((RectTransform)info.transform).anchoredPosition =
                    new Vector2(position.x, Screen.height - position.y);

                // Track by contactId
                m_ContactDebugInstances.Add(contact.contactId, info);
                break;

            case BoardContactPhase.Moved:
            case BoardContactPhase.Stationary:
                // Update existing visual
                if (m_ContactDebugInstances.TryGetValue(contact.contactId, out info))
                {
                    info.SetPositionAndRotation(contact);
                }
                break;

            case BoardContactPhase.Canceled:
            case BoardContactPhase.Ended:
                // Clean up
                if (m_ContactDebugInstances.TryGetValue(contact.contactId, out info))
                {
                    m_ContactDebugInstances.Remove(contact.contactId);
                    Destroy(info.gameObject);
                }
                break;
        }
    }
}
```

### Critical Patterns

1. **Handle Stationary phase**: A Piece placed without moving goes `Began → Stationary → Ended` (never `Moved`)
2. **Y-axis flip**: Screen coordinates have origin at bottom-left; UI often needs `Screen.height - position.y`
3. **Dictionary cleanup**: Always remove from Dictionary when contact ends
4. **Duplicate prevention**: Check `ContainsKey` before adding in `Began`

---

## BoardContactDebugInfo.cs

Visual representation component for a single contact.

### Position and Rotation

```csharp
public void SetPositionAndRotation(BoardContact contact)
{
    // Position using screen coordinates directly
    m_Transform.position = contact.screenPosition;

    // Rotation: radians to degrees, around Z axis
    m_RotationIndicatorTransform.rotation =
        Quaternion.AngleAxis(contact.orientation * Mathf.Rad2Deg, Vector3.forward);
}
```

### Type-Specific Visualization

```csharp
// Show rotation indicator only for Pieces
m_RotationIndicatorTransform.gameObject.SetActive(contact.type == BoardContactType.Glyph);

// Different labels for different types
m_TouchLabel.enabled = contact.type == BoardContactType.Finger;
m_GlyphLabel.enabled = contact.type == BoardContactType.Glyph;
```

### Glyph vs Finger Display

```csharp
if (contact.type == BoardContactType.Glyph)
{
    m_GlyphLabel.text =
        $"ID: {contact.contactId}\nGlyph: {contact.glyphId}\n{contact.screenPosition}\n{contact.orientation}";
}
else if (contact.type == BoardContactType.Finger)
{
    m_TouchLabel.text = $"ID: {contact.contactId}\n{contact.screenPosition}";
}
```

---

## Key Takeaways for Zero-Day Attack

### Token Tracking Pattern

```csharp
// TokenManager should mirror this pattern
private Dictionary<int, TokenView> _activeTokens = new Dictionary<int, TokenView>();

void ProcessGlyphContacts()
{
    var contacts = BoardInput.GetActiveContacts(BoardContactType.Glyph);
    foreach (var contact in contacts)
    {
        switch (contact.phase)
        {
            case BoardContactPhase.Began:
                // Map glyphId to token type via TokenDatabase
                var tokenData = TokenDatabase.GetByGlyphId(contact.glyphId);
                // Create/show TokenView
                break;

            case BoardContactPhase.Moved:
            case BoardContactPhase.Stationary:
                // Update token position/rotation
                break;

            case BoardContactPhase.Ended:
            case BoardContactPhase.Canceled:
                // Finalize placement or remove token
                break;
        }
    }
}
```

### Coordinate Conversion

```csharp
// Screen to World (for 2D game objects)
Vector3 worldPos = Camera.main.ScreenToWorldPoint(
    new Vector3(contact.screenPosition.x, contact.screenPosition.y, 10f)
);

// Rotation (radians to Quaternion)
Quaternion rotation = Quaternion.Euler(0, 0, -contact.orientation * Mathf.Rad2Deg);
```

### Important: Stationary Phase

```csharp
// DON'T do this:
case BoardContactPhase.Moved:
    UpdatePosition(contact); // Misses stationary contacts!
    break;

// DO this:
case BoardContactPhase.Moved:
case BoardContactPhase.Stationary:  // Include Stationary!
    UpdatePosition(contact);
    break;
```

---

## See Also

- [contact-handling.md](contact-handling.md) - BoardContact API reference
- [glyph-detection.md](glyph-detection.md) - GlyphId mapping
- [integration-patterns.md](integration-patterns.md) - Zero-Day Attack patterns
