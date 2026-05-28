# Component Patterns

## How to Use This Reference

These patterns provide starting points for common components. Adapt specifications to your design system—don't use values that conflict with your established tokens.

---

## Pattern 1: Hero Sections

### Full-Width Hero (Image Background)

```
STRUCTURE
┌────────────────────────────────────────────────────────────┐
│                    [Background Image]                       │
│                                                             │
│    ┌──────────────────────────────────────────┐            │
│    │         [Headline - H1]                   │            │
│    │                                           │            │
│    │    [Subheadline - Body Large]            │            │
│    │                                           │            │
│    │    [Primary CTA]   [Secondary CTA]       │            │
│    └──────────────────────────────────────────┘            │
│                                                             │
└────────────────────────────────────────────────────────────┘

SPECIFICATIONS
- Full viewport width
- Height: 80-100vh (desktop), auto with padding (mobile)
- Overlay: Dark gradient (rgba(0,0,0,0.4-0.6)) for text readability
- Content max-width: 600-800px, centered
- Padding: 64-96px vertical

TYPOGRAPHY
- Headline: Display size, white, centered
- Subheadline: Body large, white/off-white, centered
- Max headline width: ~20 characters/line

CTAs
- Primary: High contrast (white bg, dark text)
- Secondary: Ghost/outline (white border, white text)
- Spacing between: 16px

RESPONSIVE
- Mobile: Stack CTAs vertically
- Reduce headline size 60-70%
- Maintain adequate padding (48px+)
```

---

### Split Hero (Image + Content)

```
STRUCTURE
┌────────────────────────────────┬──────────────────────────┐
│                                │                          │
│         [Content]              │                          │
│                                │      [Image/Visual]      │
│    [Headline - H1]             │                          │
│                                │                          │
│    [Body text]                 │                          │
│                                │                          │
│    [Primary CTA]               │                          │
│                                │                          │
└────────────────────────────────┴──────────────────────────┘

SPECIFICATIONS
- 50/50 or 40/60 split
- Content side padding: 64-96px
- Content vertical centering
- Image: Cover, maintain aspect ratio

TYPOGRAPHY
- Headline: H1, left-aligned
- Body: Regular, 2-3 paragraphs max
- Keep content concise

VARIATIONS
- Image left, content right
- Content overlapping image (offset)
- Video instead of image

RESPONSIVE
- Stack: Image on top, content below
- Or: Content only, image as background
```

---

### Minimal Hero (Text-Focused)

```
STRUCTURE
┌────────────────────────────────────────────────────────────┐
│                                                             │
│                      [Eyebrow - Caption]                    │
│                                                             │
│                      [Headline - Display]                   │
│                                                             │
│                      [Subheadline - Body]                   │
│                                                             │
│                      [Primary CTA]                          │
│                                                             │
└────────────────────────────────────────────────────────────┘

SPECIFICATIONS
- White or solid color background
- Centered text
- Generous vertical padding: 96-128px
- Content max-width: 800px

TYPOGRAPHY
- Eyebrow: Caption size, uppercase, primary color, tracked
- Headline: Display size, tight line-height
- Subheadline: Body large, generous line-height

USE WHEN
- Clean, minimal aesthetic
- Copy is the hero
- No strong visual assets available
```

---

## Pattern 2: Feature Sections

### Feature Grid (3-4 Columns)

```
STRUCTURE
┌────────────────────────────────────────────────────────────┐
│                    [Section Heading]                        │
│                    [Section Subheading]                     │
├──────────────────┬──────────────────┬──────────────────────┤
│                  │                  │                      │
│     [Icon]       │     [Icon]       │     [Icon]           │
│                  │                  │                      │
│   [Feature 1]    │   [Feature 2]    │   [Feature 3]        │
│     [Title]      │     [Title]      │     [Title]          │
│  [Description]   │  [Description]   │  [Description]       │
│                  │                  │                      │
└──────────────────┴──────────────────┴──────────────────────┘

SPECIFICATIONS
- Section padding: 64-96px vertical
- Column gap: 32-48px
- Item max-width: 300-350px

ICON
- Size: 48-64px (or 24-32px for subtle)
- Color: Primary or muted
- Style: Consistent (all outline or all filled)

TYPOGRAPHY
- Title: H4 or H5, bold
- Description: Body or Body Small
- 2-3 sentences max per feature

ALIGNMENT
- Centered: Good for 3 columns, icon-led
- Left: Good for 4 columns, dense content

RESPONSIVE
- 3-col → 2-col → 1-col
- Stack features vertically on mobile
```

---

### Feature List (Icon + Text Rows)

```
STRUCTURE
┌────────────────────────────────────────────────────────────┐
│  [Icon]    [Feature Title]                                  │
│            [Feature description spans multiple lines if     │
│            needed, staying aligned with title]              │
├────────────────────────────────────────────────────────────┤
│  [Icon]    [Feature Title]                                  │
│            [Feature description]                            │
├────────────────────────────────────────────────────────────┤
│  [Icon]    [Feature Title]                                  │
│            [Feature description]                            │
└────────────────────────────────────────────────────────────┘

SPECIFICATIONS
- Icon size: 24-32px
- Icon-to-text gap: 16-24px
- Row gap: 24-32px
- Max-width: 600px (for readability)

USE WHEN
- More features to show (5+)
- Features need longer explanations
- Vertical space is preferred over horizontal
```

---

### Alternating Features (Image + Text, Zigzag)

```
STRUCTURE
┌───────────────────────────┬───────────────────────────────┐
│                           │     [Feature Title - H2]       │
│       [Image/Visual]      │                                │
│                           │     [Description]              │
│                           │     [Learn more link]          │
└───────────────────────────┴───────────────────────────────┘
┌───────────────────────────┬───────────────────────────────┐
│     [Feature Title - H2]  │                                │
│                           │       [Image/Visual]           │
│     [Description]         │                                │
│     [Learn more link]     │                                │
└───────────────────────────┴───────────────────────────────┘

SPECIFICATIONS
- 50/50 or 40/60 split
- Vertical padding between rows: 64-96px
- Images: Consistent aspect ratio (16:9 or 3:2)
- Content vertically centered

USE WHEN
- Features need visual explanation
- Long-form feature page
- Storytelling approach
```

---

## Pattern 3: Social Proof

### Testimonial Card

```
STRUCTURE
┌────────────────────────────────────────────────────────────┐
│                                                             │
│    "[Quote text goes here. Keep it focused on one          │
│    key benefit or transformation.]"                        │
│                                                             │
│    ┌──────┐                                                 │
│    │ IMG  │  [Name]                                         │
│    └──────┘  [Title, Company]                               │
│                                                             │
└────────────────────────────────────────────────────────────┘

SPECIFICATIONS
- Card padding: 32-48px
- Background: White or subtle color
- Border: None or subtle (1px light gray)
- Shadow: Subtle or none
- Border-radius: 8-16px

TYPOGRAPHY
- Quote: Body large, italic optional
- Name: Body bold
- Title: Caption, muted color

AVATAR
- Size: 48-64px
- Border-radius: Full circle
- Optional: Skip if no photos

QUOTE MARKS
- Decorative: Large quote marks in primary color (optional)
- Or use standard quotation marks in text
```

---

### Testimonial Carousel

```
STRUCTURE
┌────────────────────────────────────────────────────────────┐
│                                                             │
│    ◀  [Testimonial Card]  [Partial Card]  [Partial] ▶     │
│                                                             │
│                      ● ○ ○ ○ ○                              │
│                                                             │
└────────────────────────────────────────────────────────────┘

SPECIFICATIONS
- Show 1 full + partials, or 3 full cards
- Navigation: Arrows + dots
- Auto-advance: Optional (pause on hover)
- Gap between cards: 24-32px

ACCESSIBILITY
- Keyboard navigable
- Pause button if auto-advancing
- Swipe support on mobile
```

---

### Logo Bar (Trust Badges)

```
STRUCTURE
┌────────────────────────────────────────────────────────────┐
│    [Logo]    [Logo]    [Logo]    [Logo]    [Logo]          │
└────────────────────────────────────────────────────────────┘

SPECIFICATIONS
- Logo height: 24-40px (consistent)
- Logo spacing: 48-64px between
- Logo color: Grayscale (unless specified)
- Opacity: 60-80% (subtle)
- Alignment: Center

VARIATIONS
- Static row
- Infinite scroll animation
- "As featured in" or "Trusted by" label above

RESPONSIVE
- Wrap to 2 rows on tablet
- Wrap to 3+ rows or scroll on mobile
```

---

### Stats Section

```
STRUCTURE
┌──────────────────┬──────────────────┬──────────────────────┐
│                  │                  │                      │
│      10K+        │       99%        │       24/7           │
│                  │                  │                      │
│  Active Users    │   Satisfaction   │     Support          │
│                  │                  │                      │
└──────────────────┴──────────────────┴──────────────────────┘

SPECIFICATIONS
- 3-4 stats typical
- Generous spacing: 64px+ between
- Center-aligned

TYPOGRAPHY
- Number: Display or H1, primary color or black
- Label: Caption or Body Small, muted
- Optional: Unit or symbol in smaller size

ANIMATION
- Count-up on scroll (optional)
- Fade-in stagger
```

---

## Pattern 4: Forms

### Standard Input Field

```
STRUCTURE
┌────────────────────────────────────────────────────────────┐
│  Label                                                      │
│  ┌────────────────────────────────────────────────────┐    │
│  │ Placeholder text                                    │    │
│  └────────────────────────────────────────────────────┘    │
│  Helper text or error message                              │
└────────────────────────────────────────────────────────────┘

SPECIFICATIONS
- Label: Caption or Body Small, above input
- Input height: 40-48px
- Input padding: 12-16px horizontal
- Border: 1px solid, gray (light)
- Border-radius: 4-8px (match system)
- Background: White or very light gray

STATES
- Default: Light gray border
- Focus: Primary color border, shadow ring
- Error: Red border, error text below
- Disabled: Gray background, no interaction

TYPOGRAPHY
- Label: Semi-bold, dark
- Placeholder: Regular, muted
- Helper: Caption, muted
- Error: Caption, error color
```

---

### Contact Form Layout

```
STRUCTURE
┌────────────────────────────────────────────────────────────┐
│  Contact Us                                                 │
│                                                             │
│  ┌────────────────────┐  ┌────────────────────┐            │
│  │ First Name         │  │ Last Name          │            │
│  └────────────────────┘  └────────────────────┘            │
│                                                             │
│  ┌─────────────────────────────────────────────┐           │
│  │ Email                                        │           │
│  └─────────────────────────────────────────────┘           │
│                                                             │
│  ┌─────────────────────────────────────────────┐           │
│  │ Message                                      │           │
│  │                                              │           │
│  │                                              │           │
│  └─────────────────────────────────────────────┘           │
│                                                             │
│  [Submit Button]                                            │
│                                                             │
└────────────────────────────────────────────────────────────┘

SPECIFICATIONS
- Max form width: 500-600px
- Field gap: 16-24px
- Related fields (name) side by side on desktop
- Textarea: 4-6 rows minimum
- Submit: Full width or left-aligned

RESPONSIVE
- Stack all fields single column on mobile
```

---

## Pattern 5: CTAs

### Primary Button

```
SPECIFICATIONS
- Height: 44-48px (touch-friendly)
- Padding: 12-16px vertical, 24-32px horizontal
- Border-radius: System default (4-8px or pill)
- Background: Primary color
- Text: White (ensure contrast)
- Font weight: Semi-bold (600)
- Text size: Body (16px)

STATES
- Default: Primary background
- Hover: Slightly darker (darken 10%)
- Active/Pressed: Even darker
- Focus: Ring/outline around button
- Disabled: Muted colors, no interaction
- Loading: Spinner replacing or beside text
```

---

### Secondary Button

```
SPECIFICATIONS
Same sizing as primary, but:
- Background: White or transparent
- Border: 1-2px solid, primary or dark color
- Text: Primary color or dark

HOVER
- Background: Light primary tint
- Or border color darkens
```

---

### CTA Section (Banner)

```
STRUCTURE
┌────────────────────────────────────────────────────────────┐
│                                                             │
│          [Headline - H2 or H3]                              │
│                                                             │
│          [Short description - one line]                     │
│                                                             │
│          [Primary CTA]                                      │
│                                                             │
└────────────────────────────────────────────────────────────┘

SPECIFICATIONS
- Background: Primary color or dark
- Text: White or contrast color
- Padding: 64-96px vertical
- Content: Centered, max-width 600px

PLACEMENT
- Before footer (final push)
- After major content sections
- Mid-page for long pages
```

---

## Pattern 6: Navigation

### Header/Navbar

```
STRUCTURE
┌────────────────────────────────────────────────────────────┐
│ [Logo]     [Nav Link] [Nav Link] [Nav Link]    [CTA Button]│
└────────────────────────────────────────────────────────────┘

SPECIFICATIONS
- Height: 64-80px
- Position: Sticky (recommended)
- Background: White or transparent (on hero)
- Shadow on scroll: Subtle (optional)
- Logo height: 32-40px
- Nav link spacing: 32-48px

TYPOGRAPHY
- Nav links: Body, medium weight
- Active link: Bold or underline

RESPONSIVE
- Hamburger menu at breakpoint
- Logo stays, CTA may stay or move to menu
```

---

### Mobile Menu

```
STRUCTURE
┌────────────────────────────────────────────────────────────┐
│ [Logo]                                               [X]   │
├────────────────────────────────────────────────────────────┤
│                                                             │
│   [Nav Link]                                                │
│   [Nav Link]                                                │
│   [Nav Link]                                                │
│   [Nav Link]                                                │
│                                                             │
│   [CTA Button]                                              │
│                                                             │
└────────────────────────────────────────────────────────────┘

SPECIFICATIONS
- Full screen overlay or slide-in drawer
- Links: Large touch targets (48px+ height)
- Spacing between links: 16-24px
- Animation: Smooth open/close
- Background: Solid (not transparent)
```

---

### Footer

```
STRUCTURE
┌────────────────────────────────────────────────────────────┐
│                                                             │
│  [Logo]                                                     │
│  [Company tagline or description]                           │
│                                                             │
│  [Column 1]    [Column 2]    [Column 3]    [Column 4]      │
│   Link         Link          Link          Link            │
│   Link         Link          Link          Link            │
│   Link         Link          Link          Link            │
│                                                             │
├────────────────────────────────────────────────────────────┤
│  © 2025 Company   [Privacy] [Terms]    [Social Icons]      │
└────────────────────────────────────────────────────────────┘

SPECIFICATIONS
- Background: Dark (common) or light
- Padding: 64-96px top, 32px bottom
- Column gap: 48-64px
- Link spacing: 12-16px vertical

TYPOGRAPHY
- Column headers: Body bold or H5
- Links: Body small, muted color
- Copyright: Caption, muted

RESPONSIVE
- Columns stack 2x2, then 1 column
- Social icons: Always accessible
```

---

## Pattern 7: Cards

### Content Card

```
STRUCTURE
┌────────────────────────────────────────────────────────────┐
│  ┌────────────────────────────────────────────────────┐    │
│  │                                                     │    │
│  │                    [Image]                          │    │
│  │                                                     │    │
│  └────────────────────────────────────────────────────┘    │
│                                                             │
│  [Category - Caption]                                       │
│  [Title - H4]                                               │
│  [Description - Body, 2-3 lines]                            │
│  [Read More →]                                              │
│                                                             │
└────────────────────────────────────────────────────────────┘

SPECIFICATIONS
- Border-radius: 8-16px
- Shadow: Subtle or none
- Border: None or 1px light gray
- Image aspect: 16:9 or 3:2
- Content padding: 24px

HOVER
- Subtle shadow lift
- Or image zoom
- Or title color change
```

---

### Pricing Card

```
STRUCTURE
┌────────────────────────────────────────────────────────────┐
│                                                             │
│  [Plan Name - H4]                                           │
│                                                             │
│  [Price - Display]                                          │
│  [/month - Caption]                                         │
│                                                             │
│  [Description - Body Small]                                 │
│                                                             │
│  [CTA Button]                                               │
│                                                             │
│  ────────────────                                           │
│                                                             │
│  ✓ Feature 1                                                │
│  ✓ Feature 2                                                │
│  ✓ Feature 3                                                │
│  ✓ Feature 4                                                │
│                                                             │
└────────────────────────────────────────────────────────────┘

SPECIFICATIONS
- Padding: 32-48px
- Feature list spacing: 12-16px
- Checkmarks: Primary color or gray
- Recommended tier: Highlight with border or background

HIGHLIGHT TREATMENT (Recommended Tier)
- Border: 2px primary color
- Badge: "Most Popular" ribbon
- Background: Light primary tint
- Or: Larger/elevated card
```