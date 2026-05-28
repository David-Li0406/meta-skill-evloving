---
name: appshot
description: Create and manage App Store screenshot projects using appshot MCP tools. This skill should be used when users want to generate professional App Store screenshots with device frames, gradients, and captions. Triggers include requests to create screenshot projects, add captions, apply styling, or build final screenshots.
---

# AppShot Screenshot Generator

## Overview

AppShot generates App Store-ready screenshots with device frames, gradient backgrounds, and captions. This skill orchestrates the appshot MCP tools to create complete screenshot projects.

## Available MCP Tools

| Tool | Purpose |
|------|---------|
| `appshot_init` | Initialize new project structure |
| `appshot_captions` | Read/write/auto-generate caption text |
| `appshot_gradients` | List/apply gradient presets |
| `appshot_backgrounds` | Configure background images |
| `appshot_fonts` | List/validate available fonts |
| `appshot_config` | Modify device-specific settings |
| `appshot_build` | Generate final screenshots |
| `appshot_validate` | Check App Store compliance |
| `appshot_specs` | View App Store specifications |
| `appshot_doctor` | System diagnostics |
| `appshot_presets` | App Store preset configurations |
| `appshot_localize` | AI-powered caption translation |
| `appshot_languages` | Discover available translations |
| `appshot_frame` | Apply device frames only |
| `appshot_export` | Export for Fastlane |
| `appshot_clean` | Remove generated files |

## Project Workflow

### 1. Initialize Project

```
appshot_init with force: true
```

Creates the project structure:
```
.appshot/
├── config.json          # Main configuration
└── captions/
    ├── iphone.json      # Caption files per device
    ├── ipad.json
    ├── mac.json
    └── watch.json
screenshots/
├── iphone/              # Place screenshots here
├── ipad/
├── mac/
└── watch/
final/                   # Generated output
```

### 2. Add Captions

List existing captions:
```
appshot_captions with device: "iphone", action: "list"
```

Set a caption:
```
appshot_captions with device: "iphone", action: "set", filename: "home.png", caption: "Welcome Home", language: "en"
```

Auto-generate captions from filenames:
```
appshot_captions with device: "iphone", action: "auto"
```
This converts filenames like `home-screen.png` → "Home Screen"

Bulk set multiple captions:
```
appshot_captions with device: "iphone", action: "bulk-set", captions: "{\"home.png\": \"Welcome\", \"settings.png\": \"Settings\"}"
```

Add translations:
```
appshot_captions with device: "iphone", action: "set", filename: "home.png", caption: "Bienvenido", language: "es"
```

### 3. Apply Styling

List gradient presets:
```
appshot_gradients with action: "list"
```

Apply a gradient:
```
appshot_gradients with action: "apply", preset: "ocean"
```

Set background image:
```
appshot_backgrounds with action: "set", image: "./bg.jpg", fit: "cover"
```

Configure device settings:
```
appshot_config with device: "iphone", frameScale: 0.85, captionPosition: "above"
```

### 4. Build Screenshots

Build all devices and languages:
```
appshot_build
```

Build specific devices:
```
appshot_build with devices: ["iphone", "ipad"]
```

Build with App Store presets:
```
appshot_build with presets: ["iphone-6-9", "ipad-13"]
```

### 5. Frame Only (No Background)

Apply device frames without gradients or captions:
```
appshot_frame with input: "./screenshots/iphone"
```

Frame with output directory:
```
appshot_frame with input: "./screenshots/iphone", outputDir: "./framed"
```

Frame recursively:
```
appshot_frame with input: "./screenshots", recursive: true
```

Preview what would be framed:
```
appshot_frame with input: "./screenshots/iphone", dryRun: true
```

### 6. Validate

Check App Store compliance:
```
appshot_validate
```

## Common Scenarios

### New iPhone-Only Project

1. `appshot_init` with `force: true`
2. User adds screenshots to `screenshots/iphone/`
3. `appshot_captions` - set captions for each screenshot
4. `appshot_gradients` - apply preferred gradient
5. `appshot_build` with `devices: ["iphone"]`

### Multi-Language App Store Submission

1. `appshot_init` with `force: true`
2. `appshot_captions` - add English captions
3. `appshot_localize` with `languages: ["es", "fr", "de", "ja"]`
4. `appshot_build` with `languages: ["en", "es", "fr", "de", "ja"]`
5. `appshot_validate`

### Quick Styling Update

1. `appshot_gradients` with `action: "list"` to see options
2. `appshot_gradients` with `action: "apply", preset: "sunset"`
3. `appshot_build`

### Quick Auto-Caption Project

When filenames are descriptive (e.g., `home-screen.png`, `settings_page.png`):

1. `appshot_init` with `force: true`
2. User adds screenshots to `screenshots/iphone/`
3. `appshot_captions` with `device: "iphone", action: "auto"`
4. `appshot_gradients` with `action: "apply", preset: "ocean"`
5. `appshot_build` with `devices: ["iphone"]`

Captions are auto-generated from filenames (hyphens/underscores become spaces, title case applied).

### Frame Only (Design Mockups)

For quick device mockups without backgrounds or captions:

1. `appshot_frame` with `input: "./screenshots/iphone", outputDir: "./framed"`

Output has transparent background - perfect for presentations, design comps, or overlaying on custom backgrounds.

## Device Resolutions

### Required for App Store
- **iPhone 6.9"**: 1290x2796 or 1320x2868
- **iPad 13"**: 2064x2752 or 2048x2732

### Optional
- **Mac**: 2880x1800 (16:10)
- **Watch Ultra**: 410x502

## Configuration Options

> Note: The options below describe **v1 legacy layout controls**. v2 uses fixed layout modes and removes manual positioning. See `docs/layout-v2.md`.

### Frame Positioning
- `frameScale`: 0.1-1.5 (default: 0.9)
- `framePosition`: 0-100 or "center"
- `captionPosition`: "above", "below", "overlay"

### Caption Styling
- `captionSize`: Font size in pixels
- `marginTop`: Top margin for caption
- `marginBottom`: Bottom margin for caption

## Resources

- `references/templates.md` - Legacy v1 templates (modern/minimal/etc.)
- `docs/layout-v2.md` - v2 fixed-layout rules (header/footer/screenshot-only)
- `docs/migration-v2.md` - v1 to v2 migration guide
- `references/gradients.md` - All 24 gradient presets with colors
- `references/fonts.md` - All 10 embedded font families
- `references/troubleshooting.md` - Common errors and solutions
