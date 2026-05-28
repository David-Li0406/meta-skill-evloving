# Typography - Sharp Edges

## Font Loading Flash

### **Id**
font-loading-flash
### **Summary**
Flash of Invisible Text (FOIT) or Flash of Unstyled Text (FOUT) during font loading
### **Severity**
critical
### **Situation**
  Custom web fonts without font-display strategy. Users see blank text for 1-3 seconds
  (FOIT) or a jarring swap from system font (FOUT with layout shift).
  
### **Why**
  FOIT loses readers - they think the page is broken. FOUT without metric matching
  causes Cumulative Layout Shift (CLS), hurting Core Web Vitals and SEO.
  Google penalizes pages with high CLS.
  
### **Solution**
  # 1. Use font-display: swap (or optional for non-critical fonts)
  @font-face {
    font-family: 'Inter';
    src: url('/fonts/inter.woff2') format('woff2');
    font-display: swap;  /* Show fallback immediately */
  }
  
  # 2. Preload critical fonts
  <link rel="preload" href="/fonts/inter.woff2"
        as="font" type="font/woff2" crossorigin>
  
  # 3. Match fallback metrics to minimize shift
  @font-face {
    font-family: 'Inter Fallback';
    src: local('Arial');
    size-adjust: 107%;
    ascent-override: 90%;
    descent-override: 22%;
  }
  
  body {
    font-family: 'Inter', 'Inter Fallback', sans-serif;
  }
  
  # Tools:
  # - fontpie (generates fallback adjustments)
  # - next/font (handles this automatically)
  
### **Symptoms**
  - Users see blank text on first load
  - Layout jumps when fonts load
  - High CLS scores in Lighthouse
  - Slow First Contentful Paint
### **Detection Pattern**
@font-face\s*\{(?![^}]*font-display)

## Font Subsetting Ignored

### **Id**
font-subsetting-ignored
### **Summary**
Loading full font files when only a subset of characters is needed
### **Severity**
high
### **Situation**
  Loading 200KB+ font files containing Cyrillic, Greek, Vietnamese when only
  Latin characters are used. Multiple weights multiplying the problem.
  
### **Why**
  Font files are render-blocking. Every 100KB delays LCP. Users on slow connections
  wait seconds. Mobile data budgets are consumed. Completely unnecessary bytes.
  
### **Solution**
  # Subset fonts to only needed characters
  
  # Google Fonts - use text parameter for extreme subsetting:
  fonts.googleapis.com/css2?family=Inter&text=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789
  
  # Self-hosted - use glyphhanger or fonttools:
  glyphhanger --whitelist=US_ASCII --subset=Inter.woff2
  
  # pyftsubset for precise control:
  pyftsubset Inter.ttf \
    --output-file=Inter-subset.woff2 \
    --flavor=woff2 \
    --layout-features='kern,liga' \
    --unicodes=U+0020-007F
  
  # Size reduction example:
  # Inter full: 310KB -> Latin only: 45KB -> Critical subset: 15KB
  
### **Symptoms**
  - Font files over 100KB
  - Slow loading on mobile
  - High "Transfer Size" in DevTools
  - Multiple font files loading in parallel
### **Detection Pattern**
unicode-range:\s*U\+0000-FFFF|font.*\.(ttf|otf)["']

## Variable Font Browser Support

### **Id**
variable-font-browser-support
### **Summary**
Variable fonts failing in older browsers without fallback
### **Severity**
high
### **Situation**
  Using variable fonts with format('woff2-variations') without static font fallbacks.
  Safari < 11, Edge < 17, and older browsers show nothing or wrong font.
  
### **Why**
  ~5% of users on older browsers see broken typography or completely wrong fonts.
  Variable font syntax differs between browsers. No graceful degradation.
  
### **Solution**
  # Provide static fallbacks in @font-face
  @font-face {
    font-family: 'Inter';
    src: url('/fonts/Inter-Variable.woff2') format('woff2') tech('variations'),
         url('/fonts/Inter-Variable.woff2') format('woff2-variations'),
         url('/fonts/Inter-Regular.woff2') format('woff2');  /* Static fallback */
    font-weight: 100 900;
    font-display: swap;
  }
  
  # Or use @supports for progressive enhancement:
  @supports (font-variation-settings: normal) {
    body { font-family: 'Inter Variable', sans-serif; }
  }
  
  @supports not (font-variation-settings: normal) {
    body { font-family: 'Inter', sans-serif; }
  }
  
  # Test in BrowserStack on older Safari/Edge
  
### **Symptoms**
  - Fonts missing on older browsers
  - User reports of "wrong font"
  - QA finds issues on Safari 10
  - Fallback system fonts appearing
### **Detection Pattern**
format\(["']woff2-variations["']\)(?![^}]*format\(["']woff2["']\))

## Cls From Late Fonts

### **Id**
cls-from-late-fonts
### **Summary**
Cumulative Layout Shift from fonts loading after initial paint
### **Severity**
critical
### **Situation**
  Font loads after content renders. Fallback font has different metrics (x-height, width).
  Text reflows, buttons resize, entire layout shifts. Google's CLS threshold exceeded.
  
### **Why**
  CLS > 0.1 fails Core Web Vitals. Google uses CLS as a ranking factor.
  Users clicking get wrong target. Content jumps frustrate readers.
  Poor user experience and SEO penalty combined.
  
### **Solution**
  # 1. Preload critical fonts (loads before render)
  <link rel="preload" href="/fonts/body.woff2"
        as="font" type="font/woff2" crossorigin>
  
  # 2. Use size-adjust for fallback matching
  @font-face {
    font-family: 'Body Fallback';
    src: local('Arial');
    size-adjust: 105%;      /* Match custom font width */
    ascent-override: 92%;   /* Match ascenders */
    descent-override: 20%;  /* Match descenders */
    line-gap-override: 0%;  /* Match line gap */
  }
  
  # 3. Use font-display: optional for non-critical fonts
  @font-face {
    font-family: 'Fancy Display';
    src: url('/fonts/fancy.woff2') format('woff2');
    font-display: optional;  /* Use only if cached, skip otherwise */
  }
  
  # Tools:
  # - fontpie, Capsize - generate fallback overrides
  # - Layout Shift GIF Generator - visualize shift
  
### **Symptoms**
  - CLS score > 0.1 in Lighthouse
  - Visible text jump on load
  - Buttons moving when clicked
  - User complaints about "jumpy" pages
### **Detection Pattern**


## Tight Line Height

### **Id**
tight-line-height
### **Summary**
Line height below 1.4 for body text making reading exhausting
### **Severity**
high
### **Situation**
  line-height: 1.2 or line-height: 1 on body text. Lines crashing into each other.
  Ascenders and descenders colliding. Dense walls of unreadable text.
  
### **Why**
  WCAG requires line-height of at least 1.5 for body text. Tight leading causes eye
  strain, reduces comprehension, and makes dyslexic users struggle. Reading becomes work.
  
### **Solution**
  # Minimum line-heights by context:
  
  Body text: 1.5 - 1.7
  p { line-height: 1.6; }  /* WCAG compliant */
  
  Headlines: 1.1 - 1.3
  h1 { line-height: 1.2; }  /* Tighter OK for short text */
  
  UI labels: 1.2 - 1.4
  .label { line-height: 1.3; }
  
  # Formula based on measure:
  # line-height = 1.5 + (characters-per-line / 200)
  # 65 char line -> 1.5 + 0.325 = 1.825 (round to 1.8)
  
  # Longer lines need MORE leading, not less
  
### **Symptoms**
  - Users complain text is hard to read
  - Low time-on-page metrics
  - Squinting or zooming
  - WCAG accessibility audit failures
### **Detection Pattern**
line-height:\s*(0\.[0-9]+|1\.[0-3][0-9]*|1)

## Long Measure

### **Id**
long-measure
### **Summary**
Line length exceeding 75-80 characters, exhausting readers
### **Severity**
high
### **Situation**
  Full-width paragraphs stretching 120+ characters. No max-width on content.
  Eyes losing track when returning to next line. Reader fatigue.
  
### **Why**
  Research shows 45-75 characters optimal. Beyond 80, the eye struggles to track back
  to the next line beginning. Comprehension drops. Readers abandon content faster.
  
### **Solution**
  # Set max-width using ch unit (width of "0" character)
  
  .prose {
    max-width: 65ch;  /* Sweet spot */
    margin: 0 auto;
  }
  
  /* For denser content */
  .documentation {
    max-width: 75ch;
  }
  
  /* For columns */
  .column {
    max-width: 45ch;
  }
  
  # Alternative with container:
  .content {
    max-width: 42rem;  /* ~65ch at 16px base */
    padding: 0 1rem;
    margin: 0 auto;
  }
  
### **Symptoms**
  - Text stretching edge to edge
  - Low engagement with long-form content
  - Users highlighting to keep track
  - Readability complaints
### **Detection Pattern**
max-width:\s*(100%|100vw|none)|width:\s*100%

## Missing Font Display

### **Id**
missing-font-display
### **Summary**
No font-display value in @font-face, defaulting to browser FOIT behavior
### **Severity**
critical
### **Situation**
  @font-face without font-display property. Browser defaults to "auto" which usually
  means FOIT - invisible text for up to 3 seconds while font loads.
  
### **Why**
  Different browsers handle missing font-display differently. Safari blocks for 3s.
  Chrome for 3s then shows fallback. Users see nothing. Perceived performance tanks.
  
### **Solution**
  # ALWAYS include font-display
  
  @font-face {
    font-family: 'Inter';
    src: url('/fonts/inter.woff2') format('woff2');
    font-display: swap;  /* <-- Required! */
  }
  
  # font-display options:
  # - swap: Show fallback immediately, swap when loaded (best for body)
  # - fallback: 100ms block, then fallback (good compromise)
  # - optional: Use cached or skip entirely (non-critical fonts)
  # - block: Block up to 3s (almost never use this)
  
  # Google Fonts - add &display=swap:
  fonts.googleapis.com/css2?family=Inter&display=swap
  
### **Symptoms**
  - Invisible text during load
  - Blank page until fonts load
  - Slow First Contentful Paint
  - Poor perceived performance
### **Detection Pattern**
@font-face\s*\{[^}]*src:[^}]*\}(?![^}]*font-display)

## Too Many Weights

### **Id**
too-many-weights
### **Summary**
Loading 5+ font weights when 2-3 would suffice
### **Severity**
high
### **Situation**
  Loading 100, 200, 300, 400, 500, 600, 700, 800, 900 weights of a font.
  Each weight is another HTTP request and file download.
  
### **Why**
  Each weight adds 15-50KB. Loading 8 weights = 200-400KB of fonts alone.
  Most designs use 2-3 weights. Wasted bandwidth and slower loads.
  
### **Solution**
  # Audit your actual usage
  
  Typical needs:
  - Regular (400) - body text
  - Medium (500) - emphasis, subheadings
  - Bold (700) - headlines, strong emphasis
  
  That's it. Three weights cover 95% of use cases.
  
  # Using variable fonts solves this:
  @font-face {
    font-family: 'Inter';
    src: url('/fonts/Inter-Variable.woff2') format('woff2');
    font-weight: 100 900;  /* All weights, one file */
  }
  
  # Variable font = ~50KB for ALL weights vs 150KB+ for 3 static
  
### **Symptoms**
  - Multiple font files in Network tab
  - Slow initial load
  - Lighthouse flags font payload
  - Bundle size concerns
### **Detection Pattern**
font-weight:\s*(100|200|800|900)[;,}]

## Px Font Sizes

### **Id**
px-font-sizes
### **Summary**
Using pixel values for font-size, breaking user preferences
### **Severity**
high
### **Situation**
  font-size: 14px throughout the app. User sets browser to 150% zoom for
  accessibility. Your 14px text stays 14px. User can't read it.
  
### **Why**
  Users set browser font size for accessibility reasons. px units ignore this.
  WCAG requires text to scale to 200%. Breaking user preferences is an accessibility violation.
  
### **Solution**
  # Use rem for font sizes (relative to root)
  
  html {
    font-size: 100%;  /* Respects user preference */
  }
  
  body {
    font-size: 1rem;     /* 16px default, scales with user pref */
  }
  
  h1 {
    font-size: 2.5rem;   /* 40px default, scales */
  }
  
  .small {
    font-size: 0.875rem; /* 14px default, scales */
  }
  
  # em for component-relative sizing
  .button {
    font-size: 1em;      /* Inherits from parent */
    padding: 0.5em 1em;  /* Scales with font-size */
  }
  
  # px is OK for:
  # - Borders, shadows (don't need to scale)
  # - Media queries (reference points)
  
### **Symptoms**
  - Users complain text is too small
  - Zoom doesn't work properly
  - Accessibility audit failures
  - Text not scaling with browser settings
### **Detection Pattern**
font-size:\s*[0-9]+px

## Synthetic Styles

### **Id**
synthetic-styles
### **Summary**
Browser faking bold or italic that the font doesn't have
### **Severity**
medium
### **Situation**
  Using font-weight: bold on a font that only has Regular weight.
  Using font-style: italic on a font without italic variant.
  Browser creates ugly synthetic versions.
  
### **Why**
  Synthetic bold strokes look wrong - uniformly thickened instead of designed.
  Synthetic italic is just slanted, not true italic with redesigned letterforms.
  Type designers spend months perfecting these. Browser ruins it in milliseconds.
  
### **Solution**
  # Only use weights/styles the font actually has
  
  /* BAD - Montserrat Light + synthetic bold */
  @font-face {
    font-family: 'Montserrat';
    src: url('Montserrat-Light.woff2');
    font-weight: 300;
  }
  .bold { font-weight: 700; }  /* Browser synthesizes - ugly! */
  
  /* GOOD - Load the actual bold weight */
  @font-face {
    font-family: 'Montserrat';
    src: url('Montserrat-Bold.woff2');
    font-weight: 700;
  }
  .bold { font-weight: 700; }  /* Uses real bold */
  
  # If font has no italic, use a different font or oblique:
  font-style: oblique 14deg;
  
### **Symptoms**
  - Bold text looks thick and blobby
  - Italic text looks slanted, not designed
  - Typography feels "off" or cheap
  - Designer complaints about font rendering
### **Detection Pattern**


## Ignoring Opentype Features

### **Id**
ignoring-opentype-features
### **Summary**
Missing out on kerning, ligatures, and other OpenType features
### **Severity**
medium
### **Situation**
  Using premium fonts that include beautiful OpenType features, but they're
  disabled by default. "fi" doesn't ligate. Numbers aren't tabular in tables.
  
### **Why**
  Type designers include features like ligatures, small caps, and tabular figures
  for good reason. Ignoring them wastes the font's potential. Tables with
  proportional numbers misalign. Headlines missing proper kerning look amateur.
  
### **Solution**
  # Enable common OpenType features
  
  /* Recommended for body text */
  body {
    font-kerning: normal;               /* Proper letter spacing */
    font-feature-settings:
      'kern' 1,  /* Kerning */
      'liga' 1,  /* Standard ligatures (fi, fl, ff) */
      'calt' 1;  /* Contextual alternates */
  }
  
  /* For tabular data */
  .table-number {
    font-variant-numeric: tabular-nums; /* Aligned columns */
  }
  
  /* For prices/stats */
  .price {
    font-variant-numeric: lining-nums;  /* Uniform height */
  }
  
  /* For elegant body text */
  .prose {
    font-variant-numeric: oldstyle-nums; /* Lowercase-style numbers */
  }
  
  /* For headlines */
  .headline {
    font-feature-settings: 'dlig' 1;    /* Discretionary ligatures */
  }
  
  # Tools to explore: wakamaifondue.com shows all available features
  
### **Symptoms**
  - "fi" and "fl" not connecting in premium fonts
  - Numbers misaligning in tables
  - Headlines with awkward letter spacing
  - Not getting value from expensive fonts
### **Detection Pattern**


## Font Render Inconsistency

### **Id**
font-render-inconsistency
### **Summary**
Fonts rendering differently across operating systems
### **Severity**
medium
### **Situation**
  Font looks beautiful on macOS, thin and spindly on Windows. Same font,
  completely different appearance. Designer approves on Mac, users on Windows complain.
  
### **Why**
  macOS uses sub-pixel antialiasing that makes fonts appear slightly heavier.
  Windows uses ClearType with different hinting. The same font genuinely looks
  different. What's readable on Mac may be too thin on Windows.
  
### **Solution**
  # Choose fonts that work cross-platform
  
  Safe choices (render well everywhere):
  - Inter (designed for screens)
  - Roboto (Google's cross-platform testing)
  - Source Sans Pro (Adobe's screen optimization)
  - system-ui (native to each platform)
  
  # Test on actual Windows machine (not just Mac)
  # BrowserStack, real devices in office
  
  # CSS smoothing (use carefully):
  body {
    -webkit-font-smoothing: antialiased;     /* macOS - slightly thinner */
    -moz-osx-font-smoothing: grayscale;      /* macOS Firefox */
  }
  
  # Consider slightly heavier weight for Windows:
  # font-weight: 450 instead of 400 (with variable fonts)
  
### **Symptoms**
  - Complaints from Windows users
  - Text looks thin/unreadable
  - Cross-platform design reviews failing
  - Font appearing different in screenshots
### **Detection Pattern**
