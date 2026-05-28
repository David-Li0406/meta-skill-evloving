# Glyph Detection and Token Mapping

## Overview

Board SDK uses ML-powered glyph recognition to identify physical game pieces placed on the display. Each piece has a unique glyph pattern on its bottom that the camera recognizes.

## GlyphId System

- `glyphId` is an index (0 to N-1) within the active Piece Set
- Only valid when `contact.type == BoardContactType.Glyph`
- The SDK's `.tflite` model file determines which patterns are recognized

### Model File Location

```text
Assets/StreamingAssets/arcade_v1.3.7.tflite
```

## TokenDatabase Mapping

Create a mapping between glyphId and game tokens:

```csharp
[CreateAssetMenu(fileName = "TokenDatabase", menuName = "Zero-Day Attack/Token Database")]
public class TokenDatabase : ScriptableObject
{
    [System.Serializable]
    public class TokenEntry
    {
        public int glyphId;           // SDK glyph index
        public TokenType tokenType;   // Game token type
        public PlayerColor player;    // Red or Blue
        public Sprite sprite;         // Visual
    }

    public List<TokenEntry> tokens;

    public TokenEntry GetTokenByGlyphId(int glyphId)
    {
        return tokens.Find(t => t.glyphId == glyphId);
    }
}
```

## Zero-Day Attack Token Configuration

| GlyphId | Token Type | Player | Description        |
| ------- | ---------- | ------ | ------------------ |
| 0       | Attack     | Red    | Red Attack token   |
| 1       | Exploit    | Red    | Red Exploit token  |
| 2       | Ghost      | Red    | Red Ghost token    |
| 3       | Attack     | Blue   | Blue Attack token  |
| 4       | Exploit    | Blue   | Blue Exploit token |
| 5       | Ghost      | Blue   | Blue Ghost token   |

**Note**: Actual glyphId assignments depend on your physical piece set and model file.

## Input Settings

Configure glyph detection in `BoardInputSettings`:

```csharp
// Located at: Assets/Board/Settings/BoardInputSettings

glyphModelFilename    // .tflite model file name
persistence           // Frames to track after losing detection (default: 4)
translationSmoothing  // Position smoothing 0-1 (default: 0.5)
rotationSmoothing     // Rotation smoothing 0-1 (default: 0.5)
```

## Handling Glyph Contacts

```csharp
void ProcessGlyphContact(BoardContact contact)
{
    if (contact.type != BoardContactType.Glyph)
        return;

    int glyphId = contact.glyphId;
    var tokenEntry = TokenDatabase.Instance.GetTokenByGlyphId(glyphId);

    if (tokenEntry == null)
    {
        Debug.LogWarning($"Unknown glyphId: {glyphId}");
        return;
    }

    // Use tokenEntry.tokenType, tokenEntry.player, etc.
}
```

## Orientation

Glyph contacts include rotation information:

```csharp
float radians = contact.orientation;           // 0 to 2*PI
float degrees = radians * Mathf.Rad2Deg;       // 0 to 360

// Delta from previous frame
float deltaRadians = contact.orientation - contact.previousOrientation;
```
