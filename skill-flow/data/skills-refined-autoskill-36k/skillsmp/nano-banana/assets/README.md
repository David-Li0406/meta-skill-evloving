# Nano Banana Assets

Brand assets for TrendLife and other branded slide generation.

## Directory Structure

```
assets/
├── logos/                    # Brand logos (extracted and processed)
│   ├── trendlife-logo.png    # TrendLife logo (166 KB)
│   └── README.md             # Logo usage guidelines
├── templates/                # Reference PowerPoint templates
│   ├── 1201_TrendLife PowerPoint Deck.pptx  # TrendLife template (17 MB)
│   └── README.md             # Template information
└── README.md                 # This file
```

## Asset Types

### Logos
Processed brand logos ready for overlay on generated slides.

**Current:**
- `logos/trendlife-logo.png` - TrendLife product logo (icon + text)

**Future:**
- TrendAI logo
- Alternative logo versions (white, icon-only)

### Templates
Original PowerPoint templates for reference.

**Purpose:**
- Color palette extraction
- Layout structure reference
- Brand asset source
- Compatibility testing

**Current:**
- `templates/1201_TrendLife PowerPoint Deck.pptx` - TrendLife official template

## Usage

**Logo Overlay:**

**IMPORTANT:** Run with `uv run` to ensure dependencies are available.

```python
#!/usr/bin/env python3
# /// script
# dependencies = ["pillow"]
# ///

from pathlib import Path
from logo_overlay import overlay_logo

overlay_logo(
    background_path=generated_slide_path,
    logo_path=Path(__file__).parent / 'assets/logos/trendlife-logo.png',
    output_path=final_output_path,
    layout_type='content'
)
```

**Template Reference:**
- Extract colors from theme XML
- Analyze slide master layouts
- Reference logo placement positions
- Test output compatibility

## File Size Guidelines

**Logos:**
- PNG with transparency (RGBA)
- Optimized for web (typically 100-300 KB)
- High resolution (support 4K slides)

**Templates:**
- Keep original files unmodified
- Store compressed if possible
- Document source and version

## Notes

- All brand assets are Trend Micro property
- Internal use only
- Do not modify original templates
- Maintain asset quality and accuracy
