# Typography

## Patterns


---
  #### **Name**
Modular Type Scale
  #### **Description**
Use mathematical ratios to create harmonious type hierarchies that feel balanced
  #### **When**
Establishing typography systems for any project
  #### **Example**
    # Common ratios (base 16px):
    
    Perfect Fourth (1.333):
    - xs:    12px (0.75rem)
    - sm:    14px (0.875rem) - captions, metadata
    - base:  16px (1rem)     - body text
    - lg:    21px (1.333rem) - lead paragraphs
    - xl:    28px (1.777rem) - h3
    - 2xl:   37px (2.369rem) - h2
    - 3xl:   50px (3.157rem) - h1
    - 4xl:   67px (4.209rem) - display
    
    # Why ratios work:
    # - Musical harmony principles applied to visual design
    # - Every size relates mathematically to others
    # - Smaller jumps (1.2) for dense UIs, larger (1.5) for editorial
    
    # CSS implementation:
    :root {
      --step--2: clamp(0.69rem, 0.66rem + 0.18vw, 0.80rem);
      --step--1: clamp(0.83rem, 0.78rem + 0.29vw, 1.00rem);
      --step-0: clamp(1.00rem, 0.91rem + 0.43vw, 1.25rem);
      --step-1: clamp(1.20rem, 1.07rem + 0.63vw, 1.56rem);
      --step-2: clamp(1.44rem, 1.26rem + 0.89vw, 1.95rem);
      --step-3: clamp(1.73rem, 1.48rem + 1.24vw, 2.44rem);
    }
    

---
  #### **Name**
Line Height for Reading Comfort
  #### **Description**
Set line height (leading) based on measure and font characteristics
  #### **When**
Setting body text, headlines, or any multi-line content
  #### **Example**
    # Line height guidelines by context:
    
    Body text (45-75 char measure):
    - 1.5-1.7 (24-27px at 16px base)
    - Longer lines need more leading
    - Tight x-height fonts need more leading
    
    Headlines (short lines):
    - 1.1-1.3 (tighter is better)
    - Multi-line headlines: 1.2-1.4
    - Display type: 0.9-1.1 (negative leading OK)
    
    UI text (labels, buttons):
    - 1.2-1.4 (tighter for single lines)
    
    # Formula (approximate):
    line-height = 1.5 + (measure / 100)
    
    # Example:
    .prose {
      max-width: 65ch;     /* ~65 characters */
      line-height: 1.65;   /* Comfortable for this measure */
    }
    
    .headline {
      line-height: 1.1;    /* Tight for impact */
    }
    

---
  #### **Name**
Font Pairing Principles
  #### **Description**
Select typeface combinations that complement without competing
  #### **When**
Choosing fonts for a project requiring multiple typefaces
  #### **Example**
    # Pairing strategies that work:
    
    1. CONTRAST IN CATEGORY
       Serif headlines + Sans body (or vice versa)
       - Playfair Display + Source Sans Pro
       - Montserrat + Merriweather
    
    2. SUPERFAMILY PAIRING
       Related fonts designed to work together
       - Source Serif + Source Sans + Source Code
       - IBM Plex Serif + Sans + Mono
       - Roboto + Roboto Slab + Roboto Mono
    
    3. SIMILAR X-HEIGHT
       Fonts feel harmonious when x-heights align
       - Test by setting them side-by-side at same size
    
    4. CONTRAST IN WEIGHT/WIDTH
       Regular body + Bold condensed headlines
       - Prevents monotony while maintaining cohesion
    
    # Pairings to avoid:
    - Two decorative fonts (competition)
    - Fonts too similar (why have two?)
    - More than 2-3 fonts total
    
    # Safe starting points:
    - Inter + Newsreader (modern/editorial)
    - Space Grotesk + Crimson Pro (tech/readable)
    - Work Sans + Literata (professional/warm)
    

---
  #### **Name**
Responsive Typography with Fluid Scaling
  #### **Description**
Scale type smoothly between viewport sizes using clamp()
  #### **When**
Building responsive designs that need elegant type scaling
  #### **Example**
    # Fluid type scale with clamp():
    
    /* Minimum: 16px, Maximum: 20px, scales with viewport */
    body {
      font-size: clamp(1rem, 0.9rem + 0.5vw, 1.25rem);
    }
    
    /* Headlines scale more dramatically */
    h1 {
      font-size: clamp(2rem, 1.5rem + 2.5vw, 4rem);
    }
    
    # Formula:
    clamp(min, preferred, max)
    preferred = min + (max - min) * viewport-factor
    
    # Tools:
    - utopia.fyi (generates fluid scales)
    - type-scale.com (static scales)
    
    # Why clamp() beats media queries:
    - Smooth scaling, no jarring jumps
    - Less code to maintain
    - Respects user font size preferences
    

---
  #### **Name**
Variable Fonts for Performance and Flexibility
  #### **Description**
Use variable fonts to reduce file size while gaining design flexibility
  #### **When**
Projects need multiple weights/widths or want to reduce font requests
  #### **Example**
    # Variable font benefits:
    - One file for all weights (400, 500, 600, 700...)
    - Animate weight/width smoothly
    - Smaller total file size than multiple static fonts
    
    # Implementation:
    @font-face {
      font-family: 'Inter';
      src: url('/fonts/Inter-Variable.woff2') format('woff2-variations');
      font-weight: 100 900;  /* Available weight range */
      font-display: swap;
    }
    
    /* Use any weight in the range */
    .text-medium { font-weight: 450; }
    .text-semibold { font-weight: 550; }
    
    /* Animate on hover */
    .link {
      font-weight: 400;
      transition: font-weight 0.2s;
    }
    .link:hover {
      font-weight: 600;
    }
    
    # Popular variable fonts:
    - Inter (100-900, multiple axes)
    - Roboto Flex (full flexibility)
    - Source Sans 3 (200-900)
    - Plus Jakarta Sans (200-800)
    

---
  #### **Name**
Optimal Measure (Line Length)
  #### **Description**
Control line length for reading comfort - too long exhausts, too short disrupts
  #### **When**
Setting body text in any reading context
  #### **Example**
    # Ideal measure by context:
    
    Optimal: 45-75 characters per line
    - 65ch is the gold standard for body text
    - Includes spaces and punctuation
    
    Single column prose:
    .article {
      max-width: 65ch;  /* ~65 characters */
      margin: 0 auto;
    }
    
    Two-column layouts:
    .column {
      max-width: 45ch;  /* Shorter for columns */
    }
    
    UI text (cards, lists):
    .card-text {
      max-width: 35ch;  /* Scannable length */
    }
    
    # Why it matters:
    - Too long (100+ chars): Eye loses track returning to next line
    - Too short (30- chars): Constant line breaks disrupt flow
    - Research-backed: 66 characters optimal for comprehension
    
    # Implementation:
    /* Use ch unit for character-based widths */
    .prose { max-width: 65ch; }
    

---
  #### **Name**
Font Loading Strategy
  #### **Description**
Load fonts without blocking render or causing layout shift
  #### **When**
Implementing web fonts in production
  #### **Example**
    # Optimal loading strategy:
    
    1. PRELOAD CRITICAL FONTS
    <link rel="preload" href="/fonts/inter-var.woff2"
          as="font" type="font/woff2" crossorigin>
    
    2. USE FONT-DISPLAY: SWAP
    @font-face {
      font-family: 'Inter';
      src: url('/fonts/inter-var.woff2') format('woff2');
      font-display: swap;  /* Show fallback immediately */
    }
    
    3. MATCH FALLBACK METRICS
    @font-face {
      font-family: 'Inter Fallback';
      src: local('Arial');
      ascent-override: 90%;
      descent-override: 22%;
      line-gap-override: 0%;
      size-adjust: 107%;
    }
    
    body {
      font-family: 'Inter', 'Inter Fallback', sans-serif;
    }
    
    # font-display values:
    - swap: Show fallback immediately, swap when loaded
    - optional: Use cached font or skip (best for non-critical)
    - fallback: Short block period, then fallback forever
    

---
  #### **Name**
Vertical Rhythm
  #### **Description**
Align text and spacing to a consistent baseline grid
  #### **When**
Creating polished editorial or content-heavy layouts
  #### **Example**
    # Vertical rhythm basics:
    
    Base unit = line-height of body text
    - If body is 16px/24px, unit = 24px
    
    /* All spacing uses the rhythm unit */
    :root {
      --rhythm: 1.5rem;  /* 24px at 16px base */
    }
    
    p {
      margin-bottom: var(--rhythm);
    }
    
    h2 {
      font-size: 2rem;
      line-height: calc(var(--rhythm) * 2);  /* 48px */
      margin-top: calc(var(--rhythm) * 2);
      margin-bottom: var(--rhythm);
    }
    
    img {
      margin-bottom: var(--rhythm);
    }
    
    # Benefits:
    - Content feels organized and harmonious
    - Multi-column layouts align beautifully
    - Creates professional, editorial quality
    

## Anti-Patterns


---
  #### **Name**
Too Many Fonts
  #### **Description**
Loading 4+ typefaces, creating visual chaos and performance issues
  #### **Why**
Each font adds HTTP requests and bytes. Visual inconsistency confuses users. Cognitive overload.
  #### **Instead**
    Limit to 2-3 fonts maximum:
    - One for headings
    - One for body
    - One for code (if needed)
    
    A single variable font with multiple weights often beats multiple fonts.
    
    Before adding a font, ask: "Can an existing font handle this?"
    

---
  #### **Name**
Tiny Body Text
  #### **Description**
Setting body text below 16px to fit more content
  #### **Why**
Accessibility failure. Eye strain. Users pinch-to-zoom. WCAG requires scalable text.
  #### **Instead**
    Minimum sizes:
    - Body text: 16px (1rem) minimum on desktop
    - Mobile body: 16px minimum (no viewport scaling below this)
    - Captions/metadata: 14px with excellent contrast
    
    If content doesn't fit at readable sizes, cut content - not font size.
    

---
  #### **Name**
Synthetic Bold/Italic
  #### **Description**
Using CSS to fake weights the font doesn't have
  #### **Why**
Browsers create ugly faux styles. Strokes get distorted. Type designers weep.
  #### **Instead**
    /* BAD - browser synthesizes bold */
    .fake { font-family: 'Montserrat Light'; font-weight: bold; }
    
    /* GOOD - use actual bold weight */
    .real { font-family: 'Montserrat'; font-weight: 700; }
    
    Load the weights you need. If a font doesn't have italic, use oblique or choose another font.
    

---
  #### **Name**
All Caps Body Text
  #### **Description**
Setting paragraphs or long text in ALL CAPITALS
  #### **Why**
50% harder to read. Word shapes disappear. Feels like shouting.
  #### **Instead**
    ALL CAPS appropriate for:
    - Short labels (2-3 words)
    - Buttons/CTAs
    - Navigation items
    - Acronyms
    
    Never for:
    - Body paragraphs
    - Long headlines
    - Any text over one line
    
    Use text-transform: uppercase sparingly, with increased letter-spacing (0.05-0.1em).
    

---
  #### **Name**
Justified Text on Web
  #### **Description**
Using text-align: justify without proper hyphenation
  #### **Why**
Creates rivers of white space. Uneven word spacing. Hyphenation support is poor.
  #### **Instead**
    /* Usually bad on web */
    p { text-align: justify; }
    
    /* If you must justify: */
    p {
      text-align: justify;
      hyphens: auto;
      -webkit-hyphens: auto;
      word-spacing: -0.05em;  /* Tighten slightly */
    }
    
    Left-aligned (ragged right) is almost always better for web.
    

---
  #### **Name**
Low Contrast Text
  #### **Description**
Light gray text for "elegance" that fails accessibility
  #### **Why**
WCAG requires 4.5:1 for normal text. 15% of users have vision impairments.
  #### **Instead**
    Minimum contrast:
    - Body text: 4.5:1 (WCAG AA)
    - Large text (18px+): 3:1
    - Ideal body: 7:1 (AAA)
    
    Bad: #999 on #fff (2.8:1)
    Good: #595959 on #fff (7:1)
    
    Create hierarchy through size and weight, not low contrast.
    

---
  #### **Name**
Ignoring Font Loading Performance
  #### **Description**
Loading fonts without optimization, causing FOIT/FOUT and CLS
  #### **Why**
Invisible text (FOIT) loses readers. Layout shift (CLS) hurts UX and SEO.
  #### **Instead**
    1. Subset fonts (latin only if that's your audience)
    2. Use font-display: swap or optional
    3. Preload critical fonts
    4. Use fallback font metrics matching
    5. Consider system fonts for body text
    
    Google Fonts adds 100+ ms to critical path. Self-host when possible.
    

---
  #### **Name**
Ignoring Optical Sizing
  #### **Description**
Using display fonts at body sizes or body fonts at display sizes
  #### **Why**
Fonts optimized for one size look wrong at others. Thin strokes disappear small.
  #### **Instead**
    Font selection by size:
    - Display (48px+): Decorative, thin strokes OK
    - Headlines (24-48px): Semi-display, moderate details
    - Body (14-20px): Text-optimized, generous x-height
    - Small (12-14px): Caption-optimized, open counters
    
    Some variable fonts have optical size axis (opsz).
    Use it: font-optical-sizing: auto;
    