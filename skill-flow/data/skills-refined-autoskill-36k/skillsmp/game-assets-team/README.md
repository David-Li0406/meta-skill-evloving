# Game Assets Team

Complete game asset design, creation, implementation, and optimization team.

## Expertise

This skill provides a full art team covering:

- **Art Direction**: Style guides, visual consistency, mood boards
- **AI Image Generation**: Gemini prompting, style transfer
- **Sprite Creation**: Characters, items, UI elements
- **Background Art**: Environments, parallax layers
- **UI/UX Design**: Menus, HUDs, buttons, icons
- **Animation Specs**: Frame requirements, timing guidelines
- **Asset Optimization**: Compression, atlasing, performance
- **Audio Design**: Sound effect direction, music briefs

## When to Use

Invoke this skill when you need to:

- Create visual assets for your game
- Establish art direction and style guides
- Generate AI images with consistent style
- Design UI elements and icons
- Optimize assets for web/mobile
- Spec out animations
- Plan audio needs

## Asset Pipeline

```
┌──────────────────────────────────────────────────────────┐
│                   ASSET PIPELINE                         │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  CONCEPT        GENERATE       PROCESS        OPTIMIZE   │
│  ┌──────┐      ┌──────┐      ┌──────┐      ┌──────┐     │
│  │ Art  │  →   │Gemini│  →   │Recraft│ →   │ Web  │     │
│  │ Brief│      │  AI  │      │ API  │      │ Ready│     │
│  └──────┘      └──────┘      └──────┘      └──────┘     │
│                                                          │
│  Style guide   PNG output   Remove BG    Compressed     │
│  + prompt      1-2 MB       Vectorize    SVG/WebP       │
│                             300-500KB    <100KB         │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

## Art Style: Farming in Purria

### Visual Identity

- **Style**: Soft stylized 3D cartoon
- **Palette**: Warm earth tones, golden hour lighting
- **Shapes**: Rounded, friendly, approachable
- **Mood**: Cozy, whimsical, charming

### Character Design (Simulins)

- Cute robot companions
- Art Nouveau brass/copper details
- Botanical vine accents
- Expressive eyes
- Compact, round forms

### Environment

- Rolling farmland
- Magical valley setting
- Soft shadows
- Warm color temperature

## Prompt Engineering

### Structure

```
[Subject] + [Style] + [Composition] + [Technical] + [Mood]
```

### Example Prompts

**Character:**
```
"A cute friendly robot companion with brass gears and vine patterns,
soft stylized 3D cartoon rendering, centered composition,
transparent background, warm golden lighting, whimsical charm"
```

**UI Icon:**
```
"A golden coin with leaf emblem, flat vector style,
simple clean design, game UI icon, transparent background"
```

**Background:**
```
"Rolling hills with farmland, soft watercolor style,
wide panoramic composition, warm sunset colors, cozy pastoral mood"
```

## File Formats

| Asset Type | Format | Size Target |
|------------|--------|-------------|
| UI Icons | SVG | <50KB |
| Sprites | PNG (transparent) | <200KB |
| Backgrounds | WebP | <500KB |
| Animations | Sprite sheet PNG | <1MB |

## Integration

This skill works alongside:

- `gemini-image-generator` - Primary generation tool
- `react-game-ui` - Implementing assets in React
- `fun-advisor` - Ensuring art supports fun

## Usage in Claude Code

```
/game-assets-team

"Create a Simulin character for the tutorial..."
"Design UI icons for the inventory system..."
"What's the best approach for background parallax?"
```
