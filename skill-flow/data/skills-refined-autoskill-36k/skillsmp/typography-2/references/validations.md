# Typography - Validations

## Missing font-display in @font-face

### **Id**
missing-font-display
### **Severity**
error
### **Type**
regex
### **Pattern**
@font-face\s*\{(?![^}]*font-display)[^}]*\}
### **Message**
@font-face missing font-display property, will cause invisible text (FOIT) during loading.
### **Fix Action**
Add font-display: swap; (or optional for non-critical fonts) to @font-face rule
### **Applies To**
  - *.css
  - *.scss
  - *.sass
### **Test Cases**
  #### **Should Match**
    - @font-face { font-family: 'Inter'; src: url('inter.woff2'); }
    -       @font-face {
        font-family: 'Roboto';
        src: url('roboto.woff2');
      }
  #### **Should Not Match**
    - @font-face { font-family: 'Inter'; src: url('inter.woff2'); font-display: swap; }
    - @font-face { font-display: optional; font-family: 'Fancy'; src: url('fancy.woff2'); }

## Too Many Font Weights Loaded

### **Id**
too-many-font-weights
### **Severity**
warning
### **Type**
regex
### **Pattern**
@font-face[^}]*font-weight:\s*(100|200|800|900)[;\s}]
### **Message**
Loading extreme font weights (100, 200, 800, 900). Most designs need only 400, 500, 700.
### **Fix Action**
Audit font usage - remove unused weights or use a variable font
### **Applies To**
  - *.css
  - *.scss
### **Test Cases**
  #### **Should Match**
    - @font-face { font-family: 'Inter'; font-weight: 100; src: url('inter-thin.woff2'); }
    - @font-face { font-family: 'Roboto'; font-weight: 900; src: url('roboto-black.woff2'); }
  #### **Should Not Match**
    - @font-face { font-family: 'Inter'; font-weight: 400; src: url('inter.woff2'); }
    - @font-face { font-family: 'Inter'; font-weight: 700; src: url('inter-bold.woff2'); }

## Pixel Units for Font Size

### **Id**
px-font-size
### **Severity**
warning
### **Type**
regex
### **Pattern**
font-size:\s*[0-9]+px
### **Message**
Using px for font-size breaks user font preferences and accessibility.
### **Fix Action**
Use rem units instead (e.g., font-size: 1rem instead of font-size: 16px)
### **Applies To**
  - *.css
  - *.scss
  - *.tsx
  - *.jsx
### **Test Cases**
  #### **Should Match**
    - font-size: 14px;
    - font-size: 16px
    - fontSize: '12px'
  #### **Should Not Match**
    - font-size: 1rem;
    - font-size: clamp(1rem, 2vw, 1.5rem)
    - fontSize: '1.25rem'

## Line Height Too Tight for Body Text

### **Id**
tight-line-height
### **Severity**
error
### **Type**
regex
### **Pattern**
line-height:\s*(0\.[0-9]+|1(\.[0-3][0-9]*)?)[;\s}](?!.*\/\*.*headline|.*\/\*.*title|.*\/\*.*h[1-6])
### **Message**
Line height below 1.4 makes body text hard to read. WCAG recommends 1.5+ for body.
### **Fix Action**
Increase line-height to at least 1.5 for body text (1.1-1.3 OK for headlines)
### **Applies To**
  - *.css
  - *.scss
### **Test Cases**
  #### **Should Match**
    - line-height: 1.2;
    - line-height: 1;
    - line-height: 1.0;
  #### **Should Not Match**
    - line-height: 1.5;
    - line-height: 1.6;
    - line-height: 1.75;

## All Caps on Block Text

### **Id**
text-all-caps-block
### **Severity**
warning
### **Type**
regex
### **Pattern**
<(p|div|span)[^>]*class=["'][^"']*uppercase[^"']*["'][^>]*>(?![^<]{0,50}<\/)
### **Message**
text-transform: uppercase on potentially long text. ALL CAPS is 50% harder to read.
### **Fix Action**
Reserve uppercase for short labels (2-3 words), buttons, or navigation. Use normal case for body.
### **Applies To**
  - *.tsx
  - *.jsx
  - *.html
### **Test Cases**
  #### **Should Match**
    - <p className="uppercase">Long paragraph text here</p>
    - <div class="text-uppercase">Content block</div>
  #### **Should Not Match**
    - <span className="uppercase">CTA</span>
    - <button className="uppercase">Submit</button>

## Font Size Below Minimum Readable

### **Id**
tiny-font-size
### **Severity**
error
### **Type**
regex
### **Pattern**
font-size:\s*(0\.[0-7]rem|[0-9]px|1[0-3]px|text-(2xs|xs))
### **Message**
Font size below readable minimum. Body text should be at least 16px (1rem).
### **Fix Action**
Increase font size to at least 1rem (16px) for body, 0.875rem (14px) minimum for captions
### **Applies To**
  - *.css
  - *.scss
  - *.tsx
  - *.jsx
### **Test Cases**
  #### **Should Match**
    - font-size: 12px;
    - font-size: 0.65rem;
    - className="text-xs"
  #### **Should Not Match**
    - font-size: 1rem;
    - font-size: 16px;
    - className="text-base"

## Google Fonts Without display Parameter

### **Id**
google-fonts-no-display
### **Severity**
error
### **Type**
regex
### **Pattern**
fonts\.googleapis\.com/css2?\?[^"']*(?!display=)[^"']*["\'> ]
### **Message**
Google Fonts URL missing display=swap parameter, will cause invisible text.
### **Fix Action**
Add &display=swap to Google Fonts URL
### **Applies To**
  - *.html
  - *.tsx
  - *.jsx
  - *.css
### **Test Cases**
  #### **Should Match**
    - href="https://fonts.googleapis.com/css2?family=Inter"
    - href='https://fonts.googleapis.com/css?family=Roboto'
  #### **Should Not Match**
    - href="https://fonts.googleapis.com/css2?family=Inter&display=swap"
    - url('https://fonts.googleapis.com/css2?family=Roboto&display=swap')

## Using 'bold' Keyword Instead of Numeric Weight

### **Id**
font-weight-bold-keyword
### **Severity**
info
### **Type**
regex
### **Pattern**
font-weight:\s*bold[;\s}]
### **Message**
Using 'bold' keyword. Prefer numeric weights (700) for consistency with design tokens.
### **Fix Action**
Use font-weight: 700 instead of font-weight: bold for explicit control
### **Applies To**
  - *.css
  - *.scss
### **Test Cases**
  #### **Should Match**
    - font-weight: bold;
    - font-weight: bold }
  #### **Should Not Match**
    - font-weight: 700;
    - font-weight: 600;

## Custom Font Without System Fallback

### **Id**
no-font-fallback
### **Severity**
warning
### **Type**
regex
### **Pattern**
font-family:\s*['"][^'"]+['"][;\s}]
### **Message**
Custom font without fallback. Add system font fallback for loading states.
### **Fix Action**
Add fallback fonts: font-family: 'Inter', system-ui, sans-serif;
### **Applies To**
  - *.css
  - *.scss
### **Test Cases**
  #### **Should Match**
    - font-family: 'Inter';
    - font-family: "Roboto";
  #### **Should Not Match**
    - font-family: 'Inter', sans-serif;
    - font-family: 'Roboto', system-ui, sans-serif;

## Justified Text Without Hyphenation

### **Id**
justify-text-no-hyphens
### **Severity**
warning
### **Type**
regex
### **Pattern**
text-align:\s*justify[;\s}](?![^}]*hyphens)
### **Message**
Justified text without hyphenation creates rivers of white space.
### **Fix Action**
Add hyphens: auto; with text-align: justify; or prefer left-aligned text
### **Applies To**
  - *.css
  - *.scss
### **Test Cases**
  #### **Should Match**
    - text-align: justify;
    - text-align: justify; color: black;
  #### **Should Not Match**
    - text-align: justify; hyphens: auto;
    - text-align: left;

## Missing Letter Spacing on Uppercase Text

### **Id**
letter-spacing-em-on-uppercase
### **Severity**
info
### **Type**
regex
### **Pattern**
text-transform:\s*uppercase[;\s}](?![^}]*letter-spacing)
### **Message**
Uppercase text benefits from increased letter-spacing (0.05-0.1em).
### **Fix Action**
Add letter-spacing: 0.05em to 0.1em when using text-transform: uppercase
### **Applies To**
  - *.css
  - *.scss
### **Test Cases**
  #### **Should Match**
    - text-transform: uppercase;
    - text-transform: uppercase; font-weight: 600;
  #### **Should Not Match**
    - text-transform: uppercase; letter-spacing: 0.05em;
    - text-transform: none;

## Prose Content Without Line Length Limit

### **Id**
no-max-width-prose
### **Severity**
warning
### **Type**
regex
### **Pattern**
<(article|p|div)[^>]*class=["'][^"']*prose[^"']*["'][^>]*>(?![^<]*max-w)
### **Message**
Prose content without max-width. Long lines (80+ chars) are hard to read.
### **Fix Action**
Add max-width: 65ch (or max-w-prose in Tailwind) to limit line length
### **Applies To**
  - *.tsx
  - *.jsx
  - *.html
### **Test Cases**
  #### **Should Match**
    - <article className="prose">
    - <div class="prose lg:prose-xl">
  #### **Should Not Match**
    - <article className="prose max-w-prose">
    - <div class="prose max-w-2xl">

## Using !important on Font Size

### **Id**
font-size-important
### **Severity**
warning
### **Type**
regex
### **Pattern**
font-size:[^;]*!important
### **Message**
Using !important on font-size can break user accessibility preferences.
### **Fix Action**
Remove !important and fix specificity issues properly
### **Applies To**
  - *.css
  - *.scss
### **Test Cases**
  #### **Should Match**
    - font-size: 14px !important;
    - font-size: 1rem !important
  #### **Should Not Match**
    - font-size: 1rem;
    - font-size: 16px;

## Using TTF/OTF Instead of WOFF2

### **Id**
font-file-ttf-otf
### **Severity**
warning
### **Type**
regex
### **Pattern**
src:\s*url\(['"]?[^'"]+\.(ttf|otf)['"]?\)
### **Message**
Using TTF/OTF fonts instead of WOFF2. WOFF2 is 30-50% smaller.
### **Fix Action**
Convert fonts to WOFF2 format using fonttools or transfonter.org
### **Applies To**
  - *.css
  - *.scss
### **Test Cases**
  #### **Should Match**
    - src: url('inter.ttf');
    - src: url(roboto.otf);
  #### **Should Not Match**
    - src: url('inter.woff2');
    - src: url('inter.woff');