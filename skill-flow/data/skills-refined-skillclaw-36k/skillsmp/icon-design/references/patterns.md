# Icon Design

## Patterns


---
  #### **Name**
Base Grid System with Keylines
  #### **Description**
Establish a consistent grid with keyline shapes (circle, square, horizontal/vertical rectangles) to ensure optical balance across the entire icon set
  #### **When**
Starting any icon set or adding icons to an existing system
  #### **Example**
    24px base grid:
    - Live area: 20x20px (2px padding)
    - Keylines:
      - Circle: 20px diameter (centered)
      - Square: 18x18px (centered)
      - Horizontal rect: 20x16px
      - Vertical rect: 16x20px
    
    Icons should fill the appropriate keyline:
    - Circular objects (globe, clock) → circle keyline
    - Square objects (file, calendar) → square keyline
    - Wide objects (menu, video) → horizontal keyline
    - Tall objects (person, arrow-up) → vertical keyline
    
    This ensures all icons have equal visual weight despite different shapes.
    

---
  #### **Name**
Stroke Weight Scaling
  #### **Description**
Define stroke weights that maintain visual consistency across different icon sizes
  #### **When**
Designing icons that need to work from 12px to 48px or larger
  #### **Example**
    Stroke weight scale (1.5px base at 24px):
    - 12px icon: 1px stroke (minimum visible)
    - 16px icon: 1.25px stroke
    - 20px icon: 1.5px stroke
    - 24px icon: 1.5px stroke (base)
    - 32px icon: 2px stroke
    - 48px icon: 2.5px stroke
    
    Rule: Stroke must be at least 1px at smallest size.
    Never use fractional pixels below 1px.
    
    Alternative: Design separate icon sets for different size ranges
    - 12-16px: Simplified, 1px stroke
    - 20-32px: Standard detail, 1.5px stroke
    - 48px+: Full detail, 2px+ stroke
    

---
  #### **Name**
Optical Alignment Correction
  #### **Description**
Adjust mathematical positioning to achieve visual balance - circles and triangles need different treatment than rectangles
  #### **When**
Icons appear misaligned despite correct coordinates
  #### **Example**
    Common optical corrections:
    
    Play button (triangle):
    - Mathematically centered triangle looks left-heavy
    - Shift right by ~4% of width for visual center
    
    Circular icons:
    - Circles appear smaller than same-dimension squares
    - Extend 1-2px beyond live area or increase diameter slightly
    
    Pointed shapes (arrows, carets):
    - Mathematical center looks "short"
    - Extend point 1px past grid boundary
    
    Rule: Trust your eyes over the pixel grid.
    If it looks wrong, it is wrong - regardless of coordinates.
    

---
  #### **Name**
Metaphor Clarity Hierarchy
  #### **Description**
Choose icon metaphors based on universal recognition, with fallbacks for culturally-specific symbols
  #### **When**
Selecting what visual represents a concept
  #### **Example**
    Metaphor universality tiers:
    
    Tier 1 - Universal (use freely):
    - Magnifying glass = search
    - X = close
    - + = add
    - Gear = settings
    - House = home
    - Arrow = direction
    
    Tier 2 - Widely recognized (use with context):
    - Hamburger menu (mobile-familiar users)
    - Floppy disk = save (aging metaphor)
    - Envelope = email (works globally)
    - Shopping cart = purchase
    
    Tier 3 - Culturally specific (add labels):
    - Mailbox (US style - not universal)
    - Hand gestures (meanings vary)
    - Animals (symbolism varies)
    - Colors (red doesn't always mean stop)
    
    Rule: Tier 3 icons always need text labels.
    

---
  #### **Name**
Consistent Corner Treatment
  #### **Description**
Define corner radius rules that apply to all icons in a set for visual cohesion
  #### **When**
Creating or maintaining an icon set style
  #### **Example**
    Corner radius system:
    
    Sharp style (technical, precise):
    - Outer corners: 0px (sharp)
    - Inner corners: 0px
    - Stroke caps: butt
    - Best for: dev tools, code editors
    
    Rounded style (friendly, approachable):
    - Outer corners: 2px radius
    - Inner corners: 1px radius
    - Stroke caps: round
    - Best for: consumer apps, friendly brands
    
    Soft style (modern, playful):
    - Outer corners: 3-4px radius
    - Inner corners: 2px radius
    - Stroke caps: round
    - Stroke joins: round
    - Best for: playful brands, casual apps
    
    Mixed is chaos. Pick one and commit.
    

---
  #### **Name**
Size Variant System
  #### **Description**
Create distinct icon variants for different sizes rather than scaling a single design
  #### **When**
Icons need to work across a wide size range (12px to 48px+)
  #### **Example**
    Three-tier variant system:
    
    Small (12-16px):
    - Maximum simplification
    - Remove internal details
    - 1px stroke minimum
    - Solid fills may replace strokes
    - Single-element silhouettes
    
    Medium (20-32px):
    - Standard level of detail
    - 1.5-2px strokes
    - Internal details visible
    - Full icon complexity
    
    Large (48px+):
    - Additional detail possible
    - 2px+ strokes
    - Subtle gradients/shadows optional
    - Secondary elements visible
    
    Never just scale - redesign for each tier.
    

---
  #### **Name**
SVG Optimization Protocol
  #### **Description**
Clean and optimize SVG output for web/app deployment
  #### **When**
Exporting icons for implementation
  #### **Example**
    SVG optimization checklist:
    
    1. ViewBox standardization:
       viewBox="0 0 24 24" (match design size)
    
    2. Remove unnecessary attributes:
       - No width/height (use CSS)
       - No fill if inheriting (fill="currentColor")
       - No IDs unless needed for animation
    
    3. Path cleanup:
       - Combine overlapping paths
       - Remove empty groups
       - Simplify bezier curves
       - Remove unnecessary points
    
    4. Optimization:
       <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
            stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
         <path d="M3 12h18M12 3v18"/>
       </svg>
    
    Target: <1KB per icon after gzip
    

---
  #### **Name**
Icon Set Coherence Testing
  #### **Description**
Validate that new icons feel like part of the existing family
  #### **When**
Adding icons to an established set
  #### **Example**
    Coherence checklist:
    
    Visual weight test:
    - View all icons at actual size in grid
    - No icon should "pop" as heavier/lighter
    - Squint test: similar gray value across set
    
    Style consistency:
    - Same stroke width as set
    - Same corner radius
    - Same line cap style
    - Same level of detail
    
    Metaphor alignment:
    - Similar abstraction level
    - Consistent use of perspective (flat vs isometric)
    - Matching realism level
    
    Grid compliance:
    - Uses same keylines
    - Same optical alignment approach
    - Same padding/safe area
    

---
  #### **Name**
Accessibility-First Icon Design
  #### **Description**
Ensure icons work for users with visual impairments and in various display contexts
  #### **When**
Creating icons for public-facing products
  #### **Example**
    Accessibility requirements:
    
    Size minimums:
    - Touch target: 44x44px minimum
    - Visual icon: 16px minimum for recognition
    
    Contrast:
    - 3:1 against background (WCAG AA for UI)
    - Support both light and dark modes
    
    Don't rely on color alone:
    - Success/error icons need distinct shapes
    - Not just green check / red X
    
    Screen reader support (implementation):
    - Decorative icons: aria-hidden="true"
    - Meaningful icons: aria-label or accompanying text
    
    Text labels:
    - Always pair with text for critical actions
    - Icons-only acceptable only for universal symbols
    

---
  #### **Name**
Pixel-Perfect Alignment
  #### **Description**
Ensure icon elements align to the pixel grid to prevent blurry rendering
  #### **When**
Finalizing icons for screen display
  #### **Example**
    Pixel alignment rules:
    
    For 1px strokes:
    - Position on half-pixel (0.5, 1.5, 2.5...)
    - This centers the stroke on pixel boundaries
    
    For 2px strokes:
    - Position on whole pixels (0, 1, 2...)
    
    For fills:
    - All edges on whole pixels
    - No fractional dimensions
    
    Check at 100% zoom:
    - Horizontal/vertical lines should be crisp
    - Slight blur = off-grid elements
    
    Exception: Diagonal lines and curves will always anti-alias.
    Focus pixel-perfection on horizontal/vertical elements.
    

## Anti-Patterns


---
  #### **Name**
Inconsistent Stroke Weights
  #### **Description**
Mixing stroke weights within an icon set destroys visual cohesion
  #### **Why**
Icons look like they came from different sets. Visual language breaks down. Users sense something is "off" even if they can't articulate it.
  #### **Instead**
    Audit existing set before adding:
    - What stroke weight is used?
    - What cap style?
    - What corner radius?
    
    Match exactly. No "close enough."
    
    If set uses 1.5px strokes, every new icon uses 1.5px.
    If set uses round caps, every new icon uses round caps.
    

---
  #### **Name**
Overly Literal Metaphors
  #### **Description**
Creating complex pictorial representations instead of simple symbolic ones
  #### **Why**
Detail doesn't survive size reduction. Literal interpretations limit future meaning. Complexity increases cognitive load.
  #### **Instead**
    Simplification progression:
    
    Too literal: Detailed mailbox with flag, post, letters
    Better: Simple envelope shape
    Best: Minimal envelope outline
    
    Ask: "What's the simplest shape that conveys this meaning?"
    Then simplify one more time.
    
    Icons are symbols, not illustrations.
    

---
  #### **Name**
Scaling Without Redesigning
  #### **Description**
Using a single icon design across all sizes by simply scaling up/down
  #### **Why**
Details disappear at small sizes. Strokes become invisible or blurry. Proportions feel wrong at extreme sizes.
  #### **Instead**
    Create size-specific variants:
    
    24px design at 12px:
    - 1.5px strokes → invisible or blurry
    - Internal details → noise
    - Gaps → closed up
    
    Redesign for 12px:
    - 1px strokes (minimum)
    - Remove internal details
    - Merge close elements
    - Consider solid fill variant
    

---
  #### **Name**
Mathematical Over Optical Alignment
  #### **Description**
Trusting coordinate values over visual perception
  #### **Why**
Human vision doesn't perceive shapes mathematically. Circles look smaller than squares. Triangles look off-center. Pointed shapes look short.
  #### **Instead**
    Visual tests > coordinate checks:
    
    1. Zoom out to actual usage size
    2. Does it LOOK centered/balanced?
    3. If no, adjust optically
    4. Document the adjustment reason
    
    Common corrections:
    - Play triangle: shift right ~4%
    - Circles: extend 1-2px past boundary
    - Arrows: extend point past grid
    

---
  #### **Name**
Cultural Assumption in Metaphors
  #### **Description**
Using symbols that only make sense in specific cultures or generations
  #### **Why**
Global products need global icons. Cultural symbols exclude users. Generational metaphors age out.
  #### **Instead**
    Test metaphors for universality:
    
    Problematic:
    - Floppy disk (unknown to young users)
    - US-style mailbox (unknown outside US)
    - Hand gestures (varied meanings)
    
    Safer alternatives:
    - Floppy disk → Download arrow or checkmark
    - Mailbox → Envelope
    - Thumbs up → Checkmark or heart
    
    When in doubt, add a text label.
    

---
  #### **Name**
Ignoring Color Mode Requirements
  #### **Description**
Designing icons that only work in light mode or only in dark mode
  #### **Why**
Modern apps support both modes. Single-mode icons break or become invisible in the other mode.
  #### **Instead**
    Design for both modes:
    
    Option 1: Use currentColor
    <svg fill="currentColor">
    - Icon inherits text color
    - Works automatically in both modes
    
    Option 2: CSS custom properties
    fill="var(--icon-color)"
    
    Option 3: Separate assets
    icon-light.svg / icon-dark.svg
    - More work, more control
    
    Test: View icons on #FFFFFF and #0F0F0F backgrounds.
    

---
  #### **Name**
Hardcoded Dimensions in SVG
  #### **Description**
Including fixed width/height attributes that prevent flexible sizing
  #### **Why**
Icons should size via CSS. Hardcoded dimensions require overrides. Multiple sizes need multiple assets.
  #### **Instead**
    Flexible SVG pattern:
    
    BAD:
    <svg width="24" height="24" viewBox="0 0 24 24">
    
    GOOD:
    <svg viewBox="0 0 24 24">
    
    Size via CSS:
    .icon { width: 24px; height: 24px; }
    .icon-sm { width: 16px; height: 16px; }
    .icon-lg { width: 32px; height: 32px; }
    
    viewBox defines proportions. CSS defines size.
    

---
  #### **Name**
Decorative-Only Icons
  #### **Description**
Using icons purely for visual interest without conveying meaning
  #### **Why**
Icons that don't communicate are visual noise. They add cognitive load without benefit. Users try to decode them and fail.
  #### **Instead**
    Every icon must:
    1. Convey specific meaning, OR
    2. Provide visual affordance (clickable), OR
    3. Be removed
    
    If an icon is truly decorative:
    - Use aria-hidden="true"
    - Question if it's needed at all
    
    Icon audit question: "What does this icon tell the user?"
    If the answer is "nothing," remove it.
    

---
  #### **Name**
Icon-Only Critical Actions
  #### **Description**
Using icons without text labels for important or destructive actions
  #### **Why**
Icon meanings aren't universal. Users fear clicking unknown symbols. Critical actions need clarity over aesthetics.
  #### **Instead**
    Label requirements by action type:
    
    Always label:
    - Delete/remove
    - Submit/send
    - Settings/preferences
    - Navigation items
    
    Icon-only acceptable:
    - Close (X in modal corner)
    - Search (when input is visible)
    - Menu (hamburger - with caution)
    
    When space is tight:
    - Tooltip on hover/focus
    - Revealed label on mobile long-press
    - Accessible label via aria-label
    

---
  #### **Name**
Inconsistent Visual Perspective
  #### **Description**
Mixing flat 2D icons with isometric or 3D-style icons in the same set
  #### **Why**
Creates visual dissonance. Icons don't feel like a family. Users sense inconsistency.
  #### **Instead**
    Choose ONE perspective and commit:
    
    Flat (recommended for UI):
    - No depth, shadows, or 3D effect
    - Pure 2D shapes
    - Works at all sizes
    
    Isometric (occasional use):
    - Consistent angle (30 degrees typical)
    - Same vanishing point rules
    - All icons share perspective
    
    3D/Realistic (illustration, not icons):
    - Reserve for marketing, not UI
    - Doesn't scale to small sizes
    

---
  #### **Name**
Missing Pixel Grid Alignment
  #### **Description**
Creating icons with elements that don't align to the pixel grid
  #### **Why**
Causes blurry rendering. Strokes appear fuzzy. Icons look unprofessional.
  #### **Instead**
    Pixel alignment workflow:
    
    1. Design at target size (not scaled)
    2. Align horizontal/vertical strokes to grid:
       - 1px strokes: center on 0.5 pixel
       - 2px strokes: align to whole pixel
    3. Check at 100% zoom (no scaling)
    4. Look for blur on straight edges
    5. Adjust path points until crisp
    
    Tools: Figma's "Pixel Preview" mode
    Illustrator: View > Pixel Preview
    