# Brand Logo Assets

## TrendLife Logo

**Source:** Official TrendLife PowerPoint template (`assets/templates/1201_TrendLife PowerPoint Deck.pptx`)
- **Original file:** `ppt/media/image3.png` from template (12532×1490 pixels)
- **Processing:** Cropped using PowerPoint srcRect values to match template display
- **srcRect values:** l=0, t=1, r=38620, b=8728 (removes 38.62% right, 8.73% bottom)
- **Crop region:** (0, 0, 7693, 1360) - removes tagline and bottom margin
- **Final asset:** `trendlife-logo.png` (7693×1360 pixels)

**Why This Crop:**
- PowerPoint template uses srcRect cropping with `noChangeAspect=1`
- Original image3.png is 12532×1490 (8.4:1 ratio) and includes tagline "Where Intelligence Meets Care"
- srcRect crop removes tagline and margins: 7693×1360 (5.66:1 ratio)
- At 1920×1080, displays as 294.6×52.0 pixels maintaining 5.66:1 aspect ratio
- Result: complete "TRENDLIFE" text without distortion

**Components:**
- Red circular icon with "t" symbol (left)
- "TRENDLIFE" text (black "TREND" + red "LIFE")
- Tagline removed (was: "Where Intelligence Meets Care")
- Transparent borders (~150px left/right, ~145px top, ~5px bottom)

**Specifications:**
- **Format:** PNG with transparency (RGBA)
- **Dimensions:** 7693 × 1360 pixels (5.66:1 aspect ratio)
- **Visible content:** 7393 × 1210 pixels (excludes transparent margins)
- **Internal margins:** ~150px left/right (~6px at scaled size), ~145px top (~3px at scaled size)
- **Size:** ~150 KB (optimized PNG)
- **DPI:** High resolution, suitable for all slide sizes

**Usage:**
- Primary logo for TrendLife branded presentations
- Place in bottom-right corner of slides at 15.34% of slide width
- Maintain aspect ratio when resizing (native 5.66:1)
- Calibrated padding: (17, 20) produces visible content at (22, 20) from edges

**PowerPoint Template Position (1920×1080):**
- Logo size: 294.6 × 52.0 pixels (15.34% of slide width)
- Position (frame): x=1608.4px, y=1008.0px
- Padding (calibrated): right=17px, bottom=20px
- Visible content padding: right=22px, bottom=20px (verified via screenshot)

**Guidelines:**
- Never distort aspect ratio
- Maintain minimum clear space (10% of logo width)
- Always use PNG with transparency
- Never recreate or modify logo
- Account for internal transparent margins when positioning

**License:** Trend Micro brand assets, internal use only

---

## Future Logos

**TrendAI Logo:** To be added when TrendAI template is implemented

**Alternative Versions:**
- White logo (for dark backgrounds) - not yet implemented
- Icon-only version - can be cropped from main logo if needed
