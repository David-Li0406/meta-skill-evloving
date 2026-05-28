# Icon Design - Sharp Edges

## Pixel Grid Misalignment

### **Id**
pixel-grid-misalignment
### **Summary**
Icon strokes not aligned to pixel grid causing blurry rendering
### **Severity**
high
### **Situation**
  Icons look crisp in Figma but appear blurry in browser or app.
  Horizontal and vertical lines have a fuzzy appearance.
  Strokes seem thicker or thinner than designed.
  
### **Why**
  Screen rendering anti-aliases sub-pixel elements. A 1px stroke positioned at
  x=10 spans from 9.5 to 10.5, causing both pixels to render at 50% opacity.
  This makes sharp lines look blurry. The effect worsens on non-retina displays.
  
### **Solution**
  # Pixel alignment rules:
  
  For 1px strokes:
  - Position center on half-pixel (10.5, not 10)
  - Stroke spans 10 to 11 (full pixels)
  
  For 2px strokes:
  - Position center on whole pixel (10, not 10.5)
  - Stroke spans 9 to 11 (full pixels)
  
  # Figma workflow:
  1. View > Pixel Preview (Ctrl/Cmd + P)
  2. Zoom to 100%
  3. Check horizontal/vertical edges
  4. Nudge by 0.5px if blurry
  
  # SVG check:
  - Path coordinates should be .5 for 1px strokes
  - Path coordinates should be whole numbers for 2px strokes
  
### **Symptoms**
  - Icons look fuzzy at 100% zoom
  - Strokes appear inconsistent thickness
  - Fine details merge together
  - Icons look worse on non-retina screens
### **Detection Pattern**


## Svg Viewbox Mismatch

### **Id**
svg-viewbox-mismatch
### **Summary**
SVG viewBox doesn't match intended design dimensions
### **Severity**
critical
### **Situation**
  Icons render at wrong size or aspect ratio. Cropping or extra whitespace appears.
  Icons stretch or squish when resized.
  
### **Why**
  viewBox defines the coordinate system. If icon was designed at 24x24 but
  viewBox is "0 0 16 16", the icon is scaled and distorted. Missing viewBox
  means browser guesses dimensions based on width/height attributes.
  
### **Solution**
  # viewBox must match design artboard:
  
  # WRONG - 24px design with 16px viewBox
  <svg viewBox="0 0 16 16">
    <path d="M12 3L22 12L12 21" /> <!-- coords exceed viewBox -->
  </svg>
  
  # RIGHT - viewBox matches design
  <svg viewBox="0 0 24 24">
    <path d="M9 6L15 12L9 18" />
  </svg>
  
  # Standard viewBox values:
  - 16px icons: viewBox="0 0 16 16"
  - 20px icons: viewBox="0 0 20 20"
  - 24px icons: viewBox="0 0 24 24"
  - 32px icons: viewBox="0 0 32 32"
  
  # Export check: Verify artboard size = viewBox dimensions
  
### **Symptoms**
  - Icons cropped or have excess padding
  - Icons stretched or squished
  - Inconsistent sizing across icon set
  - Icons overflow container
### **Detection Pattern**
viewBox="0 0 (?!24 24|16 16|20 20|32 32)

## Hardcoded Colors Svg

### **Id**
hardcoded-colors-svg
### **Summary**
Colors hardcoded in SVG preventing theme/dark mode support
### **Severity**
high
### **Situation**
  Icons work in light mode but disappear or look wrong in dark mode.
  Can't change icon color via CSS. Different icons have different default colors.
  
### **Why**
  Hardcoded fill="#000000" or stroke="#333" overrides CSS.
  Icons can't inherit color from parent. Each icon needs separate assets for each color scheme.
  Maintenance nightmare when brand colors change.
  
### **Solution**
  # Use currentColor for theme support:
  
  # BAD - hardcoded color
  <svg fill="#000000">
    <path d="..." stroke="#333333"/>
  </svg>
  
  # GOOD - inherits from CSS color property
  <svg fill="currentColor">
    <path d="..."/>
  </svg>
  
  # GOOD - stroke icons
  <svg fill="none" stroke="currentColor" stroke-width="1.5">
    <path d="..."/>
  </svg>
  
  # CSS controls color:
  .icon { color: #333; }
  .dark .icon { color: #fff; }
  
  # For multi-color icons, use CSS custom properties:
  <svg>
    <path fill="var(--icon-primary)"/>
    <path fill="var(--icon-secondary)"/>
  </svg>
  
### **Symptoms**
  - Icons invisible in dark mode
  - Can't style icon color with CSS
  - Inconsistent icon colors across app
  - Need separate icon files per color
### **Detection Pattern**
fill="#[0-9a-fA-F]{3,6}"|stroke="#[0-9a-fA-F]{3,6}"

## Non Square Artboard

### **Id**
non-square-artboard
### **Summary**
Icon designed on non-square artboard causing aspect ratio issues
### **Severity**
high
### **Situation**
  Icons appear stretched or compressed. Icon doesn't fit properly in icon containers.
  Alignment issues when icons are placed in rows.
  
### **Why**
  Icons should be square for consistent sizing and alignment.
  Non-square icons (24x20, 18x24) don't fit standard icon containers.
  CSS sizing assumes square: width: 24px; height: 24px breaks non-square icons.
  
### **Solution**
  # Always use square artboards:
  
  # Standard icon sizes (all square):
  - 16x16px
  - 20x20px
  - 24x24px (most common)
  - 32x32px
  - 48x48px
  
  # For wide/tall icons:
  - Use same square artboard
  - Icon touches edges on longer dimension
  - Center on shorter dimension
  - Maintains consistent bounding box
  
  # Example: Wide "menu" icon on 24x24:
  - Menu bars: 20px wide (fills horizontal)
  - Centered vertically with 6px above/below
  - Still exports as 24x24
  
  # viewBox always square:
  viewBox="0 0 24 24"
  
### **Symptoms**
  - Icons stretched when sized uniformly
  - Uneven spacing between icons
  - Icons break layout grids
  - Aspect ratio varies across icon set
### **Detection Pattern**
viewBox="0 0 \d+ (?!\d+ ")

## Stroke Weight Scaling Failure

### **Id**
stroke-weight-scaling-failure
### **Summary**
Single stroke weight used across all sizes causing visibility issues
### **Severity**
high
### **Situation**
  Icons look fine at 24px but strokes disappear or blur at 16px.
  Icons look too heavy at 32px. Same SVG used at all sizes.
  
### **Why**
  A 1.5px stroke is 6.25% of a 24px icon but 9.4% of a 16px icon.
  At small sizes, fine strokes become sub-pixel and blur.
  At large sizes, strokes look too thin relative to icon size.
  
### **Solution**
  # Size-specific stroke weights:
  
  # 16px icons:
  stroke-width="1"    # 6.25% of icon
  # Minimum visible stroke
  
  # 24px icons (standard):
  stroke-width="1.5"  # 6.25% of icon
  # Sweet spot for detail
  
  # 32px icons:
  stroke-width="2"    # 6.25% of icon
  # Maintains proportions
  
  # Implementation options:
  
  1. Separate SVG files per size:
     icon-16.svg, icon-24.svg, icon-32.svg
  
  2. CSS scaling with stroke adjustment:
     .icon-sm svg { stroke-width: 1px; }
     .icon-md svg { stroke-width: 1.5px; }
     .icon-lg svg { stroke-width: 2px; }
  
  3. SVG stroke scaling attribute:
     vector-effect="non-scaling-stroke"
     # Stroke stays constant regardless of scale
  
### **Symptoms**
  - Strokes invisible at small sizes
  - Icons look too thin at large sizes
  - Inconsistent visual weight across sizes
  - Details merge at small sizes
### **Detection Pattern**


## Missing Touch Target

### **Id**
missing-touch-target
### **Summary**
Icon buttons smaller than minimum touch target (44x44px)
### **Severity**
critical
### **Situation**
  Users mis-tap icon buttons on mobile. Frustration with small click targets.
  Accessibility audit failures for touch target size.
  
### **Why**
  Apple guidelines: 44x44 point minimum. Android: 48x48 dp.
  WCAG 2.5.5: 44x44 CSS pixels. A 16px or 24px icon with no padding
  is impossible to tap accurately. Average finger pad is ~10mm (40px).
  
### **Solution**
  # Separate icon size from touch target:
  
  <button class="icon-button">
    <svg class="icon" viewBox="0 0 24 24">...</svg>
  </button>
  
  .icon-button {
    /* Touch target: 44x44 minimum */
    width: 44px;
    height: 44px;
    padding: 10px;  /* (44-24)/2 = 10px padding */
  
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .icon {
    /* Visual icon: 24px */
    width: 24px;
    height: 24px;
  }
  
  # Alternative: invisible touch expansion
  .icon-button::before {
    content: '';
    position: absolute;
    inset: -10px;  /* Expands touch area */
  }
  
### **Symptoms**
  - Users tap wrong icon on mobile
  - Accessibility audit failures
  - High error rate on icon actions
  - Users complain about small buttons
### **Detection Pattern**
width:\s*1[0-9]px.*height:\s*1[0-9]px|w-[3-4]\s+h-[3-4]

## Icon Only Navigation

### **Id**
icon-only-navigation
### **Summary**
Using icons without labels for navigation or critical actions
### **Severity**
high
### **Situation**
  Users unsure what icons mean. High support tickets for "where is X feature?"
  Different users interpret same icon differently.
  
### **Why**
  Icon meanings aren't universal. A gear could be settings, admin, or preferences.
  Users don't click icons they don't understand. Critical actions need clarity.
  Icon-only interfaces have lower task completion rates.
  
### **Solution**
  # Always pair non-universal icons with labels:
  
  # BAD - icon only
  <button aria-label="Settings">
    <GearIcon />
  </button>
  
  # GOOD - icon + visible label
  <button>
    <GearIcon />
    <span>Settings</span>
  </button>
  
  # Icon-only acceptable ONLY for:
  - Close (X) - in expected position
  - Search - when next to search input
  - Menu (hamburger) - familiar pattern
  
  # For space-constrained areas:
  - Tooltip on hover (not mobile-friendly)
  - Reveal label on focus
  - aria-label for screen readers (minimum)
  
  # Test: Show icon to 5 people, ask what it means
  # If answers vary, add a label
  
### **Symptoms**
  - What does this icon do?
  - Low click rates on icon-only buttons
  - Support tickets about finding features
  - Users avoid icon-only actions
### **Detection Pattern**


## Animation Without Reduced Motion

### **Id**
animation-without-reduced-motion
### **Summary**
Icon animations that ignore user motion preferences
### **Severity**
high
### **Situation**
  Icons spin, bounce, or animate continuously. Some users report discomfort.
  Animations don't respect system accessibility settings.
  
### **Why**
  Vestibular disorders affect 35% of adults over 40. Excessive motion
  causes nausea, dizziness, and headaches. WCAG requires respecting
  prefers-reduced-motion. Ignoring it is an accessibility violation.
  
### **Solution**
  # Always check motion preferences:
  
  /* Icon animation */
  .icon-loading {
    animation: spin 1s linear infinite;
  }
  
  /* Respect user preference */
  @media (prefers-reduced-motion: reduce) {
    .icon-loading {
      animation: none;
      /* Alternative: opacity pulse instead of spin */
      opacity: 0.5;
    }
  }
  
  # For critical animations (loading indicators):
  @media (prefers-reduced-motion: reduce) {
    .icon-loading {
      /* Static or subtle alternative */
      animation: pulse 2s ease-in-out infinite;
    }
  
    @keyframes pulse {
      0%, 100% { opacity: 0.5; }
      50% { opacity: 1; }
    }
  }
  
  # Rule: Any moving icon must have reduced-motion variant
  
### **Symptoms**
  - User complaints about motion
  - Accessibility audit failures
  - Excessive CPU/battery usage
  - Distracting interface
### **Detection Pattern**
animation:(?!.*prefers-reduced-motion)

## Inconsistent Icon Set Style

### **Id**
inconsistent-icon-set-style
### **Summary**
Mixing different icon styles (outlined, filled, two-tone) in same UI
### **Severity**
medium
### **Situation**
  Some icons are outline-only, others are filled. Stroke weights vary.
  Corner radii differ between icons. Icons look like they're from different sets.
  
### **Why**
  Inconsistency creates visual noise. Users subconsciously notice something
  is "off." Icons should feel like a family. Mixing styles breaks the
  visual language. Professional products maintain strict icon consistency.
  
### **Solution**
  # Choose ONE style and enforce it:
  
  # Style attributes to standardize:
  
  1. Fill vs stroke:
     - All outline (most versatile)
     - All filled (bold, simple)
     - All duotone (complex, branded)
  
  2. Stroke weight:
     - Pick one (e.g., 1.5px at 24px)
     - Every icon uses same weight
  
  3. Corner radius:
     - Sharp (0px) OR rounded (2px)
     - Apply to all icons
  
  4. Line caps:
     - Round OR square
     - Same across set
  
  # Icon audit:
  - Export all icons to grid view
  - Look for outliers
  - Fix or replace inconsistent icons
  
  # When adding new icons:
  - Reference existing icons
  - Match ALL style attributes
  - Review in context of full set
  
### **Symptoms**
  - Icons look like different families
  - Visual inconsistency across UI
  - "Something looks off" feedback
  - Design reviews catch style mixing
### **Detection Pattern**


## Svg Bloat

### **Id**
svg-bloat
### **Summary**
Unoptimized SVG with unnecessary code, metadata, and precision
### **Severity**
medium
### **Situation**
  SVG files larger than needed. Slow page loads. Large icon bundles.
  SVG contains editor metadata, unused definitions, excessive decimal places.
  
### **Why**
  Illustrator/Figma export includes unnecessary data. Editor metadata
  adds bytes without value. 8 decimal places where 2 suffice. Multiple
  icons compound the problem. Affects page load and bundle size.
  
### **Solution**
  # SVG optimization checklist:
  
  # BEFORE (exported from design tool):
  <svg xmlns="http://www.w3.org/2000/svg"
       xmlns:xlink="http://www.w3.org/1999/xlink"
       width="24" height="24" viewBox="0 0 24 24"
       xml:space="preserve" id="Layer_1">
    <metadata>Created with Illustrator</metadata>
    <defs>
      <style>.cls-1{fill:none;stroke:#000}</style>
    </defs>
    <g id="Icon">
      <path class="cls-1"
            d="M3.14159265,12.00000000 L20.85840735,12.00000000"/>
    </g>
  </svg>
  
  # AFTER (optimized):
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
       stroke-width="1.5">
    <path d="M3 12h18"/>
  </svg>
  
  # Optimization tools:
  - SVGO (command line): npx svgo icon.svg
  - SVGOMG (web): jakearchibald.github.io/svgomg/
  - Figma plugin: "SVG Export"
  
  # Target: <500 bytes per icon
  
### **Symptoms**
  - Large icon bundle size
  - SVG files with metadata/comments
  - Excessive path precision
  - Slow icon loading
### **Detection Pattern**
<metadata|xmlns:xlink|xml:space|id="Layer

## Color Only Meaning

### **Id**
color-only-meaning
### **Summary**
Using icon color alone to convey status or meaning
### **Severity**
critical
### **Situation**
  Red icon means error, green means success. Status shown only by icon color.
  Same icon shape in different colors for different states.
  
### **Why**
  8% of men have color vision deficiency. Monochrome displays exist.
  Print/fax loses color. High contrast mode changes colors.
  Color-only meaning excludes users and violates WCAG.
  
### **Solution**
  # Combine color with shape differences:
  
  # BAD - color only
  <CheckIcon color="green" />  <!-- Success -->
  <CheckIcon color="red" />    <!-- Error (same shape!) -->
  
  # GOOD - different shapes
  <CheckCircleIcon />  <!-- Success: check in circle -->
  <XCircleIcon />      <!-- Error: X in circle -->
  <AlertTriangleIcon /> <!-- Warning: triangle with ! -->
  <InfoCircleIcon />   <!-- Info: i in circle -->
  
  # Status icon system:
  - Success: Checkmark shape (circle optional)
  - Error: X shape (distinct from checkmark)
  - Warning: Triangle with exclamation
  - Info: Circle with i
  
  # Color enhances, shape defines meaning
  # Shape must be distinct enough without color
  
### **Symptoms**
  - Color blind users confused
  - Status unclear in grayscale
  - Accessibility audit failures
  - What does red mean here?
### **Detection Pattern**


## Missing Aria Labels

### **Id**
missing-aria-labels
### **Summary**
Meaningful icons without accessible names for screen readers
### **Severity**
critical
### **Situation**
  Screen reader announces "image" or "button" with no description.
  Icon-only buttons have no accessible name. SVG icons ignored by assistive tech.
  
### **Why**
  Screen reader users can't understand icon purpose. WCAG requires
  accessible names for all interactive elements. Decorative icons
  should be hidden; meaningful icons need labels.
  
### **Solution**
  # For meaningful icons (convey information):
  
  # Button with icon
  <button aria-label="Close dialog">
    <XIcon aria-hidden="true" />
  </button>
  
  # Standalone icon with meaning
  <span role="img" aria-label="Warning: action required">
    <AlertIcon />
  </span>
  
  # Icon with visible label (aria-hidden on icon)
  <button>
    <SaveIcon aria-hidden="true" />
    <span>Save</span>
  </button>
  
  # For decorative icons (no meaning):
  <SaveIcon aria-hidden="true" />
  # or
  <SaveIcon role="presentation" />
  
  # SVG-specific:
  <svg aria-hidden="true" focusable="false">
    <!-- Decorative -->
  </svg>
  
  <svg role="img" aria-labelledby="icon-title">
    <title id="icon-title">Settings</title>
    <!-- Meaningful -->
  </svg>
  
### **Symptoms**
  - Screen reader says "image" or nothing
  - Icon purpose unknown to AT users
  - Accessibility audit failures
  - Focus on decorative icons
### **Detection Pattern**
<svg(?![^>]*aria-hidden|[^>]*aria-label|[^>]*role=)