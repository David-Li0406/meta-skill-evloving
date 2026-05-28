---
name: design-brief-creation
description: |
  Frameworks for analyzing visual inspiration and translating it into actionable design specifications. Covers typography, color, spacing, and component systems.
  
  USE THIS SKILL WHEN:
  - Analyzing reference sites or moodboards
  - Creating typography specifications
  - Defining color systems
  - Building spacing/layout systems
  - Specifying components
  - Translating brand to visual language
  
  PROVIDES: Analysis frameworks, system templates, specification formats
allowed-tools: Read, Grep, Glob, WebFetch
---

# Design Brief Creation Skill

## Overview

Good design briefs turn subjective preferences into objective specifications. This skill provides frameworks for systematically analyzing inspiration and producing implementation-ready design systems.

---

## Framework 1: Inspiration Analysis

### The Systematic Approach

Don't look at reference sites and say "I like it." Instead, dissect them layer by layer.

```
INSPIRATION ANALYSIS LAYERS

┌─────────────────────────────────────────────────────────────┐
│ LAYER 1: TYPOGRAPHY                                          │
│ What fonts? What sizes? What weights? What spacing?          │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ LAYER 2: COLOR                                               │
│ What palette? Warm or cool? Saturated or muted? Contrast?    │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ LAYER 3: LAYOUT                                              │
│ Grid structure? White space? Density? Alignment?             │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ LAYER 4: IMAGERY                                             │
│ Photo style? Illustrations? Graphics? Treatment?             │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ LAYER 5: DETAILS                                             │
│ Corners? Shadows? Borders? Icons? Micro-interactions?        │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ LAYER 6: FEELING                                             │
│ Energy level? Personality? Era? What emotion does it evoke?  │
└─────────────────────────────────────────────────────────────┘
```

### Analysis Template Per Reference

```markdown
## Reference: [URL]

### Client Said
"[Their exact words about why they like it]"

### Typography Analysis
- **Heading typeface:** [Serif/Sans-serif/Slab] - [Style: geometric, humanist, etc.]
- **Body typeface:** [Same/Different]
- **Size contrast:** [Extreme/Moderate/Subtle] between headings and body
- **Weight usage:** [Light/Regular/Bold predominant]
- **Case:** [Sentence/Title/UPPERCASE for headings]
- **Letter-spacing:** [Tight/Normal/Wide]

### Color Analysis
- **Dominant color:** [Hex estimate or description]
- **Accent color:** [If present]
- **Background:** [White/Off-white/Colored/Dark]
- **Temperature:** [Warm/Neutral/Cool]
- **Saturation:** [Muted/Moderate/Vibrant]
- **Overall contrast:** [High/Medium/Low]

### Layout Analysis
- **Grid:** [Visible structure/Organic/Mixed]
- **White space:** [Minimal/Moderate/Generous]
- **Density:** [Content-heavy/Balanced/Sparse]
- **Alignment:** [Strict/Relaxed]
- **Section rhythm:** [Consistent/Varied heights]

### Imagery Analysis
- **Photography style:** [Editorial/Lifestyle/Product/Abstract]
- **Treatment:** [Natural/Filtered/Duotone/B&W]
- **Illustrations:** [Present/Absent] - [Style if present]
- **Graphics/shapes:** [Geometric/Organic/None]

### Detail Analysis
- **Border radius:** [Sharp/Slight/Rounded/Pill]
- **Shadows:** [None/Subtle/Pronounced]
- **Borders:** [Used/Not used]
- **Icons:** [Style if present]
- **Animation:** [None/Subtle/Prominent]

### Emotional Analysis
- **Energy:** [Calm — — — — Dynamic] (1-5)
- **Personality:** [Serious — — — — Playful] (1-5)
- **Sophistication:** [Accessible — — — — Premium] (1-5)

### Key Takeaways
- **Adopt:** [What to bring into our design]
- **Adapt:** [What to modify for our context]
- **Avoid:** [What doesn't fit our brand]
```

### Cross-Reference Synthesis

After analyzing multiple references:

```markdown
## Pattern Synthesis

### Consistent Patterns (High Confidence)
Elements appearing in 3+ references = likely core to what client wants
- [Pattern 1]
- [Pattern 2]
- [Pattern 3]

### Variable Patterns (Needs Decision)
Elements that differ across references
- [Element]: Reference A does [X], Reference B does [Y]
  → Recommendation: [Pick one with rationale]

### Contradictions (Needs Client Input)
When client preferences conflict with each other
- [Contradiction]
  → Question for client: [Specific question]

### Client Explicit Preferences
- Likes: [What they explicitly said they want]
- Dislikes: [What they explicitly said to avoid]
```

---

## Framework 2: Typography System

### Type Classification Quick Reference

```
TYPE CLASSIFICATIONS

SERIF (Traditional, trustworthy, editorial)
├── Old Style (Garamond, Caslon) - Classic, bookish
├── Transitional (Times, Baskerville) - Balanced, professional
├── Modern (Bodoni, Didot) - High contrast, fashion/luxury
└── Slab (Rockwell, Clarendon) - Strong, confident

SANS-SERIF (Modern, clean, digital-native)
├── Grotesque (Helvetica, Arial) - Neutral, corporate
├── Neo-Grotesque (Inter, SF Pro) - Clean, contemporary
├── Geometric (Futura, Poppins) - Modern, friendly
└── Humanist (Gill Sans, Open Sans) - Warm, readable

DISPLAY (Headlines only, personality)
├── Script - Elegant, personal
├── Decorative - Unique, brand-specific
└── Monospace - Technical, code-like
```

### Brand Voice to Typography Translation

```
VOICE-TO-TYPE MATRIX

Voice Attribute        Serif Choice              Sans Choice
─────────────────────────────────────────────────────────────
Formal (8-10)          Modern serif (Bodoni)     Grotesque (Helvetica)
Friendly (1-3)         Old Style (Caslon)        Geometric (Poppins)
Premium (8-10)         Modern serif              Geometric (Futura)
Approachable (1-3)     Slab serif                Humanist (Open Sans)
Technical (8-10)       None (use sans)           Grotesque or Mono
Creative (high)        Display/Script accent     Geometric with display
Traditional            Transitional              Avoid or minimal
Contemporary           Avoid or accent only      Neo-Grotesque (Inter)
```

### Type Scale Systems

```
MODULAR SCALES

Base: 16px (1rem) - industry standard body size

Scale Ratio Options:
- 1.125 (Major Second) - Subtle, dense designs
- 1.200 (Minor Third) - Most common, balanced
- 1.250 (Major Third) - Clear hierarchy
- 1.333 (Perfect Fourth) - Strong hierarchy
- 1.500 (Perfect Fifth) - Very dramatic

Example with 1.250 (Major Third), base 16px:
- Display:    49px (3.052rem)
- H1:         39px (2.441rem)
- H2:         31px (1.953rem)
- H3:         25px (1.563rem)
- H4:         20px (1.25rem)
- Body:       16px (1rem)
- Small:      13px (0.8rem)
- Caption:    10px (0.64rem)
```

### Line Height Guidelines

```
LINE HEIGHT BY USE CASE

Headlines (Display, H1-H2):
- Tight: 1.1 - 1.2
- Works for: Short headlines, display text
- Avoid for: Multi-line headings

Subheadings (H3-H4):
- Medium: 1.2 - 1.3
- Works for: Section headings

Body Text:
- Comfortable: 1.5 - 1.7
- 1.5 = More compact
- 1.6 = Standard
- 1.7 = Airy, premium feel

Small Text / Captions:
- Slightly tighter: 1.4 - 1.5
```

### Letter Spacing Guidelines

```
LETTER SPACING (Tracking)

Headlines:
- Normal to tight: 0 to -0.02em
- Uppercase: Always add +0.05em to +0.1em

Body Text:
- Usually 0 (normal)
- Never negative

Small Text:
- Slightly positive: +0.01em to +0.02em
- Improves readability at small sizes

Uppercase Text:
- Always add spacing: +0.05em minimum
- Prevents letters from crowding
```

---

## Framework 3: Color System

### Color Psychology Quick Reference

```
COLOR PSYCHOLOGY FOR BRANDS

Blue
- Trust, professionalism, calm, corporate
- Use for: Finance, tech, healthcare, B2B
- Avoid when: Want to stand out, warmth needed

Green
- Nature, health, growth, sustainability
- Use for: Wellness, eco, finance (growth)
- Avoid when: Appetite appeal needed

Red
- Energy, urgency, passion, appetite
- Use for: Food, sales, entertainment
- Avoid when: Calm/trust needed

Orange
- Friendly, energetic, affordable, creative
- Use for: Calls to action, youth brands
- Avoid when: Premium positioning

Yellow
- Optimism, warmth, caution, attention
- Use for: Highlights, warning states
- Avoid as: Primary (hard to read)

Purple
- Luxury, creativity, spirituality
- Use for: Premium, creative, wellness
- Avoid when: Mass market appeal needed

Pink
- Feminine, playful, modern, care
- Use for: Beauty, youth, healthcare
- Stereotyped: Use intentionally

Black
- Sophistication, luxury, power, elegance
- Use for: Fashion, luxury, minimalist
- Caution: Can feel cold/heavy

White/Off-white
- Clean, pure, minimal, space
- Use for: Backgrounds, breathing room
- Pure white (#fff) = Clinical
- Off-white = Warmer, natural
```

### Building a Color Palette

```
COLOR PALETTE STRUCTURE

CORE COLORS (3 max for brand recognition)
├── Primary: Main brand color, CTAs, key actions
├── Secondary: Supporting, alternative actions
└── Accent: Highlights, special moments (use sparingly)

NEUTRALS (Essential for UI)
├── Background: Page background (usually white/off-white)
├── Surface: Cards, elevated elements
├── Border: Dividers, subtle separation
├── Text Primary: Main body text (not pure black—use #1a1a1a)
├── Text Secondary: Supporting text, labels
└── Text Muted: Disabled, placeholder

SEMANTIC (For states and feedback)
├── Success: Positive actions, confirmation (green family)
├── Warning: Caution states (yellow/orange family)
├── Error: Errors, destructive actions (red family)
└── Info: Informational messages (blue family)
```

### Accessible Color Combinations

```
WCAG CONTRAST REQUIREMENTS

AA Standard (Minimum):
- Regular text: 4.5:1 contrast ratio
- Large text (18px+ or 14px bold): 3:1
- UI components: 3:1

AAA Standard (Enhanced):
- Regular text: 7:1
- Large text: 4.5:1

COMMON ACCESSIBLE COMBINATIONS

On White Background (#FFFFFF):
- Black text (#000000): 21:1 ✓
- Dark gray (#1a1a1a): 16.1:1 ✓
- Medium gray (#666666): 5.7:1 ✓
- Light gray (#999999): 2.8:1 ✗ (fails for small text)

Blue on White:
- Navy (#1e3a5f): 10.5:1 ✓
- Medium blue (#2563eb): 4.6:1 ✓
- Light blue (#60a5fa): 2.4:1 ✗

CHECK YOUR COLORS: Use https://webaim.org/resources/contrastchecker/
```

### Color Temperature and Mood

```
WARM vs COOL PALETTES

WARM (Inviting, friendly, energetic)
- Reds, oranges, yellows
- Warm grays (beige, taupe)
- Off-white backgrounds
- Use for: Hospitality, food, lifestyle, approachable brands

COOL (Professional, calm, trustworthy)
- Blues, greens, purples
- Cool grays (slate, charcoal)
- Pure white or blue-tinted backgrounds
- Use for: Corporate, tech, healthcare, finance

NEUTRAL (Versatile, sophisticated)
- True grays
- Black and white
- Use for: Luxury, minimalist, editorial

MIXING TEMPERATURES
- Warm primary + cool neutral = Balanced, approachable
- Cool primary + warm accent = Professional with energy
- All warm = Can feel unsophisticated
- All cool = Can feel cold/distant
```

---

## Framework 4: Spacing System

### The 8-Point Grid

```
WHY 8PX BASE?

- Divisible by 2 (half-step: 4px)
- Divisible by 4 (quarter-step)
- Scales cleanly across screen sizes
- Matches common device pixels
- Standard in design systems (Material, Apple)

SPACING SCALE (8px base)

Token    Value    Use For
────────────────────────────────────
4xs      4px      Tight gaps, inline spacing
3xs      8px      Icon-to-text, tight padding
2xs      12px     Small component padding
xs       16px     Default component padding
sm       24px     Between related items
md       32px     Between distinct elements
lg       48px     Section padding (mobile)
xl       64px     Section padding (desktop)
2xl      96px     Major section breaks
3xl      128px    Hero/footer spacing
4xl      192px    Maximum breathing room
```

### Spacing Relationships

```
SPACING HIERARCHY

Within Components (Tight)
- Icon to label: 8px
- Input padding: 12-16px
- Button padding: 12px vertical, 24px horizontal

Between Related Items (Medium)
- Stack of form fields: 16-24px
- List items: 16px
- Paragraph spacing: 1.5em

Between Components (Generous)
- Card to card: 24-32px
- Form to CTA: 32px

Between Sections (Very Generous)
- Mobile: 48-64px
- Desktop: 64-96px

Page Margins
- Mobile: 16-24px
- Tablet: 32-48px
- Desktop: 64px+ or percentage
```

### Grid System Basics

```
12-COLUMN GRID (Standard)

Why 12?
- Divisible by 2, 3, 4, 6
- Flexible layouts: 50/50, 33/33/33, 25/25/25/25
- Industry standard, familiar to developers

COMMON COLUMN CONFIGURATIONS

Full width:        12 columns
Two equal:         6 + 6
Two unequal:       4 + 8, 3 + 9
Three equal:       4 + 4 + 4
Three unequal:     2 + 8 + 2 (centered content)
Four equal:        3 + 3 + 3 + 3
Sidebar + Content: 3 + 9 or 4 + 8

RESPONSIVE BREAKPOINTS (Common)
- Mobile: 0-639px (full width, stacked)
- Tablet: 640-1023px (2-column possible)
- Desktop: 1024-1279px (full grid)
- Large: 1280px+ (max-width container)

MAX-WIDTH OPTIONS
- 1200px: Comfortable, common
- 1280px: Slightly wider
- 1440px: Very wide, modern displays
- Percentage (90%): Fluid, needs max-width cap
```

---

## Framework 5: Component Thinking

### Component Categories

```
COMPONENT TAXONOMY

NAVIGATION
- Header / Navbar
- Footer
- Sidebar navigation
- Breadcrumbs
- Pagination
- Tabs
- Mobile menu

CONTENT DISPLAY
- Hero sections
- Feature blocks
- Card layouts
- Lists
- Tables
- Accordions
- Timelines

SOCIAL PROOF
- Testimonials
- Reviews
- Logo bars
- Case study cards
- Stats/numbers

MEDIA
- Image galleries
- Video embeds
- Sliders/carousels
- Lightboxes
- Before/after

FORMS & INPUT
- Text inputs
- Selects
- Checkboxes/radios
- File uploads
- Search
- Multi-step forms

ACTIONS
- Buttons (primary, secondary, tertiary)
- Links
- CTAs (banner, sticky, popup)

FEEDBACK
- Alerts/notifications
- Toast messages
- Progress indicators
- Loading states
- Empty states
- Error states

OVERLAYS
- Modals
- Drawers
- Tooltips
- Popovers
- Dropdowns
```

### Component Specification Template

```markdown
## Component: [Name]

### Purpose
What problem does this solve? When is it used?

### Visual Specification

**Layout**
- Structure: [How elements are arranged]
- Alignment: [Left/Center/Right]
- Responsive: [How it changes on mobile]

**Typography**
- Heading: [Size/Weight/Font]
- Body: [Size/Weight/Font]
- Meta: [Size/Weight/Font]

**Colors**
- Background: [Token or hex]
- Text: [Token or hex]
- Border: [Token or hex]
- Hover state: [Changes]

**Spacing**
- Internal padding: [Value]
- Between elements: [Value]
- External margin: [Value]

**Details**
- Border radius: [Value]
- Shadow: [Value]
- Border: [Value]

### Content Slots
| Slot | Type | Required | Max Length | Notes |
|------|------|----------|------------|-------|
| [Name] | [text/image/etc] | [Y/N] | [chars/dimensions] | [guidance] |

### States
- Default: [Description]
- Hover: [Changes]
- Active/Pressed: [Changes]
- Focus: [Outline/ring]
- Disabled: [Appearance]
- Loading: [Behavior]
- Error: [Appearance]

### Accessibility
- Focus visible: [Yes + how]
- Keyboard navigable: [Yes + how]
- Screen reader: [Aria labels needed]
- Color contrast: [Verified]

### Usage Guidelines
- Do: [Best practices]
- Don't: [Anti-patterns]

### Code Notes
- [Implementation hints for developers]
```

---

## Framework 6: Brand-to-Visual Translation

### Voice Dimension to Visual Mapping

```
COMPREHENSIVE VOICE-TO-VISUAL TRANSLATION

┌─────────────────────────────────────────────────────────────┐
│ FORMALITY (Voice: 1-10)                                      │
├─────────────────────────────────────────────────────────────┤
│ Low (1-3): Casual, conversational                            │
│ → Sans-serif, especially geometric (Poppins, Nunito)        │
│ → Rounded corners                                            │
│ → Warmer colors                                              │
│ → Relaxed spacing                                            │
│ → Casual photography (candid, lifestyle)                     │
│                                                              │
│ High (8-10): Professional, authoritative                     │
│ → Serif or clean sans (Times, Helvetica)                    │
│ → Sharp or subtle corners                                    │
│ → Cooler, muted colors                                       │
│ → Precise alignment                                          │
│ → Professional photography (polished, composed)              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ ENTHUSIASM (Voice: 1-10)                                     │
├─────────────────────────────────────────────────────────────┤
│ Low (1-3): Calm, measured                                    │
│ → Subtle color palette (muted, monochromatic)               │
│ → Consistent, predictable layouts                            │
│ → Minimal animation                                          │
│ → Even rhythm between sections                               │
│                                                              │
│ High (8-10): Energetic, exciting                             │
│ → Vibrant, saturated colors                                  │
│ → Dynamic layouts (asymmetry, varied sections)               │
│ → Motion and animation                                       │
│ → Bold size contrasts                                        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ WARMTH (Voice: 1-10)                                         │
├─────────────────────────────────────────────────────────────┤
│ Low (1-3): Professional, objective                           │
│ → Cool color temperature (blues, grays)                      │
│ → Pure white backgrounds                                     │
│ → Minimal imagery or abstract                                │
│ → Geometric shapes                                           │
│                                                              │
│ High (8-10): Friendly, personal                              │
│ → Warm color temperature (yellows, oranges, warm neutrals)   │
│ → Off-white or cream backgrounds                             │
│ → People in photography (faces, lifestyle)                   │
│ → Organic shapes, rounded elements                           │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ DIRECTNESS (Voice: 1-10)                                     │
├─────────────────────────────────────────────────────────────┤
│ Low (1-3): Subtle, nuanced                                   │
│ → Softer CTAs (outline buttons, text links)                  │
│ → Gradual information reveal                                 │
│ → Subtle hover states                                        │
│                                                              │
│ High (8-10): Bold, clear                                     │
│ → Strong CTAs (high contrast buttons)                        │
│ → Prominent value propositions                               │
│ → Clear visual hierarchy                                     │
│ → Obvious interactive elements                               │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ TECHNICAL COMPLEXITY (Voice: 1-10)                           │
├─────────────────────────────────────────────────────────────┤
│ Low (1-3): Simple, accessible                                │
│ → Large, simple typography                                   │
│ → Generous white space                                       │
│ → Minimal data/charts                                        │
│ → Icon-based communication                                   │
│                                                              │
│ High (8-10): Detailed, sophisticated                         │
│ → Denser information layouts                                 │
│ → Data visualization comfort                                 │
│ → Smaller supporting text sizes                              │
│ → Technical imagery acceptable                               │
└─────────────────────────────────────────────────────────────┘
```

### Positioning to Visual Translation

```
MARKET POSITIONING → VISUAL EXPRESSION

Premium/Luxury
- Generous white space (xl+ between sections)
- High-quality photography
- Restrained color (1-2 colors max)
- Elegant typography (serifs or refined sans)
- Subtle details (thin borders, soft shadows)
- Animation: Slow, refined

Accessible/Affordable
- Efficient use of space
- Friendly, approachable photography
- More color variety acceptable
- Rounded, friendly typography
- Bolder, more obvious UI elements
- Animation: Quick, functional

Innovative/Disruptive
- Unexpected layouts (break the grid)
- Bold color choices
- Contemporary typography
- Unique visual elements
- Animation: Prominent, delightful

Trustworthy/Established
- Classic, proven layouts
- Muted, professional colors
- Traditional typography
- Predictable patterns
- Animation: Minimal, functional

Playful/Fun
- Asymmetric, dynamic layouts
- Bright, saturated colors
- Rounded, bouncy typography
- Illustrations, graphics
- Animation: Bouncy, playful
```

---

## References

For additional frameworks and examples, see:
- `references/typography-pairings.md` - Proven font combinations
- `references/color-palette-examples.md` - Real-world palette analysis
- `references/component-patterns.md` - Common component implementations